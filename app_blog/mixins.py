from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMessageMixin(AccessMixin):
    login_url = 'login'  
    message = "Para acceder a esta página debes iniciar sesión."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, self.message)
            login_url = reverse(self.login_url)
            return redirect(f'{login_url}?next={request.path}')
        return super().dispatch(request, *args, **kwargs)