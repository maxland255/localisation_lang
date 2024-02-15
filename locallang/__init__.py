from locallang.lang import LangInit

try:
    from locallang.lang import Localisation
except ImportError:
    pass

__version__ = "0.0.11"
__all__ = ["LangInit", "Localisation"]
