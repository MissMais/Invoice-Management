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
from django.db.models import Count      
import calendar
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from Auth_user.permissions import IsClientOwner,IsAdminOrReadOnly,CombinedPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.core.mail import EmailMessage





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
            client_data = {
                'client_name': validated_data.get('client_name'),
                'company_address': validated_data.get('company_address'),
            }
            client_serializer = ClientSerializer(data=validated_data)

            if client_serializer.is_valid():
                user_data = validated_data.pop('user_id',{})

                try:
                    user_obj = CoreUser.objects.create(
                                                        user_name=user_data.get("user_name"),
                                                        first_name=user_data.get("first_name"),
                                                        last_name=user_data.get("last_name"),
                                                        email=user_data.get("email"),
                                                        contact=user_data.get("contact"),
                                                        is_client=True
                                                        )
                    user_obj.set_password(user_data.get('password'))
                    user_obj.save()

                except Exception as e:
                    return Response({"Message": f"Error creating user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                try:
                    client_obj = Client.objects.create(user_id=user_obj,**client_data)

                    email = user_data['email']
                    message = EmailMessage(
                        'Test email subject',
                        'test email body,  client create successfully ',
                        settings.EMAIL_HOST_USER,
                        [email]
                    )
                    message.send(fail_silently=False)

                except Exception as e:
                    return Response({"Message": f"Error creating client: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({"Message":"Client Registered successfully"}, status=status.HTTP_201_CREATED)
            
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

    
    def patch(self,request):
        try:
            validated_data=request.data
            client_update = request.GET.get('client_update')
            client_obj = Client.objects.get(client_id=client_update)
            client_data = {
                'client_name': validated_data.get('client_name'),
                'company_address': validated_data.get('company_address'),
            }
            user_data = validated_data.pop('user_id')
            user_obj = client_obj.user_id

            try:
                user_serializer = CoreUserSerializer(user_obj,data=user_data,partial=True)

                if user_serializer.is_valid():
                    user_serializer.save() 

                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
                 
            except Exception as e:
                return Response({"Message": f"Error updating user data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
           
            try:    
                client_serializer = ClientSerializer(client_obj,data=client_data,partial=True)
                
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
            
            user_obj = client_obj.user_id

            try:
                user_obj.delete()

            except Exception as e:
                return Response({"Message": f"Error deleting user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
                invoice_serializer = InvoiceSerializer(invoice_obj, many=True)
                return Response(invoice_serializer.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"Message": f"Error executing query: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({"Message": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
              
    

    def post(self,request):
        try:
            validated_data = request.data
            invoice_serializer = InvoiceSerializer(data=validated_data)

            if invoice_serializer.is_valid():
                try:
                    client_obj = Client.objects.get(client_id=validated_data['client_id'])

                except Client.DoesNotExist:
                    return Response({"Message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
                
                invoice_obj = Invoice.objects.create(
                                                     client_id=client_obj,
                                                     due_date=validated_data['due_date'] ,
                                                     total_amount=validated_data['total_amount'],
                                                     status=validated_data['status']
                                                     )
                return Response({"Message":"Invoice created successfully"}, status=status.HTTP_201_CREATED)
            
            else:
                print(invoice_serializer._errors)
                return Response(invoice_serializer._errors, status=status.HTTP_400_BAD_REQUEST) 
             
        except Exception as e:
            return Response({"Message": f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self,request):
        try:
            validated_data = request.data

            try:
                invoice_obj = Invoice.objects.get(invoice_id=validated_data['invoice_id'])

            except Invoice.DoesNotExist:
                return Response({"Message": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            
            invoice_serializer = InvoiceSerializer(invoice_obj,data=validated_data,partial=True)

            if invoice_serializer.is_valid():
                invoice_serializer.save()
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
            serializer_obj = ProjectSerializer(data=validated_data)

            try:
                client_obj = Client.objects.get(client_id=validated_data['client_id'])

            except Client.DoesNotExist:
                return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                team_obj = Team.objects.get(team_id=validated_data['team_id'])

            except Team.DoesNotExist:
                return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

            if serializer_obj.is_valid():
                project_obj = Project.objects.create( 
                                                     project_name = validated_data["project_name"],
                                                     duration=validated_data["duration"],
                                                     client_id=client_obj,
                                                     team_id=team_obj
                                                        )
                for t_name in validated_data.get("tech_id", []):
                    obj,created = Technology.objects.get_or_create(name=t_name) 
                    project_obj.tech_id.add(obj)
                    
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
            
            serializer_obj = ProjectSerializer(project_obj, data=validated_data,partial=True)


            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({"Message":"Project updated successfully"})
            
            else:
                return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    

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
    def get(self, request):
        try:
            payment_obj = Payment.objects.all()
            serializer_obj = PaymentSerializer(payment_obj, many=True)
            return Response(serializer_obj.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def post(self, request):
        try:
            validated_data = request.data
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
            try:
                payment_obj = Payment.objects.get(payment_id=validated_data['payment_id'])

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
        
        now = datetime.datetime.now()
        current_month = now.month
        current_year = now.year

        if current_month == 1:
            previous_month = 12
            previous_year = current_year - 1
        else:
            previous_month = current_month - 1
            previous_year = current_year
        current_month_invoices = Invoice.objects.filter(due_date__year=current_year, due_date__month=current_month)
        previous_month_invoices = Invoice.objects.filter(due_date__year=previous_year, due_date__month=previous_month)
        current_month_count = current_month_invoices.count()
        previous_month_count = previous_month_invoices.count()

        invoice_counts = Invoice.objects.values('due_date__year', 'due_date__month').annotate(count=Count('invoice_id')).order_by('due_date__year', 'due_date__month')
        inv_count = []
        for count_data in invoice_counts:
            year = count_data['due_date__year']
            month = count_data['due_date__month']
            count = count_data['count']
            month_name = calendar.month_abbr[month]
            inv_count.append({'year': year, 'month': month_name, 'count': count})

        if previous_month_count == 0:
            percentage_change = 100.0 if current_month_count > 0 else 0.0
        else:
            percentage_change = ((current_month_count - previous_month_count) / previous_month_count) * 100

        inv_serializer = InvoiceSerializer(current_month_invoices, many=True).data
        inv_id = []
        total_amount = []
        due_date = []
        for i in inv_serializer:
            inv_id.append(i['invoice_id'])
            total_amount.append(i['total_amount'])
            datee = datetime.datetime.strptime(i['due_date'], "%Y-%m-%d")
            due_date.append(f'{calendar.month_abbr[datee.month]}-{datee.year}')


        tech_count = {}
        technology_counts = Technology.objects.annotate(num_projects=Count('project')).values('name', 'num_projects')
        for tech in technology_counts:
            tech_count[tech['name']] = tech['num_projects']

        return Response({
            'inv_id': inv_id,
            'total_amount': total_amount,
            'due_date': due_date,
            'current_month_count': current_month_count,
            'previous_month_count': previous_month_count,
            'percentage_change': percentage_change,
            'inv_count': inv_count,
            'technology_counts': tech_count
        })            