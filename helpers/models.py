from django.db import models

class TrackingModel(models.Model):
    #record current time upon object creation
    created_at= models.DateTimeField(auto_now_add=True)
    #record current time upon object update
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        #prevents obect creation
        abstract= True
        #With (-) the obejcts are ordered with descending order
        ordering= ('-created_at',)