from sqlalchemy.orm import Session

from authentication.models import User
from authentication.schemas import UserSchema


def signUp(user: UserSchema,db:Session):
    user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        level = user.level,
        role = user.role
    )
    db.add(user)
    db.commit()
    return user
