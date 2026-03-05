from django.contrib import admin
from .models import (
    Province, Division, SubDivision, City, Territory, 
    School, QuestionTemplate, Question, Groupe, Campaign, Recolte
)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'principal_town')
    search_fields = ('name', 'code')

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'code')
    search_fields = ('name', 'code')
    list_filter = ('province',)

@admin.register(SubDivision)
class SubDivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'code')
    search_fields = ('name', 'code')
    list_filter = ('division',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'code')
    search_fields = ('name',)
    list_filter = ('province',)

@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'code')
    search_fields = ('name',)
    list_filter = ('province',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'adm_code', 'province', 'division')
    search_fields = ('name', 'adm_code')
    list_filter = ('province', 'division')

@admin.register(QuestionTemplate)
class QuestionTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)
    ordering = ('order',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
    filter_horizontal = ('question_templates',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'template', 'groupe', 'kind')
    search_fields = ('text',)
    list_filter = ('template', 'groupe', 'kind')

@admin.register(Recolte)
class RecolteAdmin(admin.ModelAdmin):
    list_display = ('id', 'establishment', 'date', 'collector_id', 'status')
    search_fields = ('establishment__name',)
    list_filter = ('status', 'type', 'date')
