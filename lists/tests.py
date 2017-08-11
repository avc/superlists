from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
        
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')
    
    def test_redirects_after_post(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        
        # self.assertIn('A new list item', response.content.decode())
        #         self.assertTemplateUsed(response, 'home.html')
        
    def test_only_save_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
        
class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        # save 1st item
        first_item = Item()
        first_item.text = "The first (ever) item"
        first_item.save()
        
        # save 2nd item
        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()
        
        # get all items and count
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        # compare items equal to constants
        self.assertEqual(saved_items[0].text, 'The first (ever) item', )
        self.assertEqual(saved_items[1].text, 'Item the second')
        