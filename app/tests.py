import datetime
from datetime import date, time
from .models import Task, DiaryEntry
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class DiaryEntryModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')

        self.task = Task.objects.create(
            user=self.user,
            name="Test Task",
            date=datetime.date.today(),
            time=datetime.datetime.now().time(),
            color="Red",
            description="A test task.",
            completed=True
        )

    def test_diary_entry_creation(self):
        entry = DiaryEntry.objects.create(
            user=self.user,
            title="Test Entry",
            description="A test diary entry."
        )
        # Dodavanje zadatka u dnevni unos
        entry.completed.add(self.task)

        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.description, "A test diary entry.")
        self.assertTrue(entry.completed.filter(id=self.task.id).exists())


class HomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='123password')

    def test_homepage_access(self):
        self.client.login(username='testuser', password='123password')

        url = reverse('app:homepage')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345')

    def test_task_creation(self):
        task_date = date.today()
        task_time = time(14, 30)
        task = Task.objects.create(
            user=self.user,
            name='Test Task',
            date=task_date,
            time=task_time,
            color='red',
            description='Test Description',
            completed=False
        )

        self.assertEqual(task.user, self.user)
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.date, task_date)
        self.assertEqual(task.time, task_time)
        self.assertEqual(task.color, 'red')
        self.assertEqual(task.description, 'Test Description')
        self.assertFalse(task.completed)


class AddTaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.url = reverse('app:add_task')

    def test_add_task_view(self):

        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


        response = self.client.post(self.url, {
            'name': 'New Task',
            'date': '2023-01-01',
            'time': '10:00',
            'color': 'Blue',
            'description': 'A new test task.',
            'completed': False
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Task.objects.filter(name='New Task').exists())