from django.test import TestCase
from .forms import NewTaskForm
from .models import Task
# Create your tests here.

class TaskModelTest(TestCase):
    def test_task_model_exists(self):
        tasks = Task.objects.count()

        self.assertEqual(tasks, 0)
    
    def test_model_has_string_representation(self):
        task = Task.objects.create(title='First task')

        self.assertEqual(str(task), task.title)

class IndexPageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='First task')

    def test_index_page_returns_correct_response(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'task/index.html')
        self.assertEqual(response.status_code, 200)
         
    def index_page_has_tasks(self):

        response = self.client.get('/')

        self.assertContains(response, self.task.title)

class DetailPageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='First task', description='1st task description')
        self.task2 = Task.objects.create(title='Second task', description='2nd task description')

    def test_detail_page_returns_correct_response(self):
        response = self.client.get(f'/{self.task.id}/')

        self.assertTemplateUsed(response, 'task/detail.html')
        self.assertEqual(response.status_code, 200)

    def test_detail_page_has_correct_content(self):
        response = self.client.get(f'/{self.task.id}/')

        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.description)
        self.assertNotContains(response, self.task2.title)

class NewPageTest(TestCase):
        def setUp(self):
            self.form = NewTaskForm

        def test_new_page_returns_correct_response(self):
            response = self.client.get('/new/')

            self.assertTemplateUsed(response, 'task/new.html')
            self.assertEqual(response.status_code, 200)

        def test_form_can_be_valid(self):
            self.assertTrue(issubclass(self.form, NewTaskForm))
            self.assertTrue('title' in self.form.Meta.fields)
            self.assertTrue('description' in self.form.Meta.fields)

            form = self.form({
                'title': 'The title',
                'description': 'The description'
            })

            self.assertTrue(form.is_valid())

        def test_new_form_rendering(self):
            response = self.client.get('/new/')

            self.assertContains(response, '<form')
            self.assertContains(response, 'csrfmiddlewaretoken')
            self.assertContains(response, '<label for')

