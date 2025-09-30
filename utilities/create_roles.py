import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.modelos import Role, Permission, Usuario

def create_initial_data():
    
    with app.app_context():
        # --- 1. Definir y crear todos los permisos necesarios ---
        permissions_to_create = {
            'acceso:inicio': 'Acceso al módulo de Inicio',
            'acceso:usuarios': 'Acceso al módulo de Usuarios',
            'acceso:licenciamiento': 'Acceso al módulo de Licenciamiento',
            'acceso:informesUso': 'Acceso al módulo de Informes de Uso',
            'acceso:sitiosSharePoint': 'Acceso al módulo de Sitios de SharePoint',
            'acceso:configuracion': 'Acceso al módulo de Configuración'
        }
        
        for name, description in permissions_to_create.items():
            perm = Permission.query.filter_by(name=name).first()
            if not perm:
                perm = Permission(name=name, description=description)
                db.session.add(perm)
                print(f"Creando permiso: {name}")
        
        db.session.commit()
        print("Permisos de acceso a módulos verificados/creados.")

        # --- 2. Crear el rol de Administrador si no existe ---
        admin_role = Role.query.filter_by(name='Administrador').first()
        if not admin_role:
            admin_role = Role(name='Administrador', description='Acceso total a todos los módulos')
            db.session.add(admin_role)
            print(f"Creando rol: {admin_role.name}")
        
        # --- 3. Asignar TODOS los permisos existentes al rol Administrador ---
        all_permissions = Permission.query.all()
        admin_role.permissions = all_permissions
        
        db.session.commit()
        print(f"Rol '{admin_role.name}' verificado/creado con {len(all_permissions)} permisos.")

        # --- 4. Asignar el rol Administrador al usuario 'admin' ---
        admin_user = Usuario.query.filter_by(usuario='admin').first()
        if admin_user:
            # Verificar si el rol ya está asignado para evitar duplicados
            if admin_role not in admin_user.roles:
                admin_user.roles.append(admin_role)
                db.session.commit()
                print(f"Rol 'Administrador' asignado al usuario '{admin_user.usuario}'.")
            else:
                print(f"El usuario '{admin_user.usuario}' ya tiene el rol 'Administrador'.")
        else:
            print("ADVERTENCIA: No se encontró el usuario 'admin'. Por favor, créalo primero ejecutando 'registrarUsuario.py'.")

        print("\n¡Proceso completado!")

if __name__ == '__main__':
    create_initial_data()