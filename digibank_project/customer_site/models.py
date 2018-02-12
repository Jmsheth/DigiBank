from django.db import models


# Create your models here.
class Customer(models.Model):
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipCode = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=15)
    emailAdd = models.CharField(max_length=70, unique=True)
    kycId = models.CharField(max_length=50)
    idNumber = models.CharField(max_length=50, unique=True)
    userid = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.firstName

class Account(models.Model):
    # Account Model included by<kashif> to utilize Account details
    accountNum = models.IntegerField()
    routingNum = models.IntegerField()
    balance = models.FloatField(max_length=20)
    acntType = models.CharField(max_length=15)
    owner = models.ForeignKey(Customer, null=False,on_delete= models.CASCADE)

    def __str__(self):
        return self.owner


class Transaction(models.Model):
    # Transaction Model included by<kashif> to utilize Transaction details
    accntTo = models.CharField(max_length=15, null=False)
    accntFrom = models.ForeignKey(Account, null=False, on_delete= models.CASCADE)
    dateTime = models.DateTimeField(null=False)
    amount= models.FloatField(max_length=15)

    def __str__(self):
        return self.id


