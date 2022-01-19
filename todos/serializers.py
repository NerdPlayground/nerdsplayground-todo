from dataclasses import field
from todos.models import Todo
from rest_framework.serializers import ModelSerializer

#This serializer will create, read and update the model
class TodoSerializer(ModelSerializer):

    #Defines other information the serializer should know about
    class Meta:
        model= Todo
        #The fields to be serialized
        fields= ('id','title','description','is_complete',)
