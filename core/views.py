from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import *
from .forms import *
from .utils import log, crumbs


def home(request):
    banners=Banner.objects.filter(is_active=True).prefetch_related('buttons').order_by('order','-created_at')
    news=News.objects.all()[:7]
    return render(request,'frontend/home.html',{'banners':banners,'news':news})

def page_detail(request,pk):
    page=get_object_or_404(NavigationPage.objects.select_related('navigation_item__navbar').prefetch_related('documents','links','images'),pk=pk)
    return render(request,'frontend/page.html',{'page':page,'breadcrumbs':crumbs(page.navigation_item)})

def navigation_detail(request,pk):
    item=get_object_or_404(NavigationItem.objects.select_related('navbar','parent').prefetch_related('children'),pk=pk,is_active=True)
    if item.item_type=='page' and hasattr(item,'page'): return redirect('page_detail',item.page.pk)
    if item.item_type=='document' and hasattr(item,'navigation_document'): return redirect(item.navigation_document.document.url)
    if item.item_type=='link' and hasattr(item,'navigation_link'): return redirect(item.navigation_link.url)
    if item.item_type=='image' and hasattr(item,'navigation_image'): return redirect(item.navigation_image.image.url)
    return render(request,'frontend/navigation_detail.html',{'item':item,'children':item.children.filter(is_active=True),'breadcrumbs':crumbs(item)})

def login_view(request):
    if request.user.is_authenticated:return redirect('dashboard')
    error=None
    if request.method=='POST':
        u=authenticate(request,username=request.POST.get('username',''),password=request.POST.get('password',''))
        if u: login(request,u); return redirect(request.GET.get('next') or 'dashboard')
        error='Invalid username or password.'
    return render(request,'registration/login.html',{'error':error})

def logout_view(request): logout(request); return redirect('home')

@login_required
def dashboard(request):
    pages=NavigationPage.objects.prefetch_related('documents','links','images')
    health={'active_navigation':NavigationItem.objects.filter(is_active=True).count(),'published_banners':Banner.objects.filter(is_active=True).count(),'pages_without_images':pages.filter(image='').count(),'pages_without_resources':sum(1 for p in pages if not (p.documents.exists() or p.links.exists() or p.images.exists())),'banners_without_buttons':Banner.objects.annotate(n=Count('buttons')).filter(n=0).count(),'inactive_navigation':NavigationItem.objects.filter(is_active=False).count()}
    counts={'navbars':Navbar.objects.count(),'navigation':NavigationItem.objects.count(),'pages':NavigationPage.objects.count(),'documents':PageDocument.objects.count()+NavigationDocument.objects.count(),'links':PageLink.objects.count()+NavigationLink.objects.count(),'images':PageImage.objects.count()+NavigationImage.objects.count(),'banners':Banner.objects.count(),'news':News.objects.count()}
    return render(request,'dashboard/index.html',{'counts':counts,'health':health,'activities':ActivityLog.objects.select_related('user')[:10]})

@login_required
def search(request):
    q=request.GET.get('q','').strip(); results=[]
    if q:
        for x in NavigationItem.objects.filter(name__icontains=q)[:10]: results.append(('Navigation',x.name,x.get_absolute_url()))
        for x in NavigationPage.objects.filter(heading__icontains=q)[:10]: results.append(('Page',x.heading,f'/page/{x.pk}/'))
        for x in News.objects.filter(heading__icontains=q)[:10]: results.append(('News',x.heading,x.link or '#'))
        for x in PageDocument.objects.filter(name__icontains=q)[:10]: results.append(('Document',x.name,x.document.url))
        for x in NavigationDocument.objects.filter(name__icontains=q)[:10]: results.append(('Document',x.name,x.document.url))
    return render(request,'dashboard/search.html',{'q':q,'results':results})

def crud(
    request,
    form_class,
    model,
    template,
    title,
    redirect_name,
    pk=None,
    initial=None
):
    obj = get_object_or_404(model, pk=pk) if pk else None

    if request.method == "POST":

        form = form_class(
            request.POST,
            request.FILES,
            instance=obj
        )

        if form.is_valid():

            saved = form.save()

            log(
                request,
                "updated" if obj else "created",
                saved
            )

            messages.success(
                request,
                f"{title} saved successfully."
            )

            return redirect(redirect_name)

        else:
            print("================================")
            print("FORM IS INVALID")
            print(form.errors)
            print("================================")

    else:
        form = form_class(
            instance=obj,
            initial=initial
        )

    return render(
        request,
        template,
        {
            "form": form,
            "title": title,
            "object": obj
        }
    ) 

def delete_obj(request,model,pk,redirect_name):
    if request.method!='POST': return redirect(redirect_name)
    obj=get_object_or_404(model,pk=pk); name=str(obj); typ=model.__name__; obj.delete();
    if request.user.is_authenticated: ActivityLog.objects.create(user=request.user,action='deleted',object_type=typ,object_name=name)
    messages.success(request,f'{typ} deleted successfully.'); return redirect(redirect_name)

@login_required
def navbars(request): return render(request,'dashboard/list.html',{'title':'Top Navigation','description':'Main header navigation items.','items':Navbar.objects.all(),'columns':['Name','URL','Order','Status'],'kind':'navbar','add_name':'navbar_add','edit_name':'navbar_edit','delete_name':'navbar_delete'})
@login_required
def navbar_add(request): return crud(request,NavbarForm,Navbar,'dashboard/form.html','Create Navbar','navbars')
@login_required
def navbar_edit(request,pk): return crud(request,NavbarForm,Navbar,'dashboard/form.html','Edit Navbar','navbars',pk)
@login_required
@require_POST
def navbar_delete(request,pk): return delete_obj(request,Navbar,pk,'navbars')

@login_required
def navigation_list(request):
    navbars=Navbar.objects.prefetch_related('items__children__children__children__children','items__page','items__navigation_document','items__navigation_link','items__navigation_image')
    q=request.GET.get('q','').strip()
    if q: navbars=Navbar.objects.filter(Q(name__icontains=q)|Q(items__name__icontains=q)).distinct().prefetch_related('items__children__children__children__children')
    return render(request,'dashboard/navigation.html',{'navbars':navbars,'q':q})

@login_required
def navigation_add(request, parent_pk=None):

    parent = None

    if parent_pk:
        parent = get_object_or_404(
            NavigationItem,
            pk=parent_pk
        )

    if request.method == "POST":

        form = NavigationItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            item = form.save(commit=False)

            if parent:
                item.parent = parent
                item.navbar = parent.navbar

            item.save()

            messages.success(
                request,
                "Navigation item created successfully."
            )

            return redirect("navigation_list")

        else:
            print("FORM ERRORS:", form.errors)

    else:

        initial = {}

        if parent:
            initial = {
                "navbar": parent.navbar_id,
                "parent": parent.pk,
            }

        form = NavigationItemForm(
            initial=initial
        )

    return render(
        request,
        "dashboard/form.html",
        {
            "form": form,
            "title": "Create Navigation Item",
            "object": None,
        }
    )

@login_required
def navigation_edit(request,pk): return crud(request,NavigationItemForm,NavigationItem,'dashboard/form.html','Edit Navigation Item','navigation_list',pk)
@login_required
@require_POST
def navigation_delete(request,pk): return delete_obj(request,NavigationItem,pk,'navigation_list')

@login_required
def page_list(request): return render(request,'dashboard/list.html',{'title':'Pages','description':'Corporate pages connected to navigation.','items':NavigationPage.objects.select_related('navigation_item__navbar').all(),'kind':'page','add_name':'page_add','edit_name':'page_edit','delete_name':'page_delete'})
@login_required
def page_add(request): return crud(request,NavigationPageForm,NavigationPage,'dashboard/form.html','Create Page','page_list')
@login_required
def page_edit(request,pk): return crud(request,NavigationPageForm,NavigationPage,'dashboard/form.html','Edit Page','page_list',pk)
@login_required
@require_POST
def page_delete(request,pk): return delete_obj(request,NavigationPage,pk,'page_list')

RESOURCE_MAP={
 'page_documents':(PageDocument,PageDocumentForm,'Page Documents','Upload Page Document','page_document_add','page_document_edit','page_document_delete'),
 'page_links':(PageLink,PageLinkForm,'Page Links','Create Page Link','page_link_add','page_link_edit','page_link_delete'),
 'page_images':(PageImage,PageImageForm,'Page Images','Upload Page Image','page_image_add','page_image_edit','page_image_delete'),
 'navigation_documents':(NavigationDocument,NavigationDocumentForm,'Navigation Documents','Upload Navigation Document','navigation_document_add','navigation_document_edit','navigation_document_delete'),
 'navigation_links':(NavigationLink,NavigationLinkForm,'Navigation Links','Create Navigation Link','navigation_link_add','navigation_link_edit','navigation_link_delete'),
 'navigation_images':(NavigationImage,NavigationImageForm,'Navigation Images','Upload Navigation Image','navigation_image_add','navigation_image_edit','navigation_image_delete'),
}
@login_required
def resource_list(request,key):
    model,form,title,_,_,_,_=RESOURCE_MAP[key]
    return render(request,'dashboard/list.html',{'title':title,'description':'Database-managed resources.','items':model.objects.all(),'kind':'resource','resource_key':key,'add_name':key+'_add','edit_name':key+'_edit','delete_name':key+'_delete'})
@login_required
def resource_add(request,key):
    model,form,_,title,add,edit,delete=RESOURCE_MAP[key]; return crud(request,form,model,'dashboard/form.html',title,key+'_list')
@login_required
def resource_edit(request,key,pk):
    model,form,_,title,add,edit,delete=RESOURCE_MAP[key]; return crud(request,form,model,'dashboard/form.html','Edit '+model.__name__,key+'_list',pk)
@login_required
def resource_delete(request,key,pk): return delete_obj(request,RESOURCE_MAP[key][0],pk,key+'_list')

@login_required
def banner_list(request): return render(request,'dashboard/list.html',{'title':'Banners','description':'Homepage hero content and carousel slides.','items':Banner.objects.annotate(button_count=Count('buttons')).all(),'kind':'banner','add_name':'banner_add','edit_name':'banner_edit','delete_name':'banner_delete'})
@login_required
def banner_add(request): return crud(request,BannerForm,Banner,'dashboard/form.html','Create Banner','banner_list')
@login_required
def banner_edit(request,pk): return crud(request,BannerForm,Banner,'dashboard/form.html','Edit Banner','banner_list',pk)
@login_required
@require_POST
def banner_delete(request,pk): return delete_obj(request,Banner,pk,'banner_list')
@login_required
def banner_buttons(request,banner_pk):
    b=get_object_or_404(Banner,pk=banner_pk); return render(request,'dashboard/buttons.html',{'banner':b,'items':b.buttons.all()})
@login_required
def banner_button_add(request,banner_pk):
    b=get_object_or_404(Banner,pk=banner_pk)
    if request.method=='POST':
        form=BannerButtonForm(request.POST,request.FILES)
        if form.is_valid(): obj=form.save(commit=False); obj.banner=b; obj.save(); log(request,'created',obj); messages.success(request,'Banner button saved.'); return redirect('banner_buttons',banner_pk=b.pk)
    else: form=BannerButtonForm(initial={'banner':b.pk})
    form.fields['banner'].widget=forms.HiddenInput() if False else form.fields['banner'].widget
    return render(request,'dashboard/form.html',{'form':form,'title':'Add Banner Button'})
@login_required
def banner_button_edit(request,pk):
    obj=get_object_or_404(BannerButton,pk=pk)
    if request.method=='POST':
        form=BannerButtonForm(request.POST,request.FILES,instance=obj)
        if form.is_valid(): obj=form.save(); log(request,'updated',obj); messages.success(request,'Banner button updated.'); return redirect('banner_buttons',banner_pk=obj.banner_id)
    else: form=BannerButtonForm(instance=obj)
    return render(request,'dashboard/form.html',{'form':form,'title':'Edit Banner Button'})
@login_required
@require_POST
def banner_button_delete(request,pk):
    obj=get_object_or_404(BannerButton,pk=pk); b=obj.banner; name=str(obj); obj.delete(); ActivityLog.objects.create(user=request.user,action='deleted',object_type='BannerButton',object_name=name); messages.success(request,'Banner button deleted.'); return redirect('banner_buttons',banner_pk=b.pk)
@login_required
@require_POST
def banner_button_main(request,pk):
    obj=get_object_or_404(BannerButton,pk=pk); BannerButton.objects.filter(banner=obj.banner).update(is_main=False); obj.is_main=True; obj.save(); messages.success(request,'Main button updated.'); return redirect('banner_buttons',banner_pk=obj.banner_id)
@login_required
def banner_preview(request,pk): return render(request,'frontend/banner_preview.html',{'banner':get_object_or_404(Banner.objects.prefetch_related('buttons'),pk=pk)})

@login_required
def news_list(request): return render(request,'dashboard/list.html',{'title':'News & Updates','description':'Editorial updates shown on the homepage.','items':News.objects.all(),'kind':'news','add_name':'news_add','edit_name':'news_edit','delete_name':'news_delete'})
@login_required
def news_add(request): return crud(request,NewsForm,News,'dashboard/form.html','Create News','news_list')
@login_required
def news_edit(request,pk): return crud(request,NewsForm,News,'dashboard/form.html','Edit News','news_list',pk)
@login_required
@require_POST
def news_delete(request,pk): return delete_obj(request,News,pk,'news_list')

@login_required
def profile(request): return render(request,'dashboard/profile.html')
@login_required
def settings_page(request): return render(request,'dashboard/settings.html')
