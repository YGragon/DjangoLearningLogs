from django.conf.urls import url
from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views
from . import views

app_name='leaning_log'
urlpatterns = [
    # 登录页面. template_name表示使用的是模板中的登录页面，
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),

    # 退出登录.
    url(r'^logout/$', views.logout_view, name='logout'),

    # 注册页面.
    url(r'^register/$', views.register, name='register'),

    # 修改密码页面.
    url(r'^password-change/$', auth_views.password_change,
        {"post_change_redirect":"/users/password-change-done"}, name='password_change'),

    # 修改密码完成页面.
    url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),
]