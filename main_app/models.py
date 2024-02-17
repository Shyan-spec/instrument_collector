from django.db import models
from django.contrib.auth.models import User


TYPE_CHOICES = (
    ('string', 'String'),
    ('brass', 'Brass'),
    ('woodwind', 'Woodwind'),
    ('percussion', 'Percussion'),
    ('keyboard', 'Keyboard'),
)
    
CONDITION_CHOICES = (
    ('new', 'New'),
    ('used', 'Used'),
    ('repair', 'Needs Repair'),
)

# Create your models here.
class Instruments(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    serial_number = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    description = models.TextField(blank=True)
    in_stock = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

class Collections(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instruments = models.ManyToManyField(Instruments, related_name='collections')
    
    def __str__(self):
        return f"{self.title}"
    
class Renter(models.Model):
    name = models.CharField(max_length=50, default='')
    date_pick_up = models.DateField(default='')
    date_returned = models.DateField(default='')
    returned_condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, default=CONDITION_CHOICES[1][0])
    purchased = models.BooleanField(default=False)
    instrument = models.ForeignKey(Instruments, on_delete=models.CASCADE, default='')
    
    def __str__(self):
        return f"{self.name} - {self.instrument.name}"
    