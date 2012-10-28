# coding: utf8
from django.utils.translation import ugettext_lazy as _, ugettext as _tr
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django_actions.forms import ActionApproveForm, ActionForm

#common actions
def common_delete_action(request, qset, model, **kwargs):
    template = 'actions/action_delete_form.html'
    if request.method == 'POST':
        form = ActionApproveForm(request.POST, model=model, qset=qset)
        if form.is_valid():
            return {'qset': qset.delete()}
        else: 
            return {'response': render_to_response(template,
                {'form': form},
                context_instance=RequestContext(request))}
    return {'qset': qset }
common_delete_action.has_perms = ['{app}.delete_{model}', ]
common_delete_action.short_description = _('delete')
