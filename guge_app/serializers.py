# serializers.py
from rest_framework import serializers
from .models import School, Question, QuestionTemplate, Recolte, Groupe, Campaign
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

class GroupeInfoSerializer(serializers.ModelSerializer):
    """Serializer used to represent group info as a simple dict."""
    class Meta:
        model = Groupe
        fields = [
            "id",
            "name",
            "order",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    # show the groupe field as a nested dict instead of just the PK
    groupe = GroupeInfoSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "kind",
            "options",
            "groupe",
        ]


class GroupeSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Groupe
        fields = [
            "id",
            "name",
            "description",
            "order",
            "questions",
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


class CampaignSerializer(serializers.ModelSerializer):
    question_templates = QuestionTemplateSerializer(many=True, read_only=True)
    recolte_count = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "comments",
            "question_templates",
            "recolte_count",
            "created_at",
            "updated_at",
        ]

    def get_recolte_count(self, obj):
        return obj.recoltes.count()


class RecolteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recolte
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]