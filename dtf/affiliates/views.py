from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from utils.views import PermissionMixin

from .models import Partner, PartnerProduct


class PartnerListView(PermissionMixin, ListView):
    model = Partner
    decorators = {'GET': login_required}
    queryset = Partner.objects.filter(active=True)
    template_name = "affiliates/partner_list.html"


class PartnerDetailView(PermissionMixin, DetailView):
    model = Partner
    decorators = {'GET': login_required}
    template_name = "affiliates/partner_detail.html"