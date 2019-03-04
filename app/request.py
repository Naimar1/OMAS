from .models import Quotes
import urllib.request, json
base_url = None


def configure_request(app):
    global base_url
    base_url = app.config['QUOTES_API_BASE_URL']


def get_quote():
    '''
    function that gets the json response to url request
    '''
    with urllib.request.urlopen(base_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)
        print(get_quote_response)
        quote_objects = None

        if get_quote_response:
            id = get_quote_response.get('id')
            author = get_quote_response.get('author')
            quote = get_quote_response.get('quote')
            quote_objects = Quotes(id, author, quote)

    return quote_objects