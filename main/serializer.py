from rest_framework import serializers
from .models import Project
from users.models import Profile

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("user","id","title","description","link")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user","profile_pic","bio")