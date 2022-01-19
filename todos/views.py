from todos.models import Todo
from rest_framework import filters
from django.shortcuts import render
from todos.serializers import TodoSerializer
from todos.pagination import CustomNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class TodosAPIView(ListCreateAPIView):
    #data has to be serialized.
    #When a call, from postman, is sent to our server JSON data will be sent.
    #That data has to be turned into a model object and saved in the database. 
    #The serializer can be in between our views and database to ensure that
    #the data formats can be understood by different clients and our server.
    serializer_class= TodoSerializer
    pagination_class= CustomNumberPagination
    permission_classes= (IsAuthenticated,)
    filter_backends= [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    #the user can be able to filter by these fields
    filterset_fields= ['id','title','description','is_complete']
    
    #the user can be able to search by these fields
    search_fields= ['id','title','description']

    #the user can be able to order todos by these fields
    search_fields= ['id','title','is_complete']

    #this sets the owner of the todo to the person who is currently logged in
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    #when an authentication systems is in place, override the get query
    #set method to construct objects that get sent back to the current
    #logged in user.
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class= TodoSerializer
    permission_classes= (IsAuthenticated,)
    lookup_field= "id"
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
