import requests
import psycopg2
from config import api # calling the config file I created to hide my API
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity    # pretty sure all of these will be used

headers = {
    "X-API-Key": api
}

# fetch a single card by id (replace with any id you like)
# card = Card.find("xy1-1")

print("card.id =", card.id)
print("card.name =", card.name)
print("type(card.subtypes) =", type(card.subtypes))
print("card.subtypes =", card.subtypes)
print(card.set.id)
print(card.set.name)
print(type(card.set.printedTotal))
print(card.set.printedTotal)
print(card.tcgplayer)