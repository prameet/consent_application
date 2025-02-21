from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .models import ConsentForm
import uuid
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import ConsentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

import os



@login_required
def show_consent_forms(request):
    consent_forms = ConsentForm.objects.filter(user=request.user).order_by('-uploaded_at')
    # Debugging output
    print(f"Current User: {request.user}")
    print(f"Consent Forms Count: {consent_forms.count()}")
    return render(request, 'consent_form/consent_form_home.html', {'consent_forms': consent_forms})

@login_required
def create_consent_form(request):

    if request.method == 'POST':
        data = request.POST
        other_input = data.get('otherInput', '').strip()

        # Required fields
        required_fields = [
            'service_code', 'application', 'provider_legal_name', 'provider_trading_name',
            'provider_number', 'provider_abn', 'participant_full_name', 'ndis_number',
            'signing_first_name', 'signing_last_name'
        ]

        errors = {}

        # Check required fields
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."
        # Validate service categories (at least one must be selected)
        service_categories = data.getlist('services[]')
       
        if not service_categories:
            errors['services'] = "Please select at least one service category."
        
        # Validation: If 'Other' is selected, check if input is provided
        if "otherOption" in service_categories and not data.get("otherInput", "").strip():
            errors['otherInput'] = "Please specify the other service category."
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # Save the consent form if no validation errors
        consent_form = ConsentForm(
            user=request.user,
            service_code=data.get('service_code'),
            application=data.get('application'),
            consent_text='consent_text',
            provider_legal_name=data.get('provider_legal_name'),
            provider_trading_name=data.get('provider_trading_name'),
            provider_number=data.get('provider_number'),
            provider_abn=data.get('provider_abn'),
            participant_full_name=data.get('participant_full_name'),
            ndis_number=data.get('ndis_number'),
            service_categories=service_categories,
            comments=data.get('comments'),
            declaration=True,  # Since it's validated above
            signing_first_name=data.get('signing_first_name'),
            signing_last_name=data.get('signing_last_name'),
            signature=data.get('signature')
        )
        consent_form.save()

        return JsonResponse({'status': 'success'})
        # return redirect('consent_form:consent_form_home')  #
    return render(request, 'consent_form/create_form.html')

@login_required
def download_file(request, consent_form_id):
    consent_form = ConsentForm.objects.get(id=consent_form_id, user=request.user)
    
    file_path = consent_form.consent_pdf.path if consent_form.consent_pdf else None
    if not file_path or not os.path.exists(file_path):
        return render(request, "consent_form/file_not_found.html", {"filename": consent_form.consent_pdf.name})
    return FileResponse(consent_form.consent_pdf.open(), as_attachment=True, filename=consent_form.consent_pdf.name)

@login_required
def delete_consent(request, consent_form_id):
    if request.method == "POST":
        consent = get_object_or_404(ConsentForm, id=consent_form_id)
        consent.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
