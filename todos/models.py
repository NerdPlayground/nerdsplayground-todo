from tkinter import CASCADE
from django.db import models
from authentication.models import User
from helpers.models import TrackingModel

#model classes should be a singular version of what they represent
#Todos ===> todo, Products ===> product
class Todo(TrackingModel):
    title= models.CharField(max_length=255)
    description= models.TextField()
    is_complete= models.BooleanField(default=False)
    #For foreign keys, specify the model the todo is attached to
    #on_delete property handles the operations on the todo
    #when the user is deleted. CASCADE ===> Deletes along with
    owner= models.ForeignKey(to=User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title