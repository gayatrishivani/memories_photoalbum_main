from django import forms
from .models import Album,sub_album,Profile

class AlbumForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    memory_date = forms.DateField()
    description = forms.CharField(max_length=300)
    class Meta():
        model = Album
        fields = ('title','memory_date','description')


class sub_albumForm(forms.ModelForm):
    
    sub_title = forms.CharField(max_length = 100)
    
    images = forms.ImageField()
    sub_description = forms.CharField()
    class Meta():
        model = sub_album
        fields = ('sub_title','images','sub_description')
        
class profileForm(forms.ModelForm):
    
    bio = forms.CharField()
    name = forms.CharField()
    date_of_birth = forms.DateField()
    
    class Meta():
        model = Profile
        fields =('bio','name','date_of_birth')
    