from django.urls import path, include
from .           import views
from .admin import final_boss
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("", views.redirectadmin),

    path('attend/<int:pk>',views.attender, name="attend"),
    path("make-sudent-attend-with-qr/<str:pk>/  ", views.attend_with_pk_qr, name="attend-with-pk"),
    path("refresh-clients", views.refresh_clients, name="refresh_clients")
]



