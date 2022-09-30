import tables.user as table

from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from starlette import status
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.hash import bcrypt

from start.engine import get_session
from src.schemes.user import User, Token, UserCreate
from env_file import jwt_algorithm, jwt_secret, jwt_exp


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sing-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not available credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        try:
            payload = jwt.decode(
                token,
                jwt_secret,
                algorithms=jwt_algorithm,
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: User) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=jwt_exp),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }

        token = jwt.encode(
            payload,
            jwt_secret,
            algorithm=jwt_algorithm,
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User already registered',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = self.session. \
            query(table.User) \
            .filter(table.User.username == user_data.username) \
            .first()
        if user:
            raise exception from None
        user = table.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password)

        )
        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not authorized',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = self.session. \
            query(table.User) \
            .filter(table.User.username == username, ) \
            .first()

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
