from django.urls import path
import views

urlpatterns = [
    path('iherb/add_person', views.add_person),
    path('iherb/get_products', views.get_products),
    path('iherb/get_article', views.get_article),
    path('iherb/get_questions', views.get_questions),
    path('iherb/decide', views.desicion_view),
    ]
