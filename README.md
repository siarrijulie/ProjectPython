# Taux de Change et Devise Dashboard

## User Guide

Pour déployer et utiliser ce dashboard sur votre machine, suivez les étapes suivantes :
Pour les imports :
   ```bash
    from dash import Dash, dcc, html, Input
    import plotly.express as px
    from dash.dependencies import Output
    from get_data import FCApiService
    from get_data import RestCountriesService
    from get_data import MockAPIService
    import pandas as pd
    ...
    import requests
    import currencyapicom
    import random
    from datetime import datetime, timedelta
   ```
1. Installez les dépendances nécessaires en exécutant les commandes suivantes :

   ```bash
    pip install dash plotly pandas
    pip install requests
    pip install currencyapicom
    pip install dash
    pip install plotly
    pip install pandas
    ```
2. Clonez le repository sur votre machine locale :

   ```bash
   git clone [https://github.com/siarrijulie/ProjectPython.git]
   ```
3. Puis lancer le code en ouvrant l'URL à cette adresse :
   ```bash
    http://localhost:8050
    ```
### Rapport d'analyse
#####  Environnement :

Utilisation de Pycharm : c'était notre préférence. Il dispose d'une analyse de code et d'un débogueur graphique différents de ceux de Visual Studio Code (plus simple d'utilisation).

Le fichier get_data.py contient des classes définissant des services de données pour obtenir des informations liées aux taux de change, aux pays, et aux devises. Voici quelques conclusions principales tirées de l'analyse du code :

- MockAPIService pour les Données de Test :

    La classe MockAPIService simule un service d'API pour les tests, fournissant des données de taux de change et d'historique prévu pour tester l'application.
    La conversion de devise est effectuée en utilisant des taux fictifs obtenus à partir d'une API fictive (fonctionne avec EUR et USD uniquement) car pas assez de requête sur la vrai API.

- FCApiService pour les Données Réelles :

    La classe FCApiService utilise l'API réelle de CurrencyAPI pour obtenir des taux de change réels.
    La conversion de devise et l'historique des taux de change sont obtenus en interagissant avec l'API de CurrencyAPI.

- RestCountriesService pour les Données sur les Pays :

    La classe RestCountriesService interagit avec l'API Rest Countries pour obtenir des informations sur les pays et les devises associées.
    Elle fournit des méthodes pour obtenir une liste de tous les pays, ainsi que leurs devises et coordonnées associées.

### Organisation du Code (get_data.py):

Chaque classe de service est organisée de manière à séparer les méthodes pour différentes fonctionnalités (conversion de devise, historique taux de change, localisation des pays avec la devise associée).

Les erreurs potentielles lors des requêtes sont gérées et des messages d'erreur sont affichés, tel que le message indiquant quelle API est utilisée, MockApi ou FcApi.

- Gestion des Dates et des Durées :

    Les dates et les durées sont correctement gérées lors de la génération de l'historique des taux de change.
Les taux de change historiques sont générés par semaine pour une année donnée.

- Utilisation de Librairies Externes :

    Le code utilise des bibliothèques externes telles que requests, currencyapicom, et datetime pour effectuer des requêtes HTTP, interagir avec l'API CurrencyAPI, et gérer les opérations de date.
    
En conclusion, le fichier get_data.py fournit des services flexibles pour obtenir des informations liées aux taux de change, aux pays, et aux devises, en utilisant à la fois des données réelles provenant de CurrencyAPI et des données fictives pour les tests.

# Développement du Dashboard (my_dash.py)

Le développement d'un dashboard utilisant Dash et Plotly pour afficher des informations liées aux taux de change et aux devises. 

Voici une explication détaillée de la structure et des fonctionnalités du code :

### Initialisation et Services

Le code commence par importer les modules nécessaires et les services de données à partir du fichier get_data.py.

Il crée ensuite une instance de l'application Dash.
   ```bash
    app = Dash(__name__)
   ```

Des instances de services sont créées pour obtenir des données réelles et fictives tel que :
   ```bash
    service = RestCountriesService()
    current_service = service2 = FCApiService()
    //Au cas où l'API n'est plus de requête, utilisation de : 
    mockService = MockAPIService()
   ```

### Chargement des Données

Les données de test sont chargées à partir de Plotly Express pour créer un histogramme initial.
   ```bash
    fig = px.histogram(df, x="total_bill")
   ```

Les données des pays sont chargées à partir du service RestCountriesService pour créer une carte choropleth.
   ```bash
    fig2 = px.choropleth(...)
   ```

### Mise en Page du Dashboard

La mise en page du dashboard est définie en utilisant des composants HTML et Dash qui inclut des sections pour l'en-tête, le convertisseur de devises, la sortie de conversion, l'histogramme, et la carte choropleth.

### Styles et Design

Les couleurs et le style genéral du dashboard sont définit dans la variable :
   ```bash
    colors = {...}
   ```
   
Le design de l'histogramme et de la carte est également configuré.
   ```bash
    fig.update_layout(...)
    fig2.update_layout(...)
   ```
   
### Callbacks

Des fonctions de callback sont définies pour gérer la conversion de devises et la mise à jour de l'histogramme en utilisant les fonction de get_data.py.
Notamment grâce aux :
   ```bash
    @app.callback()
   ```
Suivi de :
   ```bash
    update_histogramme(...)
    handle_submit_or_blur(...)
   ```
   
## Conclusion
 Le dashboard interactif sur les taux de change et les devises. Il inclut des fonctionnalités telles que le convertisseur de devises, l'affichage d'un histogramme, et une carte choropleth. 


AB DER HALDEN Cyril et SIARRI Julie.



















   

