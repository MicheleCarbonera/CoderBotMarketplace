from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from coderbotMarketplace.models import package_db, package_category, package_version, users

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from coderbotMarketplace.forms import SearchForm,SignInForm,SignUpForm,LogoutForm



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
    else:
        pack_info = None
    pack_selected_category = package_category.objects.filter(id=pack_sel.Category)[:1].get()
    context_data = {"pack_selected":pack_sel,"pack_info":pack_info,"pack_selected_category":pack_selected_category}
    print(request.session["user"])
    return render(request, "package.html",context_data)


def login(request):
    code = 0
    error_string = None
    ok_string = None
    if request.method == 'POST':
        formIn = SignInForm(request.POST)
        code = 1
        if formIn.is_valid():            
            
            user_email = request.POST.get('user_email')
            user_password = request.POST.get('user_password')

            get_from_email = users.objects.filter(email=user_email)

            if get_from_email.count() >0:
                get_from_email_password = users.objects.filter(email=user_email).filter(password=user_password)
                if get_from_email_password.count()==1:
                    code = 4
                    request.session["user"] = user_email
                    # request.session.set_expiry(10)
                    
                    ok_string = "Accesso avvenuto con successo, clicca qui"
                else:
                    error_string = "email o password non corretta in fase login"
                    #password
            else:
                error_string = "email o password non corretta in fase login"
                #email
    if request.method == 'POST':
        formIn_1 = SignUpForm(request.POST)
        code = 1
        if formIn_1.is_valid():
            user_email = request.POST.get('user_email')
            user_password = request.POST.get('user_password')
            #registrazione
            user_email_1 = request.POST.get('user_email_1')
            user_password_1 = request.POST.get('user_password_1')
            if user_email_1 == user_email:
                if user_password_1 == user_password:
                    user_name = request.POST.get('user_name')
                    user_surname = request.POST.get('user_surname')
                    get_from_email = users.objects.filter(email=user_email)
                    if get_from_email.count() >0:
                         error_string = "email gia esistente in registrazione"
                    else:
                        users.objects.create(email=user_email,password=user_password,name=user_name,surname=user_surname)
                        ok_string = "Registrazione avvenuta con successo, clicca qui"
                        request.session["user"] = user_email
                else:
                    error_string = "password differenti in registrazione"
            else:
                error_string = "email differenti in registrazione"
    if request.method == 'POST':
        formIn_out = LogoutForm(request.POST)
        if formIn_out.is_valid():
            request.session["user"] = None
            ok_string = "Logout effetuato. A presto!"
    context_data = {"status":error_string,"ok_status":ok_string}        
    return render(request, "login.html",context_data)

def profile(request):    
    return render(request, "profile.html")
