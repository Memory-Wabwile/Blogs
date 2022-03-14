import requests
from .models import Quotes

def get_quote():
    """
    Function to consume http request and return a Quote class instance
    """
    response = requests.get("http://quotes.stormconsultancy.co.uk/random.json").json()

    random_quote = Quotes(response.get("author"), response.get("quote"))
    return random_quote