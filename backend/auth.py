from functools import wraps
from flask import session, abort, current_app
from models.modelos import Usuario

def permission_required(permission_name):
    """
    Decorador que verifica si el usuario en sesión tiene el permiso requerido.
    Aborta con 403 (Prohibido) si no lo tiene.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            # 1. Verificar si hay un usuario en la sesión.
            user_id = session.get('usuario_id')
            if not user_id:
                abort(401) 

            # 2. Obtener el usuario desde la base de datos usando el ID.
            user = Usuario.query.get(user_id)

            # 3. Comprobar si el usuario existe y tiene el permiso necesario.
            if user and user.has_permission(permission_name):
                return f(*args, **kwargs)

            # 4. Si no tiene permiso, registrar el intento y abortar.
            current_app.logger.warning(
                f"Acceso denegado para el usuario '{session.get('usuario')}' "
                f"al permiso '{permission_name}'"
            )
            abort(403)

        return decorated_function
    return decorator