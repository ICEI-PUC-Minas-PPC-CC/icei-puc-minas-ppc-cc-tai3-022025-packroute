import requests

def geocode_address(endereco, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={api_key}"
    resp = requests.get(url).json()
    if resp['status'] == 'OK':
        loc = resp['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    return None, None

