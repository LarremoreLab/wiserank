from itertools import combinations
from collections import Counter, defaultdict
import numpy as np
from .models import Item
from sqlalchemy import and_

from .rank_items import individual_ranking

def pair_item(session, db):
    ## select an algorithm for pairing items or implement a new one

    return custom_pair(session, db)
    # return random_pair(session, db)


def random_pair(session, db):
    selected = sorted([str(k.obj_id) for k in session.selections if k.selected is True])
    all_combinations = set(combinations(selected, 2))

    compared = set([tuple(sorted((str(p.win_id),
                                  str(p.lose_id)))) for p in session.comparisons])
    candidates = [c for c in all_combinations if c not in compared]

    if len(candidates) > 0:
        pair_ids = candidates[np.random.randint(0,len(candidates))]
        pair = db.session.scalars(db.select(Item).filter(and_(
                                                            Item.track == session.track,
                                                            Item.link_id.in_(pair_ids)
                                                            ))).all()
        pair_names = {str(i.link_id):i.name for i in pair}
        random_i = np.random.randint(2)
        return ([{'link_id':pair_ids[random_i],
                'name':pair_names[pair_ids[random_i]]},
                {'link_id':pair_ids[(random_i+1)%2],
                'name':pair_names[pair_ids[(random_i+1)%2]]}])
    
    return ([{'link_id':-1,'name':""},
             {'link_id':-2,'name':""}])


def custom_pair(session,db):
    """
    Pairs items dynamically based both on the number of times items have been compared and 
    the proximity of two items in a ranking inferred from already made comparisons.
    """

    pair_ids = None

    compared = set([tuple(sorted((str(p.win_id),
                                  str(p.lose_id)))) for p in session.comparisons])

    if len(compared) == 0:
        return random_pair(session, db)
    
    selected = sorted([str(k.obj_id) for k in session.selections if k.selected is True])
    all_combinations = set(combinations(selected, 2))

    times_compared = Counter(np.array([*compared]).flatten())
    times_compared = sorted([(k,times_compared[k]) if k in times_compared else (k,0) for k in selected], key = lambda x:x[1])

    wins = defaultdict(int)
    losses = defaultdict(int)
    for p in session.comparisons:
        w_id = str(p.win_id)
        l_id = str(p.lose_id)
        wins[w_id] += 1
        losses[l_id] += 1
        if p.tie is True:
            wins[l_id] += 1
            losses[w_id] += 1
    
    losers = [k for k in selected if wins[k] == 0]
    winners = [k for k in selected if losses[k] == 0]
    if len(winners) >= 2 and times_compared[0][1] > 1:
        candidates = []
        pair_ids = list(np.random.choice(winners, size=2,replace=False))
    elif len(losers) >= 2 and times_compared[0][1] > 1:
        candidates = []
        pair_ids = list(np.random.choice(losers, size=2,replace=False))

    elif times_compared[0][1] > 5:
        candidates = [c for c in all_combinations if c not in compared]

    else:
        least_compared = [x for x,y in times_compared if y == times_compared[0][1]]
        focal_node = np.random.choice(least_compared)

        candidates = [c for c in all_combinations if c not in compared and focal_node in c]
        r_candidates = [c for c in candidates if c[0] in least_compared and c[1] in least_compared]

        if times_compared[0][1] < 2 and len(r_candidates) > 0:
            candidates = r_candidates

    if len(candidates) > 0:
        ranking = {str(r[0]):r[1] for r in individual_ranking(session, db)}
        pods = sorted([(np.abs(ranking[x] -  ranking[y]),(x,y)) for x,y in candidates], key = lambda _:_[0])
        peas = [p[1] for p in pods if p[0] == pods[0][0]]
        np.random.shuffle(peas)
        pair_ids = peas[0]
        
    if pair_ids:
        pair = db.session.scalars(db.select(Item).filter(and_(
                                                            Item.track == session.track,
                                                            Item.link_id.in_(pair_ids)
                                                            ))).all()
        pair_names = {str(i.link_id):i.name for i in pair}
        random_i = np.random.randint(2)
        return ([{'link_id':pair_ids[random_i],
                'name':pair_names[pair_ids[random_i]]},
                {'link_id':pair_ids[(random_i+1)%2],
                'name':pair_names[pair_ids[(random_i+1)%2]]}])
    else:
        return ([{'link_id':-1,'name':""},
             {'link_id':-2,'name':""}])