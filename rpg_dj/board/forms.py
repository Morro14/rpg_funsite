from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Comment


class PostForm(forms.ModelForm):
#    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = ['head', 'content_upload']


class CommentsForm(forms.Form):
    all = 'all'
    weekly = 'weekly'
    daily = 'daily'
    test_choice = 'test_choice'
    choices = [
        (all, 'All'),
        (daily, 'Last hour comments'),
        (weekly, 'Weekly comments'),
        (test_choice, 'Test choice')
    ]

    time_period = forms.ChoiceField(required=False, choices=choices, label='Time period')


class CommentNewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]




