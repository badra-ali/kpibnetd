import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Créer une liste vide pour stocker les données de chaque collaborateur
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
    st.image('Logo_bnetd_transparence.png', caption='', width=200)
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

def page_saisie_donnees_collaborateur():
    # Votre fonction page_saisie_donnees_collaborateur ici
    pass

def page_tableau_de_bord():
    # Votre fonction page_tableau_de_bord ici
    pass

# Page de saisie des données des collaborateurs
def page_saisie_donnees_collaborateur():
        st.image('Logo_bnetd_transparence.png',caption=' ')
        #if st.button("Saisie les Informations"):
        init_donnees_collaborateurs()
        st.title("Saisie des données de collaborateurs")
        kpi = saisir_kpi()
        st.session_state.donnees_collaborateurs.append(kpi)  # Ajouter les données du collaborateur à la liste
    
        # Créer un DataFrame à partir de la liste de données
        df = pd.DataFrame(st.session_state.donnees_collaborateurs)
    
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
                # Supprimer le fichier existant
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

        
    
# Page du tableau de bord
def page_tableau_de_bord():
    st.image('Logo_bnetd_transparence.png',caption=' ')

    df = pd.read_excel("1_graphiques_DEFI.xlsx")
    
    # Afficher un résumé des données
    st.subheader('Résumé des données')
    st.write(df.head())
    st.write(df.info())
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
            # Visualisation de la distribution des montants
            #st.subheader('Nombre de projets par collaborateur')
            fig=plt.figure(figsize=(10, 6))
            sns.histplot(df['Nom du Collaborateur'].dropna(), bins=20, kde=True)
            plt.title('Nombre de projets par collaborateur')
            st.pyplot(fig)
            

            # Visualisation de la distribution des montants
            #st.subheader('Nombre de projets par collaborateur')
            fig=plt.figure(figsize=(10, 6))
            sns.histplot(df['Typologie de marché'].dropna(), bins=20, kde=True)
            plt.title("Répartition de la Typologie de marché")
            st.pyplot(fig)
            

            #st.subheader('Repation des collaborateur part projet')
            type_handicap = df['Zone du projet']
    
            # Compter le nombre de AO pour chaque OC
            count_handicap_types = type_handicap.value_counts()
            count_handicap_types=count_handicap_types.sort_values()
            # Créer un diagramme en secteurs
            fig=plt.figure(figsize=(8, 8))
            count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
            plt.title("Répartition des Zones du projet")
            plt.ylabel('')  # Supprimer l'étiquette y
            st.pyplot(fig)

    with col2:
            #st.subheader('Repation des collaborateur part projet')
            type_handicap = df['Nom du dossier']
    
            # Compter le nombre de AO pour chaque OC
            count_handicap_types = type_handicap.value_counts()
            count_handicap_types=count_handicap_types.sort_values()
            # Créer un diagramme en secteurs
            fig=plt.figure(figsize=(8, 8))
            count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
            plt.title('Repation des collaborateur part projet')
            plt.ylabel('')  # Supprimer l'étiquette y
            st.pyplot(fig)

            #st.subheader('Repation des collaborateur part projet')
            type_handicap = df['Phasage du projet']
    
            # Compter le nombre de AO pour chaque OC
            count_handicap_types = type_handicap.value_counts()
            count_handicap_types=count_handicap_types.sort_values()
            # Créer un diagramme en secteurs
            fig=plt.figure(figsize=(8, 8))
            count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
            plt.title('Repation des Phasages du projet')
            plt.ylabel('')  # Supprimer l'étiquette y
            st.pyplot(fig)


            #st.subheader('Nombre de projets par collaborateur')
            fig=plt.figure(figsize=(10, 6))
            sns.histplot(df["État d'avancement"].dropna(), bins=20, kde=True)
            plt.title("Repation des État d'avancement")
            st.pyplot(fig)
            
    with col3:
        # Comparaison des montants moyens par autorité contractante
        #st.subheader('Comparaison des montants moyens par autorité contractante')
        fig=plt.figure(figsize=(10, 6))
        sns.barplot(x='Montant', y='Nom du Collaborateur', data=df.sort_values(by="Montant").iloc[-20:], estimator=np.mean)
        plt.title("Comparaison des montants moyens par collaborateur")
        st.pyplot(fig)


        #st.subheader('Repation des collaborateur part projet')
        type_handicap = df["Nombre d'offres envoyées par l'agent"]
    
        # Compter le nombre de AO pour chaque OC
        count_handicap_types = type_handicap.value_counts()
        count_handicap_types=count_handicap_types.sort_values()
        # Créer un diagramme en secteurs
        fig=plt.figure(figsize=(8, 8))
        count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
        plt.title("Repation des  Nombre d'offres envoyées par agent",)
        plt.ylabel('')  # Supprimer l'étiquette y
        st.pyplot(fig)

        #st.subheader('Nombre de projets par collaborateur')
        fig=plt.figure(figsize=(10, 6))
        sns.histplot(df["Type de sollicitation"].dropna(), bins=20, kde=True)
        plt.title("Repation des  Type de sollicitation")
        st.pyplot(fig)
   
# Navigation entre les différentes pages
pages = {
    "Page d'accueil": page_accueil,
    "Page de saisie des données des collaborateurs": page_saisie_donnees_collaborateur,
    "Page du tableau de bord": page_tableau_de_bord
}

# Afficher la page sélectionnée
page_selectionnee = st.sidebar.radio("Navigation", list(pages.keys()))
pages[page_selectionnee]()
