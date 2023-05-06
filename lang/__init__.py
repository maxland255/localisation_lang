from lang.lang import LangInit

try:
    from lang.lang import Localisation
except:
    pass

__version__ = "0.0.3"
__all__ = ["LangInit", "Localisation"]