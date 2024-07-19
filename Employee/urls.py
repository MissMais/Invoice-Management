from django.urls import path,include
from .views import *



urlpatterns = [
    path('employee/',EmployeeAPI.as_view()),
    path('employee_filter/',EmployeeFilter),
    path('change_password/',ChangePasswordView.as_view()),
    path('employee_filter/',EmployeeListView.as_view()),
    path(
        "password_reset/",
        PasswordReset.as_view()
        
    ),
    path(
        "password-reset/<str:encoded_pk>/<str:token>/",
        ResetPasswordAPI.as_view(),
        name="reset-password",
),

 

]

