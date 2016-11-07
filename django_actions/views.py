# -*- coding: utf-8 -*-
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class ActionViewMixin(object):
    actions = ()

    def get_context_data(self, *args, **kwargs):
        # Saves whole object list (without pagination) for eventual post
        kwargs['_whole_object_list'] = kwargs.get('object_list', self.object_list)
        # Actions available in templates
        descriptions = []
        for action in self.actions:
            # Only available under specific conditions
            if isinstance(action, (tuple, list)):
                if not action[0](self):
                    continue
                action = action[1]
            action_description = getattr(action, 'short_description', action.__name__)
            attrs = getattr(action, 'attrs', {})
            descriptions.append((action_description, attrs))
        kwargs['actions'] = descriptions
        return super(ActionViewMixin, self).get_context_data(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Getting current queryset from simulated get method
        get_result = self.get(request, *args, **kwargs)
        qs = get_result.context_data['_whole_object_list']

        if request.POST['action'] and request.POST['action'] != u'-1':
            # Checking if we're going to use all qset or only selected items
            if 'select-across' in request.POST and 'action-select' in request.POST:
                if request.POST['select-across'] == u'0':
                    if request.POST['select-first-n'] == u'0':
                        # select a specific set of items
                        qs = qs.filter(pk__in=(request.POST.getlist('action-select')))
                    else:
                        # select first `select-first-n` items
                        qs = qs.model.objects.filter(pk__in=[__.pk for __ in qs[:int(request.POST['select-first-n'])]])

                validated_actions = []
                for action in self.actions:
                    if isinstance(action, (tuple, list)):
                        if not action[0](self):
                            continue
                        action = action[1]
                    validated_actions.append(action)

                # Pick the submitted action
                try:
                    action_to_execute = validated_actions[int(request.POST['action'])-1]
                except (KeyError, IndexError, ValueError):
                    return HttpResponseForbidden()

                return action_to_execute(self, qs)

        return redirect(request.META.get('HTTP_REFERER') or '.')
