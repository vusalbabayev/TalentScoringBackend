from django.contrib import admin
from django.urls import path, include
from talent_score.yasg import urlpatterns as doc_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]

urlpatterns += doc_urls