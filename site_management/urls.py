"""pydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (home)
from .views import (department_new, department_list, department_specific, department_update, department_delete)
from .views import (module_new, module_list, module_specific, module_update, module_delete)
from .views import (target_new, target_list, target_specific, target_update, target_delete)
from .views import (module_target_map_new, module_target_map_list, module_target_specific, module_target_update, module_target_delete)
from .views import (department_module_map_new, department_module_map_list, department_module_specific, department_module_update, department_module_delete)
from .views import (department_group_new, department_group_list, department_group_specific, department_group_update, department_group_delete)

urlpatterns = [
    path('', home, name='site_management__home'),

    path('department/new/', department_new, name='site_management__department__new'),
    path('department/list/', department_list, name='site_management__department__list'),
    path('department/update/<str:slug>/', department_update, name='site_management__department__update'),
    path('department/delete/<str:slug>/', department_delete, name='site_management__department__delete'),
    path('department/<str:slug>/', department_specific, name='site_management__department__specific'),

    path('department_group/new/', department_group_new, name='site_management__department_group__new'),
    path('department_group/list/', department_group_list, name='site_management__department_group__list'),
    path('department_group/update/<str:slug>/', department_group_update, name='site_management__department_group__update'),
    path('department_group/delete/<str:slug>/', department_group_delete, name='site_management__department_group__delete'),
    path('department_group/<str:slug>/', department_group_specific, name='site_management__department_group__specific'),



    path('module/new/', module_new, name='site_management__module__new'),
    path('module/list/', module_list, name='site_management__module__list'),
    path('module/update/<str:slug>/', module_update, name='site_management__module__update'),
    path('module/delete/<str:slug>/', module_delete, name='site_management__module__delete'),
    path('module/<str:slug>/', module_specific, name='site_management__module__specific'),

    path('target/new/', target_new, name='site_management__target__new'),
    path('target/list/', target_list, name='site_management__target__list'),
    path('target/update/<str:slug>/', target_update, name='site_management__target__update'),
    path('target/delete/<str:slug>/', target_delete, name='site_management__target__delete'),
    path('target/<str:slug>/', target_specific, name='site_management__target__specific'),


    path('module_target_map/new/', module_target_map_new, name='site_management__module_target_map__new'),
    path('module_target_map/list/', module_target_map_list, name='site_management__module_target_map__list'),
    path('module_target_map/update/<str:slug>/', module_target_update, name='site_management__module_target_map__update'),
    path('module_target_map/delete/<str:slug>/', module_target_delete, name='site_management__module_target_map__delete'),
    path('module_target_map/<str:slug>/', module_target_specific, name='site_management__module_target_map__specific'),

    path('department_module_map/new/', department_module_map_new, name='site_management__department_module_map__new'),
    path('department_module_map/list/', department_module_map_list, name='site_management__department_module_map__list'),
    path('department_module_map/update/<str:slug>/', department_module_update, name='site_management__department_module_map___update'),
    path('department_module_map/delete/<str:slug>/', department_module_delete, name='site_management__department_module_map___delete'),
    path('department_module_map/<str:slug>/', department_module_specific, name='site_management__department_module_map___specific'),
]