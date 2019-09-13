from django.shortcuts import render
from blog.models import Post
# 모델에서 포스트를 가져옴


def posts_list(request):
    posts = Post.objects.order_by('-created_at')
    # -붙이면 최신순으로 내림차순
    return render(request, 'blogs/posts_list.html', context={'posts': posts})
    # 컨텍스트에서 넣어주고 렌더에서 넣어주는데 앱의 urls.py가 posts_list함수를를
    # path('post/', views.posts_list, name='post_list'),로 바꿔줌
