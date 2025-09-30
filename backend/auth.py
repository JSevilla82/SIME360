from functools import wraps
from flask import session, abort, current_app
from models.modelos import Usuario
def KOhIYPdCotUCRHoxhpEhsjcSwGTLXgPG(permission_name):
    def JZAXexSjgVVgIuPawHjRiFYIvTaaenrF(f):
        @wraps(f)
        def AtvgLaxGFwCzGqlcFNDCOsgWCgAPKriD(*args, **kwargs):
            rQCXMPUwMKQjntjmNKOhqikErsxhhBtx = session.get('usuario_id')
            if not rQCXMPUwMKQjntjmNKOhqikErsxhhBtx:
                abort(401) 
            VtJqpBoAyzszBPPrYAPzvvBCUNdcFBCQ = Usuario.query.get(rQCXMPUwMKQjntjmNKOhqikErsxhhBtx)
            if VtJqpBoAyzszBPPrYAPzvvBCUNdcFBCQ and VtJqpBoAyzszBPPrYAPzvvBCUNdcFBCQ.has_permission(permission_name):
                return f(*args, **kwargs)
            current_app.logger.warning(
                f"Acceso denegado para el usuario '{session.get('usuario')}' "
                f"al permiso '{permission_name}'"
            )
            abort(403)
        return AtvgLaxGFwCzGqlcFNDCOsgWCgAPKriD
    return decorator