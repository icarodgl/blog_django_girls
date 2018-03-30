from django.shortcuts import render
from .models import Post
from django.utils import timezone
from .forms import PostForm, ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = Post.objects.get(id = pk)
    return render(request, 'blog/post_detail.html', {'post': post})
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def post_edit(request, pk):
    post = Post.objects.get(id = pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('blog/list.html')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    
@login_required
def profile(request):

    user = request.user
    message = ""

    current_info = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    # return HttpResponse("this is the user profile page for username '%s'. update first, last, email, username, and password here." % request.user.username)
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = ProfileForm(request.POST)

        if form.is_valid():

            if form.cleaned_data['username'] != user.username:
                user.username = form.cleaned_data['username']

            if form.cleaned_data['first_name'] != user.first_name:
                user.first_name = form.cleaned_data['first_name']

            if form.cleaned_data['last_name'] != user.last_name:
                user.last_name = form.cleaned_data['last_name']

            if form.cleaned_data['email'] != user.email:
                user.email = form.cleaned_data['email']

            if form.cleaned_data['password'] != user.password and form.cleaned_data['password'] != "":
                user.set_password(form.cleaned_data['password'])

            user.save()
            message += "Profile updated."

            return render(request, 'accounts/profile.html', {'form': form, 'message': message})

    else:
        form = ProfileForm(current_info)

    return render(request, 'accounts/profile.html', {'form': form})