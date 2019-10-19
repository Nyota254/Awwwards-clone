from django.shortcuts import render,redirect
from .forms import ProjectUploadForm,RatingUploadForm
from django.contrib.auth.decorators import login_required
from .models import Project,Rating

def Index_view(request):
    '''
    This is the function based view for the homepage
    '''
    title = "home"
    projects = Project.objects.all().order_by('-pk')
    context = {
        "title":title,
        "projects":projects,
    }
    
    return render(request,"main/index.html",context)

@login_required
def Upload_Project(request):
    '''
    This is the function based view for uploading a project to the site
    '''
    current_user = request.user
    if request.method == "POST":
        form = ProjectUploadForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
            return redirect(Index_view)
    else:
        form = ProjectUploadForm()
    context = {
        "form":form
    }

    return render(request,"main/upload_project.html",context)
