from django.urls import path
from . import views

app_name = "Choose_Courses"

urlpatterns = [
    path('index/', views.index, name="index"),
    path('detail/<int:course_id>', views.get_details, name='detail'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
