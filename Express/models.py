from django.db import models


# Create your models here.
# from users.models import User


class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(choices=gender, max_length=32, verbose_name='性别')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    has_confirmed = models.BooleanField(default=False, verbose_name='邮箱认证')

    credit = models.IntegerField(default=10, verbose_name='信誉度')
    phone = models.CharField(max_length=20, verbose_name='手机号码', null=True, blank=True)
    verify = models.CharField(verbose_name='实名认证', max_length=32, default=-1)

    # TODO

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name='确认码')
    user = models.OneToOneField('User', verbose_name='关联的用户', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user.name + ":  " + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'


class Express(models.Model):
    publish_user = models.ManyToManyField(User, related_name='publish_user', verbose_name='发单者')
    receive_user = models.ManyToManyField(User, related_name='receive_user', verbose_name='接单者')

    publish_user_rate = models.IntegerField(verbose_name='发单评分', default=-1)
    receive_user_rate = models.IntegerField(verbose_name='接单评分', default=-1)

    express_number = models.CharField(max_length=30, verbose_name='快递单号')
    express_company = models.CharField(max_length=20, verbose_name='快递公司')
    detail = models.TextField(verbose_name='详细信息')

    status = models.CharField(max_length=30, verbose_name='状态', default='publish')

    # tags = TODO
    pub_date = models.DateTimeField(verbose_name='发布时间')
    receive_date = models.DateTimeField(verbose_name='接单时间', null=True, blank=True)
    finish_date = models.DateTimeField(verbose_name='完成时间', null=True, blank=True)
    express_height = models.IntegerField(verbose_name='是否超重')
    height_cost = models.FloatField(verbose_name='超重费用')
    hurry_cost = models.FloatField(verbose_name='加急费用')
    address = models.CharField(max_length=100, verbose_name='收货地址')
    latest_time = models.DateTimeField(verbose_name='期望收货时间')
    contact = models.CharField(max_length=20, verbose_name='联系方式')
    # TODO
    tip_cost = models.FloatField(verbose_name='小费')
    total_cost = models.FloatField(verbose_name='总价')

    def __str__(self):
        return self.express_number
        # TODO

    def user_name(self):
        return User.objects
