# serializers.py
from rest_framework import serializers
from .models import School, Question, QuestionTemplate, Recolte
from django.contrib.auth.models import User

class SchoolSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source="province.name", read_only=True)
    division_name = serializers.CharField(source="division.name", read_only=True)
    sub_division_name = serializers.CharField(source="sub_division.name", read_only=True)

    class Meta:
        model = School
        fields = "__all__"

class SchoolSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["adm_code", "updated_at"]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "kind",
            "options",
        ]
class QuestionTemplateSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionTemplate
        fields = [
            "id",
            "name",
            "type",
            "questions",
        ]

class RecolteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recolte
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]