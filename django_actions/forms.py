# -*- coding: utf-8 -*-
from django import forms


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

    def execute_action(self, request, action, _qset, model_class, **kwargs):
        if action == 'None':
            return {'qset': _qset}
        action = model_class.actions[int(action)]
        return action(request, _qset, model_class, **kwargs)
