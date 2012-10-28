# coding: utf-8
import sys
from django import forms
from django.http import Http404
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

class ActionForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=[], widget=forms.MultipleHiddenInput())
    action = forms.ChoiceField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        model = kwargs['model']
        qset = kwargs['qset']
        del kwargs['qset']
        del kwargs['model']
        self.base_fields['items'].queryset = qset
        _actions = []
        for x in range(0, len(model.actions)):
            _actions.append((x, x))
        self.base_fields['action'].choices = _actions
        del _actions
        super(ActionForm, self).__init__(*args, **kwargs)

class ActionApproveForm(ActionForm):
    approve = forms.BooleanField(label=_('Approve'), required=True,
        help_text=_('Yes, i approve'))   

def action_formset(request, qset, model, permissions=[]):
    """ taken from http://stackoverflow.com/questions/1975179/creating-django-admin-like-actions-for-non-admin-front-end-users-how-to
    thanks to Judo Will for the idea of dynamicly form creation
    generates ActionForm which runs actions """
    
    class _ActionForm(forms.Form): 
        # if we want to provide form.as_ul
        # its better to add forms.MultipleHiddenInput()
        items = forms.ModelMultipleChoiceField(queryset=qset) 
        _actions = []
        for x in range(0, len(model.actions)):
            _actions.append((x, model.actions[x].short_description))

        action = forms.ChoiceField(choices=[(None, '--------'),] + _actions)
        
        del _actions

        def act(self, action, _qset, **kwargs):
            if hasattr(self, 'is_valid'):
                if action == 'None':
                    #No action have passed, no action would complete
                    return {'qset': _qset} 
                action = model.actions[int(action)]
                if hasattr(action, 'has_perms'):
                    if request.user.has_perms(action.has_perms):
                        return action(self.request, _qset, model, **kwargs)
                    else:
                        raise Http404("Permission denied you have not such perms")
                else:
                    #default permissions
                    app_label = _qset.model._meta.app_label
                    model_ = _qset.model._meta.module_name
                    perm = "{app}.delete_{model};{app}.change_{model}".format(app=app_label,
                        model=model_)
                    perms = perm.split(';')
                    if request.user.has_perms(perms):
                        return action(self.request, _qset, model, **kwargs)
                    else:
                        raise Http404("Permission denied you have not such perms")
            else:
                raise ObjectDoesNotExist, "form.is_valid should be ran fist"
        
        def do_act(self, action, _qset, **kwargs):
            """ does not check if form is valid """
            if action == 'None':
                return {'qset': _qset}
            action = model.actions[int(action)]
            return action(self.request, _qset, model, **kwargs)

        def __init__(self, *args, **kwargs):
            self.request = request
            if args:
                #blocking out users without permissions we need
                if not self.request.user.has_perms(permissions):
                    raise Http404('Your user does not have permissions you need to complete this operation.')
            super(_ActionForm, self).__init__(*args, **kwargs)
    return _ActionForm



