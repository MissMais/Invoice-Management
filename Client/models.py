from django.db import models
from Auth_user.models import CoreUser

# Create your models here.



class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255,unique=True)
    user_id = models.ForeignKey(CoreUser,on_delete=models.CASCADE,null=True)
    company_address = models.CharField(max_length=255)


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    due_date = models.DateField()
    total_amount = models.IntegerField()
    status = models.CharField(max_length=255)



