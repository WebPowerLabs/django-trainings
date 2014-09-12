from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from courses.models import Content
from utils.views import PermissionMixin
from .models import Package, InfusionsoftPackage, PackagePurchase
from facebook_groups.models import FacebookGroup


class PackageListView(ListView):

    model = Package
    template_name = "packages/list.html"


class PackageDetailView(DetailView):

    model = Package
    template_name = "packages/detail.html"

    def get_context_data(self, **kwargs):
        context = super(PackageDetailView, self).get_context_data(**kwargs)

        package = self.get_object()
        purchased = PackagePurchase.objects.purchased(self.request.user
                                                      ).filter(package=package)
        try:
            # if infusionsoft package, use that instead of package_package
            package = package.infusionsoftpackage
        except  InfusionsoftPackage.DoesNotExist:
            pass

        context['purchased'] = purchased[0] if purchased else False
        context['class_name'] = package.__class__.__name__
        context['package'] = package
        return context


class PackageListForContentView(ListView):
    model = Package
    template_name = "packages/list_for_content.html"

    def get_queryset(self):
        content = Content.objects.get(pk=self.kwargs.get('content_pk', None))
        package_list = Package.objects.get_for_content(content)
        return package_list

    def get_context_data(self, **kwargs):
        context = super(PackageListForContentView, self
                        ).get_context_data(**kwargs)
        content = Content.objects.get(pk=self.kwargs.get('content_pk', None))
        context['content'] = content
        return context


class PackageListForGroupView(ListView):
    model = Package
    template_name = "packages/list_for_group.html"

    def get_queryset(self):
        fb_group = FacebookGroup.objects.get(pk=self.kwargs.get('group_pk',
                                                                None))
        package_list = Package.objects.filter(groups=fb_group)
        return package_list

    def get_context_data(self, **kwargs):
        context = super(PackageListForGroupView, self
                        ).get_context_data(**kwargs)
        fb_group = FacebookGroup.objects.get(pk=self.kwargs.get('group_pk',
                                                                None))
        context['fb_group'] = fb_group
        return context


class PackagePurchaseListView(PermissionMixin, ListView):
    model = PackagePurchase
    template_name = "packages/package_purchase_list.html"
    decorators = {'GET': login_required}

    def get_queryset(self):
        queryset = super(PackagePurchaseListView, self).get_queryset()
        return queryset.filter(user=self.request.user)
