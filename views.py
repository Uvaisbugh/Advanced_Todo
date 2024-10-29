from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Todo_model
from . import models
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method == 'POST':
        # Get the signup form data
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'signup_login.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return render(request, 'signup_login.html')

        # Create the user
        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.save()

        # Redirect to the login page
        messages.success(request, 'Signup successful! Please log in.')
        return redirect('login')
    
    return render(request, 'signup_login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.utils import timezone

from django.shortcuts import render
from django.contrib import messages
from .models import Todo_model

def homepage(request):
    # Get the sorting option from GET request
    sort_option = request.GET.get('sort', 'created')  # Default sorting is by 'created' date

    # Determine sorting based on user selection
    if sort_option == 'due_date':
        tasks = Todo_model.objects.filter(user=request.user).order_by('due_date')
    elif sort_option == 'priority':
        tasks = Todo_model.objects.filter(user=request.user).order_by('priority')
    elif sort_option == 'completed':
        tasks = Todo_model.objects.filter(user=request.user).order_by('completed')
    else:
        tasks = Todo_model.objects.filter(user=request.user).order_by('-created')

    if request.method == 'POST':
        # Get the form data
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')  # Retrieve due date from form data
        priority = request.POST.get('priority', 'M')  # Use 'M' (Medium) as default if no priority is provided

        # Check if all required fields are filled
        if not title or not due_date:
            messages.error(request, 'Please fill out all fields.')
            return render(request, 'home.html', {'tasks': tasks, 'sort_option': sort_option})

        # Create a new Todo_model object and save it
        try:
            obj = Todo_model(
                title=title,
                due_date=due_date,  # Pass the due date
                priority=priority,   # Set priority
                user=request.user
            )
            obj.save()
            messages.success(request, 'New task created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating task: {e}')

    # Render the home template with existing tasks, if any
    context = {
        'tasks': tasks,
        'sort_option': sort_option,  # Pass current sorting option to template
    }
    return render(request, 'home.html', context)

    
def loginn(request):
    if request.method == 'POST':
        # Get the login form data
        log_name = request.POST.get('log_name')
        log_password = request.POST.get('log_password')
        print(request.POST) 

        # Authenticate the user
        user = authenticate(request, username=log_name, password=log_password)
        
        if user is not None:
            auth_login(request, user)  # Log in the user
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Redirect to homepage on success
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'signup_login.html')  # Reload login page with error

    return render(request, 'signup_login.html')


def toggle_complete(request, task_id):
    # Retrieve the task by ID and ensure it belongs to the current user
    task = get_object_or_404(Todo_model, id=task_id, user=request.user)
    
    # Toggle the 'completed' status
    task.completed = not task.completed
    task.save()
    
    # Provide a success message
    if task.completed:
        messages.success(request, f"Task '{task.title}' marked as completed.")
    else:
        messages.warning(request, f"Task '{task.title}' marked as pending.")
    
    # Redirect back to the home page
    return redirect('home')

def delete_task(request, task_id):
    # Retrieve the task by ID and ensure it belongs to the current user
    task = get_object_or_404(Todo_model, id=task_id, user=request.user)
    
    # Delete the task
    task.delete()
    
    # Provide a success message
    messages.success(request, f"Task '{task.title}' deleted successfully.")
    
    # Redirect back to the home page
    return redirect('home')
def signout(request):
    # Logout the user and redirect to the login page
    auth_logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

def edit_task(request, task_id):
    task = get_object_or_404(Todo_model, id=task_id, user=request.user)

    if request.method == 'POST':
        # Update the task with the new data
        task.title = request.POST.get('title', task.title)
        task.due_date = request.POST.get('due_date', task.due_date)
        task.priority = request.POST.get('priority', task.priority)
        task.completed = request.POST.get('completed') == 'on'  # Checkbox for completed status
        task.save()

        messages.success(request, 'Task updated successfully!')
        return redirect('home')

    return render(request, 'edit_task.html', {'task': task})