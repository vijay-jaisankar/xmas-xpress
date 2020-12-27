from django.test import TestCase
from django.test import SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Room 
# Create your tests here.

class SimpleTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)


    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code,200)


    def test_signup_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code,200)

    
    def test_logout_page_status_code(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code,302)


class RoomModelTest(TestCase):
    def setUp(self):
        Room.objects.create(name='test test',description='Test room done for testing purposes',budget=10000,password='sindel321',masterPassword='liukang321')
    
    def test_name_content(self):
        room = Room.objects.get(id=1)
        expected_room_name = "{}".format(room.name)
        self.assertEqual(expected_room_name,'test test')


class HomePageViewTest(TestCase):
    def setUp(self):
        Room.objects.create(name='test test',description='Test room done for testing purposes',budget=10000,password='sindel321',masterPassword='liukang321')

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)


    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"index.html")


class LoginPageViewTest(TestCase):
    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code,200)


    def test_view_url_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)

    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"registration/login.html")



class SignupPageViewTest(TestCase):
    def test_signup_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code,200)


    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)

    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"registration/signup.html")


class RoomListPageViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',email='test@email.com',password='secret')
        Room.objects.create(name='test test',description='Test room done for testing purposes',budget=10000,password='sindel321',masterPassword='liukang321')
    

    def test_home_page_status_code(self):
        response = self.client.get('/rooms/')
        self.assertEqual(response.status_code,200)


    def test_view_url_by_name(self):
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code,200)

    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"room/list.html")

    
    def test_post_list_view(self):
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Test room done for testing purposes")
        self.assertTemplateUsed(response,"room/list.html")


class AboutPageViewTest(TestCase):
    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code,200)


    def test_view_url_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code,200)

    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"about.html")

    
    def test_view_contains_us(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'R Prasannavenkatesh')
        self.assertContains(response,'Vijay Jaisankar')