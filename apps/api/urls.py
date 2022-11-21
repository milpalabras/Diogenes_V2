from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('records/', views.RecordsList.as_view()),
    path('records/<int:pk>/', views.RecordsDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('methods_of_payment/', views.MethodOfPaymentList.as_view()),
    path('methods_of_payment/<int:pk>/', views.MethodOfPaymentDetail.as_view()),
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<int:pk>/', views.AccountDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
