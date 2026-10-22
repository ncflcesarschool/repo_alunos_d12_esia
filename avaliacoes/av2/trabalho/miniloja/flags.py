"""Feature flags lidas do ambiente."""
import os


def promo_natal_ativa():
    return os.environ.get("MINILOJA_PROMO_NATAL", "0") == "1"
