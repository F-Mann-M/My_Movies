
current_user_id = None
current_user_name = None

def set_current_user(user_id, user_name):
    """simple helper function to simulate user profiles, it takes in user id and name to store it"""
    global current_user_id, current_user_name
    current_user_id = user_id
    current_user_name = user_name
    return None

def get_current_user():
    """returns the current user id and name"""
    return current_user_id, current_user_name

