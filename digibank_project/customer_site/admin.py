from django.contrib import admin
from . import models
from core_files.models import Transactions, Account
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(Transactions)
admin.site.register(Account)
