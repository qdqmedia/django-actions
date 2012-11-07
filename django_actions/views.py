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
