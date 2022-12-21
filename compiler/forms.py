from django import forms
from django.forms import Form
from django.forms import ModelForm
from .models import SaveFiles,Customer,Collaboration,Projet


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
languages = [(1,"python")]
languages = [(1,"python")]

class CodeExecutorForm(Form):
    has_template = forms.BooleanField(required=False,label='Enable Template?')
    code = forms.CharField(widget=forms.Textarea,label='Code',)
	
    input = forms.CharField(widget=forms.Textarea,label='Input',required=False)
    output = forms.CharField(widget=forms.Textarea,label='Output',required=True)
    language=forms.ChoiceField(choices=languages,label='Language')

		

class createprojetforms(ModelForm):
	class Meta:
		model = Projet
		fields = ['name']
		exclude = ['user']

class SaveFileForms(Form):
	class Meta:
		model = SaveFiles
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CollaborationForm(ModelForm):
	class Meta:
		model = Collaboration
        
		fields = ['members']
		exclude = ['user']
class Accepter_CollaborationForm(ModelForm):
	class Meta:
		model = Collaboration
		fields = ['Accepter']
