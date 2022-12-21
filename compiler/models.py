from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name








class Projet(models.Model):
  
   name = models.CharField(max_length=100 )
   user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
   date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 
   

   def __str__(self):
		  return self.name 

class SaveFiles(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.SET)
    code = models.TextField(max_length=10000000, blank=False)

    user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(Customer, related_name="all_groups")
  
    def __str__(self):
        return self.code

class Collaboration(models.Model):
    creater = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    members =  models.ForeignKey(Customer, on_delete=models.SET, null=True, blank=True)
    project=models.ForeignKey(Projet, on_delete=models.SET)
    Accepter = models.BooleanField(default=False)


