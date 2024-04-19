import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Créer une liste vide pour stocker les données de chaque collaborateur
st.image('téléchargement.jpeg', caption='', width=500)
def init_donnees_collaborateurs():
    #if 'donnees_collaborateurs' not in st.session_state:
    st.session_state.donnees_collaborateurs = []

# Fonction pour saisir les données d'un collaborateur
def saisir_kpi():
    # Saisie des données
    periode = st.date_input("Période", value=pd.Timestamp.now())
    nom_collaborateur = st.text_input("Nom du Collaborateur")
    nom_dossier = st.text_input("Nom du dossier")
    typologie_marche = st.selectbox("Typologie de marché", ["Technologie", "Services", "Industrie", "Finance", "Santé"])
    montant = st.number_input("Montant", step=1000000)
    etat_avancement = st.selectbox("État d'avancement", ["En cours", "Terminé"])
    type_sollicitation = st.radio("Type de sollicitation", ["Entrante", "Sortante"])
    nb_offres_envoyees = st.number_input("Nombre d'offres envoyées par l'agent", min_value=0)
    phasage_projet = st.selectbox("Phasage du projet", ["Phase de conception", "Phase de réalisation", "Phase de planification", "Phase de clôture"])
    modalite_paiement = st.selectbox("Modalité de paiement", ["Premier payement", "Deuxième payement", "Troisième payement", "Autre"])
    zone_projet = st.selectbox("Zone du projet", ["Afrique", "Asie", "Europe", "Amérique du Nord", "Amérique du Sud"])

    # Création d'un dictionnaire avec les données saisies
    kpi = {
        "Période": periode,
        "Nom du Collaborateur": nom_collaborateur,
        "Nom du dossier": nom_dossier,
        "Typologie de marché": typologie_marche,
        "Montant": montant,
        "État d'avancement": etat_avancement,
        "Type de sollicitation": type_sollicitation,
        "Nombre d'offres envoyées par l'agent": nb_offres_envoyees,
        "Phasage du projet": phasage_projet,
        "Modalité de paiement": modalite_paiement,
        "Zone du projet": zone_projet
    }

    return kpi

# Affichage du tableau de bord pour chaque collaborateur
# Page d'accueil
def page_accueil():
    st.title("Page d'accueil")
    st.markdown(
        """
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
            <p style="font-size: 18px;">Bienvenue sur la page d'accueil !</p>
            <p style="font-size: 16px;">Cliquez sur les liens ci-dessous pour accéder aux autres pages :</p>
            <div style="margin-top: 20px;">
                <button class="styled-button" onclick="window.location.href='/page_saisie_donnees_collaborateur'">Page de saisie des données des collaborateurs</button>
                <button class="styled-button" onclick="window.location.href='/page_tableau_de_bord'">Page du tableau de bord</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Ajoutez le style CSS dans un bloc de code HTML
st.markdown(
    """
    <style>
        .styled-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
            transition-duration: 0.4s;
        }

        .styled-button:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Page de saisie des données des collaborateur

def page_saisie_donnees_collaborateur():
        #if st.button("Saisie les Informations"):
        init_donnees_collaborateurs()
        st.title("Saisie des données de collaborateurs")
        kpi = saisir_kpi()
        st.session_state.donnees_collaborateurs.append(kpi)  # Ajouter les données du collaborateur à la liste
    
        # Créer un DataFrame à partir de la liste de données
        df = pd.DataFrame(st.session_state.donnees_collaborateurs)
        st.write("Données saisies:")
        st.write(df)
    
        if st.button("Enregistrer les données"):
        # Création d'un DataFrame avec les données saisies
        
            donnees=pd.read_excel("donnees_kpi.xlsx", sheet_name="Sheet1")
            df_updated = pd.concat((donnees, df), ignore_index=True)
            df_updated=df_updated.drop(["Unnamed: 0"], axis=1)
            #df_updated=df_updated.iloc[:,1:]
            # Enregistrement dans un fichier Excel
        
            import os
            import shutil
            
            # Chemin du fichier à remplacer
            chemin_fichier = 'donnees_kpi.xlsx'
            
            # Vérifier si le fichier existe
            if os.path.exists(chemin_fichier):
                # Supprimer le fichier existanta
                os.remove(chemin_fichier)
                print(f"Le fichier {chemin_fichier} existant a été supprimé.")
            
            # Copier le nouveau fichier pour le remplacer
            try:
                # Assurez-vous que vous avez les autorisations nécessaires pour écrire dans ce répertoire
                shutil.copy2('nouveau_donnees_kpi.xlsx', chemin_fichier)
                print("Le fichier a été remplacé avec succès.")
            except PermissionError:
                print("Vous n'avez pas les autorisations nécessaires pour écrire dans ce répertoire.")
            except FileNotFoundError:
                print("Le fichier source n'existe pas.")
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")
            # Enregistrement dans un fichier Excel
            df_updated.to_excel("donnees_kpi.xlsx")
            st.success("Les données ont été enregistrées avec succès dans 'donnees_kpi.xlsx'")

        #if st.button("Importez un Fichier"):
        #st.write("ok")

st.markdown(
    """
    <style>
        .button-primary {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin-top: 20px;
            cursor: pointer;
            border-radius: 5px;
            transition-duration: 0.4s;
        }

        .button-primary:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True
)

    
# Page du tableau de bord
def page_tableau_de_bord():

    # Chargement des données
    df = pd.read_excel("1_graphiques_DEFI.xlsx")

    # Titre et description
    st.title("Tableau de Bord")
    st.write("Bienvenue sur votre tableau de bord. Explorez les différentes visualisations pour comprendre vos données.")

    # Résumé des données
    st.header("Résumé des données")
    st.write(df.head())
    st.write(df.info())

    # Visualisations avec colonnes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Nombre de projets par collaborateur")
        fig, ax = plt.subplots()
        sns.histplot(df['Nom du Collaborateur'].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title('Nombre de projets par collaborateur')
        st.pyplot(fig)

        st.subheader("Répartition de la Typologie de marché")
        fig, ax = plt.subplots()
        sns.histplot(df['Typologie de marché'].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title("Répartition de la Typologie de marché")
        st.pyplot(fig)

    with col2:
        st.subheader("Répartition des Zones du projet")
        fig, ax = plt.subplots()
        df['Zone du projet'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title("Répartition des Zones du projet")
        st.pyplot(fig)

        st.subheader("Répartition des Phasages du projet")
        fig, ax = plt.subplots()
        df['Phasage du projet'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title("Répartition des Phasages du projet")
        st.pyplot(fig)

    with col3:
        st.subheader("Répartition des collaborateurs par projet")
        fig, ax = plt.subplots()
        df['Nom du dossier'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title('Répartition des collaborateurs par projet')
        st.pyplot(fig)

        st.subheader("Répartition des État d'avancement")
        fig, ax = plt.subplots()
        sns.histplot(df["État d'avancement"].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title("Répartition des État d'avancement")
        st.pyplot(fig)

    # Comparaison des montants moyens par collaborateur
    st.header("Comparaison des montants moyens par collaborateur")
    fig, ax = plt.subplots()
    sns.barplot(x='Montant', y='Nom du Collaborateur', data=df.sort_values(by="Montant").iloc[-20:], estimator=np.mean, ax=ax)
    ax.set_title("Comparaison des montants moyens par collaborateur")
    st.pyplot(fig)

    # Répartition du Nombre d'offres envoyées par agent
    st.header("Répartition du Nombre d'offres envoyées par agent")
    fig, ax = plt.subplots()
    df["Nombre d'offres envoyées par l'agent"].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_title("Répartition du Nombre d'offres envoyées par agent")
    st.pyplot(fig)

    # Répartition du Type de sollicitation
    st.header("Répartition du Type de sollicitation")
    fig, ax = plt.subplots()
    sns.histplot(df["Type de sollicitation"].dropna(), bins=20, kde=True, ax=ax)
    ax.set_title("Répartition du Type de sollicitation")
    st.pyplot(fig)
   

def gestion_profils_utilisateurs():
    st.subheader("Gestion des profils utilisateurs")
    
    # Formulaire pour créer un nouveau profil utilisateur
    with st.form(key='profil_form'):
        st.write("### Créer un nouveau profil utilisateur")
        nom_profil = st.text_input("Nom du profil utilisateur*")
        description_profil = st.text_area("Description du profil utilisateur")
        fonctionnalites_autorisees = st.text_area("Fonctionnalités autorisées*")
        submit_button = st.form_submit_button(label='Créer le profil')
        
        if submit_button:
            # Vérification des champs obligatoires
            if nom_profil and fonctionnalites_autorisees:
                # Ajoutez ici la logique pour enregistrer le nouveau profil utilisateur dans la base de données
                st.success(f"Le profil utilisateur '{nom_profil}' a été créé avec succès !")
            else:
                st.error("Les champs marqués d'une astérisque (*) sont obligatoires.")
    
    # Section pour les autres fonctionnalités de gestion des profils utilisateurs
    with st.expander("Autres actions"):
        action = st.selectbox("Sélectionner une action", ["Activer un compte", "Désactiver un compte", "Bloquer un compte", "Débloquer un compte", "Déverrouiller un compte", "Réinitialiser un mot de passe"])
        
        if action == "Activer un compte":
            # Logique pour activer un compte
            st.write("Fonctionnalité d'activation de compte")
        elif action == "Désactiver un compte":
            # Logique pour désactiver un compte
            st.write("Fonctionnalité de désactivation de compte")
        elif action == "Bloquer un compte":
            # Logique pour bloquer un compte
            st.write("Fonctionnalité de blocage de compte")
        elif action == "Débloquer un compte":
            # Logique pour débloquer un compte
            st.write("Fonctionnalité de déblocage de compte")
        elif action == "Déverrouiller un compte":
            # Logique pour déverrouiller un compte
            st.write("Fonctionnalité de déverrouillage de compte")
        elif action == "Réinitialiser un mot de passe":
            # Logique pour réinitialiser un mot de passe
            st.write("Fonctionnalité de réinitialisation de mot de passe")

def gestion_fonctionnalites_profils():
    st.subheader("Gestion des fonctionnalités des profils")
    
    # Liste des fonctionnalités disponibles
    fonctionnalites = ["Fonctionnalité 1", "Fonctionnalité 2", "Fonctionnalité 3"]  # Ajoutez ici vos fonctionnalités
    
    # Simulez une liste de profils utilisateurs (à remplacer par votre propre logique)
    profils_utilisateurs = ["Profil Utilisateur 1", "Profil Utilisateur 2", "Profil Utilisateur 3"]  

    # Affichage du tableau de sélection des fonctionnalités pour chaque profil utilisateur
    for profil in profils_utilisateurs:
        st.write(f"Profil utilisateur : {profil}")
        for fonctionnalite in fonctionnalites:
            checkbox_state = st.checkbox(fonctionnalite, key=f"{profil}_{fonctionnalite}")
            # Ajoutez ici la logique pour attribuer les fonctionnalités sélectionnées à chaque profil utilisateur
            if checkbox_state:
                st.write(f"La fonctionnalité '{fonctionnalite}' est attribuée au profil '{profil}'")


def gestion_utilisateurs():
    st.subheader("Gestion des utilisateurs")
    
    # Formulaire pour créer un nouvel utilisateur
    with st.form(key='utilisateur_form'):
        nom_utilisateur = st.text_input("Nom de l'utilisateur")
        email_utilisateur = st.text_input("Email de l'utilisateur")
        profil_utilisateur = st.selectbox("Profil de l'utilisateur", ["Profil 1", "Profil 2", "Profil 3"])  # Remplacez par vos profils disponibles
        submit_button = st.form_submit_button(label='Créer l\'utilisateur')
    
        if submit_button:
            # Ajoutez ici la logique pour enregistrer le nouvel utilisateur dans la base de données
            st.success(f"L'utilisateur '{nom_utilisateur}' a été créé avec succès !")


def parametrage_kpi():
    st.subheader("Paramétrage des KPIs")
    
    # Formulaire pour ajouter un nouveau KPI
    with st.form(key='ajout_kpi_form'):
        nom_kpi = st.text_input("Nom du KPI")
        description_kpi = st.text_area("Description du KPI")
        unite_organisationnelle = st.selectbox("Unité organisationnelle", ["Unité 1", "Unité 2", "Unité 3"])  # Remplacez par vos unités organisationnelles
        workflow = st.selectbox("Workflow", ["Workflow 1", "Workflow 2", "Workflow 3"])  # Remplacez par vos workflows
        source_donnees = st.selectbox("Source de données", ["Source 1", "Source 2", "Source 3"])  # Remplacez par vos sources de données
        exercice = st.selectbox("Exercice", ["Exercice 1", "Exercice 2", "Exercice 3"])  # Remplacez par vos exercices
        submit_button = st.form_submit_button(label='Ajouter le KPI')
    
        if submit_button:
            # Ajoutez ici la logique pour enregistrer le nouveau KPI dans la base de données
            st.success(f"Le KPI '{nom_kpi}' a été ajouté avec succès !")
    
    # Liste des KPIs existants avec possibilité de modification ou suppression
    # Ajoutez ici la logique pour récupérer les KPIs depuis la base de données
    kpis = ["KPI 1", "KPI 2", "KPI 3"]  # Exemple de liste de KPIs
    for index, kpi in enumerate(kpis):
        with st.expander(f"{kpi} - Modifier/Supprimer"):
            st.write(f"Description : Description du {kpi}")
            st.write(f"Unité organisationnelle : Unité 1")
            st.write(f"Workflow : Workflow 1")
            st.write(f"Source de données : Source 1")
            st.write(f"Exercice : Exercice 1")
            bouton_modifier = st.button(f"Modifier {index}")
            bouton_supprimer = st.button(f"Supprimer {index}")
            if bouton_modifier:
                # Ajoutez ici la logique pour modifier le KPI sélectionné
                st.info(f"Vous avez cliqué sur Modifier pour le KPI '{kpi}'")
            if bouton_supprimer:
                # Ajoutez ici la logique pour supprimer le KPI sélectionné
                st.warning(f"Vous avez cliqué sur Supprimer pour le KPI '{kpi}'")

def definition_objectifs_exercice():
    st.subheader("Définition des objectifs pour chaque exercice")
    
    # Formulaire pour ajouter un nouvel objectif
    with st.form(key='ajout_objectif_form'):
        organisation = st.selectbox("Organisation", ["Organisation 1", "Organisation 2", "Organisation 3"])  # Remplacez par vos organisations
        periode = st.text_input("Période")
        saisies = st.text_area("Saisies")
        calculs = st.text_area("Calculs")
        commentaires_recommandations = st.text_area("Commentaires/Recommandations")
        submit_button = st.form_submit_button(label='Ajouter l\'objectif')
    
        if submit_button:
            # Ajoutez ici la logique pour enregistrer le nouvel objectif dans la base de données
            st.success("L'objectif a été ajouté avec succès !")
    
    # Liste des objectifs existants avec possibilité de modification ou suppression
    # Ajoutez ici la logique pour récupérer les objectifs depuis la base de données
    objectifs = ["Objectif 1", "Objectif 2", "Objectif 3"]  # Exemple de liste d'objectifs
    for index, objectif in enumerate(objectifs):
        with st.expander(f"{objectif} - Modifier/Supprimer"):
            st.write(f"Organisation : Organisation 1")
            st.write(f"Période : Période 1")
            st.write(f"Saisies : {objectif} saisies")
            st.write(f"Calculs : {objectif} calculs")
            st.write(f"Commentaires/Recommandations : {objectif} commentaires/recommandations")
            bouton_modifier = st.button(f"Modifier {index}")
            bouton_supprimer = st.button(f"Supprimer {index}")
            if bouton_modifier:
                # Ajoutez ici la logique pour modifier l'objectif sélectionné
                st.info(f"Vous avez cliqué sur Modifier pour l'objectif '{objectif}'")
            if bouton_supprimer:
                # Ajoutez ici la logique pour supprimer l'objectif sélectionné
                st.warning(f"Vous avez cliqué sur Supprimer pour l'objectif '{objectif}'")


import streamlit as st

def suivi_audits():
    st.subheader("Suivi des adaptations effectuées dans l'application")

    # Formulaire pour ajouter un nouvel audit
    with st.form(key='ajout_audit_form'):
        date_audit = st.date_input("Date de l'audit")
        description_audit = st.text_area("Description de l'audit")
        responsable_audit = st.text_input("Responsable de l'audit")
        submit_button = st.form_submit_button(label="Ajouter l'audit")

        if submit_button:
            # Ajoutez ici la logique pour enregistrer le nouvel audit dans la base de données
            st.success("L'audit a été ajouté avec succès !")

    # Liste des audits existants avec possibilité de modification ou suppression
    # Ajoutez ici la logique pour récupérer les audits depuis la base de données
    audits = [("2024-01-01", "Audit 1", "Responsable 1"), ("2024-01-15", "Audit 2", "Responsable 2")]  # Exemple de liste d'audits
    for index, audit in enumerate(audits):
        with st.expander(f"Audit {index+1} - Modifier/Supprimer"):
            st.write(f"Date de l'audit : {audit[0]}")
            st.write(f"Description de l'audit : {audit[1]}")
            st.write(f"Responsable de l'audit : {audit[2]}")
            bouton_modifier = st.button(f"Modifier {index+1}")
            bouton_supprimer = st.button(f"Supprimer {index+1}")
            if bouton_modifier:
                # Ajoutez ici la logique pour modifier l'audit sélectionné
                st.info(f"Vous avez cliqué sur Modifier pour l'audit {index+1}")
            if bouton_supprimer:
                # Ajoutez ici la logique pour supprimer l'audit sélectionné
                st.warning(f"Vous avez cliqué sur Supprimer pour l'audit {index+1}")


# Fonction pour afficher les indicateurs spécifiques à chaque entité
def mes_indicateurs():
    st.sidebar.subheader("Mes indicateurs")
    
    # Sélection de l'entité (département, service)
    selected_entity = st.sidebar.selectbox("Sélectionnez une entité :", ["Département 1", "Département 2", "Département 3"])  # Remplacez par vos départements ou services
    
    # Simulation de données d'indicateurs (à remplacer par vos propres données)
    indicators_data = {
        "Indicateur 1": {"value": 80, "min": 60, "max": 100, "recommandation": "Améliorer la collecte de données."},
        "Indicateur 2": {"value": 40, "min": 50, "max": 90, "recommandation": "Analyser les causes de sous-performance."},
        "Indicateur 3": {"value": 70, "min": 70, "max": 120, "recommandation": "Maintenir la performance actuelle."},
    }
    
    # Affichage des indicateurs en fonction de l'entité sélectionnée
    if selected_entity:
        st.subheader(f"Indicateurs pour {selected_entity}")
        
        # Affichage des indicateurs au vert et au rouge
        st.subheader("Indicateurs au vert :")
        for indicator, data in indicators_data.items():
            if data["value"] >= data["min"] and data["value"] <= data["max"]:
                st.write(f"{indicator}: {data['value']} (Plage de valeurs acceptables)")
        
        st.subheader("Indicateurs au rouge :")
        for indicator, data in indicators_data.items():
            if data["value"] < data["min"] or data["value"] > data["max"]:
                st.write(f"{indicator}: {data['value']} (Hors de la plage de valeurs acceptables)")
        
        # Affichage des recommandations par indicateur
        st.subheader("Recommandations par indicateur :")
        for indicator, data in indicators_data.items():
            st.write(f"{indicator}: {data['recommandation']}")

# Barre de navigation
st.sidebar.title("Module Administration et KPI")
option = st.sidebar.radio("Sélectionnez une option :", ["Accueil", "Gestion des profils utilisateurs", "Gestion des fonctionnalités des profils", "Gestion des utilisateurs", "Paramétrage des KPIs", "Exercice", "Suivi et Audit", "Saisis Information KPI", "Tableau de Bord", "Mes indicateurs"])

# Affichage de la fonctionnalité sélectionnée

if option == "Accueil":
    page_accueil()
elif option == "Gestion des profils utilisateurs":
    gestion_profils_utilisateurs()
elif option == "Gestion des fonctionnalités des profils":
    gestion_fonctionnalites_profils()
elif option == "Gestion des utilisateurs":
    gestion_utilisateurs()
elif option == "Paramétrage des KPIs":
    parametrage_kpi()
elif option == "Exercice":
    definition_objectifs_exercice()
elif option == "Suivi et Audit":
    suivi_audits()
elif option == "Saisis Information KPI":
    page_saisie_donnees_collaborateur()
elif option == "Tableau de Bord":
    page_tableau_de_bord()
elif option == "Mes indicateurs":
    mes_indicateurs()
