# models.py (ConsentForm model with PDF generation)
from django.db import models
from django.core.files.base import ContentFile
import weasyprint
from django.template.loader import render_to_string
from accounts.models import CustomUser
class ConsentForm(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_code = models.CharField(max_length=100)
    application = models.CharField(max_length=50, choices=[('Coordinator', 'Coordinator'), ('Planner', 'Planner')])
    consent_text = models.TextField()
    consent_pdf = models.FileField(upload_to='consent_pdfs/', blank=True, null=True)
    provider_legal_name = models.CharField(max_length=255)
    provider_trading_name = models.CharField(max_length=255)
    provider_number = models.CharField(max_length=50)
    provider_abn = models.CharField(max_length=50)
    participant_full_name = models.CharField(max_length=255)
    ndis_number = models.CharField(max_length=50)
    service_categories = models.JSONField()
    comments = models.TextField()
    declaration = models.BooleanField(default=False)
    signing_first_name = models.CharField(max_length=255)
    signing_last_name = models.CharField(max_length=255)
    signature = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.consent_pdf:
            html_string = render_to_string('consent_form/pdf_template.html',
                                           {
                                            'service_code': self.service_code,
                                            'user': self.user,
                                            'application': self.application,
                                            'service_categories': self.service_categories,
                                            'uploaded_at': self.uploaded_at,
                                          })

            pdf_file = weasyprint.HTML(string=html_string).write_pdf()
            self.consent_pdf.save(f'consent_{self.service_code}.pdf', ContentFile(pdf_file), save=False)
        super().save(*args, **kwargs)