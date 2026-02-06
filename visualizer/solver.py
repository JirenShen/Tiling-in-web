# visualizer/solver.py

def solve_tiling(N, tiles):
    """
    Optimized Solver: 使用 BFS 和 集合去重 (Deduplication) 
    来避免 N=10 时的指数级爆炸。
    """
    if not tiles:
        return False
    
    # --- Phase 1: 快速生成所有合法的“垂直列” (Vertical Phase) ---
    # 我们不存储整个列的内部，只存储 (West_Boundary, East_Boundary)
    # 状态格式: layer_states[top_color_id] = { (west_tuple, east_tuple), ... }
    
    layer_states = {}
    
    # 1. 初始化第一层 (Layer 1)
    for t in tiles:
        n_color = t['n']
        if n_color not in layer_states:
            layer_states[n_color] = set()
        # 存入元组 (tuple)，因为列表不可哈希，无法存入 set
        layer_states[n_color].add( ((t['w'],), (t['e'],)) )
        
    # 2. 逐层向上生长 (Layer 2 to N)
    for h in range(1, N):
        next_layer_states = {}
        has_valid_column = False
        
        # 遍历上一层的所有顶端颜色
        for prev_north, pairs in layer_states.items():
            # 找到所有能接在这个颜色上面的瓦片 (South == Prev North)
            compatible_tiles = [t for t in tiles if t['s'] == prev_north]
            
            if not compatible_tiles:
                continue
                
            for t in compatible_tiles:
                new_north = t['n']
                if new_north not in next_layer_states:
                    next_layer_states[new_north] = set()
                
                # 核心优化：批量扩展，并自动去重
                # 如果有两个不同的内部组合产生了相同的边界，set 会自动把它们合并成一个！
                for (w_seq, e_seq) in pairs:
                    new_w = w_seq + (t['w'],)
                    new_e = e_seq + (t['e'],)
                    next_layer_states[new_north].add((new_w, new_e))
                    has_valid_column = True
        
        # 如果这一层长不出任何东西，说明断了，直接返回失败
        if not has_valid_column:
            return False
            
        layer_states = next_layer_states

    # --- Phase 2: 构建水平转移图 (Graph Construction) ---
    transitions = {}
    for pairs in layer_states.values():
        for (w, e) in pairs:
            if w not in transitions:
                transitions[w] = set()
            transitions[w].add(e)
            
    if not transitions:
        return False

    # --- Phase 3: 检查水平连通性 (Horizontal Reachability) ---
    # 第一列：可以是任何生成出来的列，所以所有存在的 East 边界都是潜在的起点
    current_reachable = set()
    for targets in transitions.values():
        current_reachable.update(targets)
    
    # 迭代 N-1 次 (拼接剩下的 N-1 列)
    for _ in range(1, N):
        next_reachable = set()
        for r in current_reachable:
            # r 是上一列的右边界，它必须等于下一列的左边界 (key in transitions)
            if r in transitions:
                next_reachable.update(transitions[r])
        
        if not next_reachable:
            return False # 无法继续横向拼接
        current_reachable = next_reachable

    return True