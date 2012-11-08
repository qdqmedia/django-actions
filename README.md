django-actions
==============

A small and simple application which would help you to implement actions similar to
**django.contrib.admin** case for your custom tasks outside *django admin* app.


Installation
-------------

Using *pip*:

    pip install https://github.com/qdqmedia/django-actions.git

Adding *django-actions* to *INSTALLED_APPS*:

    INSTALLED_APPS += (
        'django_actions'
    )


Usage
------

You should create a *view* based Django class which inherits from a **mixin** view
called **ActionViewMixin**. Your view shoud returns a [HttpResponse](https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpResponse) object. Also, your view will define a list with *actions* (functions or methods).

*django-actions* provides a simple template for creating a *select* HTML node (*combobox*)
which contains those actions that can be executed.

Keep in mind that *django-actions* will use two *HTTP sessions* variables to store
selected *queryset* (**serialized\_qs**), *model* class (**serialized\_model_qs**) used by
that *queryset*, and number of items in *queryset* without pagination (**all\_items\_count**).
This last one value is very useful to display a link for selecting all items.

Example
--------

In your **views.py** file:

    from django_actions.views import ActionViewMixin
    from .actions import assign_service_action

    class ServiceList(ActionViewMixin, ListView):
        actions = [assign_service_action]


In your **actions.py** file:

    def assign_service_action(**kwargs):
        return HttpResponseRedirect('.')

In your *template* file:

    <form action="" method="post" id="id_action_posts" class="form-inline">
    {% include 'actions_select.html' %}


