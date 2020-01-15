from django.conf.urls import url

from meiduo_admin.views import orders
from meiduo_admin.views import permissions
from meiduo_admin.views import users, statistical, channels, skus, spus
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url('^authorizations/$', users.AdminAuthorizeView.as_view()),
    # 数据统计
    url('^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url('^statistical/day_increment/$', statistical.UserDayIncrementView.as_view()),
    url('^statistical/day_active/$', statistical.UserDayActiveView.as_view()),
    url('^statistical/day_orders/$', statistical.UserDayActiveView.as_view()),
    url('^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url('^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    # 用户管理
    url('^users/$', users.UserInfoView.as_view()),

    # 1. 获取频道组数据
    url('^goods/channel_types/$', channels.ChannelGroupView.as_view()),
    # 2 获取一级分类
    url('^goods/categories/$', channels.GoodsCategoryView.as_view()),
    # 3 获取三级分类
    url('^skus/categories/$', channels.GoodCategory3View.as_view()),

    #  获取SKU商品简单数据
    url('^skus/simple/$', skus.SKUSimpleView.as_view()),
    # 获取SPU商品简单数据
    url('^goods/simple/$', spus.SPUSimpleView.as_view()),
    # 获取 spu 规格数据
    url('^goods/(?P<pk>\d+)/specs/$', spus.SPUSpecView.as_view()),

    # 权限类型
    # url('^permission/content_types/$', permissions.PermissionViewSet.as_view({
    #     'get': 'content_types'
    # })),
    url('^permission/content_types/$', permissions.Content_typesView.as_view()),
    # 权限简单数据
    url('^permission/simple/$', permissions.GroupViewSet.as_view({
        'get': 'simple'
    })),
    # 用户组简单数据
    url('^permission/groups/simple/$', permissions.AdminUserViewSet.as_view({
        'get': 'simple'
    })),
]

# 频道管理
router = DefaultRouter()
router.register('goods/channels', channels.ChannelViewSet, base_name='channels')
urlpatterns += router.urls

# 图片管理
router = DefaultRouter()
router.register('skus/images', skus.SKUImagesViewSet, base_name='images')
urlpatterns += router.urls

# sku管理
router = DefaultRouter()
router.register('skus', skus.SKUViewSet, base_name='skus')
urlpatterns += router.urls

# 订单管理
router = DefaultRouter()
router.register('orders', orders.OrdersViewSet, base_name='orders')
urlpatterns += router.urls

# 权限管理
router = DefaultRouter()
router.register('permission/perms', permissions.PermissionViewSet, base_name='perms')
urlpatterns += router.urls

# 用户组
router = DefaultRouter()
router.register('permission/groups', permissions.GroupViewSet, base_name='groups')
urlpatterns += router.urls

# 管理员用户
router = DefaultRouter()
router.register('permission/admins', permissions.AdminUserViewSet, base_name='admins')
urlpatterns += router.urls