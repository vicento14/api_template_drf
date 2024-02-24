# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .models import UserAccounts
from .serializers import UserAccountsSerializer
from django.db.models import Q

# Create your views here.

@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "user_accounts": reverse("user_accounts-list", request=request, format=format),
        }
    )

class UserAccountsApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        user_accounts = None

        IdNumber = request.GET.get('id_number', None)
        FullName = request.GET.get('full_name', None)
        Role = request.GET.get('role', None)

        # Start with an empty Q object
        q_objects = Q()

        # Add conditions to the Q object if the variables are present
        if IdNumber:
            q_objects |= Q(IdNumber__startswith=IdNumber)
        if FullName:
            q_objects |= Q(FullName__icontains=FullName)
        if Role:
            q_objects |= Q(Role__icontains=Role)

        if IdNumber is not None or FullName is not None or Role is not None:
            user_accounts = UserAccounts.objects.using("web_template").filter(q_objects)
        else:
            user_accounts = UserAccounts.objects.using("web_template").all()
            
        serializer = UserAccountsSerializer(user_accounts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'IdNumber': request.data.get('IdNumber'),
            'FullName': request.data.get('FullName'),
            'Username': request.data.get('Username'),
            'Password': request.data.get('Password'),
            'Section': request.data.get('Section'),
            'Role': request.data.get('Role')
        }
        
        serializer = UserAccountsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAccountsDetailsApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, Id):
        try:
            return UserAccounts.objects.using("web_template").get(id = Id)
        except UserAccounts.DoesNotExist:
            return None

    def get(self, request, Id, *args, **kwargs):
        user_account_instance = self.get_object(Id)
        if not user_account_instance:
            return Response(
                {"res": "Object with Id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserAccountsSerializer(user_account_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, Id, *args, **kwargs):
        user_account_instance = self.get_object(Id)

        if not user_account_instance:
            return Response(
                {"res": "Object with Id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'IdNumber': request.data.get('IdNumber'),
            'FullName': request.data.get('FullName'),
            'Username': request.data.get('Username'),
            'Password': request.data.get('Password'),
            'Section': request.data.get('Section'),
            'Role': request.data.get('Role')
        }

        serializer = UserAccountsSerializer(instance = user_account_instance, data=data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, Id, *args, **kwargs):
        user_account_instance = self.get_object(Id)
        
        if not user_account_instance:
            return Response(
                {"res": "Object with Id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_account_instance.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )