"""for the testing test_pet_friends"""
from api import PetFriends
from settings import *
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter="my_pets"):
    """testing get_all_pets  filter= '- 'my_pets' or empty '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='ПитбульДог', animal_type='Бульдог', age='4',
                                     pet_photo='images/dogcat.jpg'):
    """testind adding a new valid pet """

    # getting api key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # add photo directory
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #adding pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # assert result's
    assert status == 200
    assert result['name'] == name

def test_succcessful_delete_self_pet():
    """testing delete pet"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # if len my_pets = 0 create a new pet and check again
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Песдалис', 'дворняга', '69', "images/pesdalis.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # take id first of the pets and delete it
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    #res pet list again
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    #check status 200 and pet missing of the list
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successeful_update_self_pet_info(name='Tiger', animal_type='hunterdog',age='5'):
    '''check update pet info '''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    #if list of the pet is not empty try update
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        #check status == 200
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# next my methods for the module 19

def test_create_pet_simple_valid_data(name='Boss',animal_type='whife', age='35'):
    """testind simple adding  a new valid pet """

    # getting api key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # adding pet
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # assert result's
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_the_pet(pet_photo= 'images/pesdalis.jpg'):
    # getting api key adn list of the my pet
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # if list of pets empty create simple pet
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'Boss2', 'whife2', '36')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # adding photo dirrectory
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    # adding photo
    status, result = pf.add_photo_of_the_pet(auth_key, pet_id, pet_photo)

    #check status 200 and pet missing of the list
    assert status == 200
    assert result['pet_photo']

