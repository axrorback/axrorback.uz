from django.urls import path
from .views import *
urlpatterns = [
    path('thanks/', thanks, name='thanks'),
    path('',about, name='about'),
    path('blog/',blog, name='blog'),
    path('blog/<slug:slug>',blog_detail, name='blog_detail'),
    path('contact/',contact, name='contact'),
    path('questions/', questions_list, name='questions_list'),
    path('ask/', ask_question, name='ask_question'),
    path('achievements/', achievements, name='achievements'),  #
    path('media/<path:path>/', protected_media, name='protected_media'),
    path('cert/<int:pk>/<int:expire>/<str:token>/', secure_certificate_view, name='secure_certificate'),

]