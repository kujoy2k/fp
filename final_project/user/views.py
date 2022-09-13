from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user.models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


def index(request):
    user = User.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymous User!"
    print("Logged in?", request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "Anonymous User!"
    print(email)
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    msg = None
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form = AuthenticationForm(request, request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        print(form.is_valid)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
                return render(request, "index.html", {"form": form, "msg": msg})
        return render(request, "login.html", {"form": form, "msg": msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            username = form.cleaned_data.get("username")
#            email = form.cleaned_data.get("email")
#            raw_password = form.cleaned_data.get("password")
#            remember_me = form.cleaned_data.get("remember_me")
#            msg = "올바른 유저ID와 패스워드를 입력하세요."
#            try:
#                user = User.objects.get(username=username)
#            except User.DoesNotExist:
#                pass
#            else:
#                if user.check_password(raw_password):
#                    msg = None
#                    login(request, user)
#                    is_ok = True
#                    request.session["remember_me"] = remember_me
#                    return redirect("index.html")
#    else:
#        msg = None
#        form = LoginForm()
#        print("REMEMBER_ME: ", request.session.get("remember_me"))
#    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    logout(request)						
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    page = int(request.GET.get("p",1))
    users = User.objects.all().order_by("id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
