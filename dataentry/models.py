from django.db import models

# Create your models here.

class Data(models.Model):
    
	body = models.CharField(max_length=10000,blank=True)
	document = models.FileField(upload_to='documents/', blank=True)

	def __str__(self):
		return self.body

class Query(models.Model):
    
	query = models.CharField(max_length=10000,blank=True)

	def __str__(self):
		return self.query

