from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from orders.views import user_orders  # order details

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, Customer
from .tokens import account_activation_token


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(
        request,
        "account/dashboard/dashboard.html",
        {"section": "profile", "orders": orders},
    )  # rendering to the templates


@login_required
def edit_details(request):
    if request.method == "POST":  # posting a form
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():  # checking validity and save
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False  # not deleting just deactivating becuse maybe the data needed
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")  # make an view to cancel option or show thank you deleted


def account_register(request):
    # checking is the user already registered
    if request.user.is_authenticated:
        return redirect("account:dashboard")
    # if user sumbimitted the registration form (form.py) then only create account
    #'POST' method is collecting data and rendering who sumbmitted the form but activate via mail,new user will go else new registration
    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():  # checking validity form
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False  # false becuse email activation pending
            user.save()
            # email setup
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    # base 64 encode
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            user.email_user(subject=subject, message=message)
            # AFTER EMAIL SENDED the page redirected to activation send
            return render(
                request,
                "account/registration/register_email_confirm.html",
                {"form": registerForm},
            )
    # completely new user
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


# activation mail view user id and tokken needed
def account_activate(request, uidb64, token):
    try:  # url creating
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")  # login page
    else:
        return render(request, "account/registration/activation_invalid.html")


# address section
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)  # customer foreign key and list corresponding adddress
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):  # due to this id is uuid format
    if request.method == "POST":
        address = Address.objects.get(
            pk=id, customer=request.user
        )  # matching up customer table with user table both data needed for access
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    # removing unselect defult already have  finding using orm query
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    # new defult address setting
    return redirect("account:addresses")
