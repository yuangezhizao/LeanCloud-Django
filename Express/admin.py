from django.contrib import admin

# Register your models here.
from .models import User, ConfirmString, Express


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'has_confirmed', 'credit',)
    list_filter = ('credit', 'has_confirmed', )
    list_per_page = 10
    search_fields = ['name']


class ExpressAdmin(admin.ModelAdmin):
    list_display = ('id', 'express_number', 'express_company', 'detail', 'address', 'height_cost', 'hurry_cost', 'total_cost', 'status', 'publish_user_rate', 'receive_user_rate')
    list_filter = ('express_company', 'status',)
    list_per_page = 10
    search_fields = ['express_number']
    date_hierarchy = 'pub_date'
    # filter_horizontal = ('publish_user', 'receive_user', )  # 只针对多对多


admin.site.register(User, UserAdmin)
admin.site.register(Express, ExpressAdmin)
admin.site.register(ConfirmString)
