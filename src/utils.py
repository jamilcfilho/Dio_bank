from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from src.models import User, db
from functools import wraps


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name != role_name:
                return {"message": "Usuário não possui acesso!"}, HTTPStatus.UNAUTHORIZED
            return f(*args, **kwargs)

        return wrapped

    return decorator

# Somente para demonstrar o uso de 'Teste unitário' com o Pytest no arquivo 'test_utils'


def eleva_quadrado(x):
    return x**2
