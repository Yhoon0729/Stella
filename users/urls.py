"""
URL configuration for Stella project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from users import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("userinfo/", views.userinfo, name="userinfo"),
    path("userupdate/", views.userupdate, name="userupdate"),
    path("passupdate/", views.passupdate, name="passupdate"),
    path("userdelete/", views.userdelete, name="userdelete"),
    path("finduserid/", views.finduserid, name="finduserid"),
    path("findpassword/", views.findpassword, name="findpassword"),
    path("resetpassword/", views.resetpassword, name="resetpassword"),
    # path("verify_email/", views.verify_email, name="verify_email"),
    # path("verify_code/", views.verify_code, name="verify_code"),
]
