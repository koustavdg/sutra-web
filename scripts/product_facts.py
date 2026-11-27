"""Shared, owner-approved product facts used by HTML and machine-readable copy."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def product_values():
    product = json.loads((ROOT / 'content/product.json').read_text())
    offers = [offer for offer in product['pricing']['numeric_offers']
              if offer['tier'] == 'pro' and offer['currency'] == 'USD'
              and set(offer['platforms']) == {'ios', 'android'}]
    if len(offers) != 1:
        raise ValueError('Expected one shared, verified USD Pro price')
    return {**product['publication_facts'], 'pro_price_usd': offers[0]['amount'],
            'ios_release': product['current_releases']['ios'],
            'android_release': product['current_releases']['android']}


def expand_facts(text):
    values = product_values()
    def replace(match):
        key = match[1]
        if key not in values:
            raise ValueError(f'Unknown product fact: {key}')
        return values[key]
    return re.sub(r'\{\{product\.([a-z_]+)\}\}', replace, text)
