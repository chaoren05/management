from django.shortcuts import render,redirect, HttpResponse
from app01 import models

# Create your views here.
'''
def login(req):
    # models.Administrator.objects.create(
    #     username="yongchang",
    #     password="123123"
    # )
    message = ""
    if req.method == 'POST':
        user = req.POST.get('user')
        pwd = req.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            # rep = redirect('/index.html')
            # rep.set_cookie('username', user, max_age=10)
            # rep.set_cookie('email', user+'@live.com')
            # rep = redirect('/index.html')
            # rep.set_cookie('username', user)
            # rep.set_cookie('account', "12341234")
            # rep.set_cookie('pwd', "wrefdsfsfs")
            rep = redirect('/index.html')
            rep.set_signed_cookie('username', user)
            rep.set_signed_cookie('account', "12341234")
            rep.set_signed_cookie('pwd', "wrefdsfsfs")
            return rep
        else:
            message = "用户名或密码错误"
    return render(req, "login.html", {"msg":message})

def index(req):
    # username = req.COOKIES.get('username')
    username = req.get_signed_cookie('username')
    if username:
        return render(req, "index.html", {'username':username})
    else:
        return redirect('/login.html')

def test(req):
    obj = HttpResponse("ok")
    import datetime
    v = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    obj.set_cookie('k1', 'v1', max_age=30, expires=v)
    # obj.set_cookie('k2', 'v2', max_age=30, expires=v, path='/test.html')
    obj.set_cookie('k2', 'v2', max_age=30, expires=v, domain='oldboy.com')
    return obj

def xiaohu(req):
    v = req.COOKIES.get('k2')
    return HttpResponse(v)

def js_cookie(req):
    print(req.COOKIES)
    obj=render(req, 'js_cookie.html')
    obj.set_cookie('guoyongchang','girl')
    return obj
'''

from django import views
from django.utils.decorators import method_decorator

def outer(func):
    def inner(req, *args, **kwargs):
        print(req.method)
        return func(req, *args, **kwargs)
    return inner

class Login(views.View):

    def dispatch(self, req, *args, **kwargs):
        ret = super(Login, self).dispatch(req, *args, **kwargs)
        return ret

    @method_decorator(outer)
    def get(self, req, *args, **kwargs):
        return render(req, 'login.html', {'msg':''})

    @method_decorator(outer)
    def post(self, req, *args, **kwargs):
        user = req.POST.get('user')
        pwd = req.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            req.session['is_login'] = True
            req.session['username'] = user
            rep = redirect('/index.html')
            return rep
        else:
            message = "用户名或密码错误!"
            return render(req, 'login.html', {'msg': message})


def login(req):
    message = ""
    v = req.session
    print(type(v))
    from django.contrib.sessions.backends.db import SessionStore
    if req.method == 'POST':
        user = req.POST.get('user')
        pwd = req.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            req.session['is_login'] = True
            req.session['username'] = user
            rep = redirect('/index.html')
            return rep
        else:
            message = "用户名或密码错误"
    obj = render(req, "login.html", {"msg":message})
    return obj

def index(req):
    # username = req.COOKIES.get('username')
    username = req.get_signed_cookie('username')
    if username:
        return render(req, "index.html", {'username':username})
    else:
        return redirect('/login.html')

def logout(req):
    req.session.clear()
    return redirect('/login.html')

def auth(func):
    def inner(req, *args, **kwargs):
        is_login = req.session.get('is_login')
        if is_login:
            return func(req, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner

@auth
def index(req):
    current_user = req.session.get('username')
    return render(req, 'index.html', {'usernmae': current_user})

@auth
def handle_classes(req):
    current_user = req.session.get('username')
    return render(req, 'class.html', {'username': current_user})



def classes(req):
    pass
