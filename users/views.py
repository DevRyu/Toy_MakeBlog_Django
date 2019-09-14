from django.shortcuts import render

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        # 레지스터 요청이 있을시 생성은 포스트로
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            # 생성시 유효하면
            user = user_form.save(commit=False)
            # 커밋 false로 옵션을줘서 Db에 바로저장이 아닌 메모리상에서 객체로 저장
            user.set_password(user_form.cleaned_data['password'])
            # 비밀번호를 셋하고
            user.save()
            # 비밀번호까지 완료시 save()호출해서  DB 저장
            return render(request, 'registration/login.html', {'user': user})
    else:
            # 렌더링해줌
        user_form = RegisterForm()
        # 유저 생성이 아니면 레지스터 폼만 보여주도록 한다.
    return render(request, 'registration/register.html', {'user_form': user_form})
