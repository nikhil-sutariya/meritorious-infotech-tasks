from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from post.models import Post, Comment
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

def post_list(request):
    try:
        posts = Post.objects.all()
        return render(request, 'index.html', {'posts': posts})
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        comments = post.comments.all()
        return render(request, 'post_detail.html', {'post': post, 'comments': comments})
    
    except Post.DoesNotExist:
        return render(request, 'post_not_found.html')
    
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

@login_required
def post_create(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            Post.objects.create(title=title, content=content, author=request.user)
            return redirect("post_list")
        return render(request, 'post.html')

    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

@login_required
def post_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "POST" and post.author == request.user:
            post.title = request.POST.get("title")
            post.content = request.POST.get("content")
            post.updated_at = timezone.now()
            post.save()
            return redirect("post_detail", pk=pk)
        return render(request, 'post.html', {'post': post})
    
    except Post.DoesNotExist:
        return render(request, 'post_not_found.html')
    
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

@login_required
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            post.delete()
            return redirect("post_list")
        return redirect("post_detail", pk=pk)
    
    except Post.DoesNotExist:
        return render(request, 'post_not_found.html')
    
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')

@login_required
def add_comment(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            content = request.POST.get("content")
            Comment.objects.create(post=post, author=request.user, content=content, created_at=timezone.now())
            return redirect("post_detail", pk=pk)
        
    except Post.DoesNotExist:
        return render(request, 'post_not_found.html')
        
    except Exception as e:
        print(e)
        return HttpResponse('<html lang="en"><body>Something went wrong please try again leter!</body></html>')
