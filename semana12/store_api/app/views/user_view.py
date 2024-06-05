import json

def render_user_list(users):
    return [
        {
            "id": user.id,
            "username": user.name,
            "rol": [
                json.loads(user.roles)     
            ]
        }
        for user in users
    ]
    
def render_user_detail(user):
    return {
        "id": user.id,
        "username": user.name,
        "rol": [
            json.loads(user.roles)     
        ]
    }