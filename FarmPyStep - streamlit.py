#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 22:46:02 2021

@author: linuit
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate, train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px

st.set_page_config(
    page_title="FarmPyStep - Analyse de la base de donnée Agribalyse 3.0",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Nous chargeons le fichier "AGRIBALYSE3.0.1_vf.xlsm" dans un Dataframe appelé df_agri
df_agri = pd.read_excel('data/AGRIBALYSE3.0.1_vf.xlsm', sheet_name=1, header=1)

#Nous chargeons le fichier "AGRIBALYSE3_partie_agriculture_bio.xlsx" dans un Dataframe appelé df_agri_bio
df_agri_bio = pd.read_excel('data/AGRIBALYSE3_partie_agriculture_bio.xlsx', sheet_name=1, header=2)

#Nous chargeons le fichier "AGRIBALYSE3_partie_agriculture_conv.xlsx" dans un Dataframe appelé df_agri_conv
df_agri_conv = pd.read_excel('data/AGRIBALYSE3_partie_agriculture_conv.xlsx', sheet_name=1, header=2)

#Nous chargeons le fichier "tableau de ponderation EF3.xlsx" dans un Dataframe appelé df_ponderation
df_ponderation = pd.read_excel('data/Tableau_de_ponderation_EF3.xlsx')

# Création des dictionnaires associant les anciens noms aux nouveaux noms de colonnes
dict_agri = {
    "Code\nAGB" :"Code_AGB",
    "Code\nCIQUAL": "Code_CIQUAL",
    "Groupe d'aliment": "Group_aliment",
    "Sous-groupe d'aliment": "Sous_group_aliment",
    "Nom du Produit en Français": "Nom_produit",
    "LCI Name": "LCI",
    "Saisonnalité": "saisonnalite",
    "Transport par avion\n(1 : par avion)": "usage_avion",
    "Livraison": "Mode_Livraison",
    "Matériau d'emballage": "Type_emballage",
    "Préparation": "Mode_Preparation",
    "DQR - Note de qualité de la donnée (1 excellente ; 5 très faible)": "DQR",
    "Score unique EF (mPt/kg de produit)": "Score_EF",
    "Changement climatique (kg CO2 eq/kg de produit)": "Change_clima",
    "Appauvrissement de la couche d'ozone (E-06 kg CVC11 eq/kg de produit)": "impact_ozone",
    "Rayonnements ionisants (kBq U-235 eq/kg de produit)": "rayons_ionisants",
    "Formation photochimique d'ozone (E-03 kg NMVOC eq/kg de produit)": "photochimique_ozone",
    "Particules (E-06 disease inc./kg de produit)": "particules",
    "Acidification terrestre et eaux douces (mol H+ eq/kg de produit)": "acidification",
    "Eutrophisation terreste (mol N eq/kg de produit)": "Eutrophisation_terre",
    "Eutrophisation eaux douces (E-03 kg P eq/kg de produit)": "Eutrophisation_eau_douce",
    "Eutrophisation marine (E-03 kg N eq/kg de produit)": "Eutrophisation_eau_marine",
    "Utilisation du sol (Pt/kg de produit)": "usage_sol",
    "Écotoxicité pour écosystèmes aquatiques d'eau douce (CTUe/kg de produit)": "ecotoxicite",
    "Épuisement des ressources eau (m3 depriv./kg de produit)": "epuisement_eau",
    "Épuisement des ressources énergétiques (MJ/kg de produit)": "epuisement_energie",
    "Épuisement des ressources minéraux (E-06 kg Sb eq/kg de produit)": "epuisement_mineraux"
}

dict_agri_conv = {
    'Nom du Produit en Français (traduction approximative GoogleTranslate)': 'Name',
    'LCI Name': 'LCI_Name',
    'Catégorie': 'Categorie',
    'kg CO2 eq': 'Changement climatique',
    'kg CFC11 eq': 'Appauvrissement de la couche d’ozone',
    'kBq U-235 eq': 'Radiation ionisante, effet sur la santé',
    'kg NMVOC eq': 'Formation photochimique d’ozone',
    'disease inc.': 'Particules fines',
    'mol H+ eq': 'Acidification',
    'kg P eq': 'Eutrophisation, eau douce',
    'kg N eq': 'Eutrophisation, marine',
    'mol N eq': 'Eutrophisation, terrestre',
    'CTUe': 'Ecotoxicité d\'eau douce',
    'Pt': 'Usage des terres',
    'm3 depriv.': 'Épuisement des ressources en eau',
    'MJ': 'Épuisement des ressources énergétiques',
    'kg Sb eq': 'Épuisement des ressources - minéraux',
    'kg CO2 eq.1': 'Climate_Change_Fossil',
    'kg CO2 eq.2': 'Climate_Change_Biogenic',
    'kg CO2 eq.3': 'Climate_Change_Land_Use_And_Transform'
}

dict_agri_bio = {
    'Nom du Produit en Français (traduction approximative googleTranslate)': 'Name',
    'Complément d\'information, voir rapport ACV Bio pour détails': 'Additional_Information',
    'LCI Name' : 'LCI_Name',
    'Catégorie' : 'Categorie',
    'kg CO2 eq': 'Changement climatique',
    'kg CFC11 eq': 'Appauvrissement de la couche d’ozone',
    'kBq U-235 eq': 'Radiation ionisante, effet sur la santé',
    'kg NMVOC eq': 'Formation photochimique d’ozone',
    'disease inc.': 'Particules fines',
    'mol H+ eq': 'Acidification',
    'kg P eq': 'Eutrophisation, eau douce',
    'kg N eq': 'Eutrophisation, marine',
    'mol N eq': 'Eutrophisation, terrestre',
    'CTUe': 'Ecotoxicité d\'eau douce',
    'Pt': 'Usage des terres',
    'm3 depriv.': 'Épuisement des ressources en eau',
    'MJ': 'Épuisement des ressources énergétiques',
    'kg Sb eq': 'Épuisement des ressources - minéraux',
    'kg CO2 eq.1': 'Climate_Change_Fossil',
    'kg CO2 eq.2': 'Climate_Change_Biogenic',
    'kg CO2 eq.3': 'Climate_Change_Land_Use_And_Transform'
}

# Nous renommons les variables
df_agri_conv.rename(dict_agri_conv, axis = 1, inplace=True)
df_agri_bio.rename(dict_agri_bio, axis = 1, inplace=True)
df_agri.rename(dict_agri, axis = 1, inplace=True)

# Le dataframe df_agri_bio contient 2 colonnes supplémentaire non indispensable pour l'étude
# Suppression de ces 2 colonnes
df_agri_bio.drop(['Additional_Information', 'Source'], axis=1, inplace=True)

# On supprime les lignes contenant au moins une valeur manquante dans df_agri_bio
df_agri_bio = df_agri_bio.dropna(axis = 0, how = 'any').reset_index(drop=True)

# On supprime les lignes contenant au moins une valeur manquante dans df_ponderation
df_ponderation = df_ponderation.dropna(axis = 0, how = 'any').reset_index(drop=True)

# Création d'un dictionnaire pour ayant pour clé le titre et pour valeur la pondération
ponderation_ef = pd.DataFrame(data=df_ponderation[['French_Title','Final weighting factors (incl. robustness)']])
dict_ponderation = ponderation_ef.set_index('French_Title').T.to_dict('records')
dict_ponderation = dict_ponderation[0]

# Création de la fonction permettant de calculer le score
# Celle ci prend en paramétre un dataframe et un dictionnaire
def calcul_score(df, data):
    """Calcul le score EF et reourne un dataframe"""
    # La ligne ci-dessous sert a enlever l'avertissement python "SettingWithCopyWarning"
    with pd.option_context("mode.chained_assignment", None):
        df['score EF'] = np.nan
        for index in range(len(df)):
            score_item = 0
            nbre_item = 0
            for name, values in df.items():
                if name in data:
                    score_item += values[index] * (data[name]/100)
                    nbre_item += 1
            df['score EF'].iloc[index] = round(((score_item * nbre_item) / 1000),2)
        return df
    
# On applique la fonction au deux dataframe
calcul_score(df_agri_bio, dict_ponderation)
calcul_score(df_agri_conv, dict_ponderation)

# Profil moyen de consommation des français
profil_moyen = {
    'catégorie de produit': ["Produits laitiers", "Fruits et légumes", "Viandes, poissons, œufs", "Produits céréales", "Eaux et autres boissons","Autres"],
    'un enfant de 0 à 10 ans (%)': [24,18,5,6,32,15],
    'un adolescent de 11 à 17 ans (%)': [16,15,7,8,38,16],
    'un adulte (%)': [6,16,6,6,55,11]
}

df_profil = pd.DataFrame(profil_moyen)

def plot_profil(df, col):
    fig = px.pie(
        df, 
        values = df[col + ' (%)'],
        names = df['catégorie de produit'], 
        title = "<b>" + col.title() + "</b>"
    )
    st.plotly_chart(fig)


# Mise en page de l'application
if __name__ == "__main__":
    st.info("""
        Le programme Agribalyse® produit des données de référence sur les impacts environnementaux des produits agricoles et alimentaires.
        Les méthodologies et les données ont été élaborées et validées dans le cadre d’un partenariat veillant à leur qualité et leur transparence (ADEME, INRAE, les instituts techniques agricoles et agroalimentaires, des experts indépendants et des cabinets d’études).
        Agribalyse® est la base de données publique française la plus exhaustive d’indicateurs environnementaux des produits agricoles et alimentaires fondés sur l’Analyse du Cycle de Vie.
        Elle fournit des indicateurs d’impacts environnementaux.
    """)
    
with st.sidebar:
    st.title("FarmPyStep")
    options = st.selectbox("Type d'analyse", ('Profil', 'Alimentation'), 0)
    if options == 'Alimentation':
        st.subheader("Combinaison alimentaire:")
        mode = st.radio(
            "Régime alimentaire",
            [
                "consommation de tous les aliments",
                "flexitarien",
                "végétarisme",
                "végétalisme",
                "régime paléo",
                "régime céto"
            ],
        )
    else:
        st.subheader("Profil moyen de consommation alimentaire:")
        mode = st.radio(
            "Profil",
            [
                "tous les profiles",
                "un enfant de 0 à 10 ans",
                "un adolescent de 11 à 17 ans",
                "un adulte",
            ],
        )


if (mode == 'tous les profiles') or (mode == 'un enfant de 0 à 10 ans') or (mode == 'un adolescent de 11 à 17 ans') or (mode == 'un adulte'):
    st.title("Assiette étudiée")
    st.markdown(
        """
            ## Comment est construit ce profil?
            L’étude nationale de référence qui donne une photographie de la consommation alimentaire actuelle moyenne en
            France est l’étude individuelle nationale des consommations alimentaires (INCA) réalisée par l’Agence nationale
            de sécurité sanitaire de l’alimentation, de l’environnement et du travail (ANSES).
            L'étude INCA 3 et ses résultats permettent de déterminer le profil moyen de consommation alimentaire des français.
            Pour plus d'information : (https://www.anses.fr/fr/content/inca-3-en-image-dans-lassiette-des-fran%C3%A7ais)
        """
    )
    if mode == 'tous les profiles':
        st.dataframe(df_profil)
        plot_profil(df_profil, 'un enfant de 0 à 10 ans')
        plot_profil(df_profil, 'un adolescent de 11 à 17 ans')
        plot_profil(df_profil, 'un adulte')
    elif mode == 'un enfant de 0 à 10 ans':
        st.dataframe(df_profil.iloc[:,:2])
        plot_profil(df_profil, 'un enfant de 0 à 10 ans')
    elif mode == 'un adolescent de 11 à 17 ans':
        st.dataframe(df_profil[['catégorie de produit','un adolescent de 11 à 17 ans (%)']])
        plot_profil(df_profil, 'un adolescent de 11 à 17 ans')
    else:
        st.dataframe(df_profil[['catégorie de produit','un adulte (%)']])
        plot_profil(df_profil, 'un adulte')
        
if (mode == 'consommation de tous les aliments') or (mode == 'flexitarien') or (mode == 'végétarisme') or (mode == 'végétalisme') or (mode == 'régime paléo') or (mode == 'régime céto'):
    st.title(mode.title())
    if mode == 'consommation de tous les aliments':
        item = "un adulte (kg/par an)"
        st.markdown(
            """
                Sur la base des études de l'INCA 3, nous calculerons l'impact de chaque personne en fonction de sa culture alimentaire.
                Comme mentionné dans l'étude, en moyenne, les adultes de 18 à 79 ans, consomment 2,9 kg d’aliments et de boissons par jour.
                Les boissons représentent plus de la moitié de cette ration journalière, et l’eau constitue la moitié des boissons consommées.
            """
        )
        st.latex("2,9 * 12 = 1058.5 (kg/par an)")
        df_consommation_an = pd.concat([pd.DataFrame(df_profil['catégorie de produit']), pd.DataFrame((df_profil['un adulte (%)']*1058.5)/100)],  axis=1)
        df_consommation_an.rename({"un adulte (%)": "un adulte (kg/par an)"}, axis=1, inplace=True)
        
        st.text('Consommation pour un adulte')
        st.dataframe(df_consommation_an)
        df_agri_score = df_agri.groupby("Group_aliment", as_index = False).agg({"Score_EF" : "mean"})
        st.text('Score par groupe d\'aliment.')
        st.dataframe(df_agri_score.sort_values(["Score_EF"], ascending = False))
    
        plt.figure(figsize = (5,5))
        plt.title("Score des groupes d'aliments")
        plt.ylabel("Des groupes d'aliments")
        plt.xlabel("Score EF")
        sns.barplot(y='Group_aliment', x='Score_EF', data=df_agri_score)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    
        dic_categorie_produit = {
            'Catégorie de produit' : 
                ["Produits laitiers",
                 "Fruits et légumes",
                 "Viandes, poissons, œufs",
                 "Produits céréales", 
                 "Eaux et autres boissons",
                 "Autres"],
            'Score_par_an' : [
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Produits laitiers']['un adulte (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'lait et produits laitiers']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Fruits et légumes']['un adulte (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'fruits, légumes, légumineuses et oléagineux']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Viandes, poissons, œufs']['un adulte (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'viandes, œufs, poissons']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Produits céréales']['un adulte (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'produits céréaliers']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Eaux et autres boissons']['un adulte (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'boissons']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Autres']['un adulte (kg/par an)'].values[0] * ((df_agri_score[df_agri_score['Group_aliment'] == 'aides culinaires et ingrédients divers']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'glaces et sorbets']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'matières grasses']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'produits sucrés']['Score_EF'].values[0])/4),
                ]
        }
        df_agri_score_par_an = pd.DataFrame(dic_categorie_produit)
        st.text('Impact des personnes qui mange tous les aliments en un an.')
        st.dataframe(df_agri_score_par_an)
        fig = px.pie(
            df_agri_score_par_an, 
            values = df_agri_score_par_an['Score_par_an'],
            names = df_agri_score_par_an['Catégorie de produit'].values, 
            title = "<b>Score pour une année par catégorie de produits</b>"
        )
        st.plotly_chart(fig)
        score = f"{mode} : pour toutes les catégories d'aliments, le score moyen pour l'année est {df_agri_score_par_an.Score_par_an.mean()}"
        st.info(score)
        
    elif mode == 'végétarisme':
        st.markdown(
            """
                Considérez le score moyen pour une année de végétarisme.
                Le végétarisme est un régime alimentaire à base de plantes et de produits laitiers, avec le rejet de la viande et des aliments d'origine animale (y compris la volaille, le poisson et les fruits de mer).
                Certaines options végétariennes peuvent exclure les produits laitiers et les œufs. Mais dans l'analyse, j'enleverrai ce dernier.
                Remplaçons la viande et le poisson de l'assiette standard des Français par des légumes, des fruits et des légumineuses.
            """
        )
        dict_regime = {
            'catégorie de produit' : ["Produits laitiers", "Fruits et légumes", "œufs", "Produits céréales", "Eaux et autres boissons","Autres"],
            'Un végétarien (%)': [6,20,2,6,55,11]
            }
        df_profil_regime = pd.DataFrame(dict_regime)
        st.text('Profil pour un adulte végétarien')
        st.dataframe(df_profil_regime)
        
        fig = px.pie(
            df_profil_regime, 
            values = df_profil_regime['Un végétarien (%)'],
            names = df_profil_regime['catégorie de produit'], 
            title = "<b>Profil pour un adulte végétarien</b>"
            )
        st.plotly_chart(fig)
        
        st.warning("Nous excluons les produits animaux de notre base de données d'origine et calculons le score.")
        
        df_agri_regime = df_agri[(df_agri.Sous_group_aliment == 'fruits')| (df_agri.Sous_group_aliment == 'algues')|
                  (df_agri.Sous_group_aliment == 'herbes')|(df_agri.Sous_group_aliment == 'boisson alcoolisées')|
                  (df_agri.Sous_group_aliment == 'fruits à coque et graines oléagineuses')|
                  (df_agri.Sous_group_aliment == 'pâtes, riz et céréales')|
                  (df_agri.Sous_group_aliment == 'farines et pâtes à tarte')|
                  (df_agri.Sous_group_aliment == 'légumes')|
                  (df_agri.Sous_group_aliment == 'fromages')|
                  (df_agri.Sous_group_aliment == 'gâteaux et pâtisseries')|
                  (df_agri.Sous_group_aliment == 'pains et viennoiseries')|
                  (df_agri.Sous_group_aliment == 'pommes de terre et autres tubercules')|
                  (df_agri.Sous_group_aliment == 'chocolats et produits à base de chocolat')|
                  (df_agri.Sous_group_aliment == 'céréales de petit-déjeuner et biscuits')|
                  (df_agri.Sous_group_aliment == 'ingrédients divers')|
                  (df_agri.Sous_group_aliment == 'beurres')|
                  (df_agri.Sous_group_aliment == 'glaces')| (df_agri.Sous_group_aliment == 'huiles et graisses végétales')|
                  (df_agri.Sous_group_aliment == 'boissons sans alcool')|
                  (df_agri.Sous_group_aliment == 'produits laitiers frais et assimilés')|
                  (df_agri.Sous_group_aliment == 'épices')|
                  (df_agri.Sous_group_aliment == 'sauces')|
                  (df_agri.Sous_group_aliment == 'confiseries non chocolatées')|
                  (df_agri.Sous_group_aliment == 'confitures et assimilés')|(df_agri.Sous_group_aliment == 'desserts glacés')|
                  (df_agri.Sous_group_aliment == 'aides culinaires')|(df_agri.Sous_group_aliment == 'eaux')|
                  (df_agri.Sous_group_aliment == 'crèmes et spécialités à base de crème')|
                  (df_agri.Sous_group_aliment == 'légumineuses')|
                  (df_agri.Sous_group_aliment == 'sucres, miels et assimilés')|
                  (df_agri.Sous_group_aliment == 'sels')|(df_agri.Sous_group_aliment == 'sorbets')|
                  (df_agri.Sous_group_aliment == 'laits')|
                  (df_agri.Sous_group_aliment == 'autres matières grasses')|
                  (df_agri.Sous_group_aliment == 'margarines')|(df_agri.Sous_group_aliment == 'condiments')|
                  (df_agri.Sous_group_aliment == 'œufs')|
                  (df_agri.Sous_group_aliment == 'denrées destinées à une alimentation particulière')
               ]
        
        df_agri_score = df_agri_regime.groupby("Group_aliment", as_index = False).agg({"Score_EF" : "mean"})
        st.text('Score par groupe d\'aliment.')
        st.dataframe(df_agri_score.sort_values(["Score_EF"], ascending = False))
        
        plt.figure(figsize = (5,5))
        plt.title("Score des groupes d'aliments (Végétarien)")
        plt.ylabel("Des groupes d'aliments")
        plt.xlabel("Score EF")
        sns.barplot(y='Group_aliment', x='Score_EF', data=df_agri_score)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        
        df_consommation_an = pd.concat([pd.DataFrame(df_profil_regime['catégorie de produit']), pd.DataFrame((df_profil_regime['Un végétarien (%)']*1058.5)/100)],  axis=1)
        df_consommation_an.rename({"Un végétarien (%)": "un végétarien (kg/par an)"}, axis=1, inplace=True)
        st.text('Consommation pour un adulte végétarien')
        st.dataframe(df_consommation_an)
        
        dic_categorie_produit = {
            'Catégorie de produit' : 
                ["Produits laitiers",
                 "Fruits et légumes",
                 "Viandes, poissons, œufs",
                 "Produits céréales", 
                 "Eaux et autres boissons",
                 "Autres"],
            'Score_par_an' : [
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Produits laitiers']['un végétarien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'lait et produits laitiers']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Fruits et légumes']['un végétarien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'fruits, légumes, légumineuses et oléagineux']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'œufs']['un végétarien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'viandes, œufs, poissons']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Produits céréales']['un végétarien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'produits céréaliers']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Eaux et autres boissons']['un végétarien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'boissons']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Autres']['un végétarien (kg/par an)'].values[0] * ((df_agri_score[df_agri_score['Group_aliment'] == 'aides culinaires et ingrédients divers']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'glaces et sorbets']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'matières grasses']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'produits sucrés']['Score_EF'].values[0])/4),
                ]
        }
        df_agri_score_par_an = pd.DataFrame(dic_categorie_produit)
        st.text("Score annuel par catégorie d'un adulte végétarien.")
        st.dataframe(df_agri_score_par_an)
    
        fig = px.pie(
            df_agri_score_par_an, 
            values = df_agri_score_par_an['Score_par_an'],
            names = df_agri_score_par_an['Catégorie de produit'].values, 
            title = "<b>Score pour une année par catégorie de produits (végétarien)</b>"
        )
        st.plotly_chart(fig)
        score = f"{mode} : pour toutes les catégories d'aliments, le score moyen pour l'année est {df_agri_score_par_an.Score_par_an.mean()}"
        st.info(score)
    elif mode == 'végétalisme':
        st.markdown(
            """
                Considérez le score moyen pour une année végétalienne.
                Les végétaliens refusent de consommer tous les types de viande, le lait (à l'exclusion du lait maternel lorsqu'ils nourrissent les bébés), les œufs, le miel, ainsi que d'autres substances et additifs produits à partir d'animaux (comme la gélatine ou le carmin).
            """
        )
        dict_regime = {
            'catégorie de produit' : ["Fruits et légumes", "Produits céréales", "Viandes, poissons, œufs", "Produits laitiers", "Eaux et autres boissons","Autres"],
            'Un végétalien (%)': [28, 6, 0, 0, 55, 11]
            }
        df_profil_regime = pd.DataFrame(dict_regime)
        st.text('Profil pour un adulte végétalien')
        st.dataframe(df_profil_regime)
        
        fig = px.pie(
            df_profil_regime, 
            values = df_profil_regime['Un végétalien (%)'],
            names = df_profil_regime['catégorie de produit'], 
            title = "<b>Profil pour un adulte végétalien</b>"
            )
        st.plotly_chart(fig)
        
        st.warning("Nous modifions notre base de données en fonction de la culture végétalienne.")
   
        df_agri_regime = df_agri[(df_agri.Sous_group_aliment == 'fruits')| (df_agri.Sous_group_aliment == 'algues')|
                (df_agri.Sous_group_aliment == 'herbes')|(df_agri.Sous_group_aliment == 'boisson alcoolisées')|
                (df_agri.Sous_group_aliment == 'fruits à coque et graines oléagineuses')|
                (df_agri.Sous_group_aliment == 'pâtes, riz et céréales')|
                (df_agri.Sous_group_aliment == 'légumes')|
                (df_agri.Sous_group_aliment == 'pommes de terre et autres tubercules')|
                (df_agri.Sous_group_aliment == 'huiles et graisses végétales')|
                (df_agri.Sous_group_aliment == 'boissons sans alcool')|
                (df_agri.Sous_group_aliment == 'épices')|
                (df_agri.Sous_group_aliment == 'confitures et assimilés')|
                (df_agri.Sous_group_aliment == 'eaux')|
                (df_agri.Sous_group_aliment == 'légumineuses')|
                (df_agri.Sous_group_aliment == 'sels')|(df_agri.Sous_group_aliment == 'sorbets')|
                (df_agri.Sous_group_aliment == 'condiments')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment avec levure incorporée')| 
                (df_agri.Nom_produit == 'Amidon de maïs ou fécule de maïs')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment T110')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment T150')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment T45 (pour pâtisserie)')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment T55 (pour pains)')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment T65')|
                (df_agri.Nom_produit == 'Farine de blé tendre ou froment T80')|
                (df_agri.Nom_produit == 'Farine de maïs')|
                (df_agri.Nom_produit == 'Farine de millet')|
                (df_agri.Nom_produit == 'Farine de pois chiche')|
                (df_agri.Nom_produit == 'Farine de riz')|
                (df_agri.Nom_produit == 'Farine de sarrasin')|
                (df_agri.Nom_produit == 'Farine de seigle T130')|
                (df_agri.Nom_produit == 'Farine de seigle T170')|
                (df_agri.Nom_produit == 'Farine de seigle T85')|
                (df_agri.Nom_produit == 'Farine de soja')|
                (df_agri.Nom_produit == "Farine d'épeautre (grand épeautre)")|
                (df_agri.Nom_produit == "Farine d'orge")|
                (df_agri.Nom_produit == "Flocon d'avoine")|
                (df_agri.Nom_produit == 'Khatfa feuille de brick, préemballée')|
                (df_agri.Nom_produit == 'Barre céréalière "équilibre" aux fruits, enrichie en vitamines et minéraux')| 
                (df_agri.Nom_produit == 'Barre céréalière aux amandes ou noisettes')|
                (df_agri.Nom_produit == 'Barre céréalière aux fruits')|
                (df_agri.Nom_produit == 'Céréales complètes soufflées, enrichies en vitamines et minéraux')|
                (df_agri.Nom_produit == 'Céréales pour petit déjeuner "équilibre" aux fruits (non enrichies en vitamines et minéraux)')|
                (df_agri.Nom_produit == 'Céréales pour petit déjeuner "équilibre" aux fruits secs (à coque), enrichis en vitamines et minéraux')|
                (df_agri.Nom_produit == 'Céréales pour petit déjeuner "équilibre" aux fruits, enrichies en vitamines et minéraux')|
                (df_agri.Nom_produit == 'Céréales pour petit déjeuner "équilibre" nature (non enrichies en vitamines et minéraux)')|
                (df_agri.Nom_produit == 'Céréales pour petit déjeuner riches en fibres, avec ou sans fruits, enrichies en vitamines et minéraux')|
                (df_agri.Nom_produit == 'Céréales pour petit déjeuner très riches en fibres, enrichies en vitamines et minéraux')|
                (df_agri.Nom_produit == "Flocon d'avoine précuit")|
                (df_agri.Nom_produit == "Flocons d'avoine, bouillis/cuits à l'eau")|
                (df_agri.Nom_produit == 'Muesli croustillant aux fruits et/ou fruits secs, graines (non enrichi en vitamines et minéraux)')|
                (df_agri.Nom_produit == 'Multi-céréales soufflées ou extrudées, enrichies en vitamines et minéraux')|
                (df_agri.Nom_produit == "Pop-corn ou Maïs éclaté, à l'air, non salé")|
                (df_agri.Nom_produit == "Pop-corn ou Maïs éclaté, à l'huile, salé")|
                (df_agri.Nom_produit == 'Pop-corn ou Maïs éclaté, au caramel')|
                (df_agri.Nom_produit == 'Sablé à la noix de coco')|
                (df_agri.Nom_produit == "Muesli croustillant aux fruits ou fruits secs, enrichi en vitamines et minéraux")|
                (df_agri.Nom_produit == "Muesli floconneux aux fruits ou fruits secs (non enrichi en vitamines et minéraux)")|
                (df_agri.Nom_produit == "Muesli floconneux aux fruits ou fruits secs, enrichi en vitamines et minéraux")|
                (df_agri.Nom_produit == 'Muesli floconneux aux fruits ou fruits secs, sans sucres ajoutés')|
                (df_agri.Nom_produit == 'Muesli floconneux ou de type traditionnel')|
                (df_agri.Nom_produit == 'Bicarbonate de soude')|
                (df_agri.Nom_produit == 'Lécithine de soja')|
                (df_agri.Nom_produit == 'Levure alimentaire')|
                (df_agri.Nom_produit == 'Levure chimique ou Poudre à lever')|
                (df_agri.Nom_produit == 'Levure de boulanger, compressée')|
                (df_agri.Nom_produit == 'Levure de boulanger, déshydratée')|
                (df_agri.Nom_produit == 'Miso')|
                (df_agri.Nom_produit == 'Sirop léger pour fruits appertisés au sirop')|
                (df_agri.Nom_produit == 'Sirop pour fruits appertisés au sirop')|
                (df_agri.Nom_produit == "Son d'avoine")|
                (df_agri.Nom_produit == 'Son de blé')|
                (df_agri.Nom_produit == 'Son de maïs')|
                (df_agri.Nom_produit == 'Son de riz')|
                (df_agri.Nom_produit == 'Préparation culinaire à base de soja, type "crème de soja')|
                (df_agri.Nom_produit == "Pizza, sauce garniture pour")|
                (df_agri.Nom_produit == 'Édulcorant à la saccharine')|(df_agri.Nom_produit == "Fructose")|
                (df_agri.Nom_produit == 'Mélasse de canne')|(df_agri.Nom_produit == 'Sucre blanc')|
                (df_agri.Nom_produit == 'Sucre roux')|(df_agri.Nom_produit == 'Sucre vanillé')
            ]
        
        df_agri_score = df_agri_regime.groupby("Group_aliment", as_index = False).agg({"Score_EF" : "mean"})
        st.text('Score par groupe d\'aliment.')
        st.dataframe(df_agri_score.sort_values(["Score_EF"], ascending = False))
        
        plt.figure(figsize = (5,5))
        plt.title("Score des groupes d'aliments (Végétalien)")
        plt.ylabel("Des groupes d'aliments")
        plt.xlabel("Score EF")
        sns.barplot(y='Group_aliment', x='Score_EF', data=df_agri_score)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        
        df_consommation_an = pd.concat([pd.DataFrame(df_profil_regime['catégorie de produit']), pd.DataFrame((df_profil_regime['Un végétalien (%)']*1058.5)/100)],  axis=1)
        df_consommation_an.rename({"Un végétalien (%)": "un végétalien (kg/par an)"}, axis=1, inplace=True)
        st.text('Consommation pour un adulte végétalien')
        st.dataframe(df_consommation_an)
        
        dic_categorie_produit = {
            'Catégorie de produit' : 
                ["Produits laitiers",
                 "Fruits et légumes",
                 "Viandes, poissons, œufs",
                 "Produits céréales", 
                 "Eaux et autres boissons",
                 "Autres"],
            'Score_par_an' : [
                0,
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Fruits et légumes']['un végétalien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'fruits, légumes, légumineuses et oléagineux']['Score_EF'].values[0],
                0,
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Produits céréales']['un végétalien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'produits céréaliers']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Eaux et autres boissons']['un végétalien (kg/par an)'].values[0] * df_agri_score[df_agri_score['Group_aliment'] == 'boissons']['Score_EF'].values[0],
                df_consommation_an[df_consommation_an['catégorie de produit'] == 'Autres']['un végétalien (kg/par an)'].values[0] * ((df_agri_score[df_agri_score['Group_aliment'] == 'aides culinaires et ingrédients divers']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'glaces et sorbets']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'matières grasses']['Score_EF'].values[0] + df_agri_score[df_agri_score['Group_aliment'] == 'produits sucrés']['Score_EF'].values[0])/4),
                ]
        }
        df_agri_score_par_an = pd.DataFrame(dic_categorie_produit)
        st.text("Score annuel par catégorie d'un adulte végétalien.")
        st.dataframe(df_agri_score_par_an)
        
        fig = px.pie(
            df_agri_score_par_an, 
            values = df_agri_score_par_an['Score_par_an'],
            names = df_agri_score_par_an['Catégorie de produit'].values, 
            title = "<b>Score pour une année par catégorie de produits (végétalien)</b>"
        )
        st.plotly_chart(fig)
        score = f"{mode} : pour toutes les catégories d'aliments, le score moyen pour l'année est {df_agri_score_par_an.Score_par_an.mean()}"
        st.info(score)
    

#♦selected_product_bio = st.multiselect('Sélectionnez vos produits bio:', df_agri_bio.Name)

#selected_product_conv = st.multiselect('Sélectionnez vos produits conventionnel:', df_agri_conv.Name)

#panier_bio = df_agri_bio['Name'].isin(selected_product_bio)
#panier_conv = df_agri_conv['Name'].isin(selected_product_conv)

#data_selected_bio = df_agri_bio[panier_bio]
#data_selected_conv = df_agri_conv[panier_conv]

#if len(data_selected_bio) > 0:
#    st.text('Mon panier bio')
#    st.dataframe(data_selected_bio)
    
#if len(data_selected_conv) > 0:
#    st.text('Mon panier conventionnel')
#    st.dataframe(data_selected_conv)

