from django.http import HttpResponse
from django.shortcuts import redirect


#DECORATOR TAKES ANOTHER FUNCTION AS PARAMETER TO ADD EXTRA FUNCTIONALITY BEFORE MAIN FUNCTION
def unauthenticated_user(viewFunc): #  viewFunc is function  for login.html
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        elif request.user.is_authenticated == None:
            return redirect('login')
        else:
            return viewFunc(request, *args, **kwargs)
    return wrapper

def func_to_allow(allowed_groups=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
                # return redirect('fyp_navbar')
                # return HttpResponse("<h1>Sorry, You Are Not The Authorized Person To Access This Page</h1>")
        return wrapper
    return decorator

def admins_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0]
        if group == 'customers':
            return redirect('dashboard')
        if group == 'admins':
            return redirect('home')
    return wrapper