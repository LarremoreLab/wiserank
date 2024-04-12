import sqlalchemy
import json
from collections import defaultdict
from scipy import sparse
from .models import Journal, Movie
import os

data_dir = os.path.abspath(os.path.join(os.path.abspath(''),'..', "data"))
if os.environ.get('DYNO'):
    data_dir = "/app" + data_dir
movie_recs = json.load(open(data_dir+"/movie_recs.json","r"))

journal_recs = [sparse.load_npz(data_dir+'/journal_recs_mx.npz'),
                json.load(open(data_dir+'/journal_recs_ids.json','r'))]


def random_item(session, db):
    selected = set([s.obj_id for s in session.selections])
    
    for _ in range(100):
        if session.track == "Journals":
            candidate = db.session.scalars(db.select(Journal).order_by(sqlalchemy.func.random()).limit(1)).first()
        elif session.track == "Movies":
            candidate = db.session.scalars(db.select(Movie).order_by(sqlalchemy.func.random()).limit(1)).first()
        
        if candidate.link_id not in selected:
            return {"link_id": candidate.link_id, "name":candidate.name}
    return {"link_id": -1, "name":"--INTERNAL ERROR PLEASE REFRESH PAGE--"}


def retrieve_journal_votes(alice, mx, v_ids):
    i,j = mx.indptr[v_ids['v_i'][alice]], mx.indptr[v_ids['v_i'][alice]+1]
    for bob, vote in zip(mx.indices[i:j], mx.data[i:j]):
        yield v_ids['i_v'][str(bob)], vote


def rec_journal(session,db):
    seen = set([str(s.obj_id) for s in session.selections])
    selected = set([str(s.obj_id) for s in session.selections if s.selected])
    distribution = defaultdict(int)

    for s in selected: 
        try:
            for k,v in retrieve_journal_votes(s, journal_recs[0], journal_recs[1]):
                if k not in seen:
                    distribution[k] += v
        except:
            continue
    if len(distribution) > 0:
        top_id,_ = sorted([(x,y) for x,y in distribution.items()], key = lambda _:_[1],reverse=True)[0]
        candidate = db.session.scalars(db.select(Journal).filter_by(link_id=str(top_id))).first()
        return {"link_id": candidate.link_id, "name":candidate.name}
    else:
        return random_item(session, db)


def rec_movie(session, db):
    seen = set([s.obj_id for s in session.selections])
    selected = set([s.obj_id for s in session.selections if s.selected])
    distribution = defaultdict(float)

    for m in selected:
        m_recs = movie_recs.get(str(m),[(m,0)])
        for r,c in m_recs[1:]:
            if r not in seen:
                distribution[r] += c / m_recs[0][1]
    
    if len(distribution) > 0:
        top_id,_ = sorted([(x,y) for x,y in distribution.items()], key = lambda _:_[1],reverse=True)[0]
        candidate = db.session.scalars(db.select(Movie).filter_by(link_id=str(top_id))).first()
        return {"link_id": candidate.link_id, "name":candidate.name}
    else:
        return random_item(session, db)


def rec_item(session, db):
    if session.track == "Journals":
        return rec_journal(session, db)
    elif session.track == "Movies":
        return rec_movie(session, db)
    else:
        return random_item(session, db)