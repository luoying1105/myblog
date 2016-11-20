from django import forms
from .models import Comment,Ticket
"""
git remote add origin https://github.com/luoying1105/myblog.git
git push -u origin master
"""
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('name', 'email', 'body')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('choice',)