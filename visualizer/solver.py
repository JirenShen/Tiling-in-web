# visualizer/solver.py

def solve_tiling(N, tiles):
    """
    检查给定的 tiles 列表能否铺满 N x N 的区域。
    tiles: list of dicts [{'n':1, 'e':2, 's':1, 'w':0}, ...]
    """
    if not tiles:
        return False
    
    # 1. 预计算所有合法的“垂直列” (Phase 1: Vertical Columns)
    # columns_transitions: { West_Boundary_Tuple: Set(East_Boundary_Tuple) }
    transitions = {}
    
    # 辅助 DFS 函数
    def generate_columns(y, current_west, current_east, prev_north):
        if y == N:
            # 完成一列，记录转换关系
            w_tuple = tuple(current_west)
            e_tuple = tuple(current_east)
            if w_tuple not in transitions:
                transitions[w_tuple] = set()
            transitions[w_tuple].add(e_tuple)
            return

        for tile in tiles:
            # 检查垂直匹配 (South == Prev North)
            # y=0 时是底层，不需要匹配下方
            if y == 0 or tile['s'] == prev_north:
                current_west[y] = tile['w']
                current_east[y] = tile['e']
                generate_columns(y + 1, current_west, current_east, tile['n'])

    # 启动 DFS 生成列
    # 初始化长度为 N 的占位数组
    dummy_west = [0] * N
    dummy_east = [0] * N
    generate_columns(0, dummy_west, dummy_east, -1)

    if not transitions:
        return False

    # 2. 检查水平连通性 (Phase 2: Horizontal Reachability)
    # 初始集合：第一列可以是任何生成的列，所以只要是 transitions 中的右边界都可能是第一列的输出
    current_boundaries = set()
    for targets in transitions.values():
        current_boundaries.update(targets)
    
    # 迭代 N-1 次 (因为总共 N 列)
    for _ in range(1, N):
        next_boundaries = set()
        for b in current_boundaries:
            # 如果当前边界 b 可以作为下一列的左边 (即在 transitions 的 key 中)
            if b in transitions:
                next_boundaries.update(transitions[b])
        
        if not next_boundaries:
            return False # 断路了
        current_boundaries = next_boundaries

    return True