from django.shortcuts import render, redirect
import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from accounts.models import Token


def login(request):
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect("/")


def logout(request):
    auth_logout(request)
    return redirect('/')


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())

    Token.objects.create(email=email, uid=uid)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')

    send_mail('Your login link for Superlists', f'Use this link to login:\n\n{url}', 'noreplay@superlists', [email])

    return render(request, 'login_email_sent.html')
