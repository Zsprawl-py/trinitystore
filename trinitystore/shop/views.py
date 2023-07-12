from django.shortcuts import render, get_object_or_404

from .forms import ChoiceProduct
from .models import Category, Product


# def product_list(request, category_slug=None):
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     category = None
#     if category_slug:
#         category = get_object_or_404(
#             Category, slug=category_slug
#         )
#         products = products.filter(category=category)
#     return render(request,
#                   'shop/product/list.html',
#                   {'category': category,
#                    'products': products,
#                    'categories': categories})

# def product_list(request):
#     form = ChoiceProduct()
#     return render(request, 'shop/product/list2.html', {'form': form})

def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/shop.html', {'products': products,
                                                      'section': 'shop'})


def product_list1(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/list3.html', {'products': products,
                                                      'section': 'shop'})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    return render(request, 'shop/product/detail.html', {'product': product})
