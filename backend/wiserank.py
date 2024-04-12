from backend.utils.models import Journal, User, Session, Selection, Comparison, Movie
from backend.utils.database import db
from backend.utils.hasher import hash_string
from backend.utils.select_item import rec_item
from backend.utils.pair_items import random_pair
from backend.utils.rank_items import individual_ranking

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__, static_folder='../frontend/dist/',    static_url_path='/')
app.config['DEBUG'] = True
CORS(app, resources={r"/*": {"origins": "*"}})

basedir = os.path.abspath('')
database_uri = os.environ.get('DATABASE_CONNECTION_POOL_URL') or 'sqlite:///' + os.path.join(basedir, 'wiserank.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri.replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a-very-very-secret-key'

db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
db.app = app
app.db = db

@app.route('/', defaults={'path': ''})
@app.route("/<string:path>")
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/loaduser', methods=['POST'])
def load_user():
    post_data = request.get_json()
    email = post_data["email"]
    user = db.session.scalars(db.select(User).filter_by(email=email)).first()

    # create new user if none exists
    if user is None:
        email_hash = hash_string(email)
        db.session.add(User(email=email, 
                            hash=email_hash))
        db.session.commit()
        user_data = {"hash":email_hash,"email":email,
                     "sessions":[]}
    else:
        user_data = {"hash":user.hash,"email":user.email,
                     "sessions":[[s.id,s.track] for s in user.sessions]} 
    return jsonify(user=user_data)


@app.route('/loadsessions', methods=['POST'])
def load_sessions():
    options = ["Journals", "Movies"]
    # journals = db.session.scalars(db.select(Journal).limit(10))
    return jsonify(options=options)


@app.route('/newsession', methods=['POST'])
def new_session():
    post_data = request.get_json()
    track = post_data["track"]
    hash = post_data["hash"]
    user = db.session.scalars(db.select(User).filter_by(hash=hash)).first()

    s = Session(user_id=user.id, track=track)
    db.session.add(s)
    db.session.flush()
    new_id = s.id
    db.session.commit()

    return jsonify(session=[new_id,track])


@app.route('/submitloaditem', methods=['POST'])
def submit_load_item():
    post_data = request.get_json()
    sess_id = post_data["sessionID"]
    item = post_data["item"]
    selection = post_data["selection"]

    session = db.session.scalars(db.select(Session).filter_by(id=sess_id)).first()
    selected = set([int(s.obj_id) for s in session.selections])

    # submit item if necessary
    link_id = int(item['link_id'])
    if link_id != -1 and link_id not in selected:
        s = Selection(session_id=sess_id,
                      obj_id=link_id,
                      selected=bool(selection)
                      )
        db.session.add(s)
        db.session.commit()

    # load item
    session = db.session.scalars(db.select(Session).filter_by(id=sess_id)).first()
    new = rec_item(session, db)

    selected = [k.obj_id for k in session.selections if k.selected is True]
    if session.track == "Journals":
        table = Journal
    elif session.track == "Movies":
        table = Movie

    select_times = {i.obj_id:i.created_on for i in session.selections}
    selected_data = db.session.scalars(db.select(table).filter(table.link_id.in_(selected))).all()
    s = sorted([(i.link_id, i.name) for i in selected_data], key = lambda x:select_times[int(x[0])])

    return jsonify(new=new,selected=s)


@app.route('/searchitems', methods=['POST'])
def search_items():
    post_data = request.get_json()
    sess_id = post_data["sessionID"]
    session = db.session.scalars(db.select(Session).filter_by(id=sess_id)).first()
    if session.track == "Journals":
        table = Journal
    elif session.track == "Movies":
        table = Movie
    items = db.session.scalars(db.select(table).filter(table.name.ilike("%" + post_data['string'] + "%")).limit(50)).all()
    return jsonify(sorted([[j.link_id,j.name] for j in items], key = lambda x:len(x[1]))[:10])


@app.route('/submitloadpair', methods=['POST'])
def submit_load_pair():
    post_data = request.get_json()
    sess_id = post_data["sessionID"]
    pair = post_data["pair"]
    selection = post_data["selection"]

    # submit item if necessary
    if pair[0]['link_id'] != -1:
        if selection < 2:
            c = Comparison(session_id=sess_id,
                           win_id=pair[(0 + selection)%2]['link_id'],
                           lose_id=pair[(1 + selection)%2]['link_id'],
                           tie=False
                           )
        else:
            c = Comparison(session_id=sess_id,
                           win_id=pair[0]['link_id'],
                           lose_id=pair[1]['link_id'],
                           tie=True
                           )
        db.session.add(c)
        db.session.commit()

    # load item
    session = db.session.scalars(db.select(Session).filter_by(id=sess_id)).first()
    new = random_pair(session, db)

    return jsonify(new=new)

@app.route('/rankindividual', methods=['POST'])
def rank_individual():
    post_data = request.get_json()
    sess_id = post_data["sessionID"]

    session = db.session.scalars(db.select(Session).filter_by(id=sess_id)).first()
    ranking = individual_ranking(session, db)
    comparisons = [(p.win_id,p.lose_id,p.tie) for p in session.comparisons]

    return jsonify(ranking=ranking,comparisons=comparisons)


# if __name__ == '__main__':
#     app.run(debug=True, port=5001)