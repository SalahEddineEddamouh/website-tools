from django.urls import path

from . import views


urlpatterns = [
    path("",views.home,name='home'),
    path("about-us",views.about,name='about-us'),
    path("privacy-policy",views.privacy,name='privacy'),
    path("terms-and-conditions",views.conditions,name='conditions'),
    path("contact-us",views.contact,name='contact'),
    path("downloader",views.downloader,name='downloader'),
    path("download",views.download,name='download'),
    path("articles",views.articles,name='articles'),
    path("article/<slug:slug>",views.article,name='article'),

]
