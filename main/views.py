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
    # design_mean_rating = project.aggregate(Avg('design'))

    if request.method == "POST":
        form = RatingUploadForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = current_user
            rating.project = project
            rating.save()
            return redirect(RateProject)
    else:
        form = RatingUploadForm()

    context = {
        "project":project,
        "form":form,
        "project_rating":project_rating,
    }

    return render(request,"main/rateproject.html",context)

@login_required
def User_Profile(request):
    current_user = request.user
    context = {
        "current_user":current_user
    }
    return render(request,"main/profile_details.html",context)
    
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