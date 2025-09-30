import sys
import os
import getpass
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.modelos import Usuario, Role, Permission

# --- (Funciones de UI sin cambios: print_header, clear_screen) ---
def print_header(title):
    print("\n" + "=" * 60)
    print(f"|| {title.upper():^54} ||")
    print("=" * 60)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- (Funciones de Gestión sin cambios: list_users, list_roles, create_local_user) ---
def list_users():
    print_header("Lista de Usuarios")
    users = Usuario.query.order_by(Usuario.id).all()
    if not users:
        print(">> No hay usuarios registrados en la base de datos.")
        return
    print(f"{'ID':<4} | {'USUARIO (CORREO)':<35} | {'ESTADO':<10} | {'TIPO':<10} | ROLES")
    print("-" * 80)
    for user in users:
        role_names = ', '.join([role.name for role in user.roles]) or "Ninguno"
        print(f"{user.id:<4} | {user.usuario:<35} | {user.estado:<10} | {user.auth_type:<10} | {role_names}")
    print("-" * 80)

def list_roles():
    print_header("Lista de Roles y Permisos")
    roles = Role.query.all()
    if not roles:
        print(">> No hay roles configurados en la base de datos.")
        return
    for role in roles:
        print(f"\n[ ROL: {role.name} ]")
        permission_names = '\n  - '.join([p.name for p in role.permissions]) or "Ninguno"
        print(f"  Permisos:\n  - {permission_names}")
    print("-" * 60)
    
def create_local_user():
    print_header("Crear Usuario Local")
    username = input(">> Ingrese el nombre de usuario (ej: admin2): ").strip().lower()
    if not username:
        print("\n** Error: El nombre de usuario no puede estar vacío. **")
        return
    if Usuario.query.filter_by(usuario=username).first():
        print(f"\n** Error: El usuario '{username}' ya existe. **")
        return
    password = getpass.getpass(">> Ingrese la contraseña: ")
    if not password:
        print("\n** Error: La contraseña no puede estar vacía. **")
        return
    password_confirm = getpass.getpass(">> Confirme la contraseña: ")
    if password != password_confirm:
        print("\n** Error: Las contraseñas no coinciden. **")
        return
    full_name = input(">> Ingrese el nombre completo del usuario: ").strip()
    if not full_name:
        print("\n** Error: El nombre completo no puede estar vacío. **")
        return
    hashed_password = generate_password_hash(password)
    new_user = Usuario(
        usuario=username, 
        contrasena=hashed_password, 
        nombre_completo=full_name,
        auth_type='local',
        estado='Activo'
    )
    db.session.add(new_user)
    db.session.commit()
    print(f"\n¡Éxito! Usuario local '{username}' creado correctamente.")

def manage_user_roles():
    print_header("Gestionar Roles de Usuario")
    username = input(">> Ingrese el username o correo del usuario a modificar: ").strip().lower()
    user = Usuario.query.filter_by(usuario=username).first()
    if not user:
        print(f"\n** Error: No se encontró al usuario '{username}'. **")
        return
    current_roles = ', '.join([r.name for r in user.roles]) or "Ninguno"
    print(f"\nRoles actuales de '{user.nombre_completo}': {current_roles}")
    print("\nAcciones disponibles:")
    print("  1. Asignar un rol")
    print("  2. Revocar un rol")
    choice = input(">> Seleccione una opción: ").strip()
    if choice not in ['1', '2']:
        print("\n** Opción no válida. **")
        return
    list_roles()
    role_name = input(">> Ingrese el nombre exacto del rol: ").strip()
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        print(f"\n** Error: No se encontró el rol '{role_name}'. **")
        return
    if choice == '1':
        if role in user.roles:
            print(f"\n** El usuario ya tiene el rol '{role_name}'. **")
        else:
            user.roles.append(role)
            db.session.commit()
            print(f"\n¡Éxito! Rol '{role_name}' asignado a '{username}'.")
    elif choice == '2':
        if role not in user.roles:
            print(f"\n** El usuario no tiene el rol '{role_name}'. **")
        else:
            user.roles.remove(role)
            db.session.commit()
            print(f"\n¡Éxito! Rol '{role_name}' revocado de '{username}'.")

# --- ¡NUEVA FUNCIÓN! ---
def manage_user_permissions():
    """Submenú para asignar o revocar permisos individuales a un usuario."""
    print_header("Gestionar Permisos Individuales de Usuario")
    username = input(">> Ingrese el username o correo del usuario a modificar: ").strip().lower()
    user = Usuario.query.filter_by(usuario=username).first()

    if not user:
        print(f"\n** Error: No se encontró al usuario '{username}'. **")
        return
    
    current_perms = ', '.join([p.name for p in user.permissions]) or "Ninguno"
    print(f"\nPermisos individuales de '{user.nombre_completo}': {current_perms}")
    
    print("\nAcciones disponibles:")
    print("  1. Asignar un permiso")
    print("  2. Revocar un permiso")
    choice = input(">> Seleccione una opción: ").strip()

    if choice not in ['1', '2']:
        print("\n** Opción no válida. **")
        return
    
    # Listar todos los permisos disponibles
    all_permissions = Permission.query.all()
    print("\n--- Permisos Disponibles ---")
    for perm in all_permissions:
        print(f"  - {perm.name}")
    print("-" * 30)

    perm_name = input(">> Ingrese el nombre exacto del permiso: ").strip()
    permission = Permission.query.filter_by(name=perm_name).first()

    if not permission:
        print(f"\n** Error: No se encontró el permiso '{perm_name}'. **")
        return

    if choice == '1': # Asignar
        if permission in user.permissions:
            print(f"\n** El usuario ya tiene el permiso '{perm_name}'. **")
        else:
            user.permissions.append(permission)
            db.session.commit()
            print(f"\n¡Éxito! Permiso '{perm_name}' asignado a '{username}'.")
    
    elif choice == '2': # Revocar
        if permission not in user.permissions:
            print(f"\n** El usuario no tiene el permiso '{perm_name}'. **")
        else:
            user.permissions.remove(permission)
            db.session.commit()
            print(f"\n¡Éxito! Permiso '{perm_name}' revocado de '{username}'.")


def main_menu():
    """Muestra el menú principal y maneja la lógica del programa."""
    while True:
        clear_screen()
        print_header("Panel de Administración de SIME 360")
        print("1. Listar todos los usuarios")
        print("2. Listar roles y permisos")
        print("3. Crear un nuevo usuario local")
        print("4. Gestionar roles de un usuario (Asignar/Revocar)")
        # --- ¡NUEVA OPCIÓN! ---
        print("5. Gestionar permisos individuales de un usuario")
        print("0. Salir")
        print("-" * 60)
        
        choice = input(">> Seleccione una opción: ").strip()

        with app.app_context():
            if choice == '1':
                list_users()
            elif choice == '2':
                list_roles()
            elif choice == '3':
                create_local_user()
            elif choice == '4':
                manage_user_roles()
            # --- ¡NUEVA LÓGICA! ---
            elif choice == '5':
                manage_user_permissions()
            elif choice == '0':
                print("\nSaliendo del panel de administración. ¡Hasta luego!\n")
                break
            else:
                print("\n** Opción no válida, por favor intente de nuevo. **")
        
        input("\n-- Presione Enter para continuar --")

if __name__ == '__main__':
    main_menu()