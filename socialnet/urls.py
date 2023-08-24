"""
URL configuration for socialnet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('posts/<int:id>/', post_detail, name='post-detail'),
    path('post-cbv/<int:id>/', PostDetailView.as_view(), name='post-detail-cbv'),
    path('posts-list-cbv/', PostListView.as_view(), name='profile'),
    path('post-filter', PostsFilterView.as_view(), name='post-filter'),
    path('contacts/', Contacts),
    path('about_us/', about_us),
    path('profile/<int:id>/', profile_detail, name='profile'),
    path('add-profile', add_profile, name='add-profile'),
    path('shorts/', shorts, name='shorts-list'),
    path('shorts-cbv/', ShortsListView.as_view(), name='shorts-list-cbv'),
    path('short-filter/', ShortsFilterView.as_view(), name='short-filter'),
    path('short-cbv/<int:id>', ShortInfoView.as_view(), name='shorts-info-cbv'),
    path('short/<int:id>/', short_info, name='short-info'),
    path('saved_posts/', saved_posts, name='saved-posts'),
    path('update-short/<int:id>/', update_short, name='update-short'),
    path('<int:user_id>/', user_posts, name='user-posts'),
    path('add-post/', create_post, name='add-post'),
    path('add-post-form/', add_post_form, name='add-post-form'),
    path('add-short/', add_short, name='add-short'),
    path('add-saved/', add_saved, name='add-saved'),
    path('remove-saved/', remove_saved, name='remove-saved'),
    path('search/', search, name='search'),
    path('search-cbv', SearchView.as_view(), name='search'),
    path('search-result/', search_result, name='search-result'),
    path('search-result-cbv/', SearchResultView.as_view, name='search-result'),
    path('users/', include('userapp.urls')),
    path('add-subscriber/<int:profile_id>', add_subscriber, name='add_subscriber'),
    path('remove-follow/<int:profile_id>', remove_follow, name='remove_follow'),
    path('notifications/', notifications, name='notifications'),
    path('subscriber/<int:user_id>/', SubscribesView.as_view(), name='subscribes'),
    path('notification-cbv/', NotificationListView.as_view(), name='notification-cbv'),
    path('posts-api/', PostsFromAPI.as_view(), name='posts-api'),
    path('posts-api/<int:id>/', PostDetailFromApi.as_view(), name='post-api'),
    path('todos-api/', TodosFromAPI.as_view(), name='todos-api'),
    path('todos-api/<int:id>/', TodosDetailFromApi.as_view(), name='todo-api')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
