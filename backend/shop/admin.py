from django.contrib import admin
from .models import Category, Product, CustomUser, Order, OrderItem, ShippingAddress, ShoppingSession, Tag, Image, ProductImage
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_seller', 'is_active')
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        ('Main information', {'fields': ('username', 'password', 'first_name', 'last_name')}),
        ('Contact information', {'fields': ('email', 'phone_number', 'postal_code', 'address', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_seller', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ('Main information', {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name')}
        ),
        ('Contact information', {'fields': ('email', 'phone_number', 'postal_code', 'address', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_seller', 'is_active', 'groups', 'user_permissions')}),
    )
    list_display_links = ('username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_name')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'availability')
    list_filter = ('category',)
    inlines = [ProductImageInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity', 'date_added')
    list_filter = ('product', 'customer')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id', 'session')
    list_filter = ('customer', 'complete', 'date_ordered')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'address', 'postal_code', 'date_added')
    list_filter = ('customer', 'order', 'date_added')


@admin.register(ShoppingSession)
class ShoppingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'user', 'active')
    list_filter = ('session_key', 'user', 'active')


