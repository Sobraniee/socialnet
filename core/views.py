from django.shortcuts import render, HttpResponse
from .models import Post, Profile, Short, Category
def homepage(request):
    context = {}
    context["name"] = "Davlyat"
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    return render(request, 'home.html', context)

def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context["post"] = post_object
    return render(request, "post_info.html", context)

def Contacts(request):
    return HttpResponse('Наши контакты')
def about_us(request):
    return HttpResponse('Информация о нас')

def profile_detail(request, id):
    context = {}
    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'profile_detail.html', context)

def short_video(request):
    short_video = Short.objects.all()
    return render(request, 'short.html', {'short_video':short_video})

def Category(request):
    context = {}
    context['category'] = Category.object.get()
    return render(request, 'category.html', context)

