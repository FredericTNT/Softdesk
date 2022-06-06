"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from deskapi.views import ProjectList, ProjectDetail, IssueList, IssueDetail, CommentList, CommentDetail, ProjectViewSet


router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/projects/', ProjectList.as_view()),
    path('api/projects/<int:id_project>/', ProjectDetail.as_view()),
    path('api/projects/<int:id_project>/issues/', IssueList.as_view()),
    path('api/projects/<int:id_project>/issues/<int:id_issue>/', IssueDetail.as_view()),
    path('api/projects/<int:id_project>/issues/<int:id_issue>/comments/', CommentList.as_view()),
    path('api/projects/<int:id_project>/issues/<int:id_issue>/comments/<int:id_comment>/', CommentDetail.as_view()),
    path('db/', include(router.urls)),
]
