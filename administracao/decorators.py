from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def admin_member_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    # return view_func
    # coordenador, e = Group.objects.get_or_create(name="Coordenador SUS")
    return user_passes_test(
        lambda u: u.is_active and u.groups.filter(name="Coordenador SUS").exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )(view_func)


def profissional_member_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    # return view_func
    # profissinoal, e = Group.objects.get_or_create(name="Profissional Saude")
    return user_passes_test(
        lambda u: u.is_active and u.groups.filter(name="Profissional Saude").exists() and u.usuario.vinculos.filter(ativo=True).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )(view_func)

    