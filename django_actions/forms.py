# -*- coding: utf-8 -*-
from django import forms
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
        self.base_fields['action'].choices = [(model.actions.index(action), \
                                               action.short_description) \
                                               for action in model.actions]
        super(ActionForm, self).__init__(*args, **kwargs)


class ActionApproveForm(ActionForm):
    approve = forms.BooleanField(label=_('Approve'),
                                 required=True,
                                 help_text=_('Yes, I approve'))


def action_formset(request, qset, model, permissions=[]):
    '''Create a form dynamically'''
    class _ActionForm(forms.Form):
        items = forms.ModelMultipleChoiceField(queryset=qset)
        action = forms.ChoiceField(choices=[(None, '--------'), ] + \
                                           [(model.actions.index(action), \
                                           action.short_description) \
                                           for action in model.actions])

        def execute_action(self, action, _qset, **kwargs):
            if action == 'None':
                return {'qset': _qset}
            action = model.actions[int(action)]
            return action(self.request, _qset, model, **kwargs)

        def __init__(self, *args, **kwargs):
            self.request = request
            super(_ActionForm, self).__init__(*args, **kwargs)

    return _ActionForm
