from django.shortcuts import render
from userapi.serializers import *
from rest_framework.views import APIView
from rest_framework import status
from userapi.models import *
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.


class UserRegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        user_serialzer = UserRegisterSerializer(data = request.data)

        if user_serialzer.is_valid():

            user=user_serialzer.save()

            return Response(user_serialzer.data,status=status.HTTP_201_CREATED)
        
        return Response(user_serialzer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    authentication_classes = [BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self,request):

        user = request.user

        token,created = Token.objects.get_or_create(user=user)

        return Response({"message":"login success","token":token.key},status=status.HTTP_200_OK)

        # print(user.username)
        
        # print(request.user)

        return Response({"message":"login success"})


class ProductAddListView(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes =[IsAuthenticated]

    def post(self,request):

        serializer = ProductSerializer(data = request.data)

        if serializer.is_valid():

            serializer.save(user = request.user)

            return  Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


 #list all the product of logined user
 #basic authentication

    def get(self,request):

        data = Productmodel.objects.filter(user= request.user)

        serializer = ProductSerializer(data,many = True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    

class ProductRetriveUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get (self,request,**kwargs):

        id = kwargs.get('pk')

        product = get_object_or_404(Productmodel,id=id,user = request.user)

        serializer = ProductSerializer(product,many = False)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,**kwargs):

        id = kwargs.get('pk')

        product = get_object_or_404(Productmodel,id=id,user = request.user)

        serializer = ProductSerializer(product,data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,**kwargs):

        id = kwargs.get('pk')

        product = get_object_or_404(Productmodel,id=id)

        product.delete()

        return Response({"message :Product Deleted Successfully"},status=status.HTTP_200_OK)


class Productfilterbycolor(APIView):

    permission_classes =[IsAuthenticated]

    authentication_classes =[TokenAuthentication]

    def get(self,request):

        color = request.query_params.get('color')

        product = Productmodel.objects.filter(user= request.user)

        data  = product.filter(product_color__icontains = color)

        serializer = ProductSerializer(data, many = True)

        return Response(serializer.data,status=status.HTTP_200_OK)




    
    
    
    




