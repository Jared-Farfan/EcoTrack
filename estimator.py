"""Carbon-footprint estimates from Spanish natural-language text."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TypedDict


class EmissionFactor(TypedDict):
    """Named emission factor with an explicit unit."""

    name: str
    kg_co2e: float
    unit: str


# Approximate kg CO2e per kilometre (order-of-magnitude, educational use).
TRANSPORT_FACTORS: dict[str, EmissionFactor] = {
    "bus": {"name": "Bus", "kg_co2e": 0.089, "unit": "kg CO2e/km"},
    "metro": {"name": "Metro / tren", "kg_co2e": 0.041, "unit": "kg CO2e/km"},
    "carro": {"name": "Carro / taxi", "kg_co2e": 0.171, "unit": "kg CO2e/km"},
    "moto": {"name": "Moto", "kg_co2e": 0.113, "unit": "kg CO2e/km"},
    "avion": {"name": "Avión", "kg_co2e": 0.255, "unit": "kg CO2e/km"},
    "bici": {"name": "Bicicleta", "kg_co2e": 0.0, "unit": "kg CO2e/km"},
    "caminando": {"name": "A pie", "kg_co2e": 0.0, "unit": "kg CO2e/km"},
}

TRANSPORT_ALIASES: dict[str, str] = {
    "bus": "bus",
    "buseta": "bus",
    "autobus": "bus",
    "autobús": "bus",
    "transmilenio": "bus",
    "metro": "metro",
    "tren": "metro",
    "tranvia": "metro",
    "tranvía": "metro",
    "carro": "carro",
    "auto": "carro",
    "coche": "carro",
    "taxi": "carro",
    "uber": "carro",
    "moto": "moto",
    "motocicleta": "moto",
    "avion": "avion",
    "avión": "avion",
    "vuelo": "avion",
    "volé": "avion",
    "vole": "avion",
    "bicicleta": "bici",
    "bici": "bici",
    "cicla": "bici",
    "caminando": "caminando",
    "caminé": "caminando",
    "camine": "caminando",
    "pie": "caminando",
}

# Approximate kg CO2e per serving (~150 g or one unit).
FOOD_FACTORS: dict[str, EmissionFactor] = {
    "carne": {"name": "Carne de res", "kg_co2e": 4.0, "unit": "kg CO2e/porción"},
    "cerdo": {"name": "Cerdo", "kg_co2e": 1.8, "unit": "kg CO2e/porción"},
    "pollo": {"name": "Pollo", "kg_co2e": 1.0, "unit": "kg CO2e/porción"},
    "pescado": {"name": "Pescado", "kg_co2e": 0.9, "unit": "kg CO2e/porción"},
    "huevos": {"name": "Huevos", "kg_co2e": 0.4, "unit": "kg CO2e/porción"},
    "queso": {"name": "Queso", "kg_co2e": 1.3, "unit": "kg CO2e/porción"},
    "leche": {"name": "Leche", "kg_co2e": 0.6, "unit": "kg CO2e/porción"},
    "arroz": {"name": "Arroz", "kg_co2e": 0.3, "unit": "kg CO2e/porción"},
    "verduras": {"name": "Verduras", "kg_co2e": 0.2, "unit": "kg CO2e/porción"},
}

FOOD_ALIASES: dict[str, str] = {
    "carne": "carne",
    "res": "carne",
    "hamburguesa": "carne",
    "cerdo": "cerdo",
    "pollo": "pollo",
    "pescado": "pescado",
    "huevo": "huevos",
    "huevos": "huevos",
    "queso": "queso",
    "leche": "leche",
    "arroz": "arroz",
    "ensalada": "verduras",
    "verdura": "verduras",
    "verduras": "verduras",
    "vegetales": "verduras",
}

DEFAULT_TRANSPORT_KEY = "carro"

KM_PATTERN = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(?:km|kil[oó]metros?)",
    re.IGNORECASE,
)
QUANTITY_PATTERN = re.compile(
    r"(\d+)\s*(?:porciones?\s+de|platos?\s+de)?\s*$"
)
CLAUSE_SPLIT = re.compile(
    r",|;|\.|\by\b|\be\b|\badem[aá]s\b|\bluego\b|\bdespu[eé]s\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Item:
    """One detected activity and its estimated kg CO2e."""

    label: str
    kg_co2e: float
    category: str


def _split_clauses(text: str) -> list[str]:
    return [part.strip() for part in CLAUSE_SPLIT.split(text) if part.strip()]


def _find_transport_key(clause: str) -> str | None:
    words = re.findall(r"[a-záéíóúüñ]+", clause.lower())
    # Longer aliases first so "transmilenio" / "bicicleta" win over shorter ones.
    aliases = sorted(TRANSPORT_ALIASES, key=len, reverse=True)
    for alias in aliases:
        alias_words = alias.split()
        if len(alias_words) == 1 and alias in words:
            return TRANSPORT_ALIASES[alias]
        if alias in clause.lower():
            return TRANSPORT_ALIASES[alias]
    return None


def _parse_transport(clause: str) -> Item | None:
    match = KM_PATTERN.search(clause)
    if not match:
        return None
    km = float(match.group(1).replace(",", "."))
    key = _find_transport_key(clause) or DEFAULT_TRANSPORT_KEY
    factor = TRANSPORT_FACTORS[key]
    if key == "caminando":
        label = f"{km:g} km a pie"
    else:
        label = f"{km:g} km en {factor['name'].lower()}"
    return Item(
        label=label,
        kg_co2e=round(km * float(factor["kg_co2e"]), 3),
        category="transporte",
    )


def _parse_food(clause: str) -> list[Item]:
    found: list[Item] = []
    used_spans: list[tuple[int, int]] = []
    lowered = clause.lower()
    for alias in sorted(FOOD_ALIASES, key=len, reverse=True):
        for match in re.finditer(rf"\b{re.escape(alias)}\b", lowered):
            span = match.span()
            if any(span[0] < end and span[1] > start for start, end in used_spans):
                continue
            used_spans.append(span)
            qty = 1
            prefix = lowered[: match.start()]
            qty_match = QUANTITY_PATTERN.search(prefix.rstrip())
            if qty_match:
                qty = int(qty_match.group(1))
            key = FOOD_ALIASES[alias]
            factor = FOOD_FACTORS[key]
            found.append(
                Item(
                    label=f"{qty} × {factor['name'].lower()}",
                    kg_co2e=round(qty * float(factor["kg_co2e"]), 3),
                    category="comida",
                )
            )
    return found


def estimate(text: str) -> list[Item]:
    """Detect transport and meals in `text` and return kg CO2e items."""
    items: list[Item] = []
    for clause in _split_clauses(text):
        transport = _parse_transport(clause)
        if transport:
            items.append(transport)
        items.extend(_parse_food(clause))
    return items


def total_kg(items: list[Item]) -> float:
    """Sum of estimated kg CO2e for the detected items."""
    return round(sum(item.kg_co2e for item in items), 2)
