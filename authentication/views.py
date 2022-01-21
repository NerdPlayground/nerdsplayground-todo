from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework import response,status, permissions
from authentication import serializers
import authentication
from authentication.serializers import RegisterSerializer, LoginSerializer




#utilization of class based views; program inherits a lot of functionality that is available in django
#inheriting GenericAPIView enables us to test all the http requests the user makes, individually
class RegisterAPIView(GenericAPIView):
    #this overrides the jwt authentication setting
    #the empty list ensures that the user has access
    #to this view without authentication
    authentication_classes= []

    #when it's a class based view, a serializer class is set up
    serializer_class= RegisterSerializer

    #user submits form on the front end and the data is sent to the server
    def post(self,request):
        #serializer transforms json data that the user sends to python objects and vice versa
        serializer= self.serializer_class(data=request.data)

        #the serializer performs the validations based on the rules set on the data
        if serializer.is_valid():
            serializer.save()
            #informs user that their account has been created and can be accessed
            #HTTP 201 CREATED response is sent when a resource i created on a server
            return response.Response(serializer.data,status=status.HTTP_201_CREATED,)
        
        #if the request the user sent had issues
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(GenericAPIView):
    #this overrides the jwt authentication setting
    #the empty list ensures that the user has access
    #to this view without authentication
    authentication_classes= []
    serializer_class= LoginSerializer

    def post(self,request):
        email= request.data.get('email',None)
        password= request.data.get('password',None)

        user= authenticate(username=email,password=password)
        if user:
            serializer= self.serializer_class(user)
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        return response.Response({'message':'Inavlid Credentials'},status=status.HTTP_401_UNAUTHORIZED)

class AuthUserAPIView(GenericAPIView):
    #the user should have a token to access this view
    permission_classes= (permissions.IsAuthenticated,)
    serializer_class= RegisterSerializer

    def get(self,request):
        user= request.user
        serializer= RegisterSerializer(user)
        return response.Response({'user':serializer.data})
