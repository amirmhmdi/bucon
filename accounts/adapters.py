from allauth.account.adapter import DefaultAccountAdapter


class NoSignupAccountAdapter(DefaultAccountAdapter):
    """Accounts are created by a manager (labor) or an admin (manager/admin) —
    there is no public sign-up form on this site."""

    def is_open_for_signup(self, request):
        return False
