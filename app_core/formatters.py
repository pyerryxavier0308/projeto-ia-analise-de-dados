"""Formatação de valores monetários (uso apenas de apresentação)."""

def format_brl(amount: float) -> str:
    """Retorna preço no formato R$ 1.234,56."""
    value = f"{float(amount):,.2f}"
    return "R$ " + value.replace(",", "_").replace(".", ",").replace("_", ".")
