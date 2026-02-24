import json
import os
from django.core.management.base import BaseCommand
from guge_app.models import Province, Division, SubDivision
from django.db import transaction

class Command(BaseCommand):
    help = 'Importe les données des divisions et sous-divisions depuis un fichier JSON'

    def handle(self, *args, **options):
        file_path = os.path.join('data', 'Division et Sous-division.json')
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"Le fichier {file_path} n'existe pas."))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(f"Importation de {len(data)} enregistrements de provinces éducationnelles...")

        try:
            with transaction.atomic():
                for entry in data:
                    province_macro_name = entry.get('province_macro', '').strip()
                    province_edu_name = entry.get('province_educationnelle', '').strip()
                    subdivisions = entry.get('subdivisions', [])

                    if not province_macro_name or not province_edu_name:
                        continue

                    # Normalisation du nom de la province pour éviter les doublons
                    # Ex: "Kasaï Central" -> "Kasaï-Central"
                    norm_name = province_macro_name.replace(' ', '-')
                    # Cas particuliers si nécessaire
                    if norm_name == "Kongo-Central":
                        norm_name = "Kongo Central" # Semble être sans tiret dans la DB existante? 
                                                   # Vérifions : 'Kongo-Central' et 'Kongo Central' existent tous les deux.
                    
                    # On va essayer de trouver une province qui ressemble
                    province = Province.objects.filter(name__iexact=province_macro_name).first()
                    if not province:
                        province = Province.objects.filter(name__iexact=norm_name).first()
                    
                    if not province:
                        province = Province.objects.create(name=province_macro_name)
                        self.stdout.write(self.style.SUCCESS(f"Province créée : {province_macro_name}"))

                    # 2. Créer ou récupérer la Division (Province éducationnelle)
                    # Le code est optionnel dans Division, on peut essayer de le générer ou laisser vide
                    division, created = Division.objects.get_or_create(
                        province=province,
                        name=province_edu_name
                    )
                    if created:
                        self.stdout.write(f"  Division créée : {province_edu_name}")

                    # 3. Créer les SubDivisions
                    for sub in subdivisions:
                        sub_name = sub.get('subdivision_name')
                        # Le code de SubDivision est UNIQUE et REQUIS (blank=False)
                        # On va générer un code basé sur le nom de la division et de la sous-division
                        # ou utiliser un UUID pour garantir l'unicité
                        import uuid
                        sub_code = str(uuid.uuid4())[:10] # On prend une partie d'UUID pour le code par défaut si absent
                        
                        # Vérifier si elle existe déjà par le nom et la division (unique_together)
                        sub_obj = SubDivision.objects.filter(division=division, name=sub_name).first()
                        if not sub_obj:
                            SubDivision.objects.create(
                                division=division,
                                name=sub_name,
                                code=f"{division.id}-{sub_name[:50]}-{str(uuid.uuid4())[:8]}" # Code unique
                            )
                            # self.stdout.write(f"    Sous-division créée : {sub_name}")
                
            self.stdout.write(self.style.SUCCESS("Importation terminée avec succès !"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erreur lors de l'importation : {str(e)}"))
