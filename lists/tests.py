from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
        
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
class ListAndItemModelsTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        # save 1st item
        first_item = Item()
        first_item.text = "The first (ever) item"
        first_item.list = list_
        first_item.save()
        
        # save 2nd item
        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        # get all items and count
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        # compare items equal to constants
        self.assertEqual(saved_items[0].text, 'The first (ever) item', )
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, 'Item the second')
        self.assertEqual(saved_items[1].list, list_)
        
class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        
        response = self.client.get('/lists/the-only-list-in-the-world/')
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        
class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new item')
        
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')