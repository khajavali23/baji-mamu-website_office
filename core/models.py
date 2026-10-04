from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

class Stamp(models.Model):
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: abstract=True

class Navbar(Stamp):
    name=models.CharField(max_length=120); url=models.CharField(max_length=500,blank=True); order=models.PositiveIntegerField(default=0); is_active=models.BooleanField(default=True)
    class Meta: ordering=('order','name')
    def __str__(self): return self.name

class NavigationItem(Stamp):

    TYPES = [
        ('child', 'Child / Container'),
        ('page', 'Page'),
        ('document', 'Document'),
        ('link', 'Link'),
        ('image', 'Image'),
        ('url', 'URL'),
    ]

    navbar = models.ForeignKey(
        Navbar,
        on_delete=models.CASCADE,
        related_name='items'
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    name = models.CharField(max_length=180)

    item_type = models.CharField(
        max_length=20,
        choices=TYPES,
        default='child'
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order', 'name')
        indexes = [
            models.Index(
                fields=('navbar', 'parent', 'order')
            ),
            models.Index(
                fields=('item_type', 'is_active')
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):

        if self.pk and self.parent_id == self.pk:
            raise ValidationError(
                'An item cannot be its own parent.'
            )

        if self.parent and self.parent.navbar_id != self.navbar_id:
            raise ValidationError(
                'Parent must use the same navbar.'
            )

        if self.parent and self.parent.item_type != 'child':
            raise ValidationError(
                'Only Child / Container items can have children.'
            )

    def get_absolute_url(self):
        return reverse(
            'navigation_detail',
            args=[self.pk]
        ) 
    
class NavigationPage(Stamp):
    navigation_item = models.OneToOneField(
        NavigationItem,
        on_delete=models.CASCADE,
        related_name='page'
    )

    heading = models.CharField(max_length=220)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='pages/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.heading

class PageDocument(Stamp):
    page=models.ForeignKey(NavigationPage,on_delete=models.CASCADE,related_name='documents'); name=models.CharField(max_length=180); document=models.FileField(upload_to='page-documents/'); order=models.PositiveIntegerField(default=0)
    class Meta: ordering=('order','name')
    def __str__(self): return self.name

class PageLink(Stamp):
    page=models.ForeignKey(NavigationPage,on_delete=models.CASCADE,related_name='links'); name=models.CharField(max_length=180); url=models.URLField(max_length=1000); order=models.PositiveIntegerField(default=0)
    class Meta: ordering=('order','name')
    def __str__(self): return self.name

class PageImage(Stamp):
    page=models.ForeignKey(NavigationPage,on_delete=models.CASCADE,related_name='images'); name=models.CharField(max_length=180); image=models.ImageField(upload_to='page-images/'); order=models.PositiveIntegerField(default=0)
    class Meta: ordering=('order','name')
    def __str__(self): return self.name

class NavigationDocument(Stamp):
    navigation_item=models.OneToOneField(NavigationItem,on_delete=models.CASCADE,related_name='navigation_document'); name=models.CharField(max_length=180); document=models.FileField(upload_to='navigation-documents/'); order=models.PositiveIntegerField(default=0)
    def __str__(self): return self.name

class NavigationLink(Stamp):
    navigation_item=models.OneToOneField(NavigationItem,on_delete=models.CASCADE,related_name='navigation_link'); name=models.CharField(max_length=180); url=models.URLField(max_length=1000); order=models.PositiveIntegerField(default=0)
    def __str__(self): return self.name

class NavigationImage(Stamp):
    navigation_item=models.OneToOneField(NavigationItem,on_delete=models.CASCADE,related_name='navigation_image'); name=models.CharField(max_length=180); image=models.ImageField(upload_to='navigation-images/'); order=models.PositiveIntegerField(default=0)
    def __str__(self): return self.name

class Banner(Stamp):
    title=models.CharField(max_length=240); description=models.TextField(blank=True); image=models.ImageField(upload_to='banners/',blank=True,null=True); order=models.PositiveIntegerField(default=0); is_active=models.BooleanField(default=True)
    class Meta: ordering=('order','-created_at')
    def __str__(self): return self.title

class BannerButton(Stamp):
    TYPES=[('url','URL'),('page','Page'),('document','Document'),('image','Image'),('email','Email')]
    banner=models.ForeignKey(Banner,on_delete=models.CASCADE,related_name='buttons'); text=models.CharField(max_length=100); button_type=models.CharField(max_length=20,choices=TYPES,default='url'); is_main=models.BooleanField(default=False); order=models.PositiveIntegerField(default=0); is_active=models.BooleanField(default=True)
    url=models.URLField(max_length=1000,blank=True); page=models.ForeignKey(NavigationPage,on_delete=models.SET_NULL,null=True,blank=True,related_name='banner_buttons'); document=models.FileField(upload_to='banner-documents/',blank=True,null=True); image=models.ImageField(upload_to='banner-images/',blank=True,null=True); email=models.EmailField(blank=True)
    class Meta: ordering=('order','id')
    def clean(self):
        vals={'url':self.url,'page':self.page,'document':self.document,'image':self.image,'email':self.email}
        required={'url':'url','page':'page','document':'document','image':'image','email':'email'}[self.button_type]
        if not vals[required]: raise ValidationError({required:'This field is required for the selected button type.'})
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.is_main: type(self).objects.filter(banner=self.banner,is_main=True).exclude(pk=self.pk).update(is_main=False)
    def target_url(self):
        if self.button_type=='url': return self.url or '#'
        if self.button_type=='page' and self.page_id: return reverse('page_detail',args=[self.page_id])
        if self.button_type=='document' and self.document: return self.document.url
        if self.button_type=='image' and self.image: return self.image.url
        if self.button_type=='email' and self.email: return 'mailto:'+self.email
        return '#'
    def __str__(self): return self.text

class News(Stamp):
    heading=models.CharField(max_length=220); paragraph=models.TextField(); image=models.ImageField(upload_to='news/',blank=True,null=True); date=models.DateField(); link=models.URLField(max_length=1000,blank=True)
    class Meta: ordering=('-date','-created_at')
    def __str__(self): return self.heading

class ActivityLog(Stamp):
    ACTIONS=[('created','Created'),('updated','Updated'),('deleted','Deleted')]
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL); action=models.CharField(max_length=20,choices=ACTIONS); object_type=models.CharField(max_length=80); object_name=models.CharField(max_length=220)
    class Meta: ordering=('-created_at',)
    def __str__(self): return f'{self.action} {self.object_name}'
