from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from coderbotMarketplace.models import package_db, package_category, package_version, users, users_saved_package, carousel_home_slider, users_download_package, package_collection, package_collection_join

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from coderbotMarketplace.forms import SearchForm,SignInForm,SignUpForm,LogoutForm,PreferenceForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.db.models import F



# Create your views here.
def index(request):
    res = package_db.objects.all().order_by('-downloadcount')
    caros = carousel_home_slider.objects.filter(visible=1)
    carousel_help = list()
    for i in range(caros.count()):
        carousel_help.append(str(i))
    context = {"packages": res[:6], "carousel_list":caros, "carousel_help":carousel_help }

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
    try: 
        email = request.session["user"]

        if request.method == 'POST':
            formIn = PreferenceForm(request.POST)
            _likes = users_saved_package.objects.filter(email_user=email).filter(pack_id_id=pack_sel.id)
            if formIn.is_valid(): 
                if _likes.count()==0:
                    users_saved_package.objects.create(pack_id_id=pack_sel.id,email_user=email)
                else:   
                    users_saved_package.objects.filter(pack_id_id=pack_sel.id,email_user=email).delete()        
        likes = users_saved_package.objects.filter(email_user=email).filter(pack_id_id=pack_sel.id)
        if likes.count()==0:
            like=0
        else:
            like=1
    except:
        like = None
    pack_info = package_version.objects.filter(id_package=pack_sel.id).order_by('-timeupload')
    if pack_info.count()>0:
        pack_info = package_version.objects.filter(id_package=pack_sel.id).order_by('-timeupload')[:1].get()
    else:
        pack_info = None
    pack_selected_category = package_category.objects.filter(id=pack_sel.Category)[:1].get()
    collection_pack = package_collection_join.objects.filter(package_id=pack_sel.id)
    context_data = {"pack_selected":pack_sel,"pack_info":pack_info,"pack_selected_category":pack_selected_category,"like":like,"collection_pack":collection_pack}
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
                        try:
                            validate_email(user_email)
                            users.objects.create(email=user_email,password=user_password,name=user_name,surname=user_surname)
                            ok_string = "Registrazione avvenuta con successo, clicca qui"
                            request.session["user"] = user_email
                        except ValidationError as e:
                            error_string = "formato email non valido"
                else:
                    error_string = "password differenti in registrazione"
            else:
                error_string = "email differenti in registrazione"
    if request.method == 'POST':
        formIn_out = LogoutForm(request.POST)
        if formIn_out.is_valid():    
            request.session["user"] = None
            del request.session["user"]
            ok_string = "Logout effetuato. A presto!"
    context_data = {"status":error_string,"ok_status":ok_string}        
    return render(request, "login.html",context_data)

def profile(request):   
    try:  
        print("a")
        email = request.session["user"]
        print("b")
        context_data = None
        print(email)
        if email is not None:
            saved_packs = users_saved_package.objects.filter(email_user=email)
            downloaded_packs= users_download_package.objects.filter(email_user=email)
            context_data = {"saved_packs":saved_packs,"downloaded_packs":downloaded_packs}

    except:
        context_data = {"saved_packs":None}
    return render(request, "profile.html",context_data)

def download_package(request, package,version):
    pks = package_db.objects.filter(NamePackage=package)
    if pks.count() == 1:
        packs = package_db.objects.filter(NamePackage=package)[:1].get()
        pack_info = package_version.objects.filter(id_package=packs.id).filter(version=version).update(downloadcount = F('downloadcount')+1)
        pack_info = package_db.objects.filter(NamePackage=package).update(downloadcount = F('downloadcount')+1)
        try: 
            email = request.session["user"]        
            pack_dwn_up = users_download_package.objects.filter(pack_id_id=packs.id).filter(email_user=email).update(version_id = version)
            if pack_dwn_up == 0:
                users_download_package.objects.create(pack_id_id=int(packs.id),email_user=email,version_id = version)
        except:
            a = 0
    return render(request, "profile.html")

def collection(request, nameCollection):
    collectionCheck = package_collection.objects.filter(NameCollection=nameCollection)
    context_data = {}
    if (collectionCheck.count() == 1):
        collection = package_collection.objects.filter(NameCollection=nameCollection)[:1].get()
        packages = package_collection_join.objects.filter(collection_id = collection.id)
        context_data = {"collection":collection, "packages":packages}
    return render(request, "collection.html",context_data)

def collections(request):
    collections = package_collection.objects.all()
    context_data = {"collections":collections}
    return render(request, "collections.html",context_data)
