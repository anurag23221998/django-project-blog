from django import forms
from .models import Post
from django.forms import ModelForm

class CreatePost(ModelForm):
    title = forms.CharField(
        label='Post Title',
        help_text='Title of the post comes here', 
        widget=forms.TextInput(attrs={'class': "form-control"}),
        error_messages={'blank' : 'Test Error'}
    )
    content = forms.CharField(
        label = 'Post Content',
        help_text="Content of the post comes here",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']