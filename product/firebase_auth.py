from firebase_admin import auth
from rest_framework.exceptions import AuthenticationFailed

def get_uid_from_token(id_token):
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded.get("uid")
    except Exception as e:
        raise AuthenticationFailed("Invalid or expired token")