from django import forms
from .models import ConsentForm

class ConsentFormForm(forms.ModelForm):
    class Meta:
        model = ConsentForm
        fields = ['user', 'service_code', 'application', 'consent_text', 'provider_legal_name', 'provider_trading_name', 'provider_number', 'provider_abn', 'participant_full_name', 'ndis_number', 'service_categories', 'comments', 'declaration', 'signing_first_name', 'signing_last_name', 'signature']
