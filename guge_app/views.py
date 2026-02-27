from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import School, Province, Division, SubDivision, City, Territory, QuestionTemplate, Question, Recolte, Groupe, Campaign
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .serializers import SchoolSerializer, QuestionTemplateSerializer, SchoolSyncSerializer, RecolteSerializer, UserSerializer, CampaignSerializer
from .filters import SchoolFilter
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recoltes_mine(request):
    """Retourne les récoltes créées par l'utilisateur connecté."""
    recoltes_qs = Recolte.objects.filter(collector_id=request.user).order_by('-date')
    serializer = RecolteSerializer(recoltes_qs, many=True)
    return Response({
        'recoltes': serializer.data
    })

# APIS
@api_view(['POST'])
def sync_schools_by_codes(request):
    codes = request.data.get("codes", [])

    schools = School.objects.filter(adm_code__in=codes)

    serializer = SchoolSerializer(schools, many=True)

    return Response({
        "schools": serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_current_user(request):
    """Récupère les informations de l'utilisateur connecté"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # ajouter les informations utilisateur sérialisées
        data['user'] = UserSerializer(self.user).data
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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



class SchoolSyncViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = School.objects.all()
    serializer_class = SchoolSyncSerializer
    pagination_class = None  # Souvent utile pour la synchro de tout récupérer d'un coup

class RecolteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Recolte.objects.all()
    serializer_class = RecolteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "status", "establishment"]
    search_fields = ["collector_name", "establishment__name"]
    ordering_fields = ["date", "created_at"]


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Campaign.objects.prefetch_related("question_templates", "recoltes").all()
    serializer_class = CampaignSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name"]
    ordering_fields = ["start_date", "end_date", "name", "created_at"]


@login_required(login_url='users/login/')
def recolte_detail(request, pk):
    recolte = get_object_or_404(Recolte, pk=pk)

    # Préparer les paires question -> réponse
    answers = recolte.answers or {}
    qa_list = []
    for qid, answer in answers.items():
        try:
            q = Question.objects.get(pk=qid)
            q_text = q.text
        except Exception:
            q_text = str(qid)
        qa_list.append({
            'question': q_text,
            'answer': answer
        })

    return render(request, 'recolte_detail.html', {
        'recolte': recolte,
        'qa_list': qa_list
    })

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
def school_map(request):
    schools = School.objects.filter(geo_coord__isnull=False)
    return render(request, 'school_map.html', {'schools': schools})

@login_required(login_url='users/login/')
def school_list(request):
    schools_qs = School.objects.all().order_by('-created_at')
    schools = get_paginated_queryset(request, schools_qs)
    return render(request, 'school_list.html', {'schools': schools})

@login_required(login_url='users/login/')
def school_detail(request, pk):
    school = get_object_or_404(School, pk=pk)
    return render(request, 'school_detail.html', {'school': school})

@login_required(login_url='users/login/')
def school_edit(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        # Mise à jour des données
        school.name = request.POST.get('name')
        school.address = request.POST.get('address')
        school.level = request.POST.getlist('level')
        school.head_name = request.POST.get('head_name')
        school.head_phone = request.POST.get('head_phone')
        school.province_id = request.POST.get('province')
        school.city_id = request.POST.get('city') or None
        school.territory_id = request.POST.get('territory') or None
        school.division_id = request.POST.get('division')
        school.sub_division_id = request.POST.get('sub_division')
        school.village = request.POST.get('village')
        school.adm_code = request.POST.get('adm_code')
        school.legal_reference = request.POST.get('legal_reference')
        school.secope_number = request.POST.get('secope_number')
        school.management_regime = request.POST.get('management_regime')
        school.mechanized_status = request.POST.get('mechanized_status')
        school.ownership_status = request.POST.get('ownership_status')
        school.environment = request.POST.get('environment')
        
        # Coordonnées Géo dans JSONField
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        if lat and lon:
            school.geo_coord = {"lat": float(lat), "long": float(lon)}
        else:
            school.geo_coord = None

        school.regroupment_center = request.POST.get('regroupment_center')

        school.updated_at = datetime.now()
        
        school.save()
        messages.success(request, "École mise à jour avec succès.")
        return redirect('school_list')

    provinces = Province.objects.all()
    divisions = Division.objects.all()
    sub_divisions = SubDivision.objects.all()
    cities = City.objects.all()
    territories = Territory.objects.all()

    context = {
        'school': school,
        'provinces': provinces,
        'divisions': divisions,
        'sub_divisions': sub_divisions,
        'cities': cities,
        'territories': territories,
        'management_choices': School.MANAGEMENT_CHOICES,
        'mechanized_choices': School.MECHANIZED_CHOICES,
        'ownership_choices': School.OWNERSHIP_CHOICES,
        'environment_choices': School.ENVIRONMENT_CHOICES,
        'level_choices': School.NIVEAUX,
        'is_edit': True
    }
    return render(request, 'school_form.html', context)

@login_required(login_url='users/login/')
def school_delete(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        school.delete()
        messages.success(request, "École supprimée avec succès.")
        return redirect('school_list')
    return render(request, 'school_confirm_delete.html', {'school': school})

@login_required(login_url='users/login/')
def school_form(request):
    if request.method == 'POST':
        # Extraction des données du POST
        name = request.POST.get('name')
        address = request.POST.get('address')
        level = request.POST.getlist('level')
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
        
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        geo_coord = {"latitude": float(lat), "longitude": float(lon)} if lat and lon else None
        
        regroupment_center = request.POST.get('regroupment_center')

        # Création de l'école
        School.objects.create(
            name=name, address=address, level=level, head_name=head_name, head_phone=head_phone,
            province_id=province_id, city_id=city_id, territory_id=territory_id,
            division_id=division_id, sub_division_id=sub_division_id,
            village=village, adm_code=adm_code, legal_reference=legal_reference,
            secope_number=secope_number, management_regime=management_regime,
            mechanized_status=mechanized_status, ownership_status=ownership_status,
            environment=environment, geo_coord=geo_coord,
            regroupment_center=regroupment_center, updated_at=datetime.now()
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
        'level_choices': School.NIVEAUX,
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
def question_template_detail(request, pk):
    template = get_object_or_404(QuestionTemplate, pk=pk)
    questions = template.questions.all()
    return render(request, 'question_template_detail.html', {'template': template, 'questions': questions})

@login_required(login_url='users/login/')
def question_add_multiple(request, template_id):
    """Formulaire permettant d'ajouter plusieurs questions à la fois pour un template donné."""
    template = get_object_or_404(QuestionTemplate, pk=template_id)
    if request.method == 'POST':
        texts = request.POST.getlist('text')
        kinds = request.POST.getlist('kind')
        options_list = request.POST.getlist('options')
        groupe_ids = request.POST.getlist('groupe')

        for text, kind, opts, groupe_id in zip(texts, kinds, options_list, groupe_ids):
            if not text.strip():
                continue
            options = []
            if kind == 'choice' and opts:
                options = [opt.strip() for opt in opts.split(',') if opt.strip()]
            
            groupe = None
            if groupe_id and groupe_id.strip():
                try:
                    groupe = Groupe.objects.get(pk=groupe_id)
                except Groupe.DoesNotExist:
                    groupe = None
            
            Question.objects.create(
                template=template,
                groupe=groupe,
                text=text,
                kind=kind,
                options=options
            )
        messages.success(request, "Questions ajoutées avec succès.")
        return redirect('question_template_detail', pk=template_id)

    kind_choices = Question.KIND_CHOICES
    questions_qs = template.questions.all()
    questions = get_paginated_queryset(request, questions_qs)
    groupes = Groupe.objects.all()
    return render(request, 'question_bulk_add.html', {
        'template': template,
        'kind_choices': kind_choices,
        'questions': questions,
        'groupes': groupes
    })

@login_required(login_url='users/login/')
def question_template_edit(request, pk):
    template = get_object_or_404(QuestionTemplate, pk=pk)
    if request.method == 'POST':
        template.name = request.POST.get('name')
        template.type = request.POST.get('type')
        template.save()
        messages.success(request, "Questionnaire mis à jour avec succès.")
        return redirect('question_template_list')
    
    type_choices = QuestionTemplate.TYPE_CHOICES
    return render(request, 'question_template_edit.html', {'template': template, 'type_choices': type_choices})

@login_required(login_url='users/login/')
def question_template_delete(request, pk):
    template = get_object_or_404(QuestionTemplate, pk=pk)
    if request.method == 'POST':
        template.delete()
        messages.success(request, "Questionnaire supprimé avec succès.")
        return redirect('question_template_list')
    return render(request, 'question_template_confirm_delete.html', {'template': template})

@login_required(login_url='users/login/')
def question_list(request):
    if request.method == 'POST':
        template_id = request.POST.get('template')
        text = request.POST.get('text')
        kind = request.POST.get('kind')
        options_raw = request.POST.get('options')
        groupe_id = request.POST.get('groupe')

        options = []
        if options_raw:
            options = [opt.strip() for opt in options_raw.split(',') if opt.strip()]

        groupe = None
        if groupe_id and groupe_id.strip():
            try:
                groupe = Groupe.objects.get(pk=groupe_id)
            except Groupe.DoesNotExist:
                groupe = None

        Question.objects.create(
            template_id=template_id,
            groupe=groupe,
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
    groupes = Groupe.objects.all()
    return render(request, 'question_list.html', {
        'questions': questions,
        'templates': templates,
        'kind_choices': kind_choices,
        'groupes': groupes
    })

@login_required(login_url='users/login/')
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.template_id = request.POST.get('template')
        question.text = request.POST.get('text')
        question.kind = request.POST.get('kind')
        options_raw = request.POST.get('options')
        groupe_id = request.POST.get('groupe')
        
        options = []
        if options_raw:
            options = [opt.strip() for opt in options_raw.split(',') if opt.strip()]
        
        groupe = None
        if groupe_id and groupe_id.strip():
            try:
                groupe = Groupe.objects.get(pk=groupe_id)
            except Groupe.DoesNotExist:
                groupe = None
        
        question.options = options
        question.groupe = groupe
        question.save()
        messages.success(request, "Question mise à jour avec succès.")
        return redirect('question_list')
    
    templates = QuestionTemplate.objects.all()
    kind_choices = Question.KIND_CHOICES
    groupes = Groupe.objects.all()
    return render(request, 'question_edit.html', {
        'question': question,
        'templates': templates,
        'kind_choices': kind_choices,
        'groupes': groupes
    })

@login_required(login_url='users/login/')
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question supprimée avec succès.")
        return redirect('question_list')
    return render(request, 'question_confirm_delete.html', {'question': question})

@login_required(login_url='users/login/')
def groupe_list(request):
    if request.method == 'POST':
        import json
        
        # Gérer les requêtes JSON (AJAX) et les requêtes form-urlencoded
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                name = data.get('name')
                description = data.get('description', '')
                order = data.get('order', 0)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            order = request.POST.get('order', 0)
        
        if name:
            groupe = Groupe.objects.create(
                name=name,
                description=description,
                order=int(order) if order else 0
            )
            
            # Retourner JSON si c'est une requête AJAX
            if request.content_type == 'application/json':
                return JsonResponse({
                    'id': str(groupe.id),
                    'name': groupe.name,
                    'description': groupe.description,
                    'order': groupe.order,
                })
            else:
                messages.success(request, "Groupe créé avec succès.")
                return redirect('groupe_list')
        else:
            if request.content_type == 'application/json':
                return JsonResponse({'error': 'Name is required'}, status=400)

    groupes_qs = Groupe.objects.all().order_by('order')
    groupes = get_paginated_queryset(request, groupes_qs)
    return render(request, 'groupe_list.html', {'groupes': groupes})

@login_required(login_url='users/login/')
def groupe_edit(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'POST':
        groupe.name = request.POST.get('name')
        groupe.description = request.POST.get('description')
        ordre = request.POST.get('order')
        if ordre:
            groupe.order = int(ordre)
        groupe.save()
        messages.success(request, "Groupe mis à jour avec succès.")
        return redirect('groupe_list')
    
    return render(request, 'groupe_edit.html', {'groupe': groupe})

@login_required(login_url='users/login/')
def groupe_delete(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    if request.method == 'POST':
        groupe.delete()
        messages.success(request, "Groupe supprimé avec succès.")
        return redirect('groupe_list')
    return render(request, 'groupe_confirm_delete.html', {'groupe': groupe})

@login_required(login_url='users/login/')
def campaign_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        comments = request.POST.get('comments')
        question_template_ids = request.POST.getlist('question_templates')

        campaign = Campaign.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            comments=comments
        )
        campaign.question_templates.set(question_template_ids)
        messages.success(request, "Campagne créée avec succès.")
        return redirect('campaign_list')

    campaigns_qs = Campaign.objects.all().order_by('-start_date')
    campaigns = get_paginated_queryset(request, campaigns_qs)
    templates = QuestionTemplate.objects.all()
    return render(request, 'campaign_list.html', {
        'campaigns': campaigns,
        'templates': templates
    })

@login_required(login_url='users/login/')
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    return render(request, 'campaign_detail.html', {'campaign': campaign})

@login_required(login_url='users/login/')
def campaign_edit(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        campaign.name = request.POST.get('name')
        campaign.start_date = request.POST.get('start_date')
        campaign.end_date = request.POST.get('end_date')
        campaign.comments = request.POST.get('comments')
        question_template_ids = request.POST.getlist('question_templates')
        campaign.save()
        campaign.question_templates.set(question_template_ids)
        messages.success(request, "Campagne mise à jour avec succès.")
        return redirect('campaign_list')
    
    templates = QuestionTemplate.objects.all()
    return render(request, 'campaign_edit.html', {
        'campaign': campaign,
        'templates': templates
    })

@login_required(login_url='users/login/')
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, "Campagne supprimée avec succès.")
        return redirect('campaign_list')
    return render(request, 'campaign_confirm_delete.html', {'campaign': campaign})

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
