from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django_filters.views import FilterView
from django.views import View
from django.views.generic import ListView
import requests
from .filters import *
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
        if "like" in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(user=post_object.creator, text=f"{request.user.username} лайкнул ваш пост с id {post_object.id}")
            return redirect(post_detail, id=id)
        elif "dislike" in request.POST:
            post_object.likes -= 1
            post_object.save()
            return redirect(post_detail, id=id)

        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()
                Notification.objects.create(user=post_object.creator, text=f'{request.user.username} оставил комментарий')
                return HttpResponse("done")

def Contacts(request):
    return HttpResponse('Наши контакты')


def about_us(request):
    return HttpResponse('Информация о нас')
class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'post_list_cbv.html'


def profile_detail(request, id):
    context = {}
    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'profile_detail.html', context)

def posts(request):
    posts_filter = PostFilter(
        request.GET,
        queryset=Post.objects.all()
    )
    context = {'posts_filter': posts_filter}
    return render(request, "posts_filter.html", context)

class PostsFilterView(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'posts_filter.html'




def add_profile(request):
    profile_form = ProfileForm()
    context = {'profile_form': profile_form}
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            return redirect(profile_detail, id=profile_object.id)
        else:
            return HttpResponse("Not valid")
    return render(request, 'add_profile.html', context)

def shorts(request):
    short_filter = ShortFilter(request.GET, queryset=Short.objects.all())
    context = {'short_filter': short_filter}
    return render(request, 'shorts.html', context)

class ShortsFilterView(FilterView):
    model = Short
    filterset_class = ShortFilter
    template_name = 'short_filter.html'

def short_info(request, id):
    context = {}
    short_object = Short.objects.get(id=id)
    short_object.views_qty += 1
    short_object.save()
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

def update_post(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    if request.method == "POST":
        post_form = PostForm(data=request.POST, files=request.FILES, instance=post_object)
        if post_form.is_valid():
            post_form.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, "Форма не валидна")
            return render(request, 'update_post.html', context)
    post_form = PostForm(instance=post_object)
    context['post_form'] = post_form
    return render(request, 'update_post.html', context)

def update_short(request, id):
        short = Short.objects.get(id=id)
        if request.method == "POST":
            new_description = request.POST['description']
            short.description = new_description
            short.save()
            return redirect(short_info, id=short.id)
        context = {'short': short}
        return render(request, 'update_short.html', context)

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

class SearchView(View):
    def get(self, request):
        return render(request, 'search.html')

def search_result(request):
    key_word = request.GET["key_word"]
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
        new_notification = Notification(user=profile.user, text=f'Пользователь {request.user.username} подписался на вас')
        new_notification.save()
        return redirect(f'/profile/{profile.id}')

def remove_follow(request, profile_id):
        profile = Profile.objects.get(id=profile_id)
        profile.subscribers.remove(profile_id)
        profile.save()
        messages.success(request, "Вы успешно отписались!")
        return redirect(f'/profile/{profile.id}')

def notifications(request):
    notifications_list = Notification.objects.filter(user=request.user)
    for notification in notifications_list:
        notification.is_showed = True
    Notification.objects.bulk_update(notifications_list, ['is_showed'])
    context = {"notifications": notifications_list}
    return render(request=request, template_name='notifications.html', context=context)

def add_post_form(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.creator = request.user
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, f'Форма нн валидна: {post_form.errors}')
    post_form = PostForm()
    context = {}
    context['post_form'] = post_form
    return render(request, 'create_post_django_form.html', context)

class PostDetailView(View):
    def get_context(self):
        id = self.kwargs['id']
        context = {}
        post_object = Post.objects.get(id=id)
        context["post"] = post_object
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        comment_list = Comment.objects.filter(post=post_object)
        context['comments'] = comment_list
        return context
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, 'post_info.html', context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        context = {}
        post_object = Post.objects.get(id=id)
        context["post"] = post_object
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        comment_list = Comment.objects.filter(post=post_object)
        context['comments'] = comment_list
        if "like" in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(user=post_object.creator,
                                        text=f"{request.user.username} лайкнул ваш пост с id {post_object.id}")
            return redirect('post-detail-cbv', id=id)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()
                Notification.objects.create(user=post_object.creator, text=f'{request.user.username} оставил комментарий')
                return HttpResponse("done")

class SubscribesView(View):
    def get(self, request, *args, **kwargs):
        user_object = User.objects.get(id=kwargs['user_id'])
        profiles_list = user_object.followed_profile.all()
        context = {'profiles_list': profiles_list}
        return render(request, 'subscribers.html', context)

class NotificationListView(View):
    def get(self, request):
        notifications_list = Notification.objects.filter(user=request.user)
        for notification in notifications_list:
            notification.is_showed = True
        Notification.objects.bulk_update(notifications_list, ['is_showed'])
        context = {"notifications-cbv": notifications_list}
        return render(request=request, template_name='notifications.html', context=context)

class SearchResultView(View):
    def get(self, request):
        key_word = request.GET["key_word"]
        posts = Post.objects.filter(
            Q(name_icontains=key_word) |
            Q(description_icontains=key_word)
        )
        context = {'post': posts}
        return render(request, 'home.html', context)

class ShortsListView(ListView):
    queryset = Short.objects.all()
    template_name = 'core/short_list_cbv.html'

class ShortInfoView(View):
    def get(self, request, id, *args, **kwargs):
        id = self.kwargs['id']
        short = Short.objects.get(id=id)
        short.views_qty += 1
        short.viewed_users.add(request.user)
        short.save()
        context = {"short": short}
        return render(request, 'short_info.html', context)

    def create_short(request):
        if request.method == "GET":
            return render(request, "short_form.html")
        elif request.method == "POST":
            new_short = Short(
                user=request.user,
                video=request.FILES["video_file"]
            )
            new_short.save()
            return redirect('shorts-info-cbv', id=new_short.id)

    def add_saved(request):
        if request.method == 'POST':
            post_id = request.POST['post_id']
            post_object = Post.objects.get(id=post_id)
            saved_post, created = SavedPosts.objects.get_or_create(
                    user=request.user)
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

class PostsFromAPI(View):
    def get(self, request):
        context = {}
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        data = response.json()
        context['posts'] = data
        return render(request, 'core/posts_from_api.html', context)

class PostDetailFromApi(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{id}')
        post_data = response.json()
        return render(request, 'core/post_detail.html', {'post': post_data})

class TodosFromAPI(View):
    def get(self,request):
        context = {}
        response = requests.get('https://jsonplaceholder.typicode.com/todos')
        data = response.json()
        context['todos'] = data
        return render(request, 'core/todos_from_api.html', context)

class TodosDetailFromApi(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        response = requests.get(f'https://jsonplaceholder.typicode.com/todos/{id}')
        todo_data = response.json()
        return render(request, 'core/todo_from_api.html', {'todo': todo_data})
