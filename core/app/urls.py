from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('services', views.services, name='services'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('designs',views.designs,name='designs'),

]