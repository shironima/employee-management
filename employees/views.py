from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import BonusForm
from .forms import EmployeeForm
from django.http import HttpResponse
from .forms import EmployeeAddForm
from decimal import Decimal
from io import BytesIO
from reportlab.pdfgen import canvas

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        bonus_form = BonusForm(request.POST)
        if bonus_form.is_valid():
            employee.bonus = bonus_form.cleaned_data['bonus']
            employee.save()
    else:
        bonus_form = BonusForm(initial={'bonus': employee.bonus})

    return render(request, 'employees/employee_detail.html', {'employee': employee, 'bonus_form': bonus_form})

def generate_salary_slip(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        bonus_form = BonusForm(request.POST)
        if bonus_form.is_valid():
            employee.bonus = bonus_form.cleaned_data['bonus']
            employee.save()

    else:
        bonus_form = BonusForm(initial={'bonus': employee.bonus})

    # Konversi basic_salary ke Decimal jika belum
    basic_salary = Decimal(str(employee.basic_salary))

    # Hitung gaji total (basic_salary + bonus)
    gaji_total = basic_salary * Decimal('1.1') if employee.bonus else basic_salary

    # Buat dokumen PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=slip_gaji_{employee.name}.pdf'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Mulai menambahkan elemen-elemen PDF
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, f"Salary Slip for {employee.name}")
    pdf.drawString(100, 780, f"Position: {employee.position}")
    pdf.drawString(100, 760, f"Basic Salary: Rp{employee.basic_salary}")
    pdf.drawString(100, 740, f"Bonus: {'Yes' if employee.bonus else 'No'}")
    pdf.drawString(100, 720, f"Total Salary: Rp{gaji_total}")

    # Akhiri dan simpan dokumen PDF
    pdf.showPage()
    pdf.save()

    # Ambil nilai dari BytesIO dan tambahkan ke response
    pdf_data = buffer.getvalue()
    buffer.close()
    response.write(pdf_data)

    return response

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeAddForm()

    return render(request, 'employees/add_employee.html', {'form': form})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'Update'})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')

def employee_info(request):
    return render(request, 'employees/employee_info.html')