from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Product, Sale
from .forms import ProductForm, SaleForm, SaleItemFormSet


@login_required
def product_list(request):
    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, "product_list.html", {"products": products, "query": query})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "product_confirm_delete.html", {"product": product})


@login_required
@transaction.atomic
def create_sale(request):
    if request.method == "POST":
        sale_form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if sale_form.is_valid() and formset.is_valid():
            sale = sale_form.save(commit=False)
            sale.total_amount = 0
            sale.save()

            total = 0
            items = formset.save(commit=False)
            for item in items:
                item.sale = sale
                item.price_at_sale = item.product.price
                item.save()

                item.product.stock_quantity -= item.quantity
                item.product.save()

                total += item.quantity * item.price_at_sale

            sale.total_amount = total
            sale.save()

            return redirect("sale_list")
    else:
        sale_form = SaleForm()
        formset = SaleItemFormSet()

    return render(
        request, "create_sale.html", {"sale_form": sale_form, "formset": formset}
    )


@login_required
def sale_list(request):
    sales = Sale.objects.all().order_by("-date")
    return render(request, "sale_list.html", {"sales": sales})
