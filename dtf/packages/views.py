from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from courses.models import Content
from utils.views import PermissionMixin
from .models import Package, InfusionsoftPackage, PackagePurchase



class PackageListView(ListView):

    model = Package
    template_name = "packages/list.html"


class PackageDetailView(DetailView):

	model = Package
	template_name = "packages/detail.html"

	def get_context_data(self, **kwargs):
		package = self.get_object()
		try:
			package = package.infusionsoftpackage
		except  InfusionsoftPackage.DoesNotExist:
			pass
		context = super(PackageDetailView, self).get_context_data(**kwargs)
		context['class_name'] = package.__class__.__name__
		context['package'] = package
		return context


class PackageListToContentView(ListView):
	model = Package
	template_name = "packages/list_to_content.html"

	def get_queryset(self):
		content = Content.objects.get(pk=self.kwargs.get('content_pk', None))
		package = Package.objects.filter(Q(courses=content) |
						 Q(lessons=content) |
                         Q(courses=content.course)).distinct()
		return package

	def get_context_data(self, **kwargs):
		context = super(PackageListToContentView, self).get_context_data(**kwargs)
		content = Content.objects.get(pk=self.kwargs.get('content_pk', None))
		context['content'] = content
		return context


class PackagePurchaseListView(PermissionMixin, ListView):
	model = PackagePurchase
	template_name = "packages/package_purchase_list.html"
	decorators = {'GET': login_required}

	def get_queryset(self):
		queryset = super(PackagePurchaseListView, self).get_queryset()
		return queryset.filter(user=self.request.user)
