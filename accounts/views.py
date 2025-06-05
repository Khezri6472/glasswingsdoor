from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm

def combined_auth_view(request):
    login_form = LoginForm()
    signup_form = SignupForm()
    return render(request, 'account/login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })