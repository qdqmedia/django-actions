django-actions
==============

A small and simple application which would help you to implement actions similar to
**django.contrib.admin** case for your custom tasks outside django admin. Also it
provides custom form support if you would like to change some data for the queryset instances.

Based on [Django-actions](https://github.com/tarvitz/django-actions)

Actions
-------

You can create two kind of actions:

1. Actions which execute some code and return a *redirection* to *referer* page.

2. Actions which need a intermediate template and view, then return a *redirection* to a specific URL.

Usage
------

Let's imagine that we need a simple action for updating a set of records. First, we're going to
add a this action to our model called **Service**:

    class Service(models.Model):

    {...}

    actions = [update_services_action]

Now, we need to create a **actions.py** file in our application with the following code:


    def update_services_action(model, request, qset, **kwargs):
        for service in qset:
            service.save()
        return {'qset': qset, 'message': _('Services has been updated!')}

If your action pass a key called *message*, **django-actions** will use *Django's message framework* to
display that message.

The template where we're going to show *actions* for executing must contain a *form* as shows
following code:

    {% get_action_list for myapp.service as actions %}

    {% if actions.object_list %}
        <p>
            <form action="{% url actions:action actions.action %}" method="post" id="id_action_posts" class="form-inline">
            {% csrf_token %}
            {% show_actions actions.object_list %}
         </p>
    {% endif %}


Keep in mind that **get\_action\_list** is a template tag implemented in **django-actions** which needs to
receive application name followed by dot and model class name. In our example is **myapp.service** because our
application is called **myapp** and **service** is our model.

Advanced usage
--------------

If we need to write a intermediate template and view, our action should return a **redirection** object as
a value for a *key* called **response** inside a dictionary. Then a new view take the control and shoud
deal with params receive for *form* which contains selected items in previous web page.

For example, the following action captures selected items and executes a redirection to a new view:

    def assign_service_action(model, request, qset, **kwargs):
        ct = ContentType.objects.get_for_model(qset.model)
        selected = request.POST.getlist('items')
        obj_redirect = HttpResponseRedirect(reverse('workflow:assign-service') +\
                                                    '?ct={0}&ids={1}'.format(ct.pk,
                                                                             ','.join(selected)))
        return {'response': obj_redirect}


Don't forget to use *items* to get values for selected items in previous web page.
