from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['password1'].label = ""
        self.fields['username'].widget.attrs.update(
            {'class': 'myfieldclass form-control'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'myfieldclass form-control'})

        # giving place holders to fields
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Enter Your Username*'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password'})

        for text in ['username', 'password1']:
            self.fields[text].help_text = None