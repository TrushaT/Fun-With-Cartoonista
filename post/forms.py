from django import forms 
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','caption','tags']

        widgets= {
            'title' : forms.TextInput(attrs={'class': 'form-control', }),
            'caption': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control','data-role': 'tagsinput'}),
            
            
        }

class SearchForm(forms.Form):
    txtSearch = forms.CharField(max_length=20)

