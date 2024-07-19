from rest_framework import routers, serializers,viewsets
from .models import *
from Auth_user.models import *
from Auth_user.serializer import *
from django.contrib.auth.models import UserManager
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

 

class EmployeeSerializer(serializers.ModelSerializer):
    user_id =CoreUserSerializer()
    city_id = serializers.StringRelatedField(read_only=True)
    state_id = serializers.StringRelatedField(read_only=True)
    country_id = serializers.StringRelatedField(read_only=True)
    role_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


    def update(self,instance,validated_data):
        u_data = validated_data.get('user_id')
        if u_data:
            user_data = validated_data.pop('user_id')
            user_data_data = instance.user_id
            user_data_data.user_name = user_data.get('user_name',user_data_data.user_name)
            user_data_data.first_name = user_data.get('first_name',user_data_data.first_name)
            user_data_data.last_name = user_data.get('last_name',user_data_data.last_name)
            user_data_data.email = user_data.get('email',user_data_data.email)
            user_data_data.contact = user_data.get('contact',user_data_data.contact)
            user_data_data.save()

        instance.age = validated_data.get('age',instance.age)
        instance.salary = validated_data.get('salary',instance.salary)
        instance.id_proof = validated_data.get('id_proof',instance.id_proof)
        instance.address = validated_data.get('address',instance.address)
        instance.city_id = validated_data.get('city_id',instance.city_id)
        instance.state_id = validated_data.get('state_id',instance.state_id)
        instance.country_id = validated_data.get('country_id',instance.country_id)
        instance.role_id = validated_data.get('role_id',instance.role_id)
        instance.pincode = validated_data.get('pincode',instance.pincode)
        instance.save()

        return instance




class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)



 



class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()

    class Meta:
        fields = ("email",)




class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = CoreUser.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data