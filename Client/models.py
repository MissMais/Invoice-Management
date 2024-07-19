from django.db import models
from Auth_user.models import * 


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    user_id = models.OneToOneField(CoreUser,on_delete=models.CASCADE)
    company_address = models.CharField(max_length=555)
    
    DisplayField = ['client_id','client_name','user_id','company_address']
    
    def __str__(self):
        return self.client_name    
    
    class Meta:
        db_table = 'client'




class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    # due_date = models.DateField()
    total_amount = models.IntegerField()
    status = models.CharField(max_length=255)
    generated_date = models.DateField()


    DisplayField = ['invoice_id','client_id','total_amount','status','generated_date']

    def __str__(self):
        return self.status
    
    class Meta:
        db_table = 'invoice'




class Technology_option(models.Model):
    option_id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=155)

    DisplayField = ['option_id','option']

    def __str__(self):
        return self.option
    
    class Meta:
        db_table = 'technology_option'


class Technology(models.Model):
    tech_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    option_id = models.ForeignKey(Technology_option,on_delete=models.CASCADE,null=True)

    DisplayField = ['tech_id','name','option_id']

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'technology'
    

class Payment_method(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=55)

    DisplayField = ['payment_method_id','payment_type']

    def __str__(self):
        return self.payment_type
    
    class Meta:
        db_table = 'payment_method'


class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=155)
    rate = models.DecimalField(decimal_places=2,max_digits=5)

    DisplayField = ['tax_id','tax_name','rate']

    def __str__(self):
        return f'{self.tax_name} - {self.rate}%'
    
    class Meta:
        db_table = 'tax'



class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=150)

    DisplayField = ['team_id','team_name']

    def __str__(self):
        return self.team_name
    
    class Meta:
        db_table = 'team'




class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=155)
    team_id = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)
    tech_id = models.ManyToManyField(Technology)
    start_date = models.DateField(null=True)

    
    DisplayField = ['project_id','project_name','duration','team_id','tech_id','start_date']

    def __str__(self):
        return self.project_name
    
    class Meta:
        db_table = 'project'


class Invoice_item(models.Model):
    invoice_item_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    project_id = models.OneToOneField(Project,on_delete=models.CASCADE,null=True)
    item_price = models.IntegerField()
    tax_id = models.ForeignKey(Tax,on_delete=models.CASCADE,null=True)
    tax_amount = models.IntegerField()


    DisplayField = ['invoice_item_id','invoice_id','project_id','item_price','tax_id','tax_amount']


    def __str__(self):
        return f"InvoiceItem {self.invoice_item_id}"
    
    class Meta:
        db_table = 'invoice_item'




class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    method_id = models.ForeignKey(Payment_method,on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    payment_date = models.DateField(blank=False)

    DisplayField = ['payment_id','invoice_id','method_id','amount','payment_date']

    def __str__(self):
        return self.payment_id
    
    class Meta:
        db_table = 'payment'