from __init__ import db, app
with app.app_context():
    db.create_all()