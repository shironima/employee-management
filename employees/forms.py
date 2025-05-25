from django import forms
from .models import Employee
from decimal import Decimal

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'basic_salary', 'bonus']

class BonusForm(forms.Form):
    bonus = forms.BooleanField(label='Receive Bonus', required=False)

class EmployeeAddForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position']
    
    def clean_position(self):
        position = self.cleaned_data.get('position')
        if position:
            # Set basic_salary sesuai dengan posisi yang dipilih
            basic_salary = get_basic_salary(position)
            self.cleaned_data['basic_salary'] = basic_salary
        return position

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