from django.urls import path
from . import views
app_name = 'consent_form'

urlpatterns = [
    path('consents/', views.show_consent_forms, name='consent_form_home'),
    path('create/', views.create_consent_form, name='create_consent_form'),
    path('download/<int:consent_form_id>/', views.download_file, name='download_file'),
    path('delete/<int:consent_form_id>/', views.delete_consent, name='delete_consent'),
]
