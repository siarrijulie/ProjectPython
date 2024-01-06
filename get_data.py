# get_data.py

import requests
import currencyapicom
import random
from datetime import datetime, timedelta
"""
    Pour importer ce projet utiliser les méthodes d'import :
    from get_data import FCApiService
    from get_data import RestCountriesService
"""

"""
    Classe de gestion des données du marché FOREX - Données de TEST
"""


class MockAPIService:
    MOCK_API_BASE_URL = " https://658334cc02f747c8367b41e4.mockapi.io/api/v1"

    def __init__(self):
        self.mock_session = requests.Session()

    def get_mock_data(self, endpoint):
        try:
            response = self.mock_session.get(f"{self.MOCK_API_BASE_URL}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    """
        Retourne la valeur monétaire après conversion d'une devise à une autre au taux du jour. 
        from_currency : Devise source
        to_currency : Devise cible
        val : Montant à convertir
        Valeurs prises en compte : "EUR" et "USD"
    """

    def convert_currency(self, from_currency, to_currency, val):
        result = self.get_mock_data("/convert/" + from_currency)
        return float(result["data"][to_currency]['value'] * val)

    """
        Retourne l'évolution du taux de conversion par mois d'une devise vers une autre sur une semaine d'une année donnée.'. 
        from_symbol : Devise source
        to_symbol : Devise cible
        year : Année analysée
        week : Semaine analysée
        Valeurs randomisées autour d'un taux récent avec +/- 0.1 point
    """

    def get_exchange_rate_history(self, from_symbol, to_symbol, year, week):

        start_date = f"{year}-01-01"
        start_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(weeks=week - 1)).strftime("%Y-%m-%d")

        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")
        today_date = datetime.today().strftime("%Y-%m-%d")
        end_date = min(end_date, today_date)
        exchange_rates = {}
        current_date = start_date
        while current_date <= end_date:
            result = self.get_mock_data("/historical/" + from_symbol)
            exchange_rates[current_date] = random.uniform(float(result["data"][to_symbol]['value']) - 0.1,
                                                          float(result["data"][to_symbol]['value']))

            current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

        return exchange_rates


"""
    Classe de gestion des données du marché FOREX
"""
class FCApiService:
    FC_API_KEY = "cur_live_XdyqXD1VAtrO7gbye76UoMsIi0xHSZHQfOVipKG2"

    def __init__(self):
        self.fc_api_session = currencyapicom.Client(self.FC_API_KEY)

    """
        Retourne la valeur monétaire après conversion d'une devise à une autre au taux du jour. 
        from_currency : Devise source
        to_currency : Devise cible
        val : Montant à convertir
    """

    def convert_currency(self, from_currency, to_currency, val):
        result = self.fc_api_session.latest(base_currency=from_currency, currencies=[to_currency])
        try:
            return float(result["data"][to_currency]['value']) * float(val)
        except ValueError:
            # Handle the case where the string cannot be converted to a float
            # For example, you can return a default value or show an error message
            return 0.0  # Replace with the appropriate handling for your use case
    """
        Retourne l'évolution du taux de conversion par mois d'une devise vers une autre sur une semaine d'une année donnée.
        from_symbol : Devise source
        to_symbol : Devise cible
        year : Année analysée
        week : Semaine analysée
    """

    def get_exchange_rate_history(self, from_symbol, to_symbol, year, week):
        from datetime import datetime, timedelta

        start_date = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w").strftime("%Y-%m-%d")
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")
        today_date = datetime.today().strftime("%Y-%m-%d")
        end_date = min(end_date, today_date)

        exchange_rates = {}
        current_date = start_date

        while current_date <= end_date:
            result = self.fc_api_session.historical(current_date, base_currency=from_symbol, currencies=[to_symbol])
            exchange_rates[current_date] = float(result["data"][to_symbol]['value'])
            current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

        return exchange_rates


"""
    Classe de gestion des pays et des devises
"""


class RestCountriesService:
    REST_COUNTRIES_BASE_URL = " https://restcountries.com/v3.1/"

    def __init__(self):
        self.rest_countries_session = requests.Session()

    def get_rest_countries_data(self, endpoint):
        """
        Envoie une requête GET vers l'API Rest Countries avec l'endpoint donné et retourne la réponse JSON de l'API,
        None si la requête a échoué.
        """
        try:
            response = self.rest_countries_session.get(f"{self.REST_COUNTRIES_BASE_URL}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erreur : {e}")
            return None


    """
        Retourne la liste de tous les pays ainsi que les devises / coordonnées associées'. 
    """

    def get_countries(self):
        """
        Retourne une correspondance avec "currencies" comme clé et une liste de devises comme valeur,
        "cca3" comme clé et une liste de codes cca3 comme valeur,
        et "name" comme clé et une liste de noms de pays comme valeur.
        """
        endpoint = "/all"
        result = self.get_rest_countries_data(endpoint)
        mapping = {"currencies": [], "cca3": [], "name": []}

        for country_data in result:
            currencies = country_data.get("currencies", [])
            for currency in currencies:
                if isinstance(currency, str):
                    mapping["currencies"].append(currency)
                    mapping["cca3"].append(country_data.get("cca3"))
                    mapping["name"].append(country_data.get("name"))

        return mapping

    def get_currencies(self):
        """
        Retourne une liste de tous les noms des devises.
        """
        endpoint = "/all"
        result = self.get_rest_countries_data(endpoint)
        currencies = []

        for country_data in result:
            country_currencies = country_data.get("currencies", [])
            for currency in country_currencies:
                if isinstance(currency, str):
                    currencies.append(currency)

        return currencies