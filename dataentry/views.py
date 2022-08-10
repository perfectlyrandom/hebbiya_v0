from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import DataForm, QueryForm
from .globals import *

def index(request):
	if request.method == "POST":
		form = DataForm(request.POST, request.FILES)
		
		if form.is_valid():
			form.parse_and_store(request)
			form.save()
			return redirect("/index")  
	else:
		form = DataForm()
	return render(request, "new.html", {"form": form})

def query(request):
	if request.method == "POST":
		form = QueryForm(request.POST)
		
		if form.is_valid():
			form.generate_results()
			form.save()
			return redirect("/index")  
	else:
		form = QueryForm()
	return render(request, "query.html", {"form": form})	
