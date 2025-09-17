from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from .data import popular_items, Cart_items
from django.core.paginator import Paginator #To display the specific no of the items inside one page.
from .form import ItemForm
from django.shortcuts import render, get_object_or_404
@login_required(login_url='login_page')  # if not logged in → redirect to /login/
def home(request):
    context = {
        'items': Item.objects.all() #To get all of the items objects    
        }
    return render(request, 'home.html' , context)




def signup_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user already exists
        if Auth.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login instead.")
            return redirect("login_page")

        # Create new user with hashed password
        user = Auth.objects.create(
            email=email,
            password=make_password(password)   # hash password securely
        )

        # Log the user in immediately
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "sign_up.html")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Auth.objects.get(email=email)
            if check_password(password, user.password):  # secure check
                login(request, user)  # create session
                return redirect("home")
            else:
                messages.error(request, "Incorrect password!")
        except Auth.DoesNotExist:
            messages.error(request, "Invalid Email or Password")

        return redirect("login_page")

    return render(request, "login.html")

def Logout(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("login_page")

    return render(request, "Logout.html")


def Cart(request):
    context = {
        'Cart_items': Cart_items
        }
    return render(request, "cart.html",context)

def Deals(request):
    
    return render(request, "Deals.html")

def item_detail(request, pk):
    item = get_object_or_404(Item.objects.prefetch_related("images"), pk=pk)
    context = {
        'item': item,
        'images': item.images.all(),  # pass images separately if you want
    }
    return render(request, "item.html", context)

def Contact(request):
    return render(request, "Contact.html")


def ProductsPage(request):

    q = request.GET.get('q', '').strip()

    # Base queryset (you can order differently)
    qs = Item.objects.all().order_by('-id')

    # If search query present, filter by name / short_description / description
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )


    context = {
        'items': qs,  # what your template expects
    }
    return render(request, "products.html", context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import ItemForm
from .models import Item
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ObjectDoesNotExist

@login_required
def add_item(request):
    form_data = {
        'name': '',
        'description': '',
        'price': '',
        'quantity': '',
        'category': '',
    }

    keys = request.POST.getlist("spec_key[]")
    values = request.POST.getlist("spec_value[]")

    
    # Initialize form for GET requests
    form = ItemForm()
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "")
        price = request.POST.get("price", "")
        quantity = request.POST.get("quantity", "")
        category = request.POST.get("category", "")
        

        # Update form data for potential re-display
        form_data.update({
            'name': name,
            'description': description,
            'price': price,
            'quantity': quantity,
            'category': category
        })

        # Check if item already exists
        if Item_Auth(name) is None:  # Item exists
            messages.error(request, "Item already exists!")
            form = ItemForm(initial=form_data)
            context = {
                'form': form,
                'form_data': form_data,
            }
            return render(request, "add_item.html", context)
        else:
            # Process price
            try:
                price_value = Decimal(price)
                
                # Check if price has more than 2 decimal places
                if price_value.as_tuple().exponent < -2:
                    messages.error(request, "Price cannot have more than 2 decimal places!")
                    form = ItemForm(initial=form_data)
                    context = {'form': form, 'form_data': form_data}
                    return render(request, "add_item.html", context)
                
                # If it's a whole number, add .99
                if price_value == price_value.to_integral_value():
                    price_value = price_value + Decimal("0.99")
                    
            except (InvalidOperation, ValueError):
                messages.error(request, "Please enter a valid price!")
                form = ItemForm(initial=form_data)
                context = {'form': form, 'form_data': form_data}
                return render(request, "add_item.html", context)
            
            # Create new item
            new_item = Item.objects.create(
                name=name,
                description=description,
                price=price_value,
                quantity=quantity,
                category=category,
                user=request.user #Need to add for the user field too.
            )
                # Save multiple images
                    # Save multiple images
            for img in request.FILES.getlist("images"):
                ItemImage.objects.create(item=new_item, image=img)
            for k, v in zip(keys, values):
                if k.strip() and v.strip():  # avoid empty entries
                    Specification.objects.create(item=new_item, key=k.strip(), value=v.strip())
            
            messages.success(request, "Item added successfully!")
            return redirect("add_item")
    
    # GET request or after successful addition
    context = {
        'form': form,
        'form_data': form_data,
    }
    return render(request, "add_item.html", context)

def Item_Auth(name):
    try:
        Item.objects.get(name=name)
        return None  # Item exists
    except ObjectDoesNotExist:
        return name  # Item doesn't exist

def PrivacyPolicy(request):
    
    return render(request, "policydownload.html")    

from django.db.models import Q

def category(request, category_name):
    items = Item.objects.filter(category=category_name)

    context = {
        "items": items,
        "category": category_name,
    }
    return render(request, "category.html", context)


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # 1) Ownership check — only owner can edit
    if item.user != request.user:
        messages.error(request, "You are not allowed to edit this item.")
        return redirect("home")   # or return HttpResponseForbidden()

    # Prepare initial data (similar to your add_item)
    form_data = {
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'quantity': item.quantity,
        'category': item.category,
    }

    keys = request.POST.getlist("spec_key[]")
    values = request.POST.getlist("spec_value[]")

    form = ItemForm(instance=item)

    if request.method == "POST":
        # If you prefer using fields like in add_item, you can copy that logic.
        # Here's a simple approach using the form:
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            edited_item = form.save(commit=False)
            # Ensure the user remains the owner
            edited_item.user = request.user
            # validate/normalize price if needed (example)
            try:
                price_value = Decimal(request.POST.get("price", edited_item.price))
                if price_value.as_tuple().exponent < -2:
                    messages.error(request, "Price cannot have more than 2 decimal places!")
                    return render(request, "edit_item.html", {"form": form, "form_data": form_data, "item": item})
                if price_value == price_value.to_integral_value():
                    price_value = price_value + Decimal("0.99")
                edited_item.price = price_value
            except (InvalidOperation, ValueError):
                messages.error(request, "Please enter a valid price!")
                return render(request, "edit_item.html", {"form": form, "form_data": form_data, "item": item})

            edited_item.save()

            # Images: optional — here we append new uploaded images
            for img in request.FILES.getlist("images"):
                ItemImage.objects.create(item=edited_item, image=img)

            # Specs: you can choose to remove old ones then add new ones, or update
            # Example: delete all old specs and create new ones from posted spec lists:
            Specification.objects.filter(item=edited_item).delete()
            for k, v in zip(keys, values):
                if k.strip() and v.strip():
                    Specification.objects.create(item=edited_item, key=k.strip(), value=v.strip())

            messages.success(request, "Item updated successfully!")
            return redirect("item", pk=edited_item.pk)  # or wherever
        else:
            messages.error(request, "Please fix the errors below.")
            form_data.update(request.POST)

    context = {
        "form": form,
        "form_data": form_data,
        "item": item,
    }
    return render(request, "edit_item.html", context)
