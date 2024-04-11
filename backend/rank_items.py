import numpy as np
from SpringRank.SpringRank import SpringRank as sr
from models import Journal, Movie


def individual_ranking(session, db, alpha=2):
    selected = [s.obj_id for s in session.selections if s.selected is True]
    comparisons = [(p.win_id,p.lose_id,p.tie) for p in session.comparisons]

    if session.track == "Journals":
        selected_data = db.session.scalars(db.select(Journal).filter(Journal.link_id.in_(selected))).all()
    elif session.track == "Movies":
        selected_data = db.session.scalars(db.select(Movie).filter(Movie.link_id.in_(selected))).all()

    selected_names = {int(i.link_id):i.name for i in selected_data}

    # fill adjacency matrix
    a_pos = {k:i for i,k in enumerate(selected)}
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

    # # scale ranks
    # scale = .75
    # # the next line gives "ValueError: f(a) and f(b) must have different signs"
    # inverse_temperature = sr.get_inverse_temperature(a_matrix, user_ranks)
    # scaling_factor = 1 / (np.log(scale / (1 - scale)) / (2 * inverse_temperature))
    scaled_ranks = user_ranks # sr.scale_ranks(user_ranks,scaling_factor)

    # store in dictionary
    user_ranking = sorted([(k,scaled_ranks[i],selected_names[k]) for k,i in a_pos.items()], key = lambda x:x[1], reverse=True)
    return user_ranking