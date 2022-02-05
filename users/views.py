from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegistrationForm, LoginForm, ForgotPassword, GetCodeForm
from .models import UserModel
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import update_session_auth_hash
from config.helpers import *
from django.core.exceptions import ValidationError


def home_view(request):
    return render(request, "main/index.html")


class UserRegistration(View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def get(self, request):
        form = RegistrationForm()
        context = "Ro'yxatdan o'tish"
        return render(request, "main/sign_up.html", {
            'form': form,
            "title": context
        })

    def post(self, request):
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            send_sms_code(request, data["phone"]) #998944030702
            del data['confirm']
            user = UserModel(**data)
            user.set_password(user.password)
            user.save()
            return redirect('login')
        return render(request, "main/sign_up.html", {
            'form': form
        })


def user_login(request):
    request.title = "Kirish"

    form = LoginForm()
    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect('home')

            form.add_error('password', "Foydalanuvchi nomi va parol noto'g'ri!")
        return render(request, 'main/sign_in.html', {
            'form': form,
        })
    return render(request, 'main/sign_in.html', {
        'form': form
    })




@login_required
def user_logout(request):
    logout(request)
    return redirect("login")



def forgot_password(request):
    request.title = "Parolni unutdingizmi"
    form = ForgotPassword()
    if request.method == "POST":
        form = ForgotPassword(request.POST)
        if form.is_valid() and request.method == "POST":
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["new_password"]
            if UserModel.objects.filter(phone=phone).exists():
                send_sms_code(request, phone)
                request.session["recovery"] = {
                    "phone": phone,
                    "new_password": password
                }
                get_code_form = GetCodeForm()
                return render(request, "main/get_code.html", {
                    "form": get_code_form,
                    "request.title": "Kodni yuboring"
                })
    return render(request, "main/forgot_password.html", {
        'form': form,
    })



@require_POST
def post_code(request):
    # request.title = "Kodni yuboring"

    data = request.session.get("recovery")
    if request.method != "POST" or data["phone"] is None:
        return redirect('forgot_password')

    code = request.POST.get("code")

    if data["phone"] is None or not validate_sms_code(data["phone"], code):
        return False

    user = UserModel.objects.get(phone=data["phone"])
    user.set_password(data["new_password"])
    user.save()

    return redirect("login")


