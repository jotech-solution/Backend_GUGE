from django.shortcuts import render, redirect, get_object_or_404
from .models import School, Province, Division, SubDivision, City, Territory, QuestionTemplate, Question
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def school_list(request):
    schools = School.objects.all()
    return render(request, 'school_list.html', {'schools': schools})

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
    
    provinces = Province.objects.all()
    return render(request, 'province_list.html', {'provinces': provinces})

def division_list(request):
    if request.method == 'POST':
        province_id = request.POST.get('province')
        code = request.POST.get('code')
        name = request.POST.get('name')
        Division.objects.create(province_id=province_id, code=code, name=name)
        messages.success(request, "Division ajoutée avec succès.")
        return redirect('division_list')
    
    divisions = Division.objects.all()
    provinces = Province.objects.all()
    return render(request, 'division_list.html', {'divisions': divisions, 'provinces': provinces})

def subdivision_list(request):
    if request.method == 'POST':
        division_id = request.POST.get('division')
        code = request.POST.get('code')
        name = request.POST.get('name')
        SubDivision.objects.create(division_id=division_id, code=code, name=name)
        messages.success(request, "Sous-division ajoutée avec succès.")
        return redirect('subdivision_list')
    
    subdivisions = SubDivision.objects.all()
    divisions = Division.objects.all()
    return render(request, 'subdivision_list.html', {'subdivisions': subdivisions, 'divisions': divisions})

def city_list(request):
    if request.method == 'POST':
        province_id = request.POST.get('province')
        code = request.POST.get('code')
        name = request.POST.get('name')
        City.objects.create(province_id=province_id, code=code, name=name)
        messages.success(request, "Ville ajoutée avec succès.")
        return redirect('city_list')
    
    cities = City.objects.all()
    provinces = Province.objects.all()
    return render(request, 'city_list.html', {'cities': cities, 'provinces': provinces})

def territory_list(request):
    if request.method == 'POST':
        province_id = request.POST.get('province')
        code = request.POST.get('code')
        name = request.POST.get('name')
        Territory.objects.create(province_id=province_id, code=code, name=name)
        messages.success(request, "Territoire ajouté avec succès.")
        return redirect('territory_list')
    
    territories = Territory.objects.all()
    provinces = Province.objects.all()
    return render(request, 'territory_list.html', {'territories': territories, 'provinces': provinces})

def question_template_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type_q = request.POST.get('type')
        
        QuestionTemplate.objects.create(name=name, type=type_q)
        messages.success(request, "Questionnaire ajouté avec succès.")
        return redirect('question_template_list')
    
    templates = QuestionTemplate.objects.all()
    type_choices = QuestionTemplate.TYPE_CHOICES
    return render(request, 'question_template_list.html', {'templates': templates, 'type_choices': type_choices})

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
    
    questions = Question.objects.all().select_related('template')
    templates = QuestionTemplate.objects.all()
    kind_choices = Question.KIND_CHOICES
    return render(request, 'question_list.html', {
        'questions': questions, 
        'templates': templates,
        'kind_choices': kind_choices
    })
