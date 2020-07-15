import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, DeleteView, CreateView, UpdateView
from AVShop import models, forms  # forms
from users import models as _models

class ProtectedTemplateView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


def index(request):
    products = models.Product.objects.filter(is_deleted=False).order_by('title')
    return render(request, 'AVShop/shop.html',
                  {'products': products,
                   })


def product_by_id(request, product_id):
    if request.method == 'POST':
        buy_product(request, product_id)
    else:
        try:
            product = models.Product.objects.get(id=product_id)
        except (models.Product.DoesNotExist, models.Product.MultipleObjectsReturned):
            return redirect('/')
        return render(request, 'AVShop/product_by_id.html', {'product': product})
    try:
        purchases = models.Purchase.objects.filter(user=request.user.id)
    except (models.Product.DoesNotExist, models.Product.MultipleObjectsReturned):
        return redirect('/')
    return redirect('/users/personal/', {'purchase': purchases})  # render(request, 'users/personal_page.html', {'purchase': purchases})
                                                                  # redirect('/users/personal/', {'purchase': purchases})


def buy_product(request, product_id):
    product = models.Product.objects.get(id=product_id)
    user = _models.User.objects.get(id=request.user.id)
    amount_buy = int(request.POST['amount_buy'])
    error = ''
    if amount_buy > product.amount:
        print("More then present!")
        error = "More then present!"
    elif user.cash < amount_buy*product.price:
        print("You don`t have enough money!")
        error = "You don`t have enough money!"
    else:  # amount_buy <= product.amount and user.cash >= amount_buy*product.price:
        product.amount -= amount_buy
        user.cash -= amount_buy*product.price
        print(product.title + ' ' + str(product.amount))
        print(user.username + ' ' + str(user.cash))
        purchase = models.Purchase(user=user, product=product, price=product.price, amount=amount_buy)
        print(purchase)
        purchase.save()
    return request, error

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


class PurchaseListView(ListView):
    model = models.Purchase
    queryset = models.Purchase.objects.all()
    ordering = '-user'
    paginate_by = 10


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

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)


class ProductUpdate(UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    success_url = reverse_lazy('all_products')
