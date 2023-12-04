from .forms import TaskForm, UserProfileForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm,CommentForm
from .models import Task, UserProfile,Profile, Comment
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError


def home(request):
    tasks = Task.objects.all().select_related('user')  
    return render(request, 'home.html', {'tasks': tasks})


@login_required(login_url='login')  
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  
    return render(request, 'task_list.html', {'tasks': tasks}) 

@login_required(login_url='login')
def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)  
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

 
            image = form.cleaned_data.get('image')
            if image:
                image_extension = image.name.split('.')[-1].lower()
                if image_extension not in ['jpg', 'jpeg', 'png']:
                    raise ValidationError("Invalid image format. Only JPG, JPEG, and PNG are allowed.")

            task.save()
            return redirect('task_list')
    return render(request, 'create_task.html', {'form': form})

@login_required(login_url='login')
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:  # بررسی اینکه آیا وظیفه متعلق به کاربر فعلی است یا خیر
        return redirect('task_list')

    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)  # اضافه کردن request.FILES
        if form.is_valid():
            # بررسی نوع فایل تصویر
            image = form.cleaned_data.get('image')
            if image:
                image_extension = image.name.split('.')[-1].lower()
                if image_extension not in ['jpg', 'jpeg', 'png']:
                    raise ValidationError("Invalid image format. Only JPG, JPEG, and PNG are allowed.")

            form.save()
            return redirect('task_list')
    return render(request, 'edit_task.html', {'form': form, 'task': task})

@login_required(login_url='login')
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user != request.user:  # بررسی اینکه آیا وظیفه متعلق به کاربر فعلی است یا خیر
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_task.html', {'task': task}) 

@login_required(login_url='login')
def user_profile(request):
    user_profile, created= Profile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=user_profile)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    
    return render(request, 'user_profile.html', {'form': form})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
            else:
                error_message = 'Incorrect username or password.'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    
    # If login fails, suggest redirecting to the registration page
    register_redirect = 'register'
    
    return render(request, 'login.html', {'form': form, 'register_redirect': register_redirect})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            return redirect('register_done')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required(login_url='login')
def register_done(request):
    user = request.user
    return render(request, 'register_done.html', {'user': user})



def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = Comment.objects.filter(task=task)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.task = task
            new_comment.save()
            return redirect('task_details', task_id=task_id)
    else:
        comment_form = CommentForm()
        
    # بررسی اینکه آیا وظیفه متعلق به کاربر فعلی است یا خیر
    is_user_task = False
    if task.user == request.user:
        is_user_task = True
    
    return render(request, 'task_details.html', {'task': task, 'comments': comments, 'comment_form': comment_form, 'is_user_task': is_user_task})
