from django.urls import path
from . import views # 현재 폴더에 있는 views 에서 가져옴

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'), # articles views 에 있는 index 파일
    path('create/', views.create, name='create'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/update/', views.update, name='update'),
]