from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .utils import radosBindings as rados
from .forms import CreateObjectForm, EditObjectForm, LoginForm


def home(request):
    return HttpResponseRedirect(reverse('demo:container'))

def login(request):
    handlers = {
        'GET' : present_login_form,
        'POST': login_user,
    }
    return dispatch(request, handlers)

def logout(request):
    handlers = {
        'GET': logout_user,
    }
    return dispatch(request, handlers)

@login_required
def object_container(request):
    handlers = {
        'GET' : present_object_container,
        'POST': create_new_object,
    }
    return dispatch(request, handlers)

@login_required
def object_view(request, object_name):
    handlers = {
        'GET'   : present_object(object_name),
        'PUT'   : update_object(object_name),
        'DELETE': delete_object(object_name),
        'POST'  : delete_too_hard(object_name), # walkaround to put/delete items through a browser
    }
    return dispatch(request, handlers)

def dispatch(request, handlers):
    if not request.method in handlers:
        # TODO 405 page
        messages.add_message(request, messages.ERROR, 'Invalid request.')
        return HttpResponseRedirect(reverse('demo:container'))
    return handlers[request.method](request)

""" 
    User login and logout
"""
def present_login_form(request):
    initial = {
        'remember_me': 'true',
        'next_url': request.GET.get('next', reverse('demo:container'))
    }
    context = {
        'title': 'Log In',
        'form': LoginForm(initial=initial),
    }
    return render(request, 'demo/login.html', context)

def login_user(request):
    if request.method != 'POST':
        messages.add_message(request, messages.ERROR,
                             'Invalid request.')
        return HttpResponseRedirect(reverse('demo:login'))

    form = LoginForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR,
                             'Invalid credentials.')
        return HttpResponseRedirect(reverse('demo:login'))
        
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    next_url = form.cleaned_data['next_url']
    user = authenticate(username=username, password=password)
    if user is None:
        messages.add_message(request, messages.ERROR,
                             'Incorrect username of password.')
        return HttpResponseRedirect(reverse('demo:login'))

    if not user.is_active:
        messages.add_message(request, messages.ERROR,
                             'Sorry, this account has been disabled.')
        return HttpResponseRedirect(reverse('demo:login'))

    auth_login(request, user)
    return HttpResponseRedirect(next_url)

def logout_user(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('demo:login'))

"""
    Object container views
"""
def present_object_container(request):
    context = {
        'data' : sorted(rados.get_object_list()),
        'title': 'Dashboard',
    }
    return render(request, 'demo/index.html', context)

"""
    Object views
"""
def present_object(object_name):
    def handler(request):
        data = rados.get_data(object_name)
        view = request.GET.get('view')
        if view == 'createform':
            renderer = create_object_form
        elif view == 'editform':
            renderer = object_view_editform
        else:
            renderer = object_view_html
        return renderer(request, object_name, data)
    return handler

def object_view_html(request, object_name, data):
    context = {
        'title': object_name,
        'object_name': object_name,
        'data': data,
    }
    return render(request, 'demo/details.html', context)

def object_view_editform(request, object_name, data):
    initial = {'data': data, 'object_name': object_name}
    form = EditObjectForm(initial=initial)
    context = {
        'title': 'Edit ' + object_name,
        'object_name': object_name,
        'data': data,
        'form': form,
    }
    return render(request, 'demo/edit.html', context)

def create_object_form(request, object_name, data):
    form = CreateObjectForm()
    context = {
        'title': 'Create New Object',
        'form' : form,
    }
    return render(request, 'demo/create.html', context)

def update_object(object_name):
    def handler(request):
        if not rados.is_valid_name(object_name):
            messages.add_message(request, messages.ERROR,
                'Invalid object name. Only letters, numbers ' + \
                'and dashes are allowed.')
            return HttpResponseRedirect(reverse('demo:container'))
 
        form = EditObjectForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR,
                                 'The data provided was invalid.')
            return HttpResponseRedirect(reverse('demo:object', 
                                                args=(object_name,), 
                                                kwargs={'view': 'editform'}))

        data = form.cleaned_data['data']
        if rados.store_object(object_name, data):
            messages.add_message(request, messages.INFO, 
                                 'Object stored successfully.')
        else:
            messages.add_message(request, messages.ERROR, 
                                 'Unable to complete the request.')
        return HttpResponseRedirect(reverse('demo:object', args=(object_name,)))
    return handler

def delete_too_hard(object_name):
    def handler(request):
        method = request.GET.get('_method', None)
        if method == 'delete':
            return delete_object(object_name)(request)
        elif method == 'put':
            return update_object(object_name)(request)
        else:
            # TODO 405 page
            messages.add_message(request, messages.ERROR, 'Invalid request.')
            return HttpResponseRedirect(reverse('demo:container'))
    return handler

def delete_object(object_name):
    def handler(request):
        if rados.delete_object(object_name):
            messages.add_message(request, messages.INFO,
                'Object %s deleted!' % object_name)
        else:
            messages.add_message(request, messages.ERROR,
                'Unable to delete object %s.' % object_name)
        return HttpResponseRedirect(reverse('demo:container'))
    return handler
        
def create_new_object(request):
    form = CreateObjectForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR,
                             'The data provided was invalid.')
        return HttpResponseRedirect(reverse('demo:object', kwargs={'view': 'createform'}))
        
    data = form.cleaned_data['data']
    object_name = form.cleaned_data['object_name']
    if not rados.is_valid_name(object_name):
        messages.add_message(request, messages.ERROR,
            'Invalid object name. Only letters, numbers ' + \
            'and dashes are allowed.')
        return HttpResponseRedirect(reverse('demo:create'))

    if rados.exists(object_name):
        messages.add_message(request, messages.ERROR,
                             'Object already exists!')
        return HttpResponseRedirect(reverse('demo:create'))

    if rados.store_object(object_name, data):
        messages.add_message(request, messages.INFO, 
                             'Object created successfully.')
    else:
        messages.add_message(request, messages.ERROR,
                             'Unable to complete the request.')

    return HttpResponseRedirect(reverse('demo:object', args=(object_name,)))


