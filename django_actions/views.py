# -*- coding: utf-8 -*-
import pickle

from django.http import HttpResponseRedirect


class ActionViewMixin(object):
    def get_context_data(self, *args, **kwargs):
        object_list_displayed = kwargs['object_list']
        kwargs['all_items_count'] = object_list_displayed.count()
        # Storing serialized queryset using query attribute
        self.request.session['serialized_qs'] = pickle.dumps(object_list_displayed.query)
        self.request.session['serialized_model_qs'] = object_list_displayed.model
        # Selecting actions for <select> node
        actions = []
        for action in self.actions:
            if action.short_description:
                actions.append(action.short_description)
            else:
                actions(action.__name__)
        kwargs['actions'] = actions
        return super(ActionViewMixin, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        model_class = request.session['serialized_model_qs']
        if request.POST['action'] and request.POST['action'] != u'-1':
            new_qs = None
            # Checking if we're going to use all qset or only selected items
            if request.POST['select-across']:
                if request.POST['select-across'] == u'0' and request.POST['action-select']:
                    selected_ids = request.POST.getlist('action-select')
                    new_qs = model_class.objects.filter(pk__in=(selected_ids))
                else:
                    # Building a empty queryset to load pickled data
                    model_class = request.session['serialized_model_qs']
                    new_qs = model_class.objects.all()[:1]
                    new_qs.query = pickle.loads(request.session['serialized_qs'])
                # Execute action passing values
                action = request.POST['action']
                return self.actions[int(action)-1](new_qs)
        return HttpResponseRedirect('.')
