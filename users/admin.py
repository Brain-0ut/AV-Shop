from django.contrib import admin

from AVShop import models as shop
from . import models


class ProductsInline(admin.TabularInline):
    model = shop.Product
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [ProductsInline]
    list_display = ('username', 'token')


admin.site.register(models.User, UserAdmin)
