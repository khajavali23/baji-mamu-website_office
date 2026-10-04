from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # FRONTEND
    # =====================================================

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'page/<int:pk>/',
        views.page_detail,
        name='page_detail'
    ),

    path(
        'navigation/<int:pk>/',
        views.navigation_detail,
        name='navigation_detail'
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'dashboard/search/',
        views.search,
        name='search'
    ),


    # =====================================================
    # NAVBARS
    # =====================================================

    path(
        'dashboard/navbars/',
        views.navbars,
        name='navbars'
    ),

    path(
        'dashboard/navbars/add/',
        views.navbar_add,
        name='navbar_add'
    ),

    path(
        'dashboard/navbars/<int:pk>/edit/',
        views.navbar_edit,
        name='navbar_edit'
    ),

    path(
        'dashboard/navbars/<int:pk>/delete/',
        views.navbar_delete,
        name='navbar_delete'
    ),


    # =====================================================
    # NAVIGATION
    # =====================================================

    path(
        'dashboard/navigation/',
        views.navigation_list,
        name='navigation_list'
    ),

    path(
        'dashboard/navigation/add/',
        views.navigation_add,
        name='navigation_add'
    ),

    path(
        'dashboard/navigation/add/<int:parent_pk>/',
        views.navigation_add,
        name='navigation_child_add'
    ),

    path(
        'dashboard/navigation/<int:pk>/edit/',
        views.navigation_edit,
        name='navigation_edit'
    ),

    path(
        'dashboard/navigation/<int:pk>/delete/',
        views.navigation_delete,
        name='navigation_delete'
    ),


    # =====================================================
    # PAGES
    # =====================================================

    path(
        'dashboard/pages/',
        views.page_list,
        name='page_list'
    ),

    path(
        'dashboard/pages/add/',
        views.page_add,
        name='page_add'
    ),

    path(
        'dashboard/pages/<int:pk>/edit/',
        views.page_edit,
        name='page_edit'
    ),

    path(
        'dashboard/pages/<int:pk>/delete/',
        views.page_delete,
        name='page_delete'
    ),


    # =====================================================
    # BANNERS
    # =====================================================

    path(
        'dashboard/banners/',
        views.banner_list,
        name='banner_list'
    ),

    path(
        'dashboard/banners/add/',
        views.banner_add,
        name='banner_add'
    ),

    path(
        'dashboard/banners/<int:pk>/edit/',
        views.banner_edit,
        name='banner_edit'
    ),

    path(
        'dashboard/banners/<int:pk>/delete/',
        views.banner_delete,
        name='banner_delete'
    ),

    path(
        'dashboard/banners/<int:banner_pk>/buttons/',
        views.banner_buttons,
        name='banner_buttons'
    ),

    path(
        'dashboard/banners/<int:banner_pk>/buttons/add/',
        views.banner_button_add,
        name='banner_button_add'
    ),

    path(
        'dashboard/banner-buttons/<int:pk>/edit/',
        views.banner_button_edit,
        name='banner_button_edit'
    ),

    path(
        'dashboard/banner-buttons/<int:pk>/delete/',
        views.banner_button_delete,
        name='banner_button_delete'
    ),

    path(
        'dashboard/banner-buttons/<int:pk>/main/',
        views.banner_button_main,
        name='banner_button_main'
    ),

    path(
        'dashboard/banners/<int:pk>/preview/',
        views.banner_preview,
        name='banner_preview'
    ),


    # =====================================================
    # NEWS
    # =====================================================

    path(
        'dashboard/news/',
        views.news_list,
        name='news_list'
    ),

    path(
        'dashboard/news/add/',
        views.news_add,
        name='news_add'
    ),

    path(
        'dashboard/news/<int:pk>/edit/',
        views.news_edit,
        name='news_edit'
    ),

    path(
        'dashboard/news/<int:pk>/delete/',
        views.news_delete,
        name='news_delete'
    ),


    # =====================================================
    # PROFILE & SETTINGS
    # =====================================================

    path(
        'dashboard/profile/',
        views.profile,
        name='profile'
    ),

    path(
        'dashboard/settings/',
        views.settings_page,
        name='settings'
    ),
]


# =========================================================
# RESOURCE ROUTES
# =========================================================

for key in views.RESOURCE_MAP:

    base = key.replace('_', '-')

    urlpatterns += [

        path(
            f'dashboard/{base}/',
            views.resource_list,
            name=key + '_list',
            kwargs={'key': key}
        ),

        path(
            f'dashboard/{base}/add/',
            views.resource_add,
            name=key + '_add',
            kwargs={'key': key}
        ),

        path(
            f'dashboard/{base}/<int:pk>/edit/',
            views.resource_edit,
            name=key + '_edit',
            kwargs={'key': key}
        ),

        path(
            f'dashboard/{base}/<int:pk>/delete/',
            views.resource_delete,
            name=key + '_delete',
            kwargs={'key': key}
        ),
    ]