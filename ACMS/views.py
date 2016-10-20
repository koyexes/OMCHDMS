from django.shortcuts import render, get_object_or_404
from .forms import LoginForm, PatientForm, DrugForm, HmoForm, ChangePassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import hashers


# Create your views here.

login_url = '/acms/login'

def index(request):
    if request.method == "POST": # checking if it's a post request
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                if user.is_active: # checking if the user is still active
                    login(request, user) # logging the user in
                    request.session.set_expiry(1800) # setting the session expiry time, after which login is required
                    return HttpResponseRedirect(reverse('ACMS:homepage'))

            else:
                try:
                    username = User.objects.get(username = form.cleaned_data["username"])
                    # since authenticate method returns none for inactive registered users, the if statement below takes care of checking if user exist
                    # but inactive in order to forward the right feedback message
                    if username and hashers.check_password(form.cleaned_data["password"], User.objects.get(username = username).password):
                        messages.error(request, "Your account has been disabled! Contact Admin...")
                        return HttpResponseRedirect(reverse('ACMS:index'))
                    else:
                         messages.error(request, 'Incorrect username and password!!!') # saving message error to be displayed on template
                         return HttpResponseRedirect(reverse('ACMS:index'))
                except:
                    messages.error(request, 'Incorrect username and password!!!') # saving message error to be displayed on template
                    return HttpResponseRedirect(reverse('ACMS:index'))

# if the request is a GET request
    else:
        form = LoginForm() # creating new form
        if request.path == "/acms/login/":
            messages.info(request, "Please log in");
        logout(request) # logging out the user and clearing the user's session

    return render(request, 'acms/index.html', {"form": form})



@login_required(redirect_field_name="", login_url=login_url) # login required to view this page
def homepage(request):
    admin = False
    if request.user.is_staff: admin = True # checking if the user has administrative rights
    change_password_form = ChangePassword(auto_id = False)
    context = {"name" : "%s %s" % ( request.user.first_name, request.user.last_name), "username" : request.user.username, "admin" : admin, 'change_password_form' : change_password_form} # declaring the template context
    return render(request, 'acms/homepage.html', context) # rendering the homepage template

@login_required(redirect_field_name="", login_url=login_url)
def workpage(request):
    admin = False
    if request.user.is_staff: admin = True
    patient_form = PatientForm(auto_id= False)
    drug_form = DrugForm(auto_id = False)
    hmo_form = HmoForm(auto_id = False)
    change_password_form = ChangePassword(auto_id = False)
    context = {"name" : "%s %s" % (request.user.first_name, request.user.last_name), "username" :
        request.user.username, 'admin': admin, "patient_form" : patient_form, 'drug_form': drug_form, 'hmo_form': hmo_form, 'change_password_form' : change_password_form }
    return render(request, 'acms/workpage.html', context)

@login_required(redirect_field_name = "", login_url = login_url)
def patient(request):
    if request.method == 'POST': # checking the request method
        patient_form = PatientForm(request.POST, user = request.user)
        if patient_form.is_valid():
            patient_form.save()
            messages.success(request, str(patient_form))
            return HttpResponseRedirect(reverse('ACMS:workpage'))
        else:
            messages.error(request, "Patient couldn't be created")
            return HttpResponseRedirect(reverse('ACMS:workpage'))
    else:
        return HttpResponseRedirect(reverse('ACMS:workpage'))


@login_required(redirect_field_name = "", login_url = login_url)
def drug(request):
    if request.method == 'POST':
        drug_form = DrugForm(request.POST, user = request.user)
        if drug_form.is_valid():
            drug_form.save()
            messages.success(request, str(drug_form))
            return HttpResponseRedirect(reverse('ACMS:workpage'))
        else:
            messages.error(request, "Drug couldn't be created")
            return HttpResponseRedirect(reverse('ACMS:workpage'))
    else:
        return HttpResponseRedirect(reverse('ACMS:workpage'))\

@login_required(redirect_field_name = "", login_url = login_url)
def hmo(request):
    if request.method == 'POST':
        hmo_form = HmoForm(request.POST, user = request.user)
        if hmo_form.is_valid():
            hmo_form.save()
            messages.success(request, str(hmo_form))
            return HttpResponseRedirect(reverse('ACMS:workpage'))
        else:
            messages.error(request, "HMO couldn't be created")
            return HttpResponseRedirect(reverse('ACMS:workpage'))
    else:
        return HttpResponseRedirect(reverse('ACMS:workpage'))



