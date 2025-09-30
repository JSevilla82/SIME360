import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.modelos import Role, Permission, Usuario

def print_header(title):
    """Imprime un encabezado estilizado para cada sección."""
    print("\n" + "=" * 60)
    print(f"|| {title.upper():^54} ||")
    print("=" * 60)

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def list_roles():
    """Lista todos los roles y los permisos asociados a cada uno."""
    print_header("Lista de Roles y Permisos")
    roles = Role.query.order_by(Role.name).all()
    if not roles:
        print(">> No hay roles configurados en la base de datos.")
        return False

    for role in roles:
        print(f"\n[ ROL: {role.name} ]")
        print(f"  Descripción: {role.description or 'Sin descripción'}")
        permission_names = '\n    - '.join([p.name for p in role.permissions]) or "Ninguno"
        print(f"  Permisos Asignados:\n    - {permission_names}")
    print("-" * 60)
    return True

def list_permissions():
    """Muestra una lista numerada de todos los permisos disponibles."""
    print("\n--- Permisos Disponibles ---")
    permissions = Permission.query.order_by(Permission.name).all()
    if not permissions:
        print(">> No hay permisos definidos en la base de datos.")
        return None
    for idx, perm in enumerate(permissions, 1):
        print(f"  {idx}. {perm.name}")
    print("-" * 28)
    return permissions

def select_permissions(existing_perms=[]):
    """Permite al usuario seleccionar permisos de una lista."""
    all_perms = list_permissions()
    if not all_perms:
        return []
    
    existing_perm_names = {p.name for p in existing_perms}
    print("\n>> Seleccione los permisos a asignar (ej: 1, 3, 5).")
    print("   (Presione Enter para no cambiar los permisos existentes)")
    
    choice_str = input(">> Números de permisos: ").strip()
    if not choice_str:
        return existing_perms

    selected_perms = set()
    try:
        selected_indices = [int(i.strip()) - 1 for i in choice_str.split(',')]
        for index in selected_indices:
            if 0 <= index < len(all_perms):
                selected_perms.add(all_perms[index])
            else:
                print(f"** Advertencia: Número '{index + 1}' está fuera de rango y será ignorado. **")
    except ValueError:
        print("\n** Error: Entrada no válida. Use números separados por comas. **")
        return existing_perms

    return list(selected_perms)


def create_role():
    """Guía al usuario para crear un nuevo rol y asignarle permisos."""
    print_header("Crear Nuevo Rol")
    name = input(">> Ingrese el nombre del nuevo rol (ej: Editor): ").strip()
    if not name:
        print("\n** Error: El nombre del rol no puede estar vacío. **")
        return
    if Role.query.filter_by(name=name).first():
        print(f"\n** Error: El rol '{name}' ya existe. **")
        return

    description = input(">> Ingrese una descripción para el rol: ").strip()
    
    new_role = Role(name=name, description=description)
    new_role.permissions = select_permissions()
    
    db.session.add(new_role)
    db.session.commit()
    print(f"\n¡Éxito! Rol '{name}' creado correctamente.")

def edit_role():
    """Permite editar el nombre, descripción y permisos de un rol existente."""
    print_header("Editar Rol Existente")
    if not list_roles():
        return

    role_name = input(">> Ingrese el nombre exacto del rol que desea editar: ").strip()
    role = Role.query.filter_by(name=role_name).first()

    if not role:
        print(f"\n** Error: No se encontró el rol '{role_name}'. **")
        return

    print("\nEditando rol:", role.name)
    new_name = input(f">> Nuevo nombre (Enter para mantener '{role.name}'): ").strip()
    new_description = input(f">> Nueva descripción (Enter para mantener '{role.description}'): ").strip()

    if new_name and new_name != role.name:
        if Role.query.filter_by(name=new_name).first():
            print(f"\n** Error: El nombre de rol '{new_name}' ya está en uso. **")
            return
        role.name = new_name

    if new_description:
        role.description = new_description
        
    role.permissions = select_permissions(role.permissions)

    db.session.commit()
    print(f"\n¡Éxito! Rol '{role.name}' actualizado correctamente.")

def delete_role():
    """Elimina un rol de la base de datos."""
    print_header("Eliminar Rol")
    if not list_roles():
        return

    role_name = input(">> Ingrese el nombre exacto del rol que desea eliminar: ").strip()
    role = Role.query.filter_by(name=role_name).first()

    if not role:
        print(f"\n** Error: No se encontró el rol '{role_name}'. **")
        return
        
    user_count = db.session.query(Usuario).filter(Usuario.roles.any(name=role.name)).count()
    print(f"** Advertencia: {user_count} usuario(s) tienen este rol asignado. **")
    
    confirm = input(f"¿Está seguro de que quiere eliminar el rol '{role.name}'? (s/n): ").strip().lower()
    
    if confirm == 's':
        db.session.delete(role)
        db.session.commit()
        print(f"\n¡Éxito! El rol '{role.name}' ha sido eliminado.")
    else:
        print("\nOperación cancelada.")

def main_menu():
    """Muestra el menú principal y maneja la lógica del programa."""
    while True:
        clear_screen()
        print_header("Panel de Gestión de Roles")
        print("1. Listar todos los roles")
        print("2. Crear un nuevo rol")
        print("3. Editar un rol existente")
        print("4. Eliminar un rol")
        print("0. Volver al menú principal")
        print("-" * 60)
        
        choice = input(">> Seleccione una opción: ").strip()

        with app.app_context():
            if choice == '1':
                list_roles()
            elif choice == '2':
                create_role()
            elif choice == '3':
                edit_role()
            elif choice == '4':
                delete_role()
            elif choice == '0':
                print("\nVolviendo...")
                break
            else:
                print("\n** Opción no válida, por favor intente de nuevo. **")
        
        input("\n-- Presione Enter para continuar --")

if __name__ == '__main__':
    main_menu()