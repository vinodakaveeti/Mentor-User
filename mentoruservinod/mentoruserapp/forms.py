from django.contrib.auth.forms import UserCreationForm, UserChangeForm, forms
from datetime import datetime
from .models import CustomUser, Conversation


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ConversationForm(forms.ModelForm):
    document = forms.FileField()

    class Meta(forms.ModelForm):
        model = Conversation
        fields = ('sender', 'conversation', 'receipient', 'sent_at', 'document')

    # To get the required fields to show in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender'].queryset = CustomUser.objects.filter(email=kwargs['instance'].email)
        self.fields['receipient'].queryset = CustomUser.objects.filter(is_mentor=True)

    # overriding the save method in order to store the fields into the DB
    def save(self, commit=True):
        data = self.cleaned_data
        conversation = Conversation(
            sender=data['sender'], conversation=data['conversation'],
            receipient=data['receipient'], sent_at=datetime.now(),
            document=data['document']
        )
        conversation.save()


class MentorConversationForm(forms.ModelForm):
    reply = forms.Textarea()

    class Meta(forms.ModelForm):
        model = Conversation
        fields = ('sender', 'reply')

    # To get the required fields to show in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender'].queryset = CustomUser.objects.filter(email=kwargs['instance'].sender)
