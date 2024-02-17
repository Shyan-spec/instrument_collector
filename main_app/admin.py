from django.contrib import admin
from .models import Instruments, Renter, Collections
# Register your models here.

admin.site.register(Instruments)
admin.site.register(Renter)
admin.site.register(Collections)