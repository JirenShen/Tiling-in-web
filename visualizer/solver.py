# visualizer/solver.py

def solve_tiling(N, tiles):

    if not tiles:
        return False
    

    
    layer_states = {}
    
  
    for t in tiles:
        n_color = t['n']
        if n_color not in layer_states:
            layer_states[n_color] = set()

        layer_states[n_color].add( ((t['w'],), (t['e'],)) )

    for h in range(1, N):
        next_layer_states = {}
        has_valid_column = False
        for prev_north, pairs in layer_states.items():

            compatible_tiles = [t for t in tiles if t['s'] == prev_north]
            
            if not compatible_tiles:
                continue
                
            for t in compatible_tiles:
                new_north = t['n']
                if new_north not in next_layer_states:
                    next_layer_states[new_north] = set()
                
                for (w_seq, e_seq) in pairs:
                    new_w = w_seq + (t['w'],)
                    new_e = e_seq + (t['e'],)
                    next_layer_states[new_north].add((new_w, new_e))
                    has_valid_column = True
        
 
        if not has_valid_column:
            return False
            
        layer_states = next_layer_states


    transitions = {}
    for pairs in layer_states.values():
        for (w, e) in pairs:
            if w not in transitions:
                transitions[w] = set()
            transitions[w].add(e)
            
    if not transitions:
        return False


    current_reachable = set()
    for targets in transitions.values():
        current_reachable.update(targets)
    

    for _ in range(1, N):
        next_reachable = set()
        for r in current_reachable:

            if r in transitions:
                next_reachable.update(transitions[r])
        
        if not next_reachable:
            return False 
        current_reachable = next_reachable

    return True