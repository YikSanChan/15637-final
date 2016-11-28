import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    USER_TYPE = (
        (True, 'Merchant'),
        (False, 'Student'),
    )
    # allow null. User has to choose user type once he/she register then login.
    type = models.NullBooleanField(choices=USER_TYPE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    address = models.TextField(max_length=40, blank=True)
    summary = models.TextField(max_length=400, blank=True)
    image = models.ImageField(upload_to='CSS/images/avatars', blank=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Profile model will be automatically created/updated when we create/update User instances.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Menu(models.Model):
    merchant = models.ForeignKey(User)
    food_name = models.CharField(max_length=50)
    MEAL_TYPE = (
        (True, 'Lunch'),
        (False, 'Dinner'),
    )
    is_lunch = models.BooleanField(default=True, choices=MEAL_TYPE)
    meal_date = models.DateTimeField(default=timezone.localtime(timezone.now()))
    price = models.IntegerField(default=8)
    image = models.ImageField(upload_to="CSS/images/menus", blank=True)

    def __str__(self):
        return self.food_name

    @staticmethod
    def get_today_menu():
        today = timezone.localtime(timezone.now()).today().date()
        tomorrow = today + datetime.timedelta(days=1)
        return Menu.objects.filter(meal_date__gt=today, meal_date__lt=tomorrow)
        # return []

    @staticmethod
    def get_menus(merchant):
        return Menu.objects.filter(merchant=merchant)

    @staticmethod
    def get_today_lunch():
        return Menu.get_today_menu().filter(is_lunch=True)

    @staticmethod
    def get_today_dinner():
        return Menu.get_today_menu().filter(is_lunch=False)


class Location(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='CSS/images/locations')
    googleMapURL = models.URLField()
    menus = models.ManyToManyField(Menu, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User)
    menu = models.ForeignKey(Menu)
    quantity = models.IntegerField(default=1)
    Rating_Range = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    is_taken = models.BooleanField(default=False)
    location = models.ForeignKey(Location, null=True, blank=True)
    rating = models.IntegerField(blank=True, default=0, choices=Rating_Range)
    comment = models.TextField(max_length=200, blank=True)

    @staticmethod
    def get_orders(customer):
        return Order.objects.filter(customer=customer)

    @staticmethod
    def get_today_orders():
        today = timezone.localtime(timezone.now()).today().date()
        tomorrow = today + datetime.timedelta(days=1)
        return Order.objects.filter(menu__meal_date__gt=today, menu__meal_date__lt=tomorrow)


class Exchange(models.Model):
    user = models.ForeignKey(User, related_name='exchange_user')
    Restaurants = ((m.id, m.food_name) for m in Menu.get_today_menu())
    menu = models.ForeignKey(Menu, choices=Restaurants, related_name='exchange_menu')
    Exchange_TYPE = (
        (True, 'Seller'),
        (False, 'Buyer'),
    )
    is_seller = models.BooleanField(default=True, choices=Exchange_TYPE)
    quantity = models.IntegerField(default=1)


class RatingSummary(models.Model):
    user = models.ForeignKey(User, related_name='rating_user')
    menu = models.ForeignKey(Menu, related_name='rating_menu')
    rating = models.FloatField(blank=True, default=0)
