from django.shortcuts import render
from .forms import LoginForm, PatientForm, DrugForm, HmoForm, ChangePassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from models import patient, drug, hmo

# Create your views here.

login_url = '/acms/login'

main_context = {'change_password_form' : ChangePassword(auto_id = False) , "patient_form" :PatientForm(auto_id=False), 'drug_form': DrugForm(auto_id=False), 'hmo_form': HmoForm(auto_id=False), 'total_number_of_patients' : patient.total_number_of_patients(), 'total_number_of_drugs' :drug.total_number_of_drugs(), 'total_number_of_hmos' :hmo.total_number_of_hmos()}

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
                messages.info(request, "Please log")

        logout(request) # logging out the user and clearing the user's session

    return render(request, 'acms/index.html', {"form": form})



@login_required(redirect_field_name="", login_url=login_url) # login required to view this page
def homepage(request):
    context = {"user" : request.user} # declaring the template context
    main_context.update(context)
    return render(request, 'acms/homepage.html', main_context) # rendering the homepage template

@login_required(redirect_field_name = "", login_url = login_url)
def patient_form_view(request):
    if request.method == 'POST': # checking the request method
        patient_form = PatientForm(request.POST, user = request.user)
        request.session['form_response_heading'] = '1 patient'
        if patient_form.is_valid():
            result = patient_form.save()
            if result[0]:
                messages.success(request, str(patient_form), extra_tags= "form response")
            else:
                messages.error(request, result[1], extra_tags="form response")

            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            messages.error(request, "Patient couldn't be created", extra_tags= "form response")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required(redirect_field_name = "", login_url = login_url)
def drug_form_view(request):
    if request.method == 'POST':
        drug_form = DrugForm(request.POST, user = request.user)
        request.session['form_response_heading'] = '1 drug'
        if drug_form.is_valid():
            result = drug_form.save()
            if result[0]:
                messages.success(request, str(drug_form), extra_tags= "form response")
            else:
                messages.error(request, result[1], extra_tags="form response")

            return HttpResponseRedirect(request.META["HTTP_REFERER"] )
        else:
            messages.error(request, "Drug couldn't be created", extra_tags="form response")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required(redirect_field_name = "", login_url = login_url)
def hmo_form_view(request):
    if request.method == 'POST':
        hmo_form = HmoForm(request.POST, user = request.user)
        request.session['form_response_heading'] = '1 hmo'
        if hmo_form.is_valid():
            result = hmo_form.save()
            if result[0]:
                messages.success(request, str(hmo_form), extra_tags= "form response")
            else:
                messages.error(request, result[1], extra_tags="form response")

            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            messages.error(request, "HMO couldn't be created", extra_tags= "form response")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required(redirect_field_name = "", login_url = login_url)
def changePassword(request):
    if request.method == 'POST':
        change_password_form = ChangePassword(request.POST, user=request.user)  # binding the form
        if change_password_form.is_valid(): # checking if form parameters are valid
            result = hashers.check_password(change_password_form.cleaned_data['currentPassword'], request.user.password)
            if result: # checking if the formers passwords match
                if change_password_form.cleaned_data['newPassword'] == change_password_form.cleaned_data['confirmNewPassword']:
                    change_password_form.save() # changing the former password to the new password
                    messages.info(request, "Password Changed") # return appropriate messages
                    return HttpResponseRedirect(reverse('ACMS:password')) # redirecting to the appropriate url
                else:
                    messages.error(request, "Couldn't change password, Please contact your Administrator", extra_tags="password")
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])  # redirect back to the page where the password form was posted
            else:
                messages.error(request, "Incorrect Password", extra_tags= "password")
                return HttpResponseRedirect(request.META["HTTP_REFERER"]) # redirect back to the page where the password form was posted

        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

    else:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required(redirect_field_name="", login_url= login_url)
def find_patient(request):
    return render(request, 'acms/find patient.html', main_context)

@login_required(redirect_field_name="", login_url= login_url)
def find_drug(request):
    return render(request, 'acms/find drug.html', main_context)

@login_required(redirect_field_name="", login_url= login_url)
def find_hmo(request):
    return render(request, 'acms/find hmo.html', main_context)





