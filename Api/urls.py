from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from Api.MapApi import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('put_new_graph/', views.put_new_graph),
    url('show_all_maps/', views.show_all_maps),
    url(r'^api-auth/', include('rest_framework.urls')),
]
