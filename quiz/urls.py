from django.urls import path

from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('start/', views.start, name='start'),

    path('mainstart/<int:main_id>/', views.mainstart, name='mainstart'),
    path('mainquiz/<int:main_id>/<int:quiz_id>/', views.mainquiz, name='mainquiz'),
    path('mainend/<int:main_id>/', views.mainend, name='mainend'),

    path('substart/<int:main_id>/', views.substart, name='substart'),
    path('subquiz/<int:main_id>/<int:sub_id>/<int:quiz_id>/', views.subquiz, name='subquiz'),
    path('subend/<int:main_id>/<int:sub_id>/', views.subend, name='subend'),

]