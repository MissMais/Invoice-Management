from django.db import models
from Auth_user.models import * 


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=255)
    user_id = models.ForeignKey(CoreUser,on_delete=models.CASCADE,related_name='user_client')
    company_address = models.CharField(max_length=555)
    
    DisplayField = ['client_id','client_name','user_id','company_address']
    
    def __str__(self):
        return self.client_name    
    
    class Meta:
        db_table = 'client'



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
    rate = models.IntegerField()

    DisplayField = ['tax_id','tax_name','rate']

    def __str__(self):
        return self.tax_name
    
    class Meta:
        db_table = 'tax'




class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=155)

    DisplayField = ['team_id','team_name']

    def __str__(self):
        return self.team_name
    
    class Meta:
        db_table = 'team'




class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=155)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE,null=True)
    team_id = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)
    tech_id = models.ManyToManyField(Technology)

    
    DisplayField = ['project_id','project_name','duration','client_id','team_id','tech_id']

    def __str__(self):
        return self.project_name
    
    class Meta:
        db_table = 'project'



