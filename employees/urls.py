from django.urls import path
from .views import employee_list, employee_detail, employee_create, employee_update, employee_delete, generate_salary_slip, employee_info

urlpatterns = [
    path('list/', employee_list, name='employee_list'),
    path('detail/<int:pk>/', employee_detail, name='employee_detail'),
    path('detail/<int:pk>/generate-salary-slip/', generate_salary_slip, name='generate_salary_slip'),
    path('create/', employee_create, name='employee_create'),
    path('update/<int:pk>/', employee_update, name='employee_update'),
    path('delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('info/', employee_info, name='employee_info'),
]
