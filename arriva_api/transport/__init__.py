"""
# Introducción

Este módulo se encarga de todo lo relativo al transporte.

# Ejemplo rápido

Este es un simple ''cliente'' en línea de comandos que muestra en acción este submódulo con una tabla con los hoarios que solicites:

``` python
.. include:: __main__.py
```

Este también es el submódulo __main__.py, por lo tanto, puedes probarlo.python -m arriva_api.transport
"""

from ..rest_adapter import RestAdapter as RestAdapter
from ..known_servers import ARRIVA as BASE_URL

_rest_adapter = RestAdapter(BASE_URL)


from . import lines
from . import stops
from . import expeditions
from . import warning_alerts
from . import rates

__all__ = ["lines", "stops", "expeditions", "warning_alerts", "rates"]
