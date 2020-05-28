from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from coderbotMarketplace.models import package_db

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from coderbotMarketplace.forms import SearchForm



# Create your views here.
def index(request):
    res = package_db.objects.all()
    context = {"packages": res}

    return render(request, "index.html",context)

def search(request):
    if request.method == 'POST':
        formIn = SearchForm(request.POST)
        if formIn.is_valid():            
            ouy = request.POST.get('name_field')
    else:
        ouy = request.GET.get('name_field')
    
    if ouy is None:
        packs = package_db.objects.all()
    else:
        packs = package_db.objects.filter(NamePackage__contains=ouy)
    print(ouy)
    context_data = {'form': ouy, "packs": packs}
    return render(request, "search.html",context_data)
