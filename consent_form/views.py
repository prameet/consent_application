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

# class ConsentFormHome(TemplateView, ListView):
#     http_method_names = ['get', 'post']
#
#
#     def getconsent_form(self, request, *args, **kwarg):
#         print('ooooooooooooooo ConsentFormHome oooooooooooooooooo')
#         consent_forms = ConsentForm.objects.filter(user=request.user).order_by('-uploaded_at')
#         context = {
#             'consent_forms':consent_forms,
#             # 'site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY,
#         }
#         return render(request, 'consent_form/consent_form_home.html', context)


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
        consent_form = ConsentForm(
            user=request.user,
            # service_code=f"COORD-{uuid.uuid4().hex[:8]}",
            service_code=data.get('service_code'),
            application=data.get('application'),
            consent_text='consent_text',
            provider_legal_name=data.get('provider_legal_name'),
            provider_trading_name=data.get('provider_trading_name'),
            provider_number=data.get('provider_number'),
            provider_abn=data.get('provider_abn'),
            participant_full_name=data.get('participant_full_name'),
            ndis_number=data.get('ndis_number'),
            service_categories=data.getlist('services[]'),
            comments=data.get('comments'),
            declaration=data.get('declaration') == 'on',
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
    # print(consent_form)
    return FileResponse(consent_form.consent_pdf.open(), as_attachment=True, filename=consent_form.consent_pdf.name)

@login_required

def delete_consent(request, consent_form_id):
    form = get_object_or_404(ConsentForm, id=consent_form_id)
    form.delete()
    messages.success(request, "Consent form deleted successfully.")
    return redirect('consent_form:consent_form_home')  #
