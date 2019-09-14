from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from blog.models import Post

# 모델에서 포스트를 가져옴


def posts_list(request):
    posts = Post.objects.order_by('-created_at')
    # -붙이면 최신순으로 내림차순
    return render(request, 'blog/posts_list.html', context={'posts': posts})
    # 컨텍스트에서 넣어주고 렌더에서 넣어주는데 앱의 urls.py가 posts_list함수를를
    # path('post/', views.posts_list, name='post_list'),로 바꿔줌


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    return render(request, 'blog/post_detail.html', context={'post': post})

# @login_required


def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(
                user=request.user, title=title, content=content, image=image)

            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))
            # 리버스는 포스트아이디의 주소를 만들어준다라는의미 밑의것과 같다.
            # /post/%d/ % post.id == reverse('post_detail', kwargs= [post.id, article.id]}
            # 여러개받을때는 kwargs가 나음 키벨류형태에서 에러가 안남 args는 하나씩만 받음
    return render(request, 'blog/post_write.html', {'user': request.user, 'errors': errors})
