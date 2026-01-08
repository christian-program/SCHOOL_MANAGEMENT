from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Department, StudentResult, Comment
from django.contrib.auth.decorators import login_required

def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'portal/home.html', {'posts': posts})

def about_view(request):
    depts = Department.objects.all()
    return render(request, 'portal/about.html', {'departments': depts})

def announcements_view(request):
    posts = Post.objects.filter(post_type='NEWS').order_by('-created_at')
    return render(request, 'portal/announcements.html', {'posts': posts})

def schedules_view(request):
    posts = Post.objects.filter(post_type='SCHEDULE').order_by('-created_at')
    return render(request, 'portal/schedules.html', {'posts': posts})

def results_view(request):
    query = request.GET.get('matricule')
    result = StudentResult.objects.filter(student_id__iexact=query).first() if query else None
    return render(request, 'portal/results.html', {'result': result, 'query': query})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        Comment.objects.create(post_id=post_id, author=request.user, text=request.POST.get('text'))
    return redirect(request.META.get('HTTP_REFERER', 'home'))