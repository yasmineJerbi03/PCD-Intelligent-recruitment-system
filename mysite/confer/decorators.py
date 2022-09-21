from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('index')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse("vous n'avez pas l'autorisation")
        return wrapper_func
    return decorator

def candidat_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'les_recruteurs':
            return redirect("profil_recr")
        if group == 'les_candidats':
            return view_func(request, *args, **kwargs)
    return wrapper_function


def recruteur_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'les_candidats':
            return redirect("profil_cand")
        if group == 'les_recruteurs':
            return view_func(request, *args, **kwargs)
    return wrapper_function

