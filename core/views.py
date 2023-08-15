from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from django.contrib.auth.models import User
from .forms import CommentForm

def homepage(request):
    context = {}
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    shorts_list = Short.objects.all()
    context["shorts"] = shorts_list
    return render(request, 'home.html', context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context["post"] = post_object
    comment_form = CommentForm()
    context['comment_form'] = comment_form
    comment_list = Comment.objects.filter(post=post_object)
    context['comments'] = comment_list
    if request.method == "GET":
        return render(request, "post_info.html", context)
    elif request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.post = post_object
            new_comment.save()
            return HttpResponse("done")

def Contacts(request):
    return HttpResponse('Наши контакты')


def about_us(request):
    return HttpResponse('Информация о нас')


def profile_detail(request, id):
    context = {}
    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'profile_detail.html', context)


def shorts(request):
    context = Short.objects.all()
    return render(request, 'shorts.html', {'context': context})
    # def shorts(request):
    # context = {'short-list': Short.objects.all()}
    # return render(request,'shorts.html', context)


# def short_video(request):
#     short_video_object = Short.objects.all()
#     return render(request, 'short_video.html', {'short_video_object': short_video_object})


def shorts_info(request, id):
    # context = Short.objects.get(id=id)
    # return render(request, 'short_info.html', {'context': context})
    context = {}
    short_object = Short.objects.get(id=id)
    context["short"] = short_object
    return render(request, "short_info.html", context)

def saved_posts(request):
    posts = Post.objects.filter(saved_posts__user=request.user)
    context = {'posts': posts}
    return render(request, 'savedposts.html', context)

def user_posts(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(creator=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'user_posts.html', context)

def create_post(request):
    if request.method == "GET":
        return render(request, 'create_post_form.html')
    elif request.method == "POST":
        data = request.POST # словарь с данными с html-формы
        #print(data)
        new_post = Post()
        new_post.name = data['post_name']
        new_post.photo = request.FILES['photo']
        new_post.description = data['description']
        new_post.creator = request.user
        new_post.save()
        return HttpResponse('done')
# from django.contrib.auth.decorators import login_required
@login_required(login_url='/users/sign-in/')
def add_short(request):
    # if not request.user.is_authenticated:
    #     return redirect('/')
    if request.method == "GET":
        return render(request, 'short_form.html')
    elif request.method == "POST":
        new_short_object = Short(user=request.user, video=request.FILES["video_file"])
        new_short_object.save()
        return redirect('shorts-info', id=new_short_object.id)



def add_saved(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post, created = SavedPosts.objects.get_or_create(user=request.user)
        saved_post.post.add(post_object)
        saved_post.save()
        return redirect('/saved_posts/')
def remove_saved(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post = SavedPosts.objects.get(user=request.user)
        saved_post.post.remove(post_object)
        saved_post.save()
        return redirect('/saved_posts/')

def search(request):
    return render(request, 'search.html')

def search_result(request):
    key_word = request.GET["key_word"]
   # posts = Post.objects.filter(name_icontains=key_word)
    posts = Post.objects.filter(
        Q(name_icontains=key_word) |
        Q(description_icontains=key_word)
    )
    context = {'post': posts}
    return render(request, 'home.html', context)

def add_subscriber(request, profile_id):
        profile = Profile.objects.get(id=profile_id)
        profile.subscribers.add(request.user)
        profile.save()
        messages.success(request, "Вы успешно подписались!")
        return redirect(f'/profile/{profile.id}')

def remove_follow(request, profile_id):
        profile = Profile.objects.get(id=profile_id)
        profile.subscribers.remove(profile_id)
        profile.save()
        messages.success(request, "Вы успешно отписались!")
        return redirect(f'/profile/{profile.id}')