from django import forms

class createPost(forms.Form):
    content = forms.CharField(label="Post", widget=forms.Textarea, max_length=200)
