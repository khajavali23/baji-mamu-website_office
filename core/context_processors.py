from .models import Navbar

def site_navigation(request):
    qs=Navbar.objects.filter(is_active=True).prefetch_related('items__children__children__children__children','items__page','items__navigation_document','items__navigation_link','items__navigation_image')
    return {'navbars':qs}
