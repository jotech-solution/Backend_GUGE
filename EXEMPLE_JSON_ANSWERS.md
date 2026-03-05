"""
EXEMPLE DE STRUCTURE JSON POUR LE CHAMP 'answers' DU MODÈLE Recolte
====================================================================

Le champ 'answers' du modèle Recolte est un JSONField qui stocke une liste de dictionnaires.
Chaque dictionnaire contient:
- question_uuid: L'UUID de la question (correspond au champ 'id' du modèle Question)
- answer: La réponse fournie par l'utilisateur

EXEMPLE 1 - Réponses simples (texte)
=====================================

[
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440001",
        "answer": "40"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440002",
        "answer": "25"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440003",
        "answer": "Oui"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440004",
        "answer": "L'école a 3 salles de classe en bon état et 2 en mauvais état"
    }
]


EXEMPLE 2 - Avec questions optionnelles (réponses manquantes)
=============================================================

[
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440001",
        "answer": "Groupe Scolaire XYZ"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440002",
        "answer": "45"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440003",
        "answer": ""
    }
]


EXEMPLE 3 - Réponses avec plusieurs options sélectionnées (choix multiples)
==========================================================================

[
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440001",
        "answer": ["Option1", "Option3", "Option5"]
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440002",
        "answer": "Non"
    }
]


COMMENT CRÉER CETTE STRUCTURE EN PYTHON
========================================

# Lors de la création d'une récolte
recolte = Recolte.objects.create(
    establishment=school,
    campaign=campaign,
    collector_id=user,
    type='primaire',
    date=datetime.now(),
    answers=[
        {
            "question_uuid": str(question1.id),
            "answer": "réponse 1"
        },
        {
            "question_uuid": str(question2.id),
            "answer": "réponse 2"
        },
        {
            "question_uuid": str(question3.id),
            "answer": ["choix1", "choix2"]
        }
    ]
)

# Pour modifier les réponses
recolte.answers.append({
    "question_uuid": str(new_question.id),
    "answer": "nouvelle réponse"
})
recolte.save()


COMMENT LA VUE TRAITE CES DONNÉES
==================================

Dans rapport_detail (views.py):

1. On récupère le champ answers du modèle Recolte:
   rapport = recolte.answers or []

2. On crée un dictionnaire pour accès rapide:
   answer_dict = {
       item.get('question_uuid'): item.get('answer', '')
       for item in rapport
       if isinstance(item, dict)
   }
   
   Résultat:
   {
       "550e8400-e29b-41d4-a716-446655440001": "40",
       "550e8400-e29b-41d4-a716-446655440002": "25",
       "550e8400-e29b-41d4-a716-446655440003": "Oui",
       "550e8400-e29b-41d4-a716-446655440004": "L'école a 3 salles..."
   }

3. On passe ce dictionnaire au template:
   return render(request, 'model.html', {
       'answers_dict': answer_dict,
       ...
   })


COMMENT LE TEMPLATE AFFICHE LES RÉPONSES
===========================================

Dans model.html:

{% for question in questions %}
    {% if question.groupe.name == grp.name %}
        {% with answer=answers_dict|get_dict_value:question.id %}
        <p><strong>{{ question.text }} :</strong> {{ answer|default:"Non répondu" }}</p>
        {% endwith %}
    {% endif %}
{% endfor %}

1. Pour chaque question, on cherche sa réponse dans answers_dict
2. On utilise le filtre custom_filters.get_dict_value pour accéder au dict
3. Le filtre: answers_dict|get_dict_value:question.id
   - Cherche la clé question.id dans answers_dict
   - Retourne la réponse trouvée ou '' (chaîne vide)
4. Le |default:"Non répondu" affiche "Non répondu" si la réponse est vide


AVANTAGES DE CETTE APPROCHE
============================

✓ Les données de réponses sont stockées uniquement dans le modèle Recolte
✓ Le modèle Question reste pur, sans attributs temporaires
✓ Pas de pollution de la base de données avec des données non persistantes
✓ Les réponses et les questions sont clairement séparées
✓ Facile à exporter/importer les données
✓ Historique des réponses préservé
"""

