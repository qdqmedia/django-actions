# coding: utf8
#
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django_actions.forms import action_formset
from django_actions.helpers import get_content_type_or_404

def act(request, app_n_model):
    """ execute chosen action """
    app, model = app_n_model.split('.')
    ct = get_content_type_or_404(app_label=app, model=model)
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        qset = ct.model_class().objects.filter(pk__in=(request.POST.getlist('items')))
        formclass = action_formset(request, qset, ct.model_class())
        form = formclass(request.POST)
        if form.is_valid():
            #items = ct.model_class().objects.filter(pk__in=(request.POST.get('items', None)))
            qset = form.act(form.cleaned_data['action'], form.cleaned_data['items'])
            if 'response' in qset: 
                request.session['ref'] = request.META.get('HTTP_REFERER', '/')
                request.session.save()
                return qset['response']
            else:
                ref = request.session.get('ref', '/')
                if 'ref' in request.session: del request.session['ref']
                request.session.save()
                return HttpResponseRedirect(ref)
        else:       
            return HttpResponseRedirect(referer)
    return HttpResponseRedirect(referer)
