from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from coderbotMarketplace.models import package_db, package_category, package_version

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
    category_list = package_category.objects.all()
    if request.method == 'POST':
        formIn = SearchForm(request.POST)
        if formIn.is_valid():            
            words_search = request.POST.get('name_field')
    else:
        words_search = request.GET.get('name_field')
        category_search = request.GET.get('category_field')
    if (words_search is None)or(words_search==''):
        if (category_search is None)or(category_search =='')or(category_search =='0'):
            category_search = "0"
            packs = package_db.objects.all()
        else:
            packs = package_db.objects.filter(Category=category_search)
    else:
        if (category_search is None)or(category_search =='')or(category_search =='0'):
            category_search = "0"
            packs = package_db.objects.filter(NamePackage__contains=words_search)
        else:
            packs = package_db.objects.filter(NamePackage__contains=words_search).filter(Category=category_search)

    context_data = {'form': words_search,"preselect_cat": int(category_search), "packs": packs, "categories_list":category_list}
    return render(request, "search.html",context_data)

def package(request,pk):
    pack_sel = package_db.objects.filter(NamePackage=pk)[:1].get()
    

    pack_info = package_version.objects.filter(id_package=pack_sel.id).order_by('-timeupload')
    if pack_info.count()>0:
        pack_info = package_version.objects.filter(id_package=pack_sel.id).order_by('-timeupload')[:1].get()
        pack_selected_category = package_category.objects.filter(id=pack_sel.Category)[:1].get()
    else:
        pack_info = None
    context_data = {"pack_selected":pack_sel,"pack_info":pack_info,"pack_selected_category":pack_selected_category}
    return render(request, "package.html",context_data)