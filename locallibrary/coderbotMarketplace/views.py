from django.http import HttpResponse
from django.shortcuts import render
from coderbotMarketplace.models import package_db

# Create your views here.
def index(request):
    res = package_db.objects.all()
    context = {"packages": res}
    
    return render(request, "index.html",context)