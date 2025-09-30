import os
import sys
from werkzeug.security import generate_password_hash

# --- Boilerplate para permitir la importación desde la carpeta raíz ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.modelos import Usuario

def insertar_admin_local():
    """
    Crea un usuario administrador local con nombre de usuario 'admin' y contraseña 'Admin'.
    Este usuario es necesario para que el script 'create_roles.py' funcione correctamente.
    """
    with app.app_context():
        
        usuario_input = "admin"
        contrasena = "Admin"
        nombre_completo = "Admin System"

        # 1. Verificar si el usuario 'admin' ya existe.
        if Usuario.query.filter_by(usuario=usuario_input).first():
            print(f"--> El usuario '{usuario_input}' ya existe en la base de datos. No se realizarán cambios.")
            return
            
        try:
            # 2. Hashear la contraseña por seguridad.
            contrasena_hasheada = generate_password_hash(contrasena)
            
            # --- AJUSTE IMPORTANTE ---
            # Se crea la instancia de Usuario usando 'nombre_completo' en lugar de 'nombre'.
            nuevo_usuario = Usuario(
                usuario=usuario_input,
                contrasena=contrasena_hasheada,
                nombre_completo=nombre_completo,
                auth_type='local',
                estado='Activo'
            )
            
            # 3. Guardar el nuevo usuario en la base de datos.
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            print("\n¡Usuario administrador local registrado exitosamente!")
            print(f"   - Usuario: {nuevo_usuario.usuario}")
            print(f"   - Nombre: {nuevo_usuario.nombre_completo}")

        except Exception as e:
            db.session.rollback()
            print(f"\n** Error al registrar el usuario: {e} **")

if __name__ == '__main__':
    insertar_admin_local()