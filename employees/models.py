from django.db import models
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal

class Employee(models.Model):
    POSITION_CHOICES = [
        ('Pekerja Magang', 'Pekerja Magang'),
        ('Staff Junior', 'Staff Junior'),
        ('Staff Senior', 'Staff Senior'),
        ('Team Leader', 'Team Leader'),
        ('Spesialis Departemen', 'Spesialis Departemen'),
        ('Kepala Departemen', 'Kepala Departemen'),
        ('Asisten Eksekutif', 'Asisten Eksekutif'),
        ('Anggota Dewan', 'Anggota Dewan'),
        ('Eksekutif C-Suite', 'Eksekutif C-Suite'),
        ('Wakil Presiden', 'Wakil Presiden'),
        ('Presiden', 'Presiden'),
        ('Chief Executive Officer (CEO)', 'Chief Executive Officer (CEO)'),
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=Employee)
def set_basic_salary(sender, instance, **kwargs):
    # Konversi basic_salary ke Decimal jika belum
    if instance.basic_salary is None:
        instance.basic_salary = Decimal(str(get_basic_salary(instance.position)))

def get_basic_salary(position):
    # Mendapatkan nilai basic_salary sesuai dengan position
    salary_mapping = {
        'Pekerja Magang': 2500000,
        'Staff Junior': 4000000,
        'Staff Senior': 5200000,
        'Team Leader': 7000000,
        'Spesialis Departemen': 8320000,
        'Kepala Departemen': 9000000,
        'Asisten Eksekutif': 15000000,
        'Anggota Dewan': 18750000,
        'Eksekutif C-Suite': 22000000,
        'Wakil Presiden': 25000000,
        'Presiden': 32000000,
        'Chief Executive Officer (CEO)': 55000000,
    }
    return salary_mapping.get(position, 0)