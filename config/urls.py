from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    path('ckeditor5/',include('django_ckeditor_5.urls'))
]

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404