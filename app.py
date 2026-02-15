import google.generativeai as genai
import sqlite3 as sq
import streamlit as stl
from tache import Tache

if "form_ajout" not in stl.session_state:
    stl.session_state.form_ajout = False

def ouvrir_formulaire():
    stl.session_state.form_ajout = True

try:
    genai.configure(api_key=stl.secrets["GEMINI_CLE_API"])
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    stl.error(f"Problème de configuration: {e}")


# Création et Initialisation de la base de données
def initialiser_bdd():
    conn = sq.connect("tasks.db")
    cur = conn.cursor()
    tasks = []
    try:
        cur.execute("""
                    
                    CREATE TABLE IF NOT EXISTS Tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    titre TEXT, 
                    description TEXT, 
                    date TEXT, 
                    statut TEXT, 
                    priorite INT)
                    
        """)
        conn.commit()
        conn.close()
    except sq.Error as e:    
        stl.error(f"Erreur de chargement : {e}")

initialiser_bdd() 

# Fonctions CRUD
def ajouter_tache(titre, description,pr):

    try:
        # On crée une nouvelle connexion locale pour être sûr
        conn = sq.connect("tasks.db")
        cursor = conn.cursor()
        
        # On crée l'objet
        tache_obj = Tache(titre, description, pr)
        
        # On insère
        cursor.execute("""
            INSERT INTO Tasks (titre, description, date, statut, priorite) 
            VALUES (?, ?, ?, ?, ?)
        """, (titre, description, tache_obj.date, tache_obj.statut, pr))
        
        conn.commit()
        conn.close()
        return True # On indique que ça a marché
    except Exception as e:
        stl.error(f"ERREUR CRITIQUE DANS AJOUTER_TACHE : {e}")
        return False
    

def lire_tache():
    ltasks = []
    try:
        conn = sq.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Tasks ORDER BY priorite ASC""")
        tasks = cursor.fetchall()
        for task in tasks:
            new_task = Tache(task[1],task[2],task[5],id=task[0])
            ltasks.append(new_task)
        conn.close()
    except sq.Error as err:
        print(f"Erreur sql: {err}")        
    return ltasks

def modifier_priorite(idTache, nvlPriorite):
    try:
        conn = sq.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Tasks SET priorite = ? WHERE id = ?",(nvlPriorite,idTache))
        conn.commit()
        conn.close()
    except sq.Error as err:
        print(f"Erreur sql: {err}")  

def supprimer_tache():
    try:
        conn = sq.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE  FROM Tasks")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Tasks'")
        conn.commit()
        conn.close()
        stl.rerun()
    except sq.Error as err:
        print(f"Erreur sql: {err}")



#Interface graphique
stl.title("App Task-List")

maListe = lire_tache()
taches = stl.container(height=210)
with taches:
    for task in maListe:
        color = "🔴" if task.priorite == 1 else "🟡" if task.priorite == 2 else "🟢"
        stl.markdown(f"### {color} {task.titre}")
        stl.write(f"Description: {task.description}")
        stl.caption(f"Statut : {task.statut} | Priorité : {task.priorite}")
        stl.divider() 

gauche, milieu, droite = stl.columns(3)

# Bouton d'ajout de tâches
gauche.button("Ajouter une tâche", on_click=ouvrir_formulaire,width=300)

# Bouton Suppression de tâches
if milieu.button("Tout supprimer", width=300):
    supprimer_tache()
    stl.rerun()

if stl.session_state.form_ajout:
    # On crée un formulaire nommé "mon_formulaire"
    with stl.form("formulaire_ajout"):
        stl.subheader("Nouvelle tâche")
        nouveau_titre = stl.text_input("Titre de la tâche")
        nouvelle_desc = stl.text_area("Détails (Optionnel)")
        nouvelle_pr = stl.slider("Priorité", 1, 3, 2)
        
        # Le bouton de validation spécifique au formulaire
        soumettre = stl.form_submit_button("Enregistrer la tâche")
        annuler = stl.form_submit_button("Annuler")

        if soumettre:
            if nouveau_titre:
                ajouter_tache(nouveau_titre, nouvelle_desc, nouvelle_pr)
                stl.session_state.form_ajout = False
                stl.rerun()
            else:
                stl.error("Le titre est obligatoire !")
        
        if annuler:
            stl.session_state.form_ajout = False
            stl.rerun()       
        
# Bouton Organisation par IA        
prompt = ""  
# 1. Initialisation de la mémoire de suggestion (en haut du script)
if "suggestion_ia" not in stl.session_state:
    stl.session_state.suggestion_ia = None

# 2. Le bouton pour demander à l'IA
if droite.button(" Organisation par IA", width=300):
    if not maListe:
        stl.warning("Ajoutez des tâches d'abord !")
    else:
        with stl.spinner("Analyse en cours..."):
            # génération du prompt
            for tache in maListe:
                prompt += f"ID: {tache.id}, Titre: {tache.titre}, Description: {tache.description}, Priorité: {tache.priorite} ; \n"
            consigne = f"""
                    Tu es un assistant expert en organisation.
                    Voici ma liste de tâches actuelle :
                    {prompt}

                    Instructions :
                    1. Évalue la priorité de chaque tâche de 1 (urgent) à 3 (non urgent).
                    2. Réponds UNIQUEMENT sous le format 'ID:Priorité' séparés par des virgules.
                    Exemple de réponse attendue : 1:5,2:3,3:1
                    """   
            reponse = model.generate_content(consigne)
            # On stocke la réponse brute pour l'étape suivante
            stl.session_state.suggestion_ia = reponse.text.strip()

# 3. Affichage de la confirmation (si l'IA a répondu)
if stl.session_state.suggestion_ia:
    stl.info("### 💡 Suggestions de l'IA")
    
    # Affichage du résumé propre des changements
    couples = stl.session_state.suggestion_ia.split(",")
    for c in couples:
        if ":" in c:
            idx, prio = c.split(":")
            stl.write(f"- Tâche ID **{idx.strip()}** → Nouvelle priorité : **{prio.strip()}/3**")
    
    col_v, col_x = stl.columns(2)
    if col_v.button("✅ Appliquer les changements"):
        for c in couples:
            if ":" in c:
                idx, prio = c.split(":")
                modifier_priorite(int(idx.strip()), int(prio.strip()))
        
        stl.session_state.suggestion_ia = None # On vide la suggestion
        stl.success("Base de données mise à jour !")
        stl.rerun()

    if col_x.button("❌ Annuler"):
        stl.session_state.suggestion_ia = None
        stl.rerun()