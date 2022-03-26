"""ащк еру test test_pet_friends file """
from api import PetFriends
from settings import *

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_email):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
