from django.contrib import admin
from .models import hmo, drug, patient, state
# Register your models here.

class HmoList(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'address', 'hmo_status', 'added_by')
    search_fields = ['name']

class Patient(admin.ModelAdmin):
    list_display = ('surname', 'firstname', 'card_no', 'phone_number','gender', 'hmo', 'added_by')
    search_fields = ['surname', 'firstname', 'hmo__name', 'card_no']
    list_max_show_all = True

class Drug(admin.ModelAdmin):
    list_display = ('drug_name', 'drug_code', 'date_added', 'added_by')
    search_fields = ['drug_name', 'drug_code']

class State(admin.ModelAdmin):
    list_display = ('state_name',)

admin.site.register(hmo, HmoList)
admin.site.register(patient, Patient)
admin.site.register(drug, Drug)
admin.site.register(state, State)
