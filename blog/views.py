from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from blog.models import Post, Comment

# 모델에서 포스트를 가져옴


def posts_list(request):
    posts = Post.objects.order_by('-created_at')
    # -붙이면 최신순으로 내림차순
    return render(request, 'blog/posts_list.html', context={'posts': posts})
    # 컨텍스트에서 넣어주고 렌더에서 넣어주는데 앱의 urls.py가 posts_list함수를를
    # path('post/', views.posts_list, name='post_list'),로 바꿔줌


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post.id)
    # 코멘트의 오브젝트를 게시글 번호로 가져온다
    is_liked = False
    # 기본적으로 좋아요는 false
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    # 포스트 라이크를 누르면 유저 아이디가 존재하는지 필터링하고 있으면 좋아요는 true가됨
    return render(request, 'blog/post_detail.html', context={'post': post, 'comments': comments, 'is_liked': is_liked, 'total_likes': post.total_likes()})
    # 리턴해줌
# @login_required
# @require_POST
# 인증된 유저만 좋아요를 누름


def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    # 장고모델 파라미터받고 객체가 존재하지 않으면 에러발생
    is_liked = post.likes.filter(id=request.user.id).exists()

    if is_liked:
        post.likes.remove(request.user)
    # 라이크가 있으면 라이크를 지우고
    else:
        post.likes.add(request.user)
    # 라이크가 기존에 없으면 추가해줘라
    return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))


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


def comment_write(request):
    pass


# def like_toggle(request):
#     pass
