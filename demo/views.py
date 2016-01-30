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
    return HttpResponseRedirect(reverse('demo:index'))

def login(request):
    initial = {
        'remember_me': 'true',
        'next_url': request.GET.get('next', reverse('demo:index'))
    }
    context = {
        'title': 'Log In',
        'form': LoginForm(initial=initial),
    }
    return render(request, 'demo/login.html', context)

def request_login(request):
    if request.method != 'POST':
        messages.add_message(request, messages.INFO,
                             'Invalid request.')
        return HttpResponseRedirect(reverse('demo:login'))

    form = LoginForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.INFO,
                             'Invalid credentials.')
        return HttpResponseRedirect(reverse('demo:login'))
        
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    next_url = form.cleaned_data['next_url']
    user = authenticate(username=username, password=password)
    if user is None:
        messages.add_message(request, messages.INFO,
                             'Incorrect username of password.')
        return HttpResponseRedirect(reverse('demo:login'))

    if not user.is_active:
        messages.add_message(request, messages.INFO,
                             'Sorry, this account has been disabled.')
        return HttpResponseRedirect(reverse('demo:login'))

    auth_login(request, user)
    return HttpResponseRedirect(next_url)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('demo:login'))

@login_required
def index(request):
    context = {
        'data': sorted(rados.get_object_list()),
        'title': 'Dashboard',
    }
    return render(request, 'demo/index.html', context)

@login_required
def details(request, object_name):
    data = rados.get_data(object_name)
    context = {
        'title': object_name,
        'object_name': object_name,
        'data': data,
    }
    return render(request, 'demo/details.html', context)

@login_required
def edit(request, object_name):
    data = rados.get_data(object_name)
    form = EditObjectForm(initial={'data': data, 
                                   'object_name': object_name})
    context = {
        'title': 'Edit ' + object_name,
        'object_name': object_name,
        'data': data,
        'form': form,
    }
    return render(request, 'demo/edit.html', context)

@login_required
def update(request, object_name):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('demo:index'))

    if not rados.is_valid_name(object_name):
        messages.add_message(request, messages.INFO,
            'Invalid object name. Only letters, numbers ' + \
            'and dashes are allowed.')
        return HttpResponseRedirect(reverse('demo:index'))

    form = EditObjectForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.INFO,
                             'The data provided was invalid.')
        return HttpResponseRedirect(reverse('demo:edit', 
                                            args=(object_name,)))
        
    data = form.cleaned_data['data']
    if rados.store_object(object_name, data):
        message = 'Object stored successfully.'
    else:
        message = 'Unable to complete the request.'
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('demo:details',
                                        args=(object_name,)))

@login_required
def delete(request, object_name):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('demo:index'))

    if not rados.exists(object_name):
        messages.add_message(request, messages.INFO,
            'Object %s not found.' % object_name)
        return HttpResponseRedirect(reverse('demo:index'))
    else:
        rados.delete_object(object_name)
        messages.add_message(request, messages.INFO,
            'Object %s deleted!' % object_name)
        return HttpResponseRedirect(reverse('demo:index'))
        
@login_required
def create(request):
    form = CreateObjectForm()
    context = {
        'title': 'Create New Object',
        'form': form,
    }
    return render(request, 'demo/create.html', context)

@login_required
def store(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('demo:index'))

    form = CreateObjectForm(request.POST)
    if not form.is_valid():
        messages.add_message(request, messages.INFO,
                             'The data provided was invalid.')
        return HttpResponseRedirect(reverse('demo:create'))
        
    data = form.cleaned_data['data']
    object_name = form.cleaned_data['object_name']
    if not rados.is_valid_name(object_name):
        messages.add_message(request, messages.INFO,
            'Invalid object name. Only letters, numbers ' + \
            'and dashes are allowed.')
        return HttpResponseRedirect(reverse('demo:create'))

    if rados.exists(object_name):
        messages.add_message(request, messages.INFO,
            'Object already exists!')
        return HttpResponseRedirect(reverse('demo:create'))

    if rados.store_object(object_name, data):
        message = 'Object created successfully.'
    else:
        message = 'Unable to complete the request.'
                             
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('demo:details',
                                        args=(object_name,)))

