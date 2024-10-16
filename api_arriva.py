import requests

BASE_URL = "https://arriva.gal/plataforma/api/"

def make_request(endpoint):
    """
    Realiza una solicitud GET al endpoint específico de la API y devuelve la respuesta en formato JSON.
    
    Parámetros:
        endpoint (str): El endpoint específico de la API al que se desea hacer la solicitud.
    
    Retorna:
        dict | None: El contenido de la respuesta en formato JSON si la solicitud es exitosa; 
                     de lo contrario, None si ocurre un error.
    """
    url = BASE_URL + endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hay errores en la respuesta
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None

def get_stops():
    """
    Obtiene la lista de todas las paradas de autobús disponibles desde la API.
    
    Retorna:
        list | None: Una lista de paradas de autobús si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    data = make_request("superparadas/index.json")
    return data.get("paradas", []) if data else None

def get_stops_from_origin(origin_stop):
    """
    Obtiene la lista de paradas de autobús que están disponibles desde una parada de origen específica.
    
    Parámetros:
        origin_stop (str): El identificador de la parada de origen.
    
    Retorna:
        dict | None: Los datos de las paradas relacionadas con la parada de origen si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"superparadas/por-origen/{origin_stop}.json"
    data = make_request(endpoint)
    return data if data else None

def search_expeditions(origin_stop, destination_stop, date):
    """
    Busca las expediciones disponibles entre dos paradas en una fecha específica.
    
    Parámetros:
        origin_stop (str): El identificador de la parada de origen.
        destination_stop (str): El identificador de la parada de destino.
        date (str): La fecha para buscar expediciones (puede ser 'today', 'tomorrow' o 'yesterday').
    
    Retorna:
        dict | None: Los datos de las expediciones disponibles si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"buscador/search/{origin_stop}/{destination_stop}/{date}.json"
    data = make_request(endpoint)
    return data if data else None

def get_price(origin_stop, destination_stop):
    """
    Obtiene el precio de un billete entre dos paradas específicas.
    
    Parámetros:
        origin_stop (str): El identificador de la parada de origen.
        destination_stop (str): El identificador de la parada de destino.
    
    Retorna:
        dict | None: Los datos del precio del billete si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"buscador/precio/{origin_stop}/{destination_stop}.json"
    data = make_request(endpoint)
    return data if data else None

def get_lines():
    """
    Obtiene la lista de todas las líneas de autobús disponibles.
    
    Retorna:
        list | None: Una lista de líneas de autobús si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    data = make_request("superparadas/index.json")
    return data.get("paradas", []) if data else None

def view_line(line):
    """
    Muestra los detalles de una línea de autobús específica.
    
    Parámetros:
        line (str): El identificador de la línea de autobús.
    
    Retorna:
        dict | None: Los detalles de la línea de autobús si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"lineas/view/{line}.json"
    data = make_request(endpoint)
    return data if data else None

def view_expedition(expedition_num):
    """
    Obtiene los detalles de una expedición específica.
    
    Parámetros:
        expedition_num (str): El identificador de la expedición.
    
    Retorna:
        dict | None: Los detalles de la expedición si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"expediciones/get/{expedition_num}.json"
    data = make_request(endpoint)
    return data if data else None

def view_stop(stop):
    """
    Muestra detalles sobre una parada específica y las expediciones que pasan por ella.
    
    Parámetros:
        stop (str): El identificador de la parada.
    
    Retorna:
        dict | None: Los detalles de la parada y las expediciones relacionadas si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"superparadas/view/{stop}.json"
    data = make_request(endpoint)
    return data if data else None

def get_stop_expeditions_today(stop):
    """
    Muestra las expediciones que pasan hoy por una parada específica.
    
    Parámetros:
        stop (str): El identificador de la parada.
    
    Retorna:
        dict | None: Los detalles de las expediciones del día si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"superparadas/expediciones-fecha/{stop}.json"
    data = make_request(endpoint)
    return data if data else None

def get_bus_last_area(bus):
    """
    Muestra el último área por el que ha pasado un bus específico.
    
    Parámetros:
        bus (str): El identificador del bus.
    
    Retorna:
        dict | None: Los datos del área más reciente por donde ha pasado el bus si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"buses/getLastArea/{bus}.json"
    data = make_request(endpoint)
    return data if data else None

def get_bus_last_stop(bus):
    """
    Muestra la última parada por la que ha pasado un bus específico.
    
    Parámetros:
        bus (str): El identificador del bus.
    
    Retorna:
        dict | None: Los datos de la última parada por donde ha pasado el bus si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"buses/getLastStop/{bus}.json"
    data = make_request(endpoint)
    return data if data else None

def get_bus_geoloc(bus):
    """
    Muestra la posición geográfica y detalles de un bus específico.
    
    Parámetros:
        bus (str): El identificador del bus.
    
    Retorna:
        dict | None: Los datos de la geolocalización del bus si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"buses/getGeoloc/{bus}.json"
    data = make_request(endpoint)
    return data if data else None

def get_buses():
    """
    Muestra todos los buses con sus posiciones geográficas y detalles.
    
    Retorna:
        dict | None: Los datos de todos los buses y sus posiciones si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    data = make_request("buses/getGeolocs.json")
    return data if data else None

def get_messages():
    """
    Muestra todos los avisos y comunicaciones disponibles.
    
    Retorna:
        dict | None: Los datos de los avisos y comunicaciones si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    data = make_request("comunicaciones/index.json")
    return data if data else None

def view_message(message):
    """
    Muestra detalles sobre un aviso o comunicación específica.
    
    Parámetros:
        message (str): El identificador del aviso o comunicación.
    
    Retorna:
        dict | None: Los detalles del aviso o comunicación si la solicitud es exitosa;
                     de lo contrario, None si ocurre un error o no hay datos disponibles.
    """
    endpoint = f"comunicaciones/view/{message}.json"
    data = make_request(endpoint)
    return data if data else None

# Ejemplo de uso de la función get_bus_geoloc
print(get_bus_geoloc('774'))
