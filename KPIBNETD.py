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


# Page de saisie des données des collaborateur

def page_saisie_donnees_collaborateur():
    st.image('Logo_bnetd_transparence.png', caption='', width=200)
    
    st.title("Saisie des données de collaborateurs")
    
    # Saisie des KPIs
    kpi = saisir_kpi()
    
    # Ajout des données du collaborateur à la session
    if 'donnees_collaborateurs' not in st.session_state:
        st.session_state.donnees_collaborateurs = []
        st.session_state.donnees_collaborateurs.append(kpi)
    
    # Affichage des données saisies dans un DataFrame
    st.write("Données saisies:")
    df = pd.DataFrame(st.session_state.donnees_collaborateurs)
    st.write(df)
    
    # Bouton pour enregistrer les données
    if st.button("Enregistrer les données"):
        enregistrer_donnees(df)
        st.success("Les données ont été enregistrées avec succès dans 'donnees_kpi.xlsx'")

def enregistrer_donnees(df):
    # Enregistrement des données dans un fichier Excel
    
    # Lecture des données existantes depuis le fichier Excel
    donnees = pd.read_excel("donnees_kpi.xlsx", sheet_name="Sheet1")
    
    # Concaténation des nouvelles données avec les données existantes
    df_updated = pd.concat([donnees, df], ignore_index=True)
    
    # Suppression de la colonne "Unnamed: 0" si elle existe
    if "Unnamed: 0" in df_updated.columns:
        df_updated = df_updated.drop(columns=["Unnamed: 0"])
    
    # Remplacement du fichier Excel existant
    chemin_fichier = 'donnees_kpi.xlsx'
    if os.path.exists(chemin_fichier):
        os.remove(chemin_fichier)
    shutil.copy2('nouveau_donnees_kpi.xlsx', chemin_fichier)
    
    # Enregistrement des données dans le fichier Excel
    df_updated.to_excel("donnees_kpi.xlsx", index=False)

# Appel de la fonction page_saisie_donnees_collaborateur
page_saisie_donnees_collaborateur()

# Ajout du style CSS dans un bloc de code HTML
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
