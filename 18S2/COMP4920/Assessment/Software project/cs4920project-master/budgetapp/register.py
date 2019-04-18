import secrets
from query_calls import add_new_profile, add_new_confirmation, get_where

def register_new_profile(username, name, gender, dob, email, password, confirmed):
    try:
        add_new_profile(username, name, gender, dob, email, password, confirmed)
        p_id = get_where("profiles", "id", "username=\"{}\"".format(username))
        id = p_id[0][0]
        add_new_confirmation(secrets.token_urlsafe(), id)
    except:
    	print("Error : Couldn't register new user")