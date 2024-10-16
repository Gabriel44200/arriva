from . import _rest_adapter
from .stops import Stop


## vvv Classes vvv ##

class Line():
    """
    Una línea de bus
    """

    def __init__(self, id: int, name: str, origin: Stop = None, destination: Stop = None, id_sitme: str = None, concession: str = None, name_ida: str = None, name_vta: str = None):
        self.id = id
        """
        Id de la línea en el sistema de Arriva.
        """

        self.name = name
        """
        Nombre de la línea
        """

        self.origin = origin
        """
        Parada de origen (ID SITME)
        """

        self.destination = destination
        """
        Parada de destino (ID SITME)
        """

        self.id_sitme = id_sitme
        """
        Id de la línea en el SITME de la Xunta.
        """

        self.concession = concession
        """
        Numero de la concesión sin el XG delante
        """

        self.name_ida = name_ida
        """
        Nombre de la línea que sale en los rótulos a la ida (Sentido 1)
        """

        self.name_vta = name_vta
        """
        Nombre de la línea que sale en los rótulos a la vuelta (Sentido 2)
        """

    def __repr__(self):
        return self.name

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_stop(data: dict) -> Stop:
    """
    Builds a stop based on the data given by the API. Nothe this is specific to the lines endpoints, e.g. the "nome" attribute
    """

    # Only busstops are posible as a line's origin or destination, kinda obvious
    return Stop(id=data["id"],
                type="busstop",
                name=data["nome"],
                lat=data.get("latitude"),
                long=data.get("longitude"))


def _parse_line(data: dict) -> Line:
    """
    Construye una línea con los datos obtenidos de la API
    """

    origin = None
    destination = None
    origin_data = data.get("origin")
    destination_data = data.get("destination")
    if origin_data and destination_data:
        origin = _parse_stop(origin_data)
        destination = _parse_stop(destination_data)

    return Line(id=data["linea"]["id"],
                name=data["linea"]["mom_linea"],
                origin=origin,
                destination=destination)


def search_lines_from_stop(stop_id: int, page_number: int = 1, page_size: int = 2147483647) -> list[Line]:
    """
    Based on a stop id, obtains all the lines that go through it. **WARNING**: The API seems to have deprecated this, almost-always returns an empty list, again `15004` works, check `busGal_api.transport.stops.get_stop_name`

    :param page_number: The page number to retrieve. Defaults to the first one.

    :param page_size: Number of results per page. Defaults to the maximum integer value the API would accept, a.k.a. the maximum positive value for a 32-bit signed binary integer (Wikipedia), a.k.a. 2,147,483,647
    """

    data = _rest_adapter.get("/lines/search",
                            ep_params={"stop_id": stop_id,
                                       "page_number": page_number,
                                       "page_size": page_size})

    # Last element in list is total_results
    return [_parse_line(el) for el in data[:-1]]


def get_all_lines():
    """
    Obtiene todas las líneas (calls `concession_search_lines` with no filters)
    """

    data = _rest_adapter.get("/lineas/index.json")

    return [Line(id=el["linea"]["id"],
                name=el["linea"]["mom_linea"],
                origin=origin,
                destination=destination)
            for el in data]


def get_line(line_id: int) -> Line:
    """
    Fetch a line with it's id. **WARNING**: The API seems to have deprecated this (kind-of), 
    it just keeps saying we're missing `X-CSRF-TOKEN` header, which hints to a form to check this somewhere, 
    but I'm tired and I don't want to play that game
    """

    return _parse_line(_rest_adapter.get(f"/lineas/view/{line_id}"))

## ^^^ Methods ^^^ ##
