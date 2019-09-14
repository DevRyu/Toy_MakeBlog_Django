from django.urls import path

from . import views
# 뷰에서 렌더한걸 urls에서 가져옴
urlpatterns = [
    path('post/', views.posts_list, name='posts_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/write', views.post_write, name='post_write'),

]
