from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def clean_username(self, username):
        return username

    def clean_email(self, email):
        return ""
