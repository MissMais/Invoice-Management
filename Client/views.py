from rest_framework.response import Response
from .models import * 
from .serializer import *
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import *
import datetime
from django.db.models import Count,Sum     
import calendar
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from Auth_user.permissions import IsEmployeeOwner,IsAdminOrReadOnly,CombinedPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import response
from django.urls import reverse







class ClientAPI(APIView):
    def get(self,request):
        try:
            client_obj = Client.objects.all()
            client_serializer = ClientSerializer(client_obj,many=True)
            return Response(client_serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def post(self,request):

        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            client_data = {
                'client_name': validated_data.get('client_name'),
                'email':validated_data.get("email"),
                'contact':validated_data.get("contact"),
                'address': validated_data.get('address'),
                'pincode': validated_data.get('pincode'),
            }
            client_serializer = ClientSerializer(data=validated_data)

            if client_serializer.is_valid():
                try:
                    client_obj = Client.objects.create(**client_data)
                    client_obj.save()

                    # email = client_data['email']
                    # message = EmailMessage(
                    #     'Test email subject',
                    #     'test email body,  client create successfully ',
                    #     settings.EMAIL_HOST_USER,
                    #     [email]
                    # )
                    # message.send(fail_silently=False)

                except Exception as e:
                    return Response({"Message": f"Error creating client: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({"Message":"Client Registered successfully"}, status=status.HTTP_201_CREATED)
            
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

    
    def patch(self,request):
        try:
            validated_data=request.data
            print('\n\n\n',validated_data,'\n\n\n')
            client_update = request.GET.get('client_update')
            client_obj = Client.objects.get(client_id=client_update)
            try:    
                client_serializer = ClientSerializer(client_obj,data=validated_data,partial=True)
                
                if client_serializer.is_valid():
                    client_serializer.save()
                    return Response({"Message":"Data updated successfully"}, status=status.HTTP_200_OK)
                
                return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
             
            except Exception as e:
                return Response({"Message": f"Error updating client data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Client.DoesNotExist:
            return Response({"Message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self,request):
        try:
            delete_client = request.GET.get('delete_client')
            
            if not delete_client:
                return Response({"Message": "Client ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                client_obj = Client.objects.get(client_id=delete_client)

            except Client.DoesNotExist:
                return Response({"Message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                client_obj.delete()

            except Exception as e:
                return Response({"Message": f"Error deleting client: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"Message":"Client deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ClientFilter
             





class InvoiceAPI(APIView):
    def get(self,request ):
        try:
            sort_by = request.GET.get('sort_by')
            query = "SELECT * FROM invoice"

            if sort_by == 'ascending':
                query += " ORDER BY total_amount"

            elif sort_by == 'descending':
                query += " ORDER BY total_amount DESC"

            try:
                invoice_obj = Invoice.objects.raw(query)
                invoice_serializer = InvoiceSerializer(invoice_obj, many=True,context={"request":request})
                return Response(invoice_serializer.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"Message": f"Error executing query: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
              
    

    def post(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            invoice_serializer = InvoiceSerializer(data=validated_data)

            if invoice_serializer.is_valid():
                try:
                    client_obj = Client.objects.get(client_id=validated_data['client_id'])

                except Client.DoesNotExist:
                    return Response({"Message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
                
                invoice_obj = Invoice.objects.create(
                                                     client_id=client_obj,
                                                     total_amount=validated_data['total_amount'],
                                                     status=validated_data['status'],
                                                     generated_date = validated_data['generated_date'],
                                                     invoice_number = validated_data['invoice_number']
                                                     )
                for inv_item in validated_data.get("invoice_item_id", []):
                    obj,created = Invoice_item.objects.get_or_create(invoice_item_id=inv_item) 
                    invoice_obj.invoice_item_id.add(obj)
                
                invoice_obj.save()
            
                return Response({"Message":"Invoice created successfully"}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(invoice_serializer._errors, status=status.HTTP_400_BAD_REQUEST) 
             
        except Exception as e:
            return Response({"Message": f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')

            try:
                invoice_obj = Invoice.objects.get(invoice_id=validated_data['invoice_id'])

            except Invoice.DoesNotExist:
                return Response({"Message": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            invoice_serializer = InvoiceSerializer(invoice_obj,data=validated_data,partial=True)
            if invoice_serializer.is_valid():
                invoice_serializer.save()
                if 'invoice_item_id' in validated_data:
                    invoice_obj.invoice_item_id.clear()
                    for inv_item in validated_data.get("invoice_item_id", []):
                        obj, created = Invoice_item.objects.get_or_create(invoice_item_id=inv_item)
                        invoice_obj.invoice_item_id.add(obj)
                return Response({"Message":"Updated successfully"}, status=status.HTTP_200_OK )
            
            else:
                return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
             
        except Exception as e:
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request):
        try:
            delete = request.GET.get('delete')

            if delete:
                try:
                    invoice_obj = Invoice.objects.get(invoice_id=delete)
                    invoice_obj.delete()
                    return Response({"Message":"data deleted successfully "}, status=status.HTTP_200_OK)
                
                except Invoice.DoesNotExist:
                    return Response({"Message": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"Message": "No invoice ID provided"}, status=status.HTTP_400_BAD_REQUEST)  
            
        except Exception as e:  
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        
        
        
        
class SendInvoice(APIView):
    def post(self,request):
        try:
            data = request.data.get('client_id')
            print('\n\n\n',data,'\n\n\n')
            # inv_pdf = data.get('user_id')
            client_obj = Invoice.objects.get(client_id=data)
            print('\n\n\n',client_obj.client_id.user_id.email,'\n\n\n')
            print('\n\n\n',client_obj.invoice_pdf,'\n\n\n')
            email = client_obj.client_id.user_id.email
            message = EmailMessage(
                        'Test email subject',
                        'test email body,  invoice create successfully ',
                        settings.EMAIL_HOST_USER,
                        [email]
                    )
            file_path = f"{settings.BASE_DIR}/media/{client_obj.invoice_pdf}"
            message.attach_file(file_path)
            message.send()
            print('\n\n\n','Done','\n\n\n')
            return Response('Done')
        except Exception as e:  
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class InvoiceListView(generics.ListAPIView):  
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend]
    filterset_class = InvoiceFilter

class TeamAPIView(APIView):
    serializer_class = TeamSerializer
    def get(self, request):
        try:
            team = Team.objects.all()
            team_serializer = self.serializer_class(team, many=True)
            return Response(team_serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            validated_data = request.data
            serializer_obj = self.serializer_class(data=validated_data)

            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"team create successfully"}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request):
        try:
            validated_data = request.data

            try:
                team = Team.objects.get(team_id=validated_data['team_id'])

            except Team.DoesNotExist:
                return Response({"Message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer_obj = self.serializer_class(team, data=request.data)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"Team update Successfully"}, status=status.HTTP_200_OK)
            
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    team_obj = Team.objects.get(team_id=delete)
                    team_obj.delete()
                    return Response({"Message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Team.DoesNotExist:
                    return Response({"Message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"Message": "No team ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = TeamFilter



class ProjectAPIView(APIView):
    def get(self, request):
        try:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self, request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,  '\n\n\n')
            serializer_obj = ProjectSerializer(data=validated_data)
            if serializer_obj.is_valid():
                project_obj = Project.objects.create( 
                                                     project_name = validated_data["project_name"],
                                                     duration=validated_data["duration"],
                                                     start_date = validated_data["start_date"],
                                                        )
                project_obj.save()
                    
                return Response({"Message":"Project created successfully","Data":serializer_obj.data}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request):
        try:
            validated_data = request.data
            try:
                project_obj = Project.objects.get(project_id=validated_data['project_id'])

            except Project.DoesNotExist:
                return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer_obj = ProjectSerializer(project_obj, data=validated_data, partial=True)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message": "Project updated successfully"})
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    project_obj = Project.objects.get(project_id=delete)
                    project_obj.delete()
                    return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Project.DoesNotExist:
                    return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"message": "No project ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProjectListView(generics.ListAPIView):  
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend]
    filterset_class = ProjectFilter
 


class InvoiceitemAPI(APIView):
    def get(self,request):
        try:
            invoiceitem_obj = Invoice_item.objects.all()
            invoiceitem_serializer = InvoiceitemSerializer(invoiceitem_obj,many=True)
            return Response(invoiceitem_serializer.data,status=status.HTTP_200_OK)  
        
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            invoiceitem_serializer = InvoiceitemSerializer(data=validated_data)

            if invoiceitem_serializer.is_valid():
               invoiceitem_serializer.save()
               return Response({"Message":"data posted successfully"}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(invoiceitem_serializer._errors, status=status.HTTP_400_BAD_REQUEST) 
             
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self,request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            try:
                invoiceitem_obj = Invoice_item.objects.get(invoice_item_id=validated_data['invoice_item_id'])

            except Invoice_item.DoesNotExist:
                return Response({"message": "Invoice item not found"}, status=status.HTTP_404_NOT_FOUND)
            
            invoiceitem_serializer = InvoiceitemSerializer(invoiceitem_obj,data=validated_data,partial=True)


            if invoiceitem_serializer.is_valid():
                invoiceitem_serializer.save()
                return Response({"Message":"data updated successfully"},status=status.HTTP_200_OK )

            else:
                return Response(invoiceitem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    invoiceitem_obj = Invoice_item.objects.get(invoice_item_id=delete)
                    invoiceitem_obj.delete()
                    return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Invoice_item.DoesNotExist:
                    return Response({"message": "Invoice item not found"}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"message": "No invoice item ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        

class PaymentAPIView(APIView):
    def get(self,request ):
        try:
            sort_by = request.query_params.get('sort_by')
            query = "SELECT * FROM payment"

            if sort_by == 'ascending':
                query += " ORDER BY amount"

            elif sort_by == 'descending':
                query += " ORDER BY amount DESC"

            try:
                payment_obj = Payment.objects.raw(query)
                serializer_obj = PaymentSerializer(payment_obj, many=True)
                return Response(serializer_obj.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Message": f"Error executing query: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            serializer_obj = PaymentSerializer(data=validated_data)
    
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"created payment successfully"},status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def put(self, request):
        try:
            validated_data = request.data
            print('\n\n\n',validated_data,'\n\n\n')
            update_payment = request.GET.get('update_payment')
            try:
                payment_obj = Payment.objects.get(payment_id=update_payment)

            except Payment.DoesNotExist:
                return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer_obj = PaymentSerializer(payment_obj ,data=validated_data)

            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"Updated successfully"},status=status.HTTP_201_CREATED)

            else:
                return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
        try:
            delete = request.GET.get('delete')
            if delete:
                try:
                    payment_obj = Payment.objects.get(payment_id=delete)
                    payment_obj.delete()
                    return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                
                except Payment.DoesNotExist:
                    return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "No payment ID provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = PaymentFilter
        
class Technology_optionViewSet(viewsets.ModelViewSet):
    queryset = Technology_option.objects.all()
    serializer_class = Technology_optionSerializer
    
class TechnologyViewSet(viewsets.ModelViewSet):

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = TechnologyFilter
    
class Payment_methodViewSet(viewsets.ModelViewSet):
    queryset = Payment_method.objects.all()
    serializer_class = Payment_methodSerializer

class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer  
              
    
    

        
@api_view(['GET'])
def invoice_chart(request):
    if request.method == 'GET':
        pass
        # now = datetime.datetime.now()
        # current_month = now.month
        # current_year = now.year
        # if current_month == 1:
        #     previous_month = 12
        #     previous_year = current_year - 1
        # else:
        #     previous_month = current_month - 1
        #     previous_year = current_year
        # current_month_invoices = Invoice.objects.filter(generated_date__year=current_year, generated_date__month=current_month)
        # previous_month_invoices = Invoice.objects.filter(generated_date__year=previous_year, generated_date__month=previous_month)
        # current_month_count = current_month_invoices.count()
        # previous_month_count = previous_month_invoices.count()

        # invoice_counts = Invoice.objects.values('generated_date__year', 'generated_date__month').annotate(count=Count('invoice_id')).order_by('generated_date__year', 'generated_date__month')
        # inv_count = []
        # for count_data in invoice_counts:
        #     year = count_data['generated_date__year']
        #     month = count_data['generated_date__month']
        #     count = count_data['count']
        #     month_name = calendar.month_abbr[month]
        #     inv_count.append({'year': year, 'month': month_name, 'count': count})

        # if previous_month_count == 0:
        #     percentage_change = 100.0 if current_month_count > 0 else 0.0
        # else:
        #     percentage_change = ((current_month_count - previous_month_count) / previous_month_count) * 100


        # inv_serializer = InvoiceSerializer(current_month_invoices, many=True).data
        # inv_obj_model=Invoice.objects.all()
        # inv_serializer_1 = InvoiceSerializer(inv_obj_model, many=True).data
        # total_amount = []
        # due = []
        # generated_date = []
        # for i in inv_serializer_1:
        #     total_amount.append(i['total_amount'])
        #     due.append(i['generated_date'])
        #     datee = datetime.datetime.strptime(i['generated_date'], "%Y-%m-%d")
        #     generated_date.append(f'{calendar.month_abbr[datee.month]}-{datee.year}')


        # tech_count_num=[]
        # tech_count_name=[]
        # tech_count = {}
        # technology_counts = Technology.objects.annotate(num_projects=Count('project')).values('name', 'num_projects')
        # for tech in technology_counts:
        #     tech_count_name.append(tech['name'])
        #     tech_count_num.append(tech['num_projects'])
        #     tech_count[tech['name']] = tech['num_projects']
            
        # return Response({
        #     'total_amount': total_amount,
        #     'due': due,
        #     'generated_date': generated_date,
        #     'current_month_count': current_month_count,
        #     'previous_month_count': previous_month_count,
        #     'percentage_change': percentage_change,
        #     'inv_count': inv_count,
        #    'technology_counts': tech_count,
        #     "tech_count_num":tech_count_num,
        #     "tech_count_name":tech_count_name
        # }) 
        
    





class ChangePasswordView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        data = request.data
        user_obj = self.request.user
        change_serializer=ChangePasswordSerializer(data=data)
        if change_serializer.is_valid():
            if not user_obj.check_password(data["old_password"]):
                return Response({"old_password":["Wrong Password"]})
            user_obj.set_password(data["new_password"])
            user_obj.save()

            response = {
                "password updated successfully"
            }

            return Response(response)
        
        return Response(change_serializer.errors)
    
    





class PasswordResetView(APIView):
    def post(self,request):
        data = request.data
        reset_serializer = PasswordResetSerializer(data=data)
        reset_serializer.is_valid(raise_exception=True)
        email = reset_serializer.data["email"]
        user = CoreUser.objects.filter(email=email).first()
        print(user)
        if user:
            user_id_encode = urlsafe_base64_encode(force_bytes(user.user_id))
            token_generator = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset-password",
                kwargs={"user_id_encode":user_id_encode,"token":token_generator}
            )
            reset_link = f"localhost:8000{reset_url}"

            return response.Response({"message":f"your password reset link:{reset_link}"})
        
        else:
            return response.Response({"message":"user does not exits"})
        

class PasswordResetConfirmView(APIView):

    confirm_serializer = PasswordResetConfirmSerializer

    def patch(self,request,*args,**kwargs):
        data = request.data

        serializer = self.confirm_serializer(data=data,context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)

        return response.Response({"message":"password reset complete"})



@api_view(['GET'])
def sales_per_month(request):
    if request.method == 'GET':
        pass
        # now = datetime.datetime.now()
        # current_month = now.month
        # current_year = now.year
        # if current_month == 1:
        #     previous_month = 12
        #     previous_year = current_year - 1
        # else:
        #     previous_month = current_month - 1
        #     previous_year = current_year

        # invoice_sales = Invoice.objects.values('generated_date__year','generated_date__month').annotate(total_sale=Sum('total_amount')).order_by('generated_date__year','generated_date__month')
        # invoice_sales_per_month = []
        # for sale_data in invoice_sales:
        #     year  = sale_data['generated_date__year']
        #     month = sale_data['generated_date__month']
        #     total_sale = sale_data['total_sale']
        #     month_name = calendar.month_abbr[month]
        #     invoice_sales_per_month.append({'year': year,'month':month_name,'total_sale':total_sale})
            
        # return Response({
        #    'invoice_sales_per_month':invoice_sales_per_month,
        # })

            






        


        



                   

            


