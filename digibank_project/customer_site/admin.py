from django.contrib import admin
from . import models
from core_files.models import Transaction, Account
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(Transaction)
admin.site.register(Account)
