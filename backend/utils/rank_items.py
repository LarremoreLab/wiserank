import numpy as np
from .SpringRank.SpringRank import SpringRank as sr
from .models import Item
from sqlalchemy import and_

def format_name(i):
    if i.meta is not None and i.meta != "":
        return i.name+" ("+i.meta+")"
    else:
        return i.name


def individual_ranking(session, db, alpha=2):
    selected = [str(s.obj_id) for s in session.selections if s.selected is True]
    comparisons = [(str(p.win_id),
                    str(p.lose_id),
                    p.tie) for p in session.comparisons]
    selected_data = db.session.scalars(db.select(Item).filter(and_(
                                                        Item.track == session.track,
                                                        Item.link_id.in_(selected)
                                                        ))).all()
    selected_names = {str(i.link_id):format_name(i) for i in selected_data}

    # fill adjacency matrix
    a_pos = {str(k):i for i,k in enumerate(selected)}
    M = len(selected)
    a_matrix = np.zeros((M,M)).astype(int)

    for w,l,t in comparisons:
        if t is False:
            a_matrix[a_pos[w],
                    a_pos[l]] += 1
        else:
            # ties
            a_matrix[a_pos[w],
                    a_pos[l]] += .5
            a_matrix[a_pos[l],
                    a_pos[w]] += .5
            
    user_ranks = sr.SpringRank(a_matrix,alpha=alpha)

    user_ranking = sorted([(int(k),user_ranks[i],selected_names[k]) for k,i in a_pos.items()], key = lambda x:x[1], reverse=True)
    return user_ranking