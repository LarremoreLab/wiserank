from itertools import combinations
import numpy as np
from .models import Item
from sqlalchemy import and_


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