from django.contrib.auth.mixins import LoginRequiredMixin

class ProtectedMixin(LoginRequiredMixin):
    login_url = "/account/login/"