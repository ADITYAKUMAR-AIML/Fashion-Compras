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
    item = get_object_or_404(Item, pk=pk)   # safer than .get()
    context = {'item': item}
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
        'image': '',
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
        image = request.FILES.get("image", None)
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
                image=image,
                category=category
            )
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

def category(request, category_name):
    items = Item.objects.filter(category=category_name)
    context = {
        'items': items,
        'category': category_name
    }
    return render(request, 'category.html', context)
   