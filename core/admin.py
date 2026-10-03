from django.contrib import admin
from .models import *
for m in [Navbar,NavigationItem,NavigationPage,PageDocument,PageLink,PageImage,NavigationDocument,NavigationLink,NavigationImage,Banner,BannerButton,News,ActivityLog]:
    admin.site.register(m)
