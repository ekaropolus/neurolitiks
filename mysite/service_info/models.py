from mysite import db

class ServiceInfo(db.Model):
    id_service = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(120), unique=True, nullable=False)
    service_icon = db.Column(db.String(20), nullable=False, default = 'bi bi-0-circle')
    service_abstract = db.Column(db.String(240), nullable = False)
    service_description = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"Service('{self.service_name}', '{self.service_abstract}')"