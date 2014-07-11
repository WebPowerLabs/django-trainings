from django.views.generic import DetailView, ListView

from .models import Package#, InfusionsoftPackage


class PackageListView(ListView):

	model = Package
	template_name = "packages/list.html"


class PackageDetailView(DetailView):

	model = Package
	template_name = "packages/detail.html"

	def get_context_data(self, **kwargs):
		package = self.get_object()
		package = package.infusionsoftpackage if package.infusionsoftpackage else package
		context = super(PackageDetailView, self).get_context_data(**kwargs)
		context['class_name'] = package.__class__.__name__
		context['package'] = package
		return context