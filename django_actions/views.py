# -*- coding: utf-8 -*-
import pickle

from django.http import HttpResponseRedirect
from django.contrib import messages
from django_actions.forms import ActionForm
from django.contrib.contenttypes.models import ContentType


class ActionViewMixin(object):
    def get_context_data(self, *args, **kwargs):
        object_list_displayed = kwargs['object_list']
        self.request.session['serialized_qs'] = pickle.dumps(object_list_displayed.query)
        self.request.session['serialized_model_qs'] = object_list_displayed.model
        actions = []
        for action in self.actions:
            if action.short_description:
                actions.append(action.short_description)
            else:
                actions(action.__name__)
        kwargs['actions'] = actions
        return super(ActionViewMixin, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST['action'] and request.POST['action'] != u'-1':
            # Execute action passing values
            action = request.POST['action']
            # Building a empty queryset to load pickled data
            model_class = request.session['serialized_model_qs']
            new_qs = model_class.objects.all()[:1]
            new_qs.query = pickle.loads(request.session['serialized_qs'])
            response = self.actions[int(action)-1](new_qs)
            return response
        return HttpResponseRedirect('.')


def act(request, app_n_model):
    """ execute chosen action """
    app, model = app_n_model.split('.')
    model_class = ContentType.objects.get(app_label=app,
                                          model=model).model_class()
    referer = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        # Checking if all queryset was selected
        if 'allqset' in request.POST.keys():
            qset = model_class.objects.raw(request.session['allqset'])
        else:
            qset = model_class.objects.filter(pk__in=(request.POST.getlist('items')))
        form = ActionForm(request.POST, qset=qset, model=model_class)
        qset2 = form.execute_action(request,
                                    request.POST['action'],
                                    #form.cleaned_data['action'],
                                    #form.cleaned_data['items'],
                                    qset,
                                    model_class)
        if 'response' in qset2:
            return qset2['response']
        else:
            # Action has been executed
            ref = request.META.get('HTTP_REFERER', '/')
            if 'message' in qset2:
                messages.add_message(request, messages.INFO, qset['message'])
            return HttpResponseRedirect(ref)

        #if form.is_valid():
        #    qset2 = form.execute_action(request,
        #                                form.cleaned_data['action'],
        #                                #form.cleaned_data['items'],
        #                                qset,
        #                                model_class)
        #    if 'response' in qset2:
        #        return qset2['response']
        #    else:
        #        # Action has been executed
        #        ref = request.META.get('HTTP_REFERER', '/')
        #        if 'message' in qset2:
        #            messages.add_message(request, messages.INFO, qset['message'])
        #        return HttpResponseRedirect(ref)
        #else:
        #    return HttpResponseRedirect(referer)
    return HttpResponseRedirect(referer)
