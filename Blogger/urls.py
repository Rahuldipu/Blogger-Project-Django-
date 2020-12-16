"""Blogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='home'),
    path('about', About, name = 'about'),
    path('contact', Contact, name = 'contact'),
    path('login', Login, name = 'login'),
    path('signup', Signup, name = 'signup'),
    path('like/(?P<pid>[0-9]+)', Blog_Like, name = 'like'),
    path('logout', Logout, name = 'logout'),
    path('blogdetail/(?P<pid>[0-9]+)', Blog_detail, name = 'blogdetail'),
    path('blogcomment(?P<pid>[0-9]+)', Blog_Comment, name='blogcomment'),
    path('fashion', blog_pannel, name='fashion'),
    path('deleteblog/(?P<pid>[0-9]+)', delete_blog, name='deleteblog'),
    path('addblog', Add_blog, name="addblog"),
    path('categorypost/(?P<cid>[0-9]+)', Category_post, name='categorypost'),
    path('edit_detail', Edit_detail, name="edit"),
    path('change_password', Change_password, name="change"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
