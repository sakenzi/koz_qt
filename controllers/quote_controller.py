from api_handlers.quote import get_quote
from models.models import Quote


class QuoteController:
    def __init__(self):
        self.quotes = []

    def fetch_quotes(self):
        response = get_quote()
        if response.status_code == 200:
            data = response.json()
            self.quotes = [Quote(item["description"]) for item in data]
            return self.quotes
        else:
            return []
        
    def get_quotes(self):
        return self.quotes