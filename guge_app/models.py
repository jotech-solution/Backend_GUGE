from django.db import models
import uuid

class Province(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    principal_town = models.CharField(max_length=255, null=True, blank=True)
    surface = models.CharField(max_length=50, null=True, blank=True)
    population = models.CharField(max_length=50, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Division(models.Model):
    province = models.ForeignKey(Province, on_delete=models.RESTRICT, related_name="divisions")
    code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubDivision(models.Model):
    division = models.ForeignKey(Division, on_delete=models.RESTRICT, related_name="sub_divisions")
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("division", "name")

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.RESTRICT, related_name="cities")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True, null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("province", "name")

    def __str__(self):
        return self.name


class Territory(models.Model):
    province = models.ForeignKey(Province, on_delete=models.RESTRICT, related_name="territories")
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("province", "name")

    def __str__(self):
        return self.name


class School(models.Model):

    MANAGEMENT_CHOICES = [
        ('École Non Conventionnée', 'École Non Conventionnée'),
        ('Catholique', 'Catholique'),
        ('Protestant', 'Protestant'),
        ('Kimbaguiste', 'Kimbaguiste'),
        ('Islamique', 'Islamique'),
        ('Salutiste', 'Salutiste'),
        ('Fraternité', 'Fraternité'),
        ('Privée', 'Privée'),
        ('Autres', 'Autres'),
    ]

    MECHANIZED_CHOICES = [
        ('mecanise_paye', 'Mécanisé Payé'),
        ('mecanise_non_paye', 'Mécanisé Non Payé'),
        ('non_mecanise', 'Non Mécanisé'),
    ]

    OWNERSHIP_CHOICES = [
        ('proprietaire', 'Propriétaire'),
        ('locataire', 'Locataire'),
        ('coproprietaire', 'Copropriétaire'),
    ]

    ENVIRONMENT_CHOICES = [
        ('rural', 'Rural'),
        ('urbain', 'Urbain'),
    ]

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    head_name = models.CharField(max_length=255)
    head_phone = models.CharField(max_length=255)

    province = models.ForeignKey(Province, on_delete=models.RESTRICT)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, null=True, blank=True)
    territory = models.ForeignKey(Territory, on_delete=models.RESTRICT, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.RESTRICT)
    sub_division = models.ForeignKey(SubDivision, on_delete=models.RESTRICT)

    village = models.CharField(max_length=255, null=True, blank=True)

    adm_code = models.CharField(max_length=255, unique=True)
    legal_reference = models.CharField(max_length=255)
    secope_number = models.CharField(max_length=255)

    management_regime = models.CharField(max_length=50, choices=MANAGEMENT_CHOICES)
    mechanized_status = models.CharField(max_length=50, choices=MECHANIZED_CHOICES)
    ownership_status = models.CharField(max_length=50, choices=OWNERSHIP_CHOICES)
    environment = models.CharField(max_length=20, choices=ENVIRONMENT_CHOICES)

    geo_coord = models.JSONField(null=True, blank=True)
    regroupment_center = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class QuestionTemplate(models.Model):

    TYPE_CHOICES = [
        ('pre-scolaire', 'Pré-scolaire'),
        ('primaire', 'Primaire'),
        ('secondaire', 'Secondaire'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Question(models.Model):

    KIND_CHOICES = [
        ('choice', 'Choix'),
        ('text', 'Texte'),
        ('number', 'Nombre'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    template = models.ForeignKey(
        QuestionTemplate,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    text = models.TextField()
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)

    # Pour stocker les options de type "choice"
    options = models.JSONField(blank=True, default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Recolte(models.Model):

    TYPE_CHOICES = [
        ('pre-scolaire', 'Pré-scolaire'),
        ('primaire', 'Primaire'),
        ('secondaire', 'Secondaire'),
    ]

    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    establishment = models.ForeignKey(
        "School",
        on_delete=models.CASCADE,
        related_name="recoltes"
    )

    date = models.DateTimeField()

    collector_name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    # questionId -> answer
    answers = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Récolte - {self.establishment.name} - {self.date.date()} ({self.get_status_display()})"