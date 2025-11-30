from django.shortcuts import render,get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .views import EmailPostForm
# Create your views here.
# def post_list(request):
#     post_list=Post.published.all()
#     #pagination with 3 post per page
#     paginator=Paginator(post_list,3)
#     page_number=request.GET.get('page',1)
#     try:
#         posts=paginator.page(page_number)
#     except PageNotAnInteger:
#         posts=paginator.page(1)
#     except EmptyPage:
#         posts=paginator.page(paginator.num_pages)
#     return render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    try:
        post=Post.published.get(slug=post,publish__year=year,publish__month=month,publish__day=day)
    except Post.DoesNotExist:
        raise Http404("No Post found")
    return render(request,'blog/post/detail.html',{'post':post})


class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'

def post_share(request,post_id):
    #retrieve post by id
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    if request.method=='POST':
        #Form was submitted
        form=EmailPostForm(request.POST)
        if form.is_valid():
            #form fields pass validation
            cd=form.cleaned_data
        
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form})