import uuid
from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.contrib.sessions.models import Session
from django.core.validators import FileExtensionValidator
from crum import get_current_user, get_current_request
from .services import datetime_now

from django.db.models import ImageField, FileField, signals
from django.dispatch import dispatcher, Signal
from django.conf import settings
import shutil, os, glob, re
from distutils.dir_util import mkpath


ext_validator = FileExtensionValidator(['png', 'jpg'])




class CustomUser(AbstractUser, PermissionsMixin):
    is_seller = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomImageField(ImageField):
    """Allows model instance to specify upload_to dynamically.

    Model class should have a method like:

        def get_upload_to(self, attname):
            return 'path/to/{0}'.format(self.id)
    """
    def __init__(self, *args, **kwargs):
        kwargs['upload_to'] = kwargs.get('upload_to', 'tmp')

        try:
            self.use_key = kwargs.pop('use_key')
        except KeyError:
            self.use_key = False

        super(CustomImageField, self).__init__(*args, **kwargs)


    def _move_image(self, instance=None):
        """
            Function to move the temporarily uploaded image to a more suitable directory 
            using the model's get_upload_to() method.
        """
        if hasattr(instance, 'get_upload_to'):
            src = getattr(instance, self.attname)
            if src:
                m = re.match(r"%s/(.*)" % self.upload_to, src)
                if m:
                    if self.use_key:
                        dst = "%s/%d_%s" % (instance.get_upload_to(self.attname), instance.id, m.groups()[0])
                    else:
                        dst = "%s/%s" % (instance.get_upload_to(self.attname), m.groups()[0])
                    basedir = "%s%s/" % (settings.MEDIA_ROOT, os.path.dirname(dst))
                    mkpath(basedir)
                    shutil.move("%s%s" % (settings.MEDIA_ROOT, src),"%s%s" % (settings.MEDIA_ROOT, dst))
                    setattr(instance, self.attname, dst)
                    instance.save()

    def db_type(self, x):
        """Required by Django for ORM."""
        return 'varchar(100)'


# def user_directory_path(instance, filename):
#     print(instance.__dict__, filename)
#     date_now = datetime_now()
#     print(date_now.strftime("%Y-%m-%d"))
#     return f'images/product_images/{instance.id}/{filename}'


# Load multiple files
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/ 'images/product_images/%Y-%m-%d'
class Image(models.Model):
    def user_directory_path(instance, filename):
        print(instance, filename)
        date_now = datetime_now()
        print(date_now.strftime("%Y-%m-%d"))
        return f'images/product_images/{instance.id}/{filename}'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img_name = models.ImageField(upload_to=user_directory_path, validators=[ext_validator], blank=True, null=True)

# class Image(models.Model):
#     img_name = CustomImageField(use_key=True, upload_to='tmp')

#     def get_upload_to(self, attname):
#         return 'images/product_images/{0}'.format(self.id)

class ProductManager(models.Manager):
    def get_or_None(self, slug):
        try:
            product = self.get(slug=slug)
        except:
            product = None
        return product
        

# TODO Cange all price fields to Integer cents
class Product(models.Model):
    class Meta:
        ordering = ['id']
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField(Image, through="ProductImage", blank=True,)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, blank=True, null=True)
    availability = models.BooleanField(default=True)
    date_added = models.DateTimeField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    slug = models.SlugField()

    objects = ProductManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    # class Meta:
    #     db_table = "shop_product_images"

    def save(self, *args, **kwargs):
        if not self.id and not self.image:
            super().save(*args, **kwargs)
        elif not self.id and self.image:
            super().save(*args, **kwargs)
            self.product.productimage_set.add(self)
        else:
            super().save(*args, **kwargs)


class OrderItemManager(models.Manager):
    def add_to_cart(self, product, quantity=1, customer=None, session=None):
        if customer:
            cart, created = self.get_or_create(customer=customer, product=product)
        else:
            cart, created = self.get_or_create(session=session, product=product)

        if not created:
            cart.quantity += quantity
            cart.save()
        else:
            cart.quantity = quantity
            cart.save()
        return cart

    def remove_from_cart(self, product, customer=None, session=None):
        if customer:
            self.filter(customer=customer, product=product).delete()
        else:
            self.filter(session=session, product=product).delete()

    def sub_total(self):
        pass

class OrderItem(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2) # TODO need add price in order, becouse customer need to be sure that he buing same price, he put in cart

    objects = OrderItemManager()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def sub_total(self):
        subtotal = self.quantity * self.product.price
        return subtotal

    


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    response_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    # def count_items(self):
    #     for item in self.items:
    #         item




class ShippingAddress(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Shipping addresses"

    def __str__(self):
        return self.address


class ShoppingSession(models.Model):
    session_key = models.CharField(max_length=40, null=False, blank=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}'s shopping session ({self.session_key})"


