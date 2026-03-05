"""
GUIDE D'UTILISATION - SYSTÈME DE RÉPONSE AUX QUESTIONS POUR LES RÉCOLTES
=========================================================================

FONCTIONNALITÉS AJOUTÉES
========================

1. Bouton "Répondre aux questions" dans la liste des récoltes (recolte_list.html)
   - Permet d'accéder au formulaire de réponse aux questions
   - Icône: crayon (ti ti-edit)
   - Disponible pour toutes les récoltes

2. Vue recolte_answer (views.py)
   - Affiche toutes les questions liées à la campagne de la récolte
   - Groupe les questions par catégorie (groupe)
   - Récupère les réponses existantes si elles existent
   - Sauvegarde les réponses dans le champ JSON 'answers' du modèle Recolte

3. Template recolte_answer.html
   - Formulaire dynamique généré selon le type de question
   - Support de plusieurs types de réponses:
     * text: Champ de texte simple
     * number: Champ numérique
     * choice: Choix unique (radio buttons)
     * multiple_choice: Choix multiples (checkboxes)
     * textarea: Zone de texte multi-lignes


TYPES DE QUESTIONS SUPPORTÉS
=============================

1. TEXT (text)
   └─ Input type="text"
   └─ Réponse: chaîne de caractères simple

2. NUMBER (number)
   └─ Input type="number"
   └─ Réponse: nombre entier ou décimal

3. CHOICE (choice)
   └─ Radio buttons
   └─ Réponse: une seule option sélectionnée
   └─ Format: "Option1" ou "Option2"

4. MULTIPLE_CHOICE (multiple_choice)
   └─ Checkboxes
   └─ Réponse: tableau d'options
   └─ Format: ["Option1", "Option3", "Option5"]

5. TEXTAREA (textarea)
   └─ Textarea multi-lignes
   └─ Réponse: texte long


STRUCTURE DES RÉPONSES ENREGISTRÉES
====================================

Les réponses sont stockées dans recolte.answers comme une liste de dictionnaires:

[
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440001",
        "answer": "réponse simple"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440002",
        "answer": 42
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440003",
        "answer": "Option A"
    },
    {
        "question_uuid": "550e8400-e29b-41d4-a716-446655440004",
        "answer": ["Option1", "Option3", "Option5"]
    }
]


FLUX DE TRAVAIL UTILISATEUR
============================

1. Aller à la liste des récoltes (ex: /manage_guge/recoltes/primaire/)
2. Cliquer sur le bouton "Répondre aux questions" (crayon)
3. Voir les questions groupées par catégorie
4. Remplir les réponses selon le type de question
5. Cliquer sur "Enregistrer les réponses"
6. Les réponses sont sauvegardées et on retourne à la liste


POINTS TECHNIQUES
=================

1. Groupement des questions
   - Les questions sont automatiquement groupées par leur champ 'groupe'
   - Les questions sans groupe apparaissent sous "Autres questions"
   - Les groupes sont ordonnés par le champ 'order'

2. Réponses existantes
   - Si des réponses existent déjà, elles sont récupérées et affichées
   - Utilisation du filtre custom_filters.get_dict_value pour l'accès au dictionnaire
   - Les valeurs sont pré-remplies dans les champs

3. Sauvegarde
   - Les réponses sont converties en JSON
   - Chaque réponse est associée à l'UUID de la question
   - Le statut de la récolte ne change pas (reste 'en_attente')
   - Un message de confirmation s'affiche

4. Traitement des types de questions
   - Les checkboxes (multiple_choice) retournent un tableau
   - Les radio buttons (choice) retournent une string
   - Les champs texte retournent une string
   - Les champs vides retournent une chaîne vide ou un tableau vide


INTÉGRATION AVEC LE RESTE DU SYSTÈME
=====================================

1. Modèle Recolte
   - answers: JSONField(default=list, blank=True, null=True)
   - Stocke les réponses sous forme de liste de dictionnaires
   - Pas d'attribut temporaire sur le modèle Question

2. URL Pattern
   - path('recoltes/<uuid:pk>/answer/', views.recolte_answer, name='recolte_answer')
   - Accepte l'UUID de la récolte

3. Permissions
   - Authentification requise (@login_required)
   - Chaque utilisateur peut répondre aux questions de ses récoltes

4. Affichage des réponses
   - Les réponses peuvent être affichées dans rapport_detail (rapport.html)
   - Utilisation du filtre custom_filters.get_dict_value


EXEMPLE D'UTILISATION EN PYTHON
================================

# Créer une récolte avec des réponses
recolte = Recolte.objects.create(
    establishment=school,
    campaign=campaign,
    type='primaire',
    date=datetime.now(),
    answers=[
        {"question_uuid": str(q1.id), "answer": "40"},
        {"question_uuid": str(q2.id), "answer": "Oui"},
        {"question_uuid": str(q3.id), "answer": ["Option1", "Option3"]}
    ]
)

# Accéder aux réponses
for item in recolte.answers:
    question_id = item['question_uuid']
    answer = item['answer']
    question = Question.objects.get(id=question_id)
    print(f"{question.text}: {answer}")

# Modifier les réponses
new_answers = [...]
recolte.answers = new_answers
recolte.save()
"""

