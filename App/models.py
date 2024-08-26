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

    def create_superuser(self,user_name,password,**kwargs):
        user = self.create_user(
            user_name ,password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user



class CoreUser(AbstractBaseUser,PermissionsMixin):
        user_id = models.AutoField(primary_key=True)
        user_name = models.CharField(max_length=255,unique=True)
        is_admin=models.BooleanField(default=False)
        is_staff=models.BooleanField(default=False)
        role = models.ForeignKey('Role',on_delete=models.SET_NULL,related_name='user_role',null=True)

        USERNAME_FIELD = 'user_name'
        objects = UserManager() 
        DisplayField = ['user_id','user_name']
        
        class Meta: 
            db_table = 'core_user'
            
        def __str__(self):
            return self.user_name
        
        
class Role(models.Model):
    role_id=models.AutoField(primary_key=True)
    role_type=models.CharField(max_length=255)
    
    DisplayField = ['role_id','role_type']
    
    def __str__(self):
        return self.role_type
    
    class Meta:
        db_table = 'role'
        

class CompanyDetails(models.Model):
    company_details_id = models.AutoField(primary_key=True)
    user_id =models.ForeignKey(CoreUser,on_delete=models.CASCADE,related_name='company_user')
    company_name = models.CharField(max_length=155)
    company_logo=models.ImageField(upload_to='CompanyLogo/')
    bank_name=models.CharField(max_length=155)
    branch_name=models.CharField(max_length=155)
    account_number=models.CharField(max_length=155)
    ifsc_code=models.CharField(max_length=155)
    gst_in=models.CharField(max_length=155)
    digital_seal=models.ImageField(upload_to='CompanyLogo/')
    digital_signature=models.ImageField(upload_to='CompanyLogo/')
    company_address = models.CharField(max_length=155)
    HNO =models.BigIntegerField(null=True) 
    landmark = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    pincode=models.CharField(max_length=15)
    state = models.CharField(max_length=255,null=True)
    contry = models.CharField(max_length=255,null=True)
    
    DisplayField = ['company_details_id','company_name','company_address','pincode','bank_name']
    
    def __str__(self):
        return self.company_name
    class Meta:
        db_table='company_details'
                
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    address = models.CharField(max_length=555)
    city = models.CharField(max_length=255)
    pincode=models.CharField(max_length=15)
    country = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone =PhoneNumberField(unique=True)
    
    DisplayField = ['customer_id','customer_name','contact_name','city','country','pincode','email','phone','address']
    
    def __str__(self):
        return self.customer_name    
    
    class Meta:
        db_table = 'customer'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10,decimal_places=3)
    stock_quantity = models.IntegerField()
    
    DisplayField = ['product_id','product_name','description','stock_quantity']

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'product'
        
class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_number=models.CharField(max_length=100,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,related_name='client_invoice')
    generated_date = models.DateField()
    due_date = models.DateField() 
    total_amount = models.IntegerField()
    status = models.CharField(max_length=255)
    invoice_item_id = models.ManyToManyField("Invoice_item")
    

    DisplayField = ['invoice_id','customer','total_amount','status','generated_date']

    def __str__(self):
        return self.customer.customer_name   
    
    class Meta:
        db_table = 'invoice'        
        
class Invoice_item(models.Model):
    invoice_item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    total_amount = models.DecimalField(decimal_places=2,max_digits=10,null=True)
    tax_amount=models.DecimalField(max_digits=10,decimal_places=3)


    DisplayField = ['invoice_item_id','product_id','quantity','unit_price','total_amount','tax_amount']


    def __str__(self):
        return self.product_id.product_name
    
    class Meta:
        db_table = 'invoice_item'        
        
class Item_tax(models.Model):
    item_tax_id = models.AutoField(primary_key=True)
    invoice_item = models.ForeignKey(Invoice_item,on_delete=models.CASCADE,related_name='item')
    tax = models.ForeignKey('Tax',on_delete=models.CASCADE,related_name='tax')
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    DisplayField = ['item_tax_id','invoice_item','tax','amount']

    # def __str__(self):
    #     return f"ItemTax {self.tax.tax_name}"

    class Meta:
        db_table = 'item_tax'
        
                
class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=155)
    rate = models.DecimalField(decimal_places=2,max_digits=5)

    DisplayField = ['tax_id','tax_name','rate']

    def __str__(self):
        return f'{self.tax_name} - {self.rate}%'
    
    class Meta:
        db_table = 'tax'        
        
   
   
class Payment_method(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=55)

    DisplayField = ['payment_method_id','payment_type']

    def __str__(self):
        return self.payment_type
    
    class Meta:
        db_table = 'payment_method'
        
                
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    method_id = models.ForeignKey(Payment_method,on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    payment_date = models.DateField(blank=False)

    DisplayField = ['payment_id','invoice_id','method_id','amount','payment_date']

    # def __str__(self):
    #     return self.payment_id
    
    class Meta:
        db_table = 'payment'        