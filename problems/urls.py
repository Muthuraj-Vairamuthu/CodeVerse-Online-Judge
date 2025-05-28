from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('submissions/mine/', views.my_submissions, name='my_submissions'),  # ✅ add this
]
