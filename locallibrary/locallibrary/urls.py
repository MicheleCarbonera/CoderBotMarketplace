from django.urls import path
from django.conf.urls.static import static

from coderbotMarketplace import views
from locallibrary import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('product', views.index, name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

