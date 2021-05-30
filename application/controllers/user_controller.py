from ..models.models import db, User
from datetime import datetime as dt

async def checkExistingUser(username, email):
    existing_user = User.query.filter(
        User.username == username or User.email == email
    ).first()
    print(existing_user)
    if existing_user:
        return True
    return False
