from django.contrib.auth.models import UserManager


# Usamos esse CustomUserManager para pegar o usuario tanto pelo login
# quanto pelo e-mail, assim quanto o Backend do Authenticator do Django
# pegar o usuario, tanto o e-mail quanto o login poderao ser usados para fazer login
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        if '@' in username:
            return self.get(email__iexact=username)
        return self.get(username__iexact=username)
