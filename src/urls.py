"""Diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from src.global_constants import LOCAL_ENV

api_v1_urlpatterns: list[path] = [
    # path('auth/', include(('auth.urls', 'auth'), namespace='project_auth')),
    path('employees/', include(('employee.urls', 'employee'), namespace='employee')),
    path('reviews/', include(('performance_review.urls', 'performance_review'), namespace='performance_review')),
    ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_v1_urlpatterns, 'api_v1'))),
]

if settings.ENVIRONMENT == LOCAL_ENV:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
