# -*- coding: utf-8 -*-
from django.template import Library, Node, TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


register = Library()

error_msg = 'Please, use: {% get_action_list for <app.model> as varname %}'


class GetActionListNode(Node):
    def __init__(self, app_model, varname, *args, **kwargs):
        self.app_model = app_model
        self.varname = varname

    def render(self, context):
        '''Modify context to add a list of actions for given model'''
        app, model = self.app_model.split('.')

        try:
            model_class = ContentType.objects.get(app_label=app,
                                                  model=model).model_class()
        except ObjectDoesNotExist:
            raise TemplateSyntaxError(error_msg)

        actions = []
        if not hasattr(model_class, 'actions'):
            return ''

        model_actions = model_class.actions
        for action in model_class.actions:
            if hasattr(action, 'short_description'):
                short_desc = action.short_description
            else:
                short_desc = action.func_name
            actions.append((model_actions.index(action), short_desc))
        context[self.varname] = {'object_list': actions, 'action': self.app_model}
        return ''


@register.tag
def get_action_list(parser, token):
    '''Call to render method passing app_model and varname used by template'''
    token_contents = token.split_contents()

    if len(token_contents) != 5 or (token_contents[1] != 'for' or token_contents[3] != 'as'):
        raise TemplateSyntaxError(error_msg)

    return GetActionListNode(token_contents[2], token_contents[4])


@register.inclusion_tag('actions_select.html')
def show_actions(actions):
    return {'actions': actions}
