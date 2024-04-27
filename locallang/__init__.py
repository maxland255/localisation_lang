#  Copyright (c) 2024 pieteraerens.eu
#  All rights reserved.
#  The file __init__.py is a part of localisation.
#  Created by harrypieteraerens
#  Created: 4/28/24, 1:37 AM
#  Last modified: 4/28/24, 1:37 AM

from lang_init import LangInit

try:
    from local.localisation import Localisation
except ImportError:
    pass

__version__ = "0.0.12"
__all__ = ["LangInit", "Localisation"]


def getLocalisation(local: str):
    """
    Get the localization object

    :param local:
    :return:
    """
    try:
        from local.localisation import Localisation
        return Localisation(local)
    except ImportError:
        return None
