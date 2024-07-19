from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, user_name, password):
        if not user_name:
            raise ValueError('user name is required')
        if not password:
            raise ValueError('password is required')
        
        user = self.model(user_name=user_name)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, user_name,password,**kwargs):
        user = self.create_user(
            user_name ,password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.save()
        return user



class CoreUser(AbstractBaseUser,PermissionsMixin):
        user_id = models.AutoField(primary_key=True)
        user_name = models.CharField(max_length=255,unique=True)
        first_name = models.CharField(max_length=155)
        last_name = models.CharField(max_length=155)
        email = models.EmailField(null=True,unique=True)
        contact =PhoneNumberField(null=True,unique=True)
        is_client=models.BooleanField(default=False,null=True)
        is_employee=models.BooleanField(default=False,null=True)
        is_admin=models.BooleanField(default=False)
        is_staff=models.BooleanField(default=False)

        USERNAME_FIELD = 'user_name'
        REQUIRED_FIELDS = ['first_name','last_name']
        objects = UserManager() 
        
        class Meta: 
            db_table = 'core_user'
            
        def __str__(self):
            return f'{self.first_name} {self.last_name} '


        DisplayField = ['user_id','user_name','first_name','last_name','email','contact','is_client','is_employee']
    



class Role(models.Model):
    role_id=models.AutoField(primary_key=True)
    role_type=models.CharField(max_length=255)


    DisplayField = ['role_id','role_type']


    
    def __str__(self):
        return self.role_type
    
    class Meta:
        db_table = 'role'

class Country(models.Model):
    country_id=models.AutoField(primary_key=True)
    country_name=models.CharField(max_length=255)

    DisplayField = ['country_id','country_name']
    
    def __str__(self):
        return self.country_name
    
    class Meta:
        db_table = 'country'
class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name=models.CharField(max_length=255)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,related_name='state_country')

    DisplayField = ['state_id','state_name']
    
    def __str__(self):
        return self.state_name
    
    class Meta:
        db_table = 'state'
    
class City(models.Model):
    city_id=models.AutoField(primary_key=True)
    city_name=models.CharField(max_length=255)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,related_name='city_state')

    DisplayField = ['city_id','city_name']
    
    def __str__(self):
        return self.city_name
    
    class Meta:
        db_table = 'city'
    
        