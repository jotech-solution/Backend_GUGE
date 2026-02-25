from django.shortcuts import render, redirect, get_object_or_404
from .models import School, Province, Division, SubDivision, City, Territory, QuestionTemplate, Question, Recolte
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .serializers import SchoolSerializer, QuestionTemplateSerializer
from .filters import SchoolFilter
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# APIS
class QuestionTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = QuestionTemplate.objects.prefetch_related("questions").all()
    serializer_class = QuestionTemplateSerializer

    filterset_fields = ["type"]   # pour filtrer par type

class SchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = School.objects.select_related(
        "province",
        "division",
        "sub_division",
        "city",
        "territory"
    ).all()

    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = [
        "name",
        "adm_code",
        "head_name",
        "village",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

# Create your views here.
@login_required(login_url='users/login/')
def home(request):
    divisions = Division.objects.all()
    nbr_divisions = len(divisions)
    nbr_users = len(User.objects.all())
    nbr_recolte =  len(Recolte.objects.all())
    nbr_school = len(School.objects.all())
    context = {
        'divisions': divisions,
        'nbr_divisions': nbr_divisions,
        'nbr_users': nbr_users,
        'nbr_recolte': nbr_recolte,
        'nbr_school': nbr_school
    }
    return render(request, 'home.html', context)

def get_paginated_queryset(request, queryset, count=10):
    paginator = Paginator(queryset, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

@login_required(login_url='users/login/')
def school_list(request):
    schools_qs = School.objects.all().order_by('-created_at')
    schools = get_paginated_queryset(request, schools_qs)
    return render(request, 'school_list.html', {'schools': schools})

@login_required(login_url='users/login/')
def school_form(request):
    if request.method == 'POST':
        # Extraction des données du POST
        name = request.POST.get('name')
        address = request.POST.get('address')
        head_name = request.POST.get('head_name')
        head_phone = request.POST.get('head_phone')
        province_id = request.POST.get('province')
        city_id = request.POST.get('city')
        territory_id = request.POST.get('territory')
        division_id = request.POST.get('division')
        sub_division_id = request.POST.get('sub_division')
        village = request.POST.get('village')
        adm_code = request.POST.get('adm_code')
        legal_reference = request.POST.get('legal_reference')
        secope_number = request.POST.get('secope_number')
        management_regime = request.POST.get('management_regime')
        mechanized_status = request.POST.get('mechanized_status')
        ownership_status = request.POST.get('ownership_status')
        environment = request.POST.get('environment')
        regroupment_center = request.POST.get('regroupment_center')

        # Création de l'école
        School.objects.create(
            name=name, address=address, head_name=head_name, head_phone=head_phone,
            province_id=province_id, city_id=city_id, territory_id=territory_id,
            division_id=division_id, sub_division_id=sub_division_id,
            village=village, adm_code=adm_code, legal_reference=legal_reference,
            secope_number=secope_number, management_regime=management_regime,
            mechanized_status=mechanized_status, ownership_status=ownership_status,
            environment=environment, regroupment_center=regroupment_center
        )
        messages.success(request, "École ajoutée avec succès.")
        return redirect('school_list')

    provinces = Province.objects.all()
    divisions = Division.objects.all()
    sub_divisions = SubDivision.objects.all()
    cities = City.objects.all()
    territories = Territory.objects.all()

    context = {
        'provinces': provinces,
        'divisions': divisions,
        'sub_divisions': sub_divisions,
        'cities': cities,
        'territories': territories,
        'management_choices': School.MANAGEMENT_CHOICES,
        'mechanized_choices': School.MECHANIZED_CHOICES,
        'ownership_choices': School.OWNERSHIP_CHOICES,
        'environment_choices': School.ENVIRONMENT_CHOICES,
    }
    return render(request, 'school_form.html', context)

@login_required(login_url='users/login/')
def province_list(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        principal_town = request.POST.get('principal_town')
        surface = request.POST.get('surface')
        population = request.POST.get('population')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        Province.objects.create(
            code=code,
            name=name,
            principal_town=principal_town,
            surface=surface,
            population=population,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None
        )
        messages.success(request, "Province ajoutée avec succès.")
        return redirect('province_list')

    provinces_qs = Province.objects.all().order_by('name')
    provinces = get_paginated_queryset(request, provinces_qs)
    return render(request, 'province_list.html', {'provinces': provinces})

@login_required(login_url='users/login/')
def division_list(request):
    if request.method == 'POST':
        province_id = request.POST.get('province')
        code = request.POST.get('code')
        name = request.POST.get('name')
        Division.objects.create(province_id=province_id, code=code, name=name)
        messages.success(request, "Division ajoutée avec succès.")
        return redirect('division_list')

    divisions_qs = Division.objects.all().order_by('name')
    divisions = get_paginated_queryset(request, divisions_qs)
    provinces = Province.objects.all()
    return render(request, 'division_list.html', {'divisions': divisions, 'provinces': provinces})

@login_required(login_url='users/login/')
def subdivision_list(request):
    if request.method == 'POST':
        division_id = request.POST.get('division')
        code = request.POST.get('code')
        name = request.POST.get('name')
        SubDivision.objects.create(division_id=division_id, code=code, name=name)
        messages.success(request, "Sous-division ajoutée avec succès.")
        return redirect('subdivision_list')

    subdivisions_qs = SubDivision.objects.all().order_by('name')
    subdivisions = get_paginated_queryset(request, subdivisions_qs)
    divisions = Division.objects.all()
    return render(request, 'subdivision_list.html', {'subdivisions': subdivisions, 'divisions': divisions})

@login_required(login_url='users/login/')
def city_list(request):
    if request.method == 'POST':
        province_id = request.POST.get('province')
        code = request.POST.get('code')
        name = request.POST.get('name')
        City.objects.create(province_id=province_id, code=code, name=name)
        messages.success(request, "Ville ajoutée avec succès.")
        return redirect('city_list')

    cities_qs = City.objects.all().order_by('name')
    cities = get_paginated_queryset(request, cities_qs)
    provinces = Province.objects.all()
    return render(request, 'city_list.html', {'cities': cities, 'provinces': provinces})

@login_required(login_url='users/login/')
def territory_list(request):
    if request.method == 'POST':
        province_id = request.POST.get('province')
        code = request.POST.get('code')
        name = request.POST.get('name')
        Territory.objects.create(province_id=province_id, code=code, name=name)
        messages.success(request, "Territoire ajouté avec succès.")
        return redirect('territory_list')

    territories_qs = Territory.objects.all().order_by('name')
    territories = get_paginated_queryset(request, territories_qs)
    provinces = Province.objects.all()
    return render(request, 'territory_list.html', {'territories': territories, 'provinces': provinces})

@login_required(login_url='users/login/')
def question_template_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type_q = request.POST.get('type')

        QuestionTemplate.objects.create(name=name, type=type_q)
        messages.success(request, "Questionnaire ajouté avec succès.")
        return redirect('question_template_list')

    templates_qs = QuestionTemplate.objects.all().order_by('-created_at')
    templates = get_paginated_queryset(request, templates_qs)
    type_choices = QuestionTemplate.TYPE_CHOICES
    return render(request, 'question_template_list.html', {'templates': templates, 'type_choices': type_choices})

@login_required(login_url='users/login/')
def question_list(request):
    if request.method == 'POST':
        template_id = request.POST.get('template')
        text = request.POST.get('text')
        kind = request.POST.get('kind')
        options_raw = request.POST.get('options')

        options = []
        if options_raw:
            options = [opt.strip() for opt in options_raw.split(',') if opt.strip()]

        Question.objects.create(
            template_id=template_id,
            text=text,
            kind=kind,
            options=options
        )
        messages.success(request, "Question ajoutée avec succès.")
        return redirect('question_list')

    questions_qs = Question.objects.all().select_related('template').order_by('template__name')
    questions = get_paginated_queryset(request, questions_qs)
    templates = QuestionTemplate.objects.all()
    kind_choices = Question.KIND_CHOICES
    return render(request, 'question_list.html', {
        'questions': questions,
        'templates': templates,
        'kind_choices': kind_choices
    })

@login_required(login_url='users/login/')
def recolte_list(request, type_recolte):
    # type_recolte sera 'pre-scolaire', 'primaire' ou 'secondaire'
    recoltes_qs = Recolte.objects.filter(type=type_recolte).order_by('-date')
    recoltes = get_paginated_queryset(request, recoltes_qs)
    
    context = {
        'recoltes': recoltes,
        'type_recolte': type_recolte,
        'title': f"Fiches de Récolte - {dict(Recolte.TYPE_CHOICES).get(type_recolte)}"
    }
    return render(request, 'recolte_list.html', context)

@login_required(login_url='users/login/')
def recolte_validate(request, pk):
    recolte = get_object_or_404(Recolte, pk=pk)
    recolte.status = 'valide'
    recolte.save()
    messages.success(request, f"La fiche de récolte pour {recolte.establishment.name} a été validée.")
    return redirect('recolte_list', type_recolte=recolte.type)

@login_required(login_url='users/login/')
def recolte_reject(request, pk):
    recolte = get_object_or_404(Recolte, pk=pk)
    recolte.status = 'rejete'
    recolte.save()
    messages.warning(request, f"La fiche de récolte pour {recolte.establishment.name} a été rejetée.")
    return redirect('recolte_list', type_recolte=recolte.type)
