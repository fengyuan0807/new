from datetime import datetime

from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from meiduo_admin.serializers.statistical import GoodsVisitCountSerializer
from users.models import User


# 数据统计

# GET /meiduo_admin/statistical/total_count/
# 用户总人数
class UserTotalCountView(APIView):
    permission_classes = [IsAdminUser]

    # permission_classes = [IsAuthenticated]

    # # permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        count = User.objects.count()
        # 获取今天的日期
        now_date = timezone.now()
        response_data = {
            'count': count,
            # date: 只返回`年-月-日`
            'date': now_date.date(),
        }
        return Response(response_data)


# 日增用户统计
# GET /meiduo_admin/statistical/day_increment/
class UserDayIncrementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_joined__gte=now_date).count()
        response_data = {
            'count': count,
            'date': now_date.date()

        }
        return Response(response_data)


# 日活跃统计
# GET /meiduo_admin/statistical/day_active/
class UserDayActiveView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()
        response_data = {
            'count': count,
            'date': now_date.date()
        }
        return Response(response_data)


# 日下单统计
class UserDayOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # orders=user.orderinfo_set.all()[0]　user.orders.all()[0]
        count = User.objects.filter(orders__create_time__ghe=now_date).distinct().count()
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


# 一个月每日的新增量
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        # 结束日期
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 开始日期
        begin_date = now_date - timezone.timedelta(days=29)
        # # 当天的日期
        # current_date = begin_date
        moth_li = []
        while begin_date <= now_date:
            next_date = begin_date + timezone.timedelta(days=1)
            count = User.objects.filter(date_joined__gte=begin_date, date_joined__lt=next_date).count()
            moth_li.append({
                'count': count,
                'date': begin_date.date()
            })
            begin_date += timezone.timedelta(days=1)
        return Response(moth_li)


# 日分类商品访问量
class GoodsDayView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        now_date = timezone.now().date()
        from goods.models import GoodsVisitCount
        goods_visit_count = GoodsVisitCount.objects.filter(date=now_date)
        serializer = GoodsVisitCountSerializer(goods_visit_count, many=True)
        return Response(serializer.data)


