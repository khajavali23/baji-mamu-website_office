from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Navbar,NavigationItem,NavigationPage,PageDocument,PageLink,Banner,BannerButton,News
class Command(BaseCommand):
    help='Create optional database demo content.'
    def handle(self,*args,**kwargs):
        nav,_=Navbar.objects.get_or_create(name='Policies & Procedures',defaults={'order':1})
        cars,_=NavigationItem.objects.get_or_create(navbar=nav,parent=None,name='HR',defaults={'item_type':'child','order':1})
        page_item,_=NavigationItem.objects.get_or_create(navbar=nav,parent=cars,name='Employee Handbook',defaults={'item_type':'page','order':1})
        page,_=NavigationPage.objects.get_or_create(navigation_item=page_item,defaults={'heading':'Employee Handbook','content':'Centralised policies, procedures and trusted internal resources.'})
        PageLink.objects.get_or_create(page=page,name='Arab Invest Website',defaults={'url':'https://www.arabinvest.com','order':1})
        banner,_=Banner.objects.get_or_create(title='A rooted Arab heritage, for a prosperous future',defaults={'description':'A secure, modern intranet for teams, policies, resources and trusted internal services.','order':1})
        BannerButton.objects.get_or_create(banner=banner,text='Explore Company',defaults={'button_type':'page','page':page,'is_main':True,'order':1})
        BannerButton.objects.get_or_create(banner=banner,text='Contact',defaults={'button_type':'email','email':'info@example.com','order':2})
        News.objects.get_or_create(heading='Welcome to the Arab Invest Intranet',defaults={'paragraph':'Explore policies, internal resources and the latest company updates in one place.','date':timezone.localdate()})
        self.stdout.write(self.style.SUCCESS('Demo database records created.'))
