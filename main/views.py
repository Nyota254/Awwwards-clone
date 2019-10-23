from django.shortcuts import render,redirect
from .forms import ProjectUploadForm,RatingUploadForm
from django.contrib.auth.decorators import login_required
from .models import Project,Rating
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
from users.models import Profile
from django.contrib.auth.models import User

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

@login_required
def RateProject(request,pk):
    '''
    Function to display single Project and rate it
    '''
    project = Project.objects.get(id=pk)
    title = "Rating"
    current_user = request.user
    project_rating = Rating.objects.filter(project=project).order_by("pk")
    current_user_id = request.user.id
    project_rated = Rating.objects.filter(user=current_user_id)


    design_mean_rating = []
    for d_rating in project_rating:
        design_mean_rating.append(d_rating.design)
    try:
        design_average = sum(design_mean_rating)/len(design_mean_rating)
        design_percent = design_average * 10
    except ZeroDivisionError:
        design_average = "no ratings yet"
        design_percent = 0

    usability_mean_rating = []
    for u_rating in project_rating:
        usability_mean_rating.append(u_rating.usability)
    try:
        usability_average = sum(usability_mean_rating)/len(usability_mean_rating)
        usability_percent = usability_average *10
    except ZeroDivisionError:
        usability_average = "no ratings yet"
        usability_percent = 0
    
    content_mean_rating = []
    for c_rating in project_rating:
        content_mean_rating.append(c_rating.content)
    try:
        content_average = sum(content_mean_rating)/len(content_mean_rating)
        content_percent = content_average * 10
    except ZeroDivisionError:
        content_average = "no ratings yet"
        content_percent = 0

    if request.method == "POST":
        form = RatingUploadForm(request.POST)
        if form.is_valid() and project_rated is None:
            rating = form.save(commit=False)
            rating.user = current_user
            rating.project = project
            rating.save()
            return redirect(RateProject)
        elif form.is_valid() and project_rated is not None:
            project_rated.delete()
            rating = form.save(commit=False)
            rating.user = current_user
            rating.project = project
            rating.save()
            return redirect(RateProject,pk)
    else:
        form = RatingUploadForm()

    context = {
        "project":project,
        "form":form,
        "project_rating":project_rating,
        "design_average":design_average,
        "content_average":content_average,
        "usability_average":usability_average,
        "usability_percent":usability_percent,
        "content_percent":content_percent,
        "design_percent":design_percent
    }

    return render(request,"main/rateproject.html",context)

@login_required
def User_Profile(request):
    current_user = request.user
    context = {
        "current_user":current_user
    }
    return render(request,"main/profile_details.html",context)

@login_required
def Dev_center(request):
    title = "Devcenter"
    context = {
        "title":title
    }
    return render(request,"main/devcenter.html",context)
    
class ProjectList(APIView):
    def get(self,request,format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects,many=True)
        return Response(serializers.data)

class ProfileList(APIView):
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)