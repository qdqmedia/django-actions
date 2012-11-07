# -*- coding: utf-8 -*-
from django import forms
from django.db.models.query import RawQuerySet


class ActionForm(forms.Form):
    #items = forms.ModelMultipleChoiceField(queryset=[], widget=forms.MultipleHiddenInput())
    items = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput())
    action = forms.ChoiceField(widget=forms.HiddenInput())
    allqset = forms.CharField(max_length=1, required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        model = kwargs['model']
        qset = kwargs['qset']
        del kwargs['qset']
        del kwargs['model']

        self.base_fields['items'].choices = [(ele.pk, ele.pk) for ele in qset]

        for action in model.actions:
            try:
                action_desc = action.short_description
            except AttributeError:
                action_desc = action.__name__
            self.base_fields['action'].choices.append((model.actions.index(action),
                                                       action_desc))
        super(ActionForm, self).__init__(*args, **kwargs)

    def execute_action(self, request, action, queryset, model_class, **kwargs):
        if action == 'None':
            return {'qset': queryset}
        action = model_class.actions[int(action)]
        return action(model_class, request, queryset, **kwargs)
