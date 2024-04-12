from .database import db


class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

    obj_id = db.Column(db.Integer)
    selected = db.Column(db.Boolean)

    def __repr__(self):
        return '<{}, {}>'.format(self.session_id, self.obj_id)


class Comparison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    
    win_id = db.Column(db.Integer)
    lose_id = db.Column(db.Integer)
    tie = db.Column(db.Boolean)

    def __repr__(self):
        return '<{}, {}>'.format(self.win_id, self.lose_id)
    

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    track = db.Column(db.String(64))
    selections = db.relationship('Selection')
    comparisons = db.relationship('Comparison')
    completed_on = db.Column(db.DateTime)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    email = db.Column(db.String(120), unique=True)
    hash = db.Column(db.String(64))

    sessions = db.relationship('Session')

    # consented = db.Column(db.Boolean)
    # ref = db.Column(db.String(64))
    # keep_email = db.Column(db.String(64))
    # firstname = db.Column(db.String(120))
    # lastname = db.Column(db.String(120))

    def __repr__(self):
        return '<{}>'.format(self.email)


class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.String(16))
    name = db.Column(db.String(240))

    def __repr__(self):
        return '<{}>'.format(self.name)
    

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.String(16))
    name = db.Column(db.String(240))

    def __repr__(self):
        return '<{}>'.format(self.name)