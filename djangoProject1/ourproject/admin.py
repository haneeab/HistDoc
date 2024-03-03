from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Worker)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(cart)
admin.site.register(Feedback)
# admin.site.register(Work_schedule)
admin.site.register(Shift)
admin.site.register(WeekDay)
admin.site.register(WeekDayShift)



