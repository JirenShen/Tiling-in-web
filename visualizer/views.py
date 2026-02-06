# visualizer/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .solver import solve_tiling
import json

def index(request):
    # 定义一个简单的 Tileset
    # 颜色代码: 0=Gray, 1=Red, 2=Blue, 3=Green
    # 结构: [id, North, East, South, West]
    tileset_data = [
        {'id': 1, 'n': 1, 'e': 2, 's': 1, 'w': 2}, # 瓦片 1
        {'id': 2, 'n': 2, 'e': 1, 's': 2, 'w': 1}, # 瓦片 2
        {'id': 3, 'n': 1, 'e': 1, 's': 2, 'w': 2}, # 瓦片 3
        {'id': 4, 'n': 2, 'e': 2, 's': 1, 'w': 1}, # 瓦片 4
        # ... 您可以添加更多
    ]

    # 颜色映射表 (用于前端显示)
    color_map = {
        0: '#dddddd', # Gray/Empty
        1: '#ff6b6b', # Red
        2: '#4ecdc4', # Teal
        3: '#ffe66d', # Yellow
    }

    context = {
        'tileset_json': json.dumps(tileset_data),
        'colormap_json': json.dumps(color_map)
    }
    return render(request, 'visualizer/creator.html', context)

def creator(request):
    colors = [
        {'id': 0, 'hex': '#dddddd', 'name': 'Gray'},
        {'id': 1, 'hex': '#ff6b6b', 'name': 'Red'},
        {'id': 2, 'hex': '#4ecdc4', 'name': 'Teal'},
        {'id': 3, 'hex': '#ffe66d', 'name': 'Yellow'},
        {'id': 4, 'hex': '#1a535c', 'name': 'Dark Blue'},
        {'id': 5, 'hex': '#ff9f1c', 'name': 'Orange'},
    ]
    return render(request, 'visualizer/creator.html', {'colors': colors})

def check_tileset(request):
    """API: 接收 tileset，返回是否能铺满 10x10"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tiles = data.get('tiles', [])
            # 调用算法检查 N=10
            result = solve_tiling(10, tiles)
            return JsonResponse({'success': True, 'can_tile': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})