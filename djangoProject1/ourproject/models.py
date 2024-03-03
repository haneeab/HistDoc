from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# we don't need this any more



# we don't need this any more
class Worker(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    worker_id = models.CharField(max_length=9, null=True)
    bank_acccount = models.CharField(max_length=16, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


# we don't need this any more
# class Admin(models.Model):
# 	user_name=models.CharField(max_length=200,null=True)
# 	pass_word=models.CharField(max_length=200,null=True)

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Pen-Markers', 'Pen-Markers'),
        ('Paint', 'Paint'), ('Brushes', 'Brushes'),
        ('Art paper&board', 'Art paper&board'),
        ('Canvas', 'Canvas'),
        ('Drawing media', 'Drawing media')
    )
    name = models.CharField(max_length=200, null=True)
    bar_code = models.CharField(max_length=10, null=True)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    name_of_product = models.CharField(max_length=200, null=True)
    customer_name = models.CharField(max_length=200, null=True)
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)



class Feedback(models.Model):
	customer=models.CharField(null=True,max_length=100)
	feedback=models.CharField(max_length=1200,null=True)
class cart(models.Model):
	customer=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE)
# class work_schedule(models.Model):
class Shift(models.Model):
    shift_id = models.IntegerField(primary_key=True, default=0)
    shifts = (
        ('shift1', 'shift1'),
        ('shift2', 'shift2'), ('shift3', 'shift3'),

    )
    shift_name = models.CharField(max_length=200, null=True, choices=shifts)

    def __str__(self):
        return self.shift_name


class WeekDay(models.Model):
    day_id = models.IntegerField(primary_key=True, default=0)
    daysName = (
        ('sunday', 'sunday'),
        ('moneday', 'moneday'), ('tuesday', 'tuesday'),
        ('wensday', 'wensday'),
        ('thersday', 'thersday'),
    )
    day_name = models.CharField(max_length=200, null=True, choices=daysName)
    shifts = models.ManyToManyField(Shift, through='WeekDayShift')

    def __str__(self):
        return self.day_name


class WeekDayShift(models.Model):
    worker_name = models.CharField(max_length=200, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)
    day = models.ForeignKey(WeekDay, on_delete=models.CASCADE, null=True)

# we need to add two tabels carts and feedback
