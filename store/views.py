from django.contrib.auth.decorators import login_required

from .filters import ProductFilters
from .models import Product, Category, Cart, CartItem
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from store.forms import UserForm, ContactForm, ProductForm, ProductUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect


class ProductCreateView(CreateView):
    template_name = 'create_user.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = 'Felicitate! {f_name} {l_name} a fost adaugat cu success!'
    permission_required = 'student.add_student'  # app_lebel.codename

    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=self.object.name)


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = 'all_products'
    fields = '__all__'

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def get_context_data(self, get_all_products=None, **kwargs):
        context = super().get_context_data(**kwargs)

        my_filters = ProductFilters(self.request.GET, queryset=Product.objects.filter(active=True))
        get_all_products = my_filters.qs
        #
        context['products'] = get_all_products
        context['form_filters'] = my_filters.form

        return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            pass
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def success(request):
    return HttpResponse('Success!')


class HomeTemplateView(TemplateView):
    template_name = 'homepage.html'


class UserCreateView(CreateView):
    template_name = 'create_user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')


class CategoryDetailsView(DetailView):
    template_name = "product_list.html"
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context[self.context_object_name]
        products = Product.objects.filter(category=category)
        context['products'] = products
        return context


class ProductUpdateView(UpdateView):
    template_name = 'product_modify.html'
    model = Product
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_list')
    # permission_required = 'student.change_student'


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html', {'product': product})

def get(self, request, *args, **kwargs):
    return HttpResponse()

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_product_to_cart(request):
    if request.method == 'POST':
        open_cart, created = Cart.objects.get_or_create(user=request.user, status='open')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        cart_item, created = CartItem.objects.get_or_create(product_id=product_id, cart=open_cart)
        cart_item.quantity += quantity
        cart_item.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required()
def remove_from_cart(request, id):
    try:
        product_id = request.session['product_id']
        cart = Cart.objects.get(id=p)
    except:
        return HttpResponseRedirect(reverse('open_cart'))
    cartitem = CartItem.objects.get(id=product_id)
    cartitem.delete()
    return HttpResponseRedirect(reverse('open_cart'))


@login_required
def open_cart_view(request):
    open_cart, created = Cart.objects.get_or_create(user=request.user, status='open')
    return render(request, 'open_cart.html', {'cart': open_cart})
