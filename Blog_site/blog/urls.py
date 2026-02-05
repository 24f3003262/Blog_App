from django.urls import path
from . import views
from .feeds import LatestPostsFeed
app_name = 'blog'
urlpatterns = [
    # Auth URLs
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('setup/', views.setup_superuser, name='setup'),
    
    # Blog URLs
    path('blog/', views.post_list, name='post_list'),
    path('blog/create/', views.post_create, name='post_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share,name='post_share'),
    path('<int:post_id>/comment/',views.post_comment,name='post_comment'),
    path('tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
    path('feed/',LatestPostsFeed(),name='post_feed'),
    path('search/',views.post_search,name='post_search'),
]
