import django_filters
from store.models import Product, Category


class ProductFilters(django_filters.FilterSet):
    list_of_products = [((product.name, product.name.upper())) for product in Product.objects.filter(active=True)]
    name = django_filters.CharFilter(lookup_expr='icontains', label='name of product')
    price = django_filters.CharFilter(lookup_expr='icontains', label='price')

    class Meta:
        model = Product
        fields = ['name','price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters['name'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter the name of product'})
        self.filters['price'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter the price'})




