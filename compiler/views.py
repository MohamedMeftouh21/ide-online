from django.shortcuts import render, redirect 
from django.http import HttpResponse
from . import forms
from . import CompilerUtils
from .CompilerUtils import Compiler, Language
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .forms import  CreateUserForm,CollaborationForm,createprojetforms
from django.contrib.sessions.models import Session

from django.contrib.auth.decorators import login_required
from .forms import  CreateUserForm
from django.db import transaction
from .decorators import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='login')


def test(request,pk):
 author = Customer.objects.get(user=request.user)
 project_test = Projet.objects.get(id=pk)
 display_data = []
 display_data_forms=[]

 
 
 if Projet.objects.filter(id=pk,user=author).exists() or  Collaboration.objects.filter(project=project_test,members=author).exists():
    template_data = {}
    author = Customer.objects.get(user=request.user)

    
    if request.method == 'POST':
        form = forms.CodeExecutorForm(request.POST)
       
        if form.is_valid():
            project_name = Projet.objects.get(id=pk)
           
            executor = Compiler()
            code = form.cleaned_data['code']
            input_data = form.cleaned_data['input']
            projet=   Projet.objects.get(id=pk)

            expected_output = form.cleaned_data['output']
            #if pour verifié la authourisation  dans le projet ou dans la collaboration
            if SaveFiles.objects.filter(projet=project_name).exists():
                      if Collaboration.objects.filter(project=project_name,creater=request.user,Accepter=True).exists() or Collaboration.objects.filter(project=project_name,members=author,Accepter=True).exists():

                      
                         SaveFiles.objects.filter(projet=projet).update(code = code,user=author)
                       
                      else:   

                                               SaveFiles.objects.filter(projet=projet).update(code = code,user=author)

                     

            elif Collaboration.objects.filter(project=project_name,creater=request.user,Accepter=True).exists() or Collaboration.objects.filter(project=project_name,members=author,Accepter=True).exists():
                          v=SaveFiles.objects.create(code=code,user=author,projet=projet,)
                          v.save()
            else:
                    v=SaveFiles.objects.create(code=code,user=author,projet=projet,)
                    v.save()


            test_cases = CompilerUtils.generate_test_cases(input_data, expected_output)
            for test_case in test_cases:
                executor.add_test_case(test_case)
            lan = Language(int(form.cleaned_data['language']))
            has_template = form.cleaned_data['has_template']
            if has_template:
                code_template = form.cleaned_data['template']
            if len(input_data) == 0 or input_data is None:
                template_data['error'] = "Invalid code"
                return render(request, 'generic_error.html', template_data)
            else:
                if lan == Language.PYTHON:
                    executor.set_code(code)
                    executor.set_language(lan)
                    if has_template:
                        executor.set_template(code_template)
                    execution_result = executor.execute()
                    template_data['result'] = execution_result.name
                    template_data['test_cases_total'] = executor.get_num_test_cases()
                    if executor.get_num_failed_test_cases() is not None:
                        template_data['test_cases_passed'] = executor.get_num_test_cases() - executor.get_num_failed_test_cases()
                    executor.delete_code_file()
                    if executor.hasExecuted:
                        checked_values = executor.compare_outputs()
                        outputs = executor.get_output()
                        errors = executor.get_errors()
                        for i in range(len(outputs)):
                            if executor.hasErrors:
                                e = errors[i]
                            else:
                                e = "No errors!"
                            temp_tuple = (i+1, checked_values[i], outputs[i], e)
                            display_data.append(temp_tuple)
                          
                        template_data['display_data'] = display_data
                       
                        return render(request, 'OutputView.html', template_data)
                    else:
                        return render(request, 'generic_error.html', {'error': 'Sorry! Execution failed'})
        else:
            return HttpResponse("Cannot sanitize form data")
    else:
        form = forms.CodeExecutorForm()
      
        project_name2 = Projet.objects.get(id=pk)
        # if else filter
        if SaveFiles.objects.filter(projet=project_name2).exists():
            project_1= SaveFiles.objects.filter(projet=project_name2)[0]
        else:
                        project_1= SaveFiles.objects.filter(projet=project_name2)

          
     
        template_data['form'] = form
        template_data['display_data_forms'] = display_data_forms
     

        context = {'form':form,'project_1':project_1,'display_data_forms':display_data_forms}

        return render(request, 'test.html', context)
        
 else:
            return redirect('createprojet')


def error_404_view(request, exception):
    return render(request,'404.html')  

@login_required(login_url='login')

def createprojet(request):
    context = {}

    author = Customer.objects.get(user=request.user)

    project_name = Projet.objects.filter(user=author)
    liste_Collaboration=Collaboration.objects.filter(members=author,Accepter=True) 
    liste=Collaboration.objects.filter(creater=request.user,Accepter=True)

    context = {'project_name':project_name,'liste_Collaboration':liste_Collaboration,'liste':liste
    }
    form = createprojetforms(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            print("\n\n form is valid")
            name = form.cleaned_data['name']

            author = Customer.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
         
            if Projet.objects.filter(name=name,user=author).exists():
                           return HttpResponse("le nom de Projet est deja existe")

            else:

               new_post.save()
               return redirect('/')


  
            
        
    context.update({
            'form': form,
            'project_name':project_name,
            'liste_Collaboration':liste_Collaboration,
            'liste':liste
    })
    return render(request, 'accounts/main.html', context)	




@login_required(login_url='login')

def liste_Collaboration (request):
    context = {}

    author = Customer.objects.get(user=request.user)
    liste_Collaboration=Collaboration.objects.filter(members=author,Accepter=False)
    




    context.update({
         
            'liste_Collaboration':liste_Collaboration
    })    

    return render(request, 'accounts/liste_project.html', context)	
@login_required(login_url='login')

def delete_project(request, pk):
    author = Customer.objects.get(user=request.user)
    projet = Projet.objects.get(id=pk)
    SaveFiles_delete = SaveFiles.objects.filter(projet=projet)
    Collaboration_delete = Collaboration.objects.filter(project=projet)


    if request.method == 'POST':
        SaveFiles_delete.delete()
        Collaboration_delete.delete()
        projet.delete()

        return redirect('/')

    context = {'item':projet}
    return render(request, 'accounts/delete.html', context)	
@login_required(login_url='login')

def delete_Collaboration_members(request,pk_user,pk):
    author = Customer.objects.get(id=pk_user)
    projet = Projet.objects.get(id=pk)
    projet_delete_Collaboration_members = Collaboration.objects.get(project=projet,members=author)

    if request.method == 'POST':
        projet_delete_Collaboration_members.delete()
        return redirect('/')

    context = {'item':projet,'author':author}
    return render(request, 'accounts/Collaboration_delete_user.html', context)
 
	

@login_required(login_url='login')


def delete_Collaboration(request, pk):
    author = Customer.objects.get(user=request.user)
    projet = Projet.objects.get(id=pk)
    Collaboration_delete = Collaboration.objects.filter(project=projet,members=author)


    if request.method == 'POST':
        Collaboration_delete.delete()

        return redirect('/')

    context = {'item':projet}
    return render(request, 'accounts/delete_collaboration.html', context)	
    
@login_required(login_url='login')

def accepter_Collaboration (request, pk):
    author = Customer.objects.get(user=request.user)
    projet = Collaboration.objects.get(id=pk)
    if request.method == 'POST':
        Collaboration.objects.filter(id=pk,members=author).update(Accepter =True)
        return redirect('/')

    context = {'item':projet}
    return render(request, 'accounts/accepter.html', context)	



  
@login_required(login_url='login')

def save(request,pk):
    context = {}
    author = Customer.objects.get(user=request.user)
    
    project_name = SaveFiles.objects.get(id=pk)

    if request.method == 'POST':
             form = forms.SaveFileForms(request.POST)
       
             if form.is_valid():
                 code = form.cleaned_data['code']
                 input_data = form.cleaned_data['input']
                 name = form.cleaned_data['name']

                 expected_output = form.cleaned_data['output']
                 print(code)
                 v=SaveFiles.objects.create(code=code,scriptFiles=pk,name=name,user=author,)
                 v.save()  

    context.update({
         
            'project_name':project_name
    })    

    return render(request, 'test-compiler.html',context)

        


@unauthenticated_user

def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

		
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		
    
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('createprojet')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)
@login_required(login_url='login')

def logoutUser(request):
	logout(request)
	return redirect('login')
@login_required(login_url='login')

def home(request):

    author = Customer.objects.get(user=request.user)
    project_name = SaveFiles.objects.filter(user=author)
    context = {'project_name':project_name}
    return render(request, 'accounts/main.html', context)

@login_required(login_url='login')

def Collaboratio_projet(request,pk):
 author = Customer.objects.get(user=request.user)
 project_test = Projet.objects.get(id=pk)
 customer = Customer.objects.all()
 Collaboration_liste = Collaboration.objects.filter(project=project_test,Accepter=True)


 if Projet.objects.filter(id=pk,user=author).exists() or  Collaboration.objects.filter(project=project_test,members=author).exists():
    context = {}
    project_name = Projet.objects.get(id=pk)
    
    context = {'project_name':project_name}
    form = CollaborationForm(request.POST or None)
#if else pour savefile class
    if request.method == "POST":

        if form.is_valid():
            print("\n\n form is valid")
            selected_members = form.cleaned_data.get('members')
            print(selected_members)

            author = Customer.objects.get(user=request.user)
            if Collaboration.objects.filter(project=project_name,creater=request.user,members=selected_members).exists():
                               return HttpResponse("L'invitation est déjà envoyé")

            else:
                v=Collaboration.objects.create(creater=request.user,project=project_name,members=selected_members)
                v.save()
 
              



              
                 
                


               
  
            
        
    context.update({
            'form': form,
            'title': 'Create New Post',
            'project_name':project_name,
            'Collaboration_liste':Collaboration_liste,
    })
    return render(request, 'accounts/single_project.html', context)
 else:
            return redirect('createprojet')
 
"""""
def project(request,pk):

    project_name = SaveFiles.objects.get(id=pk)
    context = {'project_name':project_name}

    return render(request, 'accounts/single_project.html', context)

def project(request,pk):

    project_name = Project_name.objects.get(id=pk)
    context = {'project_name':project_name}

    return render(request, 'accounts/single_project.html', context)

  selected_members = form.cleaned_data.get('members')
            for members in selected_members:
                  member_obj = Customer.objects.get(user=members) #get object by title i.e I declared unique for title under Category model

                  new_post.members.add(member_obj)

  

"""
		
      
            