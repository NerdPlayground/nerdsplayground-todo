from os import stat
from todos.models import Todo
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

#Inheriting from APITestCase gives us access to a client e.g Postman
class TodosAPITestCase(APITestCase):
    def create_todo(self):
        sample_todo= {'title':'What To Do?','description':'19th January, 2022 - (8.00 A.M - 10.00 A.M)'}
        return self.client.post(reverse('todos'),sample_todo)

    def authenticate(self):
        sample_user= {'username':'username','email':'email@gmail.com','password':'password'}
        self.client.post(reverse('register'),sample_user)
        response= self.client.post(reverse('login'),{'email':sample_user['email'],'password':sample_user['password']})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
    
    def verify_operation(self,response,count):
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)
        self.assertIsInstance(response.data['count'],int)
        self.assertEqual(response.data['count'],count)

class TestListCreateTodos(TodosAPITestCase):
    def test_should_not_create_todos_with_no_authentication(self):
        self.assertEqual(self.create_todo().status_code,status.HTTP_403_FORBIDDEN)
    
    def test_should_create_todos_with_authentication(self):
        self.authenticate()
        previous_todo_count= Todo.objects.all().count()
        response= self.create_todo()
        sample_todo= {'title':'What To Do?','description':'19th January, 2022 - (8.00 A.M - 10.00 A.M)'}
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],sample_todo['title'])
        self.assertEqual(response.data['description'],sample_todo['description'])
        self.assertEqual(Todo.objects.all().count(),previous_todo_count+1)

    def test_retrieves_all_with_no_todos(self):
        self.authenticate()
        response= self.client.get(reverse('todos'))
        self.verify_operation(response,0)

    def test_retrieves_all_with_at_least_one_todo(self):
        self.authenticate()
        sample_todos= [
            {'title':'What To Do?','description':'19th January, 2022 - (8.00 A.M - 10.00 A.M)'},
            {'title':'What To Do?','description':'19th January, 2022 - (11.00 A.M - 1.00 P.M)'},
            {'title':'What To Do?','description':'19th January, 2022 - (2.00 P.M - 4.00 P.M)'},
            {'title':'What To Do?','description':'19th January, 2022 - (5.00 P.M - 7.00 P.M)'},
            {'title':'What To Do?','description':'19th January, 2022 - (8.00 P.M - 10.00 P.M)'}
        ]
        for sample_todo in sample_todos:
            self.client.post(reverse('todos'),sample_todo)

        response= self.client.get(reverse('todos'))
        self.verify_operation(response,len(sample_todos))

class TestTodoDetailAPIView(TodosAPITestCase):
    def test_retrieves_one(self):
        self.authenticate()
        create_response= self.create_todo()
        retrive_response= self.client.get(reverse('todo',kwargs={'id':create_response.data['id']}))
        self.assertEqual(retrive_response.status_code,status.HTTP_200_OK)
        todo= Todo.objects.get(id=create_response.data['id'])
        self.assertEqual(todo.title,retrive_response.data['title'])
        self.assertEqual(todo.description,retrive_response.data['description'])
        self.assertEqual(todo.is_complete,retrive_response.data['is_complete'])


    def test_updates_one(self):
        self.authenticate()
        create_response= self.create_todo()
        previous_todo_status= create_response.data['is_complete']
        update_response= self.client.patch(reverse('todo',kwargs={'id':create_response.data['id']}),{'is_complete':True})
        self.assertEqual(update_response.status_code,status.HTTP_200_OK)
        self.assertNotEqual(update_response.data['is_complete'],previous_todo_status)
        self.assertEqual(Todo.objects.get(id=update_response.data['id']).is_complete,True)

    def test_deletes_one(self):
        self.authenticate()
        create_response= self.create_todo()
        previous_todo_count= Todo.objects.all().count()
        self.assertGreater(previous_todo_count,0)
        self.assertEqual(previous_todo_count,1)
        delete_response= self.client.delete(reverse('todo',kwargs={'id':create_response.data['id']}))
        self.assertEqual(delete_response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(),previous_todo_count-1)