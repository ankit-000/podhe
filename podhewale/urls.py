from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path(settings.SECRET_ADMIN_URL +'/admin/', admin.site.urls),
	    path('',include('home.urls')),
	    path('customer/',include('customer.urls')),
	    path('vendor/',include('vendor.urls',namespace="vendor")),
	    path('product/',include('product.urls')),
	] 

if settings.DEBUG:
	urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
