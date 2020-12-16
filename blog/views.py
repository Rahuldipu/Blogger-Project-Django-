from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings



# Create your views here.
def Send_Mail(to, name, title):
    from_email = settings.EMAIL_HOST_USER
    sub = "Confimation_mail"
    msg = EmailMultiAlternatives(sub,'',from_email,[to])

    d = {'name':name, 'title':title}

    html = get_template('email.html').render(d)
    msg.attach_alternative(html, 'text/html')
    msg.send()
    

def all_category():
    all_cat = Category.objects.all()
    return all_cat

def Home(request):
    all_cat =all_category()

    all_post = Post.objects.all()
    li = []
    b = 0
    for i in all_post:
        a = Post_Like.objects.filter(post=i)
        for j in a:
            b += j.like
        li.append(b)
        b = 0
    z = zip(all_post, li)
    recent, topthree = all_need_value()

    d = {'all_cat': all_cat, 'all_post': z, 'recent': recent, 'topthree': topthree}

    return render(request, 'index.html', d)

def About(request):
    all_cat = all_category()
    recent, topthree = all_need_value()
    d = {'all_cat': all_cat, 'recent': recent, 'topthree': topthree}

    return render(request, 'about.html', d)

def Contact(request):

    all_cat = all_category()
    d = {'all_cat': all_cat}
    return render(request, 'contact.html', d)

def Login(request):
    error = False
    if request.method == 'POST':
        u = request.POST.get('name')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('home')
            message1 = messages.info(request, 'You Logged in')
        else:
            error = True


    all_cat = all_category()
    d = {'all_cat': all_cat, 'error': error}
    return render(request, 'login.html', d)

def Signup(request):
    error2 = False
    if request.method == "POST":
        n = request.POST['name']
        e = request.POST['email']
        p = request.POST['password']
        u = request.POST['user']
        i = request.FILES['image']
        user = User.objects.filter(username=u)
        if user:
            error2 = True

        else:
            u = User.objects.create_user(username=u, password=p, email=e, first_name=n)
            User_detail.objects.create(image=i, user=u)
            return redirect('login')


    all_cat = all_category()
    d = {'all_cat': all_cat, 'error': error2}
    return render(request, 'signup.html', d)

def Blog_Like(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=pid)
    data = Post_Like.objects.filter(post=post).first()
    data2 = Post_Like.objects.filter(post=post, user=request.user)
    if data2:
        return redirect('home')
    else:
        if data and data2:
            data.like += 1
            data.save()
        else:
            Post_Like.objects.create(post=post, like=1, user=request.user)

    return redirect('home')

def Logout(request):
        auth.logout(request)
        return redirect('home')

def Blog_detail(request, pid):
    blog_detail = Post.objects.get(id=pid)

    all_cat = all_category()

    recent, topthree = all_need_value()
    d = {'all_cat': all_cat,'detail': blog_detail, 'recent': recent, 'topthree': topthree}
    return render(request, 'singlepage.html', d)

def Blog_Comment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    post = Post.objects.get(id=pid)

    if request.method == "POST":
        c = request.POST['Message']
        i = User_detail.objects.get(user=request.user)
        Comment.objects.create(post=post, user=request.user, comment=c, userdetail=i)
        return redirect('blogdetail', pid)


def blog_pannel(request):
    all_post = Post.objects.filter(user=request.user)
    recent, topthree = all_need_value()
    user_detail = User_detail.objects.filter(user=request.user).first()
    d = {'all_cat': all_category(), 'all_post': all_post, 'recent': recent, 'topthree': topthree, 'detail': user_detail}
    return render(request, 'fashion.html', d)

def delete_blog(request,pid):
    data = Post.objects.get(id=pid)
    data.delete()
    return redirect('fashion')

def Add_blog(request):
    if request.method=="POST":
        c = request.POST['cid']
        t = request.POST['title']
        s = request.POST['subtitle']
        d = request.POST['description']
        i = request.FILES['image']
        cat = Category.objects.get(id=c)
        td = date.today()
        Post.objects.create(category=cat, title=t, sub_title=s, description=d, image=i, user=request.user, date=td)
        Send_Mail(request.user.email, request.user.username, t)
        return redirect('fashion')
        
    recent, topthree = all_need_value()
    d = {'all_cat': all_category(), 'recent':recent, 'topthree': topthree}

    return render(request, 'addblog.html', d)


def Category_post(request,cid):
    data = Category.objects.get(id=cid)
    all_post = data.post_set.all()
    recent, topthree = all_need_value()
    d = {'all_cat': all_category(), 'all_post': all_post, 'data':data, 'recent':recent, 'topthree': topthree}
    return render(request, 'category_post.html', d)

def all_need_value():
    all_post = Post.objects.all().order_by('-id')
    recent = all_post[:3]
    li = []
    pos = []
    for i in all_post:
        a = i.post_like_set.count()
        li.append(a)
    for i in all_post:
        if max(li) > 0:
            a = max(li)
            ind = li.index(a)
            pos.append(all_post[ind])
            li.pop(ind)
            li.insert(ind, 0)
    topthree = pos[:3]
    return recent, topthree

def Edit_detail(request):
    data = User_detail.objects.get(user=request.user)
    if request.method=="POST":
        n = request.POST['name']
        e = request.POST['email']
        request.user.username = n
        request.user.email = e
        request.user.save()
        try:
            i = request.FILES['image']
            data.image = i
            data.save()
        except:
            pass
    d = {'all_cat': all_category(), 'data': data}
    return render(request, 'edit_detail.html', d)


def Change_password(request):
    error = False
    if request.method == "POST":
        p1 = request.POST['pwd1']
        p2 = request.POST['pwd2']
        udata = authenticate(username=request.user, password=p1)
        if udata:
            udata.set_password(p2)
            udata.save()
            login(request, udata)
        else:
            error = True
    d = {'error': error}
    return render(request, 'change_password.html', d)