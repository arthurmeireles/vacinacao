from django.contrib.auth.models import User
from social.exceptions import AuthException


def associate_by_username(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.

    This pipeline entry is not 100% secure unless you know that the providers
    enabled enforce email verification on their side, otherwise a user can
    attempt to take over another user account by using the same (not validated)
    email address on some provider.  This pipeline entry is disabled by
    default.
    """
    if user:
        return None

    username = details.get('username')
    if username:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = User.objects.filter(username=username)
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given username is associated with another account'
            )
        else:
            return {'user': users[0],
                    'is_new': False}
