import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, DeleteView, CreateView, UpdateView
from AVShop import models, forms  # forms


class ProtectedTemplateView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


def index(request):
    products = models.Product.objects.filter(is_deleted=False).order_by('name')
    return render(request, 'AVShop/base.html',
                  {'products': products,
                   })


def product_by_name(request, product_name):
    now = datetime.datetime.now()
    return render(request, 'AVShop/product_by_name.html',
                  {'name': product_name,
                   'len': len(product_name),
                   'rendered': now})


def product_by_id(request, product_id):
    try:
        product = models.Product.objects.get(id=product_id)
    except (models.Product.DoesNotExist, models.Product.MultipleObjectsReturned):
        return redirect('/')
    return render(request, 'AVShop/product_by_id.html', {'Product': product})


def search(request):
    # Get request value
    # Filter products
    # Render page
    search = request.GET.get('search', '')
    products = models.Product.objects.filter(title__icontains=search)
    return render(request, 'AVShop/search_result.html', {'products': products, 'search': search})


# def like_product(request, product_id):
#     # Dont scare this. It was just complicated example. lol
#     product = models.product.objects.get(id=product_id)
#     if request.method == 'POST':
#         product.add_like(request.user)
#     return JsonResponse(dict(count=product.likes_set.count()))
#     # return redirect(reverse('product_by_id', kwargs={"product_id": product_id}))
#
#
class ProductDetailView(DetailView):
    model = models.Product
    context_object_name = 'product'


class ProductsListView(ListView):
    model = models.Product
    queryset = models.Product.objects.filter(is_deleted=False)
    ordering = '-title'
    paginate_by = 10

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     categories = models.Category.objects.all()
    #     context = super().get_context_data()
    #     context.update(dict(categories=categories))
    #     return context


class ProductDelete(DeleteView):
    model = models.Product
    success_url = reverse_lazy('all_products')


class ProductCreate(CreateView):
    model = models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('all_products')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdate(UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('all_products')
