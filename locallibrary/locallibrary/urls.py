from django.urls import path
from django.conf.urls.static import static

from coderbotMarketplace import views
from locallibrary import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('package/<str:pk>', views.package, name='package'),
    path('login/', views.login, name='login'),
    path('profile', views.profile, name='profile')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

