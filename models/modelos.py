from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt = SQLAlchemy()
ZMVDhbXOUSNjMvcZACVOtUUwQORcUfMG = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Table('user_roles',
    wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column('user_id', wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.ForeignKey('usuarios.id'), primary_key=True),
    wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column('role_id', wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.ForeignKey('role.id'), primary_key=True)
)
LNuHWMqYjPIsHutUZlqxFrjZNwxKhkQd = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Table('role_permissions',
    wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column('role_id', wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.ForeignKey('role.id'), primary_key=True),
    wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column('permission_id', wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.ForeignKey('permission.id'), primary_key=True)
)
YNnssSAGionVEQQQYnkmFfvXoiNpkAZy = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Table('user_permissions',
    wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column('user_id', wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.ForeignKey('usuarios.id'), primary_key=True),
    wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column('permission_id', wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.ForeignKey('permission.id'), primary_key=True)
)
class gjGYhklRgfsKSuXSwkqOFVEehdzrmusG(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Model):
    id = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, primary_key=True)
    BwqrFVnWNHJyYvjrvTOZsIzVltwDKIeX = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(80), unique=True, nullable=False)
    YcmXeJxcgWhZEFjJoEgaDwZfmpOLHlPH = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(255))
    uNTbtPuiJxHBxVxNyDixXVruAcpEXSkr = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.relationship('Permission', secondary=LNuHWMqYjPIsHutUZlqxFrjZNwxKhkQd, lazy='subquery',
                                  mTGDVBZazkezgdnJEyDMfcesTfYlceEG=wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.mTGDVBZazkezgdnJEyDMfcesTfYlceEG('roles', lazy=True))
    def __repr__(self):
        return f'<Role {self.name}>'
class xIIVFmUxFCQRPWIWRpWOSHbnHRZiskry(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Model):
    id = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, primary_key=True)
    BwqrFVnWNHJyYvjrvTOZsIzVltwDKIeX = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(80), unique=True, nullable=False)
    YcmXeJxcgWhZEFjJoEgaDwZfmpOLHlPH = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(255))
    def __repr__(self):
        return f'<Permission {self.name}>'
class fKrGhJPChRoGbjUuUnIgWblgvpBGRKqS(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Model):
    gZJduevAmBWnvkaLIjKxoXVVQYDNHzAK = 'usuarios'
    id = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, primary_key=True)
    bGbslKilcdOqepewLaYWNBnDQgTWoKmn = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(150), unique=True, nullable=False)
    vHLEMdmHDYWyrRwIAkQOPJQrRArmvmfv = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(150), nullable=True)
    lQqaEcArwWrIiYvxPBRDnPCqUbwCVCiz = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(150), nullable=True)
    UxVJBDsZZtafyvjfFHidQttbBovuyWYi = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(20), nullable=False, default='local')
    UdwsZpZTZTZZzwYJXSAAOyqnuUuPDOSN = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(100), unique=True, nullable=True)
    NVhmGXRjvdkkUJkSXILfqobuOxHMzwBV = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(50), nullable=False, default='Activo')
    fiOkbGxwjpHcFpVmfvbFzzlfhnPiWZYD = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.DateTime, default=datetime.utcnow)
    enEJqxjFAFiFONZixXzvPYopplNyLJPB = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.relationship('Role', secondary=ZMVDhbXOUSNjMvcZACVOtUUwQORcUfMG, lazy='subquery',
                            mTGDVBZazkezgdnJEyDMfcesTfYlceEG=wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.mTGDVBZazkezgdnJEyDMfcesTfYlceEG('users', lazy=True))
    uNTbtPuiJxHBxVxNyDixXVruAcpEXSkr = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.relationship('Permission', secondary=YNnssSAGionVEQQQYnkmFfvXoiNpkAZy, lazy='subquery',
                                  mTGDVBZazkezgdnJEyDMfcesTfYlceEG=wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.mTGDVBZazkezgdnJEyDMfcesTfYlceEG('users', lazy=True))
    def rxkAfmWNluTZaxHnoYNQevkNjoFywtoB(self, permission_name):
        if permission_name == 'acceso:inicio':
            return True
        for ypRGRfwMNVcmSjCzFWoZtVnETPWMjcDz in self.enEJqxjFAFiFONZixXzvPYopplNyLJPB:
            for ykefJOrywUrmfJwQyQXQDLhVvhkqHLDg in ypRGRfwMNVcmSjCzFWoZtVnETPWMjcDz.uNTbtPuiJxHBxVxNyDixXVruAcpEXSkr:
                if ykefJOrywUrmfJwQyQXQDLhVvhkqHLDg.BwqrFVnWNHJyYvjrvTOZsIzVltwDKIeX == permission_name:
                    return True
        for ykefJOrywUrmfJwQyQXQDLhVvhkqHLDg in self.uNTbtPuiJxHBxVxNyDixXVruAcpEXSkr:
            if ykefJOrywUrmfJwQyQXQDLhVvhkqHLDg.BwqrFVnWNHJyYvjrvTOZsIzVltwDKIeX == permission_name:
                return True
        return False
class FjGEUTfanljqTCWXgcJcLLolRqyIuIrw(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Model):
    id = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Integer, primary_key=True)
    LKfZpKWnQmWzDDLAkQCYzwIUGDqnEtIZ = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(100), unique=True, nullable=False)
    QyGHMPLufYZUIWZvTkESFfWZcXXyXSBd = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.String(150), nullable=False)
    mRlWUeafDNzIHobfHuUcVbaNGJSuIUPt = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Boolean, default=False)
    xCdgecDKBvVtGbYCMNwombbcPTqHcEWJ = wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Column(wCmkeJYOhgRMDbFBoxghgyoVgnxaGdTt.Boolean, default=False)
    def __repr__(self):
        return f"<Licencia {self.NombreLicencia}>"