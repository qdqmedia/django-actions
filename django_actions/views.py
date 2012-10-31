# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib import messages
from django_actions.forms import ActionForm
from django.contrib.contenttypes.models import ContentType


def act(request, app_n_model):
    """ execute chosen action """
    app, model = app_n_model.split('.')
    model_class = ContentType.objects.get(app_label=app,
                                          model=model).model_class()
    referer = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        qset = model_class.objects.filter(pk__in=(request.POST.getlist('items')))

        form = ActionForm(request.POST, qset=qset, model=model_class)

        if form.is_valid():
            qset = form.execute_action(request,
                                       form.cleaned_data['action'],
                                       form.cleaned_data['items'],
                                       model_class)
            if 'response' in qset:
                return qset['response']
            else:
                # Action has been executed
                ref = request.META.get('HTTP_REFERER', '/')
                if 'message' in qset:
                    messages.add_message(request, messages.INFO, qset['message'])
                return HttpResponseRedirect(ref)
        else:
            return HttpResponseRedirect(referer)
    return HttpResponseRedirect(referer)
