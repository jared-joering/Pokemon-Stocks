import requests
import pandas as pd # we'll use pandas to curate and populate our postgre db 
from psycopg2 import sql
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





# make API request /all
# using //if// break up variant cards (i.e. reverse and masterball holos) -- I think we'll do this when adding the prices to the cards we put in.
# print to separate lines
# check to see //(nested) if// duplicates every 'week', if duplicate: add TCGPlayer prices to the price table