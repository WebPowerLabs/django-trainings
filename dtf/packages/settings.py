from django.conf import settings

INFUSIONSOFT_COMPANY = getattr(settings, 'INFUSIONSOFT_COMPANY_ID', None)
INFUSIONSOFT_API_KEY = getattr(settings, 'INFUSIONSOFT_API_KEY', None)
