from django.shortcuts import render,get_object_or_404, redirect
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm, SearchForm, UserRegistrationForm, UserLoginForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def setup_superuser(request):
    """Setup page to create initial superuser if none exists"""
    if User.objects.filter(is_superuser=True).exists():
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if username and email and password and len(password) >= 6:
            try:
                User.objects.create_superuser(username, email, password)
                messages.success(request, 'Superuser created! You can now login.')
                return redirect('/admin/login/')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Please fill all fields. Password must be at least 6 characters.')
    
    return render(request, 'blog/setup.html')


def post_list(request,tag_slug=None):
    post_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    #pagination with 3 post per page
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page',1)
    try:
        posts=paginator.page(page_number)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts,'tag':tag})

def post_detail(request,year,month,day,post):
    try:
        post=Post.published.get(slug=post,publish__year=year,publish__month=month,publish__day=day)
        comments=post.comments.filter(active=True)
        form=CommentForm()
        post_tags_ids=post.tags.values_list('id',flat=True)
        similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(request,'blog/post/detail.html',{'post':post,'comments':comments,'form':form,'similar_posts':similar_posts})


# class PostListView(ListView):
#     queryset=Post.published.all()
#     context_object_name='posts'
#     paginate_by=3
#     template_name='blog/post/list.html'

def post_share(request,post_id):
    #retrieve post by id
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent=False
    if request.method=='POST':
        #Form was submitted
        form=EmailPostForm(request.POST)
        if form.is_valid():
            #form fields pass validation
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url)
            subject=(f"{cd['name']} {cd['email']}"
                     f"recommends you read {post.title}")
            message=(f"Read {post.title} at {post_url}\n\n"
                     f"{cd['name']}\'s comments: {cd['comments']}")

            send_mail(subject=subject,message=message,from_email=None,recipient_list=[cd['to']])
            sent=True        
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

@require_POST
def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment=None
    form = CommentForm(data=request.POST)
    if form.is_valid():
 # Assign the post to the comment
        comment=form.save(commit=False)
        comment.post = post
 # Save the comment to the database
        comment.save()
    return render(request,'blog/post/comment.html',
            {'post'
            : post,
            'form'
            : form,
            'comment'
            : comment
                    })


def post_search(request):
    form=SearchForm()
    query=None
    results=[]
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results=(
                Post.published.annotate(
                    similarity=TrigramSimilarity('title',query)
                )
                .filter(similarity__gt=0.1).order_by('-similarity')
            )
    return render(request,'blog/post/search.html',{
        'form':form,
        'query':query,
        'results':results
    })


def homepage(request):
    """Homepage with welcome message and blog overview"""
    total_posts = Post.published.count()
    recent_posts = Post.published.all()[:5]
    context = {
        'total_posts': total_posts,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/homepage.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the blog.')
            return redirect('blog:post_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('blog:post_list')
    else:
        form = UserLoginForm()
    
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('blog:homepage')


@login_required(login_url='blog:login')
def user_profile(request):
    """User profile page"""
    return render(request, 'blog/profile.html', {'user': request.user})