from . import _rest_adapter

from datetime import date

## vvv Classes vvv ##


class SpecialRate():
    """
    A special rate (a discount)
    """

    def __init__(self, id: int, text: str, type_id: int, type_name: str):
        self.id = id
        """
        The special rate id
        """

        self.text = text
        """
        The text of the discount
        """

        self.type_id = type_id
        """
        The id of the type of discount
        """

        self.type_name = type_name
        """
        The name of the type of discount
        """

    def __repr__(self):
        return f"{self.type_name}: {self.text}"


class Rate():
    """
    Una tarifa (el precio de un viaje)
    """

    def __init__(self, effective: float, credit_card: float, special_rates: list[SpecialRate] = None):
        self.effective = effective
        """
        El precio del viaje en efectivo
        """

        self.credit_card = credit_card
        """
        El precio del viaje con una tarjeta de transporte (TMG, TXN, TCM, TCL)
        """

        self.special_rates = special_rates
        """
        Las tarifas especiales aplicables
        """

    def __repr__(self):
        return f"Efectivo: {self.effective}€ || Tarjeta: {self.credit_card}€"

## ^^^ Classes ^^^ ##


## vvv Methods vvv ##

def _parse_special_rate(data: dict) -> SpecialRate:
    return SpecialRate(id=data["special_rate_id"],
                       text=data["special_rate_text"],
                       type_id=data["special_rate_type_id"],
                       type_name=data["special_rate_type_name"])


def _parse_rate(data: dict) -> Rate:
    return Rate(effective=data["effective"],
                credit_card=data["credit_card"],
                special_rates=[_parse_special_rate(sr) for sr in data["special_rates"]] if data.get("special_rates") else None)


def get_rate(origin_id: int, destination_id: int) -> Rate:
    """
    Obtiene los precios de un viaje, incluyendo tarifas especiales
    """

    return _parse_rate(_rest_adapter.get(f"/buscador/precio/{origin_id}/{destination_id}.json"))

## ^^^ Methods ^^^ ##
