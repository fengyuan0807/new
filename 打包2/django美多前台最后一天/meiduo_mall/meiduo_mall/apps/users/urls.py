from django.conf.urls import url

from . import views

# from meiduo_mall.meiduo_mall.apps.users import views 必须是导入一个包才能导入

urlpatterns = [
    # 用户注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 用户名是否重复注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    url(r'^emails/$', views.EmailView.as_view(), name='emails'),
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    url(r'^addresses/$', views.AddressView.as_view(), name='address'),# 展示用户地址
    url(r'^addresses/create/$', views.CreateAddressView.as_view()),# 展示新增用户地址
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    url(r'^pass/$', views.ChangePasswordView.as_view(),name='pass'),
    url(r'^browse_histories/$', views.UserBrowseHistory.as_view()),# 保存和查询浏览记录


]
