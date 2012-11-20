# -*- coding: utf-8 -*-
import pickle

from django.http import HttpResponseRedirect, HttpResponseForbidden


class ActionViewMixin(object):
    actions = ()

    def get_context_data(self, *args, **kwargs):
        object_list_displayed = kwargs['object_list']
        kwargs['all_items_count'] = object_list_displayed.count()
        # Storing serialized queryset using query attribute
        self.request.session['serialized_qs'] = pickle.dumps(object_list_displayed.query)
        self.request.session['serialized_model_qs'] = object_list_displayed.model

        # Selecting actions for <select> node
        available_actions = []
        for action in self.actions:
            # Only available under specific conditions
            if isinstance(action, (tuple, list)):
                if not action[0](self):
                    continue
                action = action[1]
            available_actions.append(getattr(action, 'short_description', action.__name__))
        kwargs['actions'] = available_actions
        return super(ActionViewMixin, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        model_class = request.session['serialized_model_qs']
        if request.POST['action'] and request.POST['action'] != u'-1':
            # Checking if we're going to use all qset or only selected items
            if 'select-across' in request.POST and 'action-select' in request.POST:
                if request.POST['select-across'] == u'0':
                    # select a specific set of items
                    qs = model_class.objects.filter(pk__in=(request.POST.getlist('action-select')))
                else:
                    # Building a empty queryset to load pickled data
                    qs = model_class.objects.all()[:1]
                    qs.query = pickle.loads(request.session['serialized_qs'])

                # Pick the submitted action
                try:
                    action_to_execute = self.actions[int(request.POST['action'])-1]
                except (KeyError, IndexError, ValueError):
                    return HttpResponseForbidden()

                # Perform condition checks
                if isinstance(action_to_execute, (tuple, list)):
                    if not action_to_execute[0](self):
                        return HttpResponseForbidden()
                    action_to_execute = action_to_execute[1]

                return action_to_execute(self, qs)
        return HttpResponseRedirect('.')
