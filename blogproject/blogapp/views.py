from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from .forms import SignUpForms, LoginForms, Postform, CommentForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comments
from django.contrib.auth.models import Group


def home(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/home.html', {'posts': posts})


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = Group.objects.all()
        return render(request, 'blogapp/dashboard.html', {'posts': posts, 'full_name': full_name, 'gps': gps})
    else:
        return redirect('/')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForms(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You became our blog member.')
            user = form.save()
            form = SignUpForms()
            group = Group.objects.get(name='Members')
            user.groups.add(group)
    else:
        form = SignUpForms()
    return render(request, 'blogapp/signup.html', {'form': form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForms(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if request.user is not None:
                    login(request, user)
                    messages.success(request , 'Welcome!!! You are successfully loged in!')
                    return redirect('/dashboard/')
        else:
            form = LoginForms()
    else:
        return redirect('/dashboard/')
    return render(request, 'blogapp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = Postform()
        else:
            form = Postform()
        return render(request, 'blogapp/addpost.html', {'form': form})
    else:
        return redirect('/')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request, 'blogapp/updatepost.html', {'form': form})
    else:
        return redirect('/')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return redirect('/dashboard/')
    else:
        return redirect('/')


def blog_page(request, id):
    post = Post.objects.filter(id=id).first()
    comment = Comments.objects.filter(post=post).order_by('-id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated:
                content = request.POST.get('content')
            else:
                return redirect('/login/')
            comment = Comments.objects.create(post=post, user=request.user, content=content)
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    return render(request, 'blogapp/BlogPage.html', {'post': post, 'comment': comment, 'comment_form': comment_form})


def deletecomment(request, id):
    if request.user.is_authenticated:
        pi = Comments.objects.filter(pk=id).first()
        pi.delete()
        next = request.GET.get('next')
        return HttpResponseRedirect(next)
    else:
        return redirect('/login/')

    # return HttpResponseRedirect('/dashboard/')

