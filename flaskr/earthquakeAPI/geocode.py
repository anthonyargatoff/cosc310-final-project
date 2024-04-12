import aiohttp

def address_to_url(address):
    """
    Convert an address string with commas and spaces to a string separated by plus signs (+).
    Replace ", " with a single plus symbol.

    Parameters:
        address (str): The address string to convert.
    
    Returns:
        str: The converted address string.
    """
    address_with_plus = address.replace(', ', '+').replace(',', '+').replace(' ', '+')
    
    return address_with_plus


async def fetch_geocode(session, addressString):
    """
    Fetch geocode data asynchronously for the given address.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp client session.
        address (str): The address string to geocode.
        APIKey (str): API key to use the API

    Returns:
        dict: The geocode data as a JSON object.
    """
    url = f"https://geocode.maps.co/search?q={addressString}&api_key=6612fe31db408262351014htr8789af"
    async with session.get(url) as response:
        return await response.json()

async def main(address):
    async with aiohttp.ClientSession() as session:
        geocode_data = await fetch_geocode(session, address)
        return geocode_data

async def convertAddress(address):
    geocode_data = await main(address_to_url(address))
    return [geocode_data[0]['lat'], geocode_data[0]['lon']]