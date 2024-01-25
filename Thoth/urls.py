from django.urls import path
from .           import views

urlpatterns = [
    path("", views.redirectadmin),

    path('attend/<int:pk>',views.attender, name="attend"),
    path("make-sudent-attend-with-qr/<str:pk>/  ", views.attend_with_pk_qr, name="attend-with-pk"),
    path("refresh-clients", views.refresh_clients, name="refresh_clients"),
    path("attend-grid-course/<int:pk>/", views.attend_grid, name="attend-grid-course"),
    path("attend-all-students-with-qr-scanner/", views.attend_all_students_with_qr_scanner, name="attend-all-students-with-qr-scanner"),
    


]



