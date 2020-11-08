from django.shortcuts import render, redirect
import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from accounts.models import Token



