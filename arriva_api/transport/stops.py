from . import _rest_adapter

from datetime import datetime
import math


## vvv Classes vvv ##

class Location():
    """
    Una ubicación geográfica (latitud y longitud)
    """

    def __init__(self, lat: float, long: float):
        self.lat = float(lat)
        """
        Latitud
        """

        self.long = float(long)
        """
        Longitud
        """

    def __repr__(self):
        return f"Lat: {self.lat}, Long: {self.long}"


class Stop():
    """
    Una parada de bus
    """

    def __init__(self, id: int, name: str = None, name_council: str = None, peso: int = None, location: Location = None, lat: float = None, long: float = None, school_integration: bool = None, ordinal: int = None, simob_id: int = None, council_simob: str = None, sitme_id: int = None, time: datetime = None):
        self.id = id
        """
        Id de la parada dentro del sistema de Arriva. También llamado superparada_id
        """

        self.name = name
        """
        Nombre de la parada
        """

        self.council_simob = council_simob
        """
        Id del ayuntamiento del SIMOB (Nuevo sistema de la Xunta), se numeran igual que los numera el INE.
        """

        self.name_council = name_council
        """
        Nombre de la parada con el ayuntamiento entre paréntesis
        """

        self.peso = peso
        """
        Peso de la parada ( ¯_(ツ)_/¯ )
        """

        self.location = location or (
            Location(lat, long) if lat and long else None)
        """
        Posición geográfica de la parada
        """

        self.school_integration = bool(school_integration)
        """
        Indica si es un servicio escolar integrado
        """

        self.ordinal = ordinal
        """
        El orden que ocupa dentro de una ruta
        """

        self.simob_id = simob_id
        """
        Id de la parada dentro del sistema de Arriva. Se compone de dos elementos, ayuntamiento y parada e incluso posición (15030-1-2 es la parada 1 del sentido 2 del ayuntamiento 15030)
        """

        self.sitme_id = sitme_id
        """
        También llamado gescar_id. Es usando en el last_area o en el SIRI de la Xunta
        """

        self.time = time
        """
        Indica la hora de paso del bus por la parada en una expedición
        """

    def fetch_name(self) -> str:
        """
        Obtiene el nombre (y lo asocia) para este id de parada de la API
        """

        self.name = get_stop_name(self.id)

        return self.name

    def fetch_location(self) -> Location:
        """
        Obitiene la ubicación (y la asocia) para este id de parada de la API
        """

        self.location = get_stop_location(self.id)

        return self.location

    def __repr__(self):
        return self.name

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def search_stops(query: str, num_results: int = 2147483647) -> list[Stop]:
    """
    Busca paradas por su nombre, usando la API de Arriva.

    :param query: Nombre de la búsqueda
    :param num_results: Numero de resultados a devolver. Por defecto, el valor entero máximo que acepta la API, es decir, el valor positivo máximo para un entero binario con signo de 32 bits (2,147,483,647).
    """

    # Llamar al endpoint de la API
    data = _rest_adapter.get(endpoint="/superparadas/index/buscador.json")

    stops = []

    # Recorrer las paradas devueltas por la API
    for parada_data in data['paradas']:
        # Si la búsqueda es por nombre, filtramos
        if query.lower() in parada_data["nombre"].lower():
            # Crear objeto Location
            location = Location(lat=parada_data.get("lat"),
                                long=parada_data.get("lon"))

            # Crear objeto Stop
            stop = Stop(
                id=parada_data["parada"],
                name=parada_data["nombre"],
                name_council=parada_data.get("nom_web"),
                peso=parada_data.get("peso"),
                location=location
            )

            stops.append(stop)

            # Limitar el número de resultados si es necesario
            if len(stops) >= num_results:
                break

    return stops


    


def get_all_stops() -> list[Stop]:
    """
    Obtiene todas las paradas existentes (llama a `search_stops` con una query vacía)
    """

    return search_stops(query='')

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia del círculo máximo en kilómetros entre dos puntos 
    en la Tierra (especificado en grados decimales).
    """
    # Convertir decimal degrees a radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferencia entre las coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radio de la Tierra en kilómetros
    return c * r

def location_search_stops(location: Location = None, lat: float = None, long: float = None, radius=5) -> list[Stop]:
    """
    Busca por las paradas existentes en un punto con un determinado radio (latitud, longitud).

    :param lat: Latitud del punto de búsqueda.
    :param lon: Longitud del punto de búsqueda.
    :param radius: Radio en kilómetros para la búsqueda.
    """

    # Llamar al endpoint de la API para obtener todas las paradas
    data = _rest_adapter.get(endpoint="/superparadas/index/buscador.json")

    stops_in_range = []

    # Recorrer todas las paradas devueltas por la API
    for parada_data in data['paradas']:
        # Obtener la latitud y longitud de la parada
        parada_lat = parada_data.get("lat")
        parada_lon = parada_data.get("lon")

        # Calcular la distancia desde el punto dado hasta la parada
        distance = haversine(lat, long, parada_lat, parada_lon)

        # Si la parada está dentro del rango especificado
        if distance <= radius:
            # Crear objeto Location
            location = Location(lat=parada_lat, long=parada_lon)

            # Crear objeto Stop
            stop = Stop(
                id=parada_data["parada"],
                name=parada_data["nombre"],
                name_council=parada_data.get("nom_web"),
                peso=parada_data.get("peso"),
                location=location
            )

            stops_in_range.append(stop)

    return stops_in_range


def get_stop_name(stop_id: int) -> str:
    """
    Obtiene el nombre de una parada por su id
    """

    data = _rest_adapter.get(endpoint=f"/superparadas/expediciones-fecha/{stop_id}.json")

    return data["paradas"][0]["nom_parada"]


def get_stop_location(stop_id: int) -> Location:
    """
    Obtiene la ubicación de una parada por su id
    """

    data = _rest_adapter.get(endpoint=f"/superparadas/expediciones-fecha/{stop_id}.json")

    return Location(data["paradas"][0]["lat"], data["paradas"][0]["lon"])

## ^^^ Methods ^^^ ##
