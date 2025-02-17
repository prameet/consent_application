from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('coordinator/', include('coordinator.urls')),
    # path('', include('consent_form.urls')),
    path('consent_form/', include('consent_form.urls')),
    # path('planner/', include('planner.urls')),

    path('', dashboard, name='dashboard'),
]
