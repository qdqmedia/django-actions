# coding: utf8
from django.template import Library, Node, TemplateSyntaxError
from django_actions.helpers import get_content_type_or_None
from django_actions.helpers import parse_perms, get_description

register = Library()

class GetActionListNode(Node):
    def __init__(self, app_n_model, varname, *args, **kwargs):
        self.app_n_model = app_n_model
        self.varname = varname
    
    def render(self, context):
        if isinstance(self.app_n_model, str) or\
            isinstance(self.app_n_model, unicode):
            action = self.app_n_model[1:-1]
            app, model = action.split('.')
        else:
            inst = self.app_n_model.resolve(context, ignore_failures=True)
            if hasattr(inst, 'model'):
                model = inst.model._meta.module_name
                app = inst.model._meta.app_label
                action = "%s.%s" % (app, model)
            else:
               raise TemplateSyntaxError, "Nor string neither model or queryset was given" 
        user = context['user']
        ct = get_content_type_or_None(app_label=app, model=model)
        if ct:
            model_class = ct.model_class()
            _actions = []
            for x in range(0, len(model_class.actions)):
                if hasattr(model_class.actions[x], 'has_perms'): 
                    perms = [p.format(app=app, model=model) for p in model_class.actions[x].has_perms]
                    if user.has_perms(perms):
                        _actions.append((x,
                            get_description(model_class.actions[x])))
                else:
                    _actions.append((x, get_description(model_class.actions[x])))
            context[self.varname] = {'object_list': _actions, 'action': action, }
            return ''
            
        else:
            context[self.varname] = None
            return ''

#get_action_list for 'app.model' as varname
#get_action_list for queryset as varname
@register.tag
def get_action_list(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, 'USE: {% get_action_list for <"app.model"|model|queryset> as varname %}'
    if bits[1] != 'for' or bits[3] != 'as':
        raise TemplateSyntaxError, 'USE {% get_action_list for <"app.model"|model|queryset> as varname %}'
    if "'" in bits[2] or '"' in bits[2]:
        inst = bits[2]
    else:
        inst = parser.compile_filter(bits[2])
    return GetActionListNode(inst, bits[4])

@register.inclusion_tag('actions_select.html')
def show_actions(actions):
    return {'actions': actions}
