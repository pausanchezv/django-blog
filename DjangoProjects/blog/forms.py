from django import forms


class RegisterForm(forms.Form):
    """ Register form """

    username = forms.CharField(label='Your name', max_length=30, required=True)
    email = forms.EmailField(label='Your email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class ArticleForm(forms.Form):
    """ Article form """

    title = forms.CharField(label='Enter title', max_length=100, required=True)
    body = forms.CharField(widget=forms.Textarea, required=True)
    image = forms.ImageField()


class UserEditForm(forms.Form):
    """ Article form """

    username = forms.CharField(label='Your name', max_length=30, required=True)
    email = forms.EmailField(label='Your email', required=True)
    image = forms.ImageField()
