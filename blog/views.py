from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse , HttpResponseRedirect
from django.core import serializers

# Create your views here.

def home(req): 
    all_of_posts = Post.objects.all().order_by('-pub_date')

    # pagination
    paginator = Paginator(all_of_posts,5)
    page = req.GET.get('page')    
    posts = paginator.get_page(page)

    # hottest posts
    all_of_posts_with_views = Post.objects.all().order_by('-views' , '-pub_date')[:3]
    
    return render(req , './home.html' , { 'posts' : posts , 'hottest_posts' : all_of_posts_with_views })

def detail(req , post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()
    comments_list = Comment.objects.filter(post = post_id).order_by('-date')
    return render(req, 'detail.html', {'post':post, 'comments':comments_list})

def create_post(req):
    if req.method == "POST" and req.POST['title'].strip() != "" and req.POST['content'].strip() != "":
        new_post = Post()
        new_post.title = req.POST['title'] 
        new_post.body = req.POST['content']
        new_post.writer = req.user.username
        new_post.pub_date = timezone.datetime.now()
        new_post.save()
        return HttpResponseRedirect('/blog/%d'%new_post.pk)
    return render(req , 'post.html' , { 'status' : 'create' })

def update_post(req , post_id):
    current_post = get_object_or_404(Post , pk=post_id)
    if req.method == "POST":
        current_post.title = req.POST['title']
        current_post.content = req.POST['content']
        current_post.save()
        return HttpResponseRedirect('/blog/%d'%post_id)
    return render(req , 'post.html' , { 'post' : current_post , 'status' : 'update' })

def delete_post(req , post_id):
    current_post = Post.objects.get(id=post_id)
    current_post.delete()
    return redirect('home')

def search(req):
    if req.GET.get('q'):
        que = req.GET.get('q')
        variable_column = req.GET.get('search_filter')
        search_type = 'contains'
        filter = variable_column + '__' + search_type
        posts = Post.objects.filter(**{ filter: req.GET.get('q') }).order_by('-pub_date') 
        return render(req , 'result.html' , {'result' : posts , 'query' : que})
    else:
        return redirect('home')    

# API
@csrf_exempt
def get_comment(req , post_id):
    post = get_object_or_404(Post , pk=post_id)
    comments_list = Comment.objects.filter(post = post_id).order_by('-date')
    return JsonResponse({
        'code' : 1 ,
        'message' : 'success',
        'data' : {
            'comments' : serializers.serialize('json' , comments_list)
        }
    }, json_dumps_params = {'ensure_ascii': True})

@csrf_exempt
def comment_create(req , post_id):
    comment = Comment()
    comment.writer = req.POST['writer']
    comment.content = req.POST['content']
    comment.post = get_object_or_404(Post , pk=post_id)
    comment.save()
    return JsonResponse({
        'code' : 1 ,
        'message' : 'success',
    }, json_dumps_params = {'ensure_ascii': True})

def comment_update(req , comment_id):
    return JsonResponse({
        'message' : 'success',
    }, json_dumps_params = {'ensure_ascii': True})

def comment_delete(req , comment_id):
    return JsonResponse({
        'message' : 'success',
    }, json_dumps_params = {'ensure_ascii': True})

def comment_delete_not_api(req , comment_id):
    current_comment = get_object_or_404(Comment , pk=comment_id)
    related_post = get_object_or_404(Post , pk=current_comment.post.pk)
    current_comment.delete()
    return HttpResponseRedirect('/blog/%d'%related_post.pk)
    