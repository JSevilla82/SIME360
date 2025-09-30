from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# --- TABLAS DE ASOCIACIÓN ---

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

# --- MODELOS PRINCIPALES ---

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permissions = db.relationship('Permission', secondary=role_permissions, lazy='subquery',
                                  backref=db.backref('roles', lazy=True))
    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    def __repr__(self):
        return f'<Permission {self.name}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150), unique=True, nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=True)
    contrasena = db.Column(db.String(150), nullable=True)
    auth_type = db.Column(db.String(20), nullable=False, default='local')
    microsoft_object_id = db.Column(db.String(100), unique=True, nullable=True)
    estado = db.Column(db.String(50), nullable=False, default='Activo')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                            backref=db.backref('users', lazy=True))
    
    permissions = db.relationship('Permission', secondary=user_permissions, lazy='subquery',
                                  backref=db.backref('users', lazy=True))

    def has_permission(self, permission_name):
        # --- AJUSTE IMPORTANTE: PERMISO DE INICIO POR DEFECTO ---
        # Se otorga acceso al módulo de inicio a todos los usuarios, independientemente de sus roles.
        if permission_name == 'acceso:inicio':
            return True

        # 1. Verificar permisos heredados de los roles
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        
        # 2. Verificar permisos asignados individualmente
        for perm in self.permissions:
            if perm.name == permission_name:
                return True
        
        return False

class Licencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LicenciaSkuId = db.Column(db.String(100), unique=True, nullable=False)
    NombreLicencia = db.Column(db.String(150), nullable=False)
    LicenciaPrincipal = db.Column(db.Boolean, default=False)
    LicenciaDePago = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f"<Licencia {self.NombreLicencia}>"