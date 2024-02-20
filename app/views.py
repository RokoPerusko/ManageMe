import datetime

from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import UserProfile, Task



def SignupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Automatska prijava korisnika
            return redirect('app:homepage')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def LoginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('app:homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('app:login')


@login_required
def homepage(request):
    return render(request, 'homepage.html')



@login_required
def add_diary_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.save()

            # Automatsko povezivanje izvršenih zadataka s dnevnim unosom
            completed_tasks_for_date = Task.objects.filter(
                user=request.user,
                date=diary_entry.date,
                completed=True
            )
            for task in completed_tasks_for_date:
                diary_entry.completed.add(task)  # Povezuje zadatak s dnevnikom

            return redirect('app:diary_list')
    else:
        form = DiaryEntryForm()

    return render(request, 'add_diary_entry.html', {'form': form})


@login_required
def diary_list(request):
    diary_entries_query = DiaryEntry.objects.filter(user=request.user)

    # Handle date filtering
    filter_date = request.GET.get('filter-date')
    if filter_date:
        diary_entries_query = diary_entries_query.filter(date=filter_date)

    diary_entries = diary_entries_query.order_by('-date')

    for entry in diary_entries:
        entry.completed_tasks_list = entry.completed.filter(completed=True)

    context = {
        'diary_entries': diary_entries,
        'filter_date': filter_date,
    }
    return render(request, 'diary_list.html', context)


@login_required
def edit_diary_entry(request, entry_id):  # Changed from diary_entry_id to entry_id
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('app:diary_list')
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'edit_diary_entry.html', {'form': form})



@login_required
def delete_diary_entry(request, diary_entry_id):
    diary_entry = get_object_or_404(DiaryEntry, id=diary_entry_id, user=request.user)
    if request.method == 'POST':
        diary_entry.delete()
        return redirect('app:diary_list')
    else:
        return redirect('app:diary_list')




@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-date')
    filter_date = request.GET.get('filter-date')

    if filter_date:
        tasks = tasks.filter(date=filter_date)
        date_selected = True
    else:
        date_selected = False

    context = {
        'tasks': tasks,
        'date_selected': date_selected,
        'filter_date': filter_date
    }
    return render(request, 'task_list.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('app:task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure the task belongs to the user
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('app:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task_id': task_id})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('app:task_list')
    else:

        return redirect('app:task_list')




@login_required
def view_user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    today_date = date.today()

    # Daily
    today_tasks = Task.objects.filter(user=request.user, date=today_date)
    completed_today_tasks = today_tasks.filter(completed=True).count()
    daily_success_percentage = (completed_today_tasks / today_tasks.count() * 100) if today_tasks.count() else 0


    context = {
        'profile': profile,
        'daily_success_percentage': daily_success_percentage,
        'today_tasks': today_tasks,
        'completed_today_tasks': completed_today_tasks,
    }

    return render(request, 'view_user_profile.html', context)


@login_required
def edit_user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('app:view_user_profile')  # Adjust the redirect as needed
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_user_profile.html', {'form': form})





@login_required
def user_profile_week(request):
    today = timezone.now().date()
    week_start = today - datetime.timedelta(days=6)  # 7 dana uključujući i današnji dan
    week_end = today

    user = request.user
    weekly_tasks = user.tasks.filter(date__range=[week_start, week_end])
    tasks_completed = weekly_tasks.filter(completed=True).count()
    total_tasks = weekly_tasks.count()

    weekly_success = (tasks_completed / total_tasks * 100) if total_tasks else 0

    context = {
        'user': user,
        'weekly_success': weekly_success,
        'week_start': week_start,
        'week_end': week_end,
        'weekly_tasks': weekly_tasks,
    }
    return render(request, 'weekly_view.html', context)