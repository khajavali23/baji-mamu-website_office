from django import forms
from .models import *

class Base(forms.ModelForm):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        for n,f in self.fields.items():
            if isinstance(f.widget,forms.CheckboxInput): f.widget.attrs['class']='form-check'
            elif isinstance(f.widget,forms.Select): f.widget.attrs['class']='form-select'
            else: f.widget.attrs['class']='form-control'

class NavbarForm(Base):
    class Meta: model=Navbar; fields=['name','url','order','is_active']


class NavigationItemForm(Base):

    class Meta:
        model = NavigationItem

        fields = [
            "navbar",
            "parent",
            "name",
            "item_type",
            "order",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["parent"].required = False

        self.fields["parent"].queryset = (
            NavigationItem.objects
            .filter(
                item_type="child",
                is_active=True
            )
            .select_related("navbar")
            .order_by(
                "navbar__name",
                "order",
                "name"
            )
        )

        if self.instance.pk:
            self.fields["parent"].queryset = (
                self.fields["parent"].queryset
                .exclude(pk=self.instance.pk)
            )
                    
class NavigationPageForm(Base):
    class Meta: model=NavigationPage; fields=['navigation_item','heading','content','image']; widgets={'content':forms.Textarea(attrs={'rows':14})}
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw); self.fields['navigation_item'].queryset=NavigationItem.objects.filter(item_type='page').order_by('navbar__name','name')
class PageDocumentForm(Base):
    class Meta: model=PageDocument; fields=['page','name','document','order']
class PageLinkForm(Base):
    class Meta: model=PageLink; fields=['page','name','url','order']
class PageImageForm(Base):
    class Meta: model=PageImage; fields=['page','name','image','order']
class NavigationDocumentForm(Base):
    class Meta: model=NavigationDocument; fields=['navigation_item','name','document','order']
    def __init__(self,*a,**kw): super().__init__(*a,**kw); self.fields['navigation_item'].queryset=NavigationItem.objects.filter(item_type='document')
class NavigationLinkForm(Base):
    class Meta: model=NavigationLink; fields=['navigation_item','name','url','order']
    def __init__(self,*a,**kw): super().__init__(*a,**kw); self.fields['navigation_item'].queryset=NavigationItem.objects.filter(item_type='link')
class NavigationImageForm(Base):
    class Meta: model=NavigationImage; fields=['navigation_item','name','image','order']
    def __init__(self,*a,**kw): super().__init__(*a,**kw); self.fields['navigation_item'].queryset=NavigationItem.objects.filter(item_type='image')
class BannerForm(Base):
    class Meta: model=Banner; fields=['title','description','image','order','is_active']; widgets={'description':forms.Textarea(attrs={'rows':8})}
class BannerButtonForm(Base):
    class Meta: model=BannerButton; fields=['banner','text','button_type','is_main','order','is_active','url','page','document','image','email']
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw); self.fields['page'].queryset=NavigationPage.objects.select_related('navigation_item').all()
class NewsForm(Base):
    class Meta: model=News; fields=['heading','paragraph','image','date','link']; widgets={'paragraph':forms.Textarea(attrs={'rows':8}),'date':forms.DateInput(attrs={'type':'date'})}
