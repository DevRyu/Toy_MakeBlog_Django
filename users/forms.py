from django import forms

from .models import User


class RegisterForm(forms.ModelForm):
    # 회원가입 폼
    # 장고에서는 HTML 입력 요소를 widget(위젯) 이라고 말한다.
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='confirm password', widget=forms.PasswordInput)
    # 패스워드 필드도 있지만 캐릭터필드로 위젯인 옵션으로 패스워드 태그를 인풋햇다라고 보면됨

    # 메타 데이터 명세
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'email']

    def clean_confirm_password(self):
        # 비밀번호 일치 유효성 검사
        cd = self.cleaned_data
        # cd는 cleaned_data약자라고 보셈
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다!')

        return cd['confirm_password']
