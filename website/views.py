from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pytube import YouTube
import os
from wsgiref.util import FileWrapper
from .models import Article

def downloader(request):
    if request.method == 'POST':
        video_url = request.POST.get('url')

        try:
            yt = YouTube(video_url)
            video_title = yt.title
            stream = yt.streams.get_highest_resolution()
            download_url = stream.url
            thumbnail_url = yt.thumbnail_url

            context = {
                'video_title': video_title,
                'download_url': download_url,
                'thumbnail_url': thumbnail_url,
                'video_url':video_url,
            }

            return render(request, 'pages/result.html', context)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render(request, 'pages/home.html', {'error_message': error_message})

    return render(request, 'pages/home.html')




def download(request):
    if request.method == "POST":
        url = request.POST.get('url')
        itag = request.POST.get('itag')

        yt = YouTube(url).streams.get_by_itag(itag)
        title = yt.title

        homedir = os.path.expanduser("~")
        dirs = os.path.join(homedir, 'Downloads')

        if yt.type != 'audio':
            file_path = os.path.join(dirs, f"{title}.mp4")
            yt.download(output_path=dirs, filename=f"{title}.mp4")
            file = FileWrapper(open(file_path, 'rb'))

            response = HttpResponse(file, content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{title}.mp4"'

            os.remove(file_path)  # Remove the file after serving
            return response

        else:
            file_path = os.path.join(dirs, f"{title}.mp3")
            yt.download(output_path=dirs, filename=f"{title}.mp3")
            file = FileWrapper(open(file_path, 'rb'))

            response = HttpResponse(file, content_type='audio/mp3')
            response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'

            os.remove(file_path)  # Remove the file after serving
            return response

    return render(request, 'pages/home.html')


def home(request):
    return render(request,"pages/home.html")

def about(request):
    return render(request,"pages/about.html")

def privacy(request):
    return render(request,"pages/privacy.html")

def conditions(request):
    return render(request,"pages/conditions.html")

def contact(request):
    return render(request,"pages/contact.html")

def articles(request):
    all_posts = Article.objects.all()

    paginator = Paginator(all_posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'articles': page_obj,
    }
    return render(request,"pages/articles.html",context)

def article(request,slug):
    post = get_object_or_404(Article, slug=slug)
    context = {
        'article': post,
    }
    return render(request,"pages/article.html",context)
