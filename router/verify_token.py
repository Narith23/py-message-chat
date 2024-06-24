from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/login")

JWT_SECRET_KEY = "-gZNIH52GyRUXi9hThhTw8Kvbi6UMlgz8UjKHJIL3faJqqAXreq_I0WAdfSqjnxk"
JWT_ALGORITHM = "HS256"

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTError:  # You can catch specific JWT errors here
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
