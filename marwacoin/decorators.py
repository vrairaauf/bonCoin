from django.shortcuts import redirect


#si le client est en cour de session alors n a pas de possibilote de voir la page login ou register
def notLoggedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



#cette fonction pour differencier les differents group dutilisateur
def allowed_users(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowedGroups:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home_page')
        return wrapper_func
    return decorator




def notLoggedAuteur(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
