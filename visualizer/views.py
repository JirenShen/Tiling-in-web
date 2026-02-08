# visualizer/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .solver import solve_tiling
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

@ensure_csrf_cookie
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

@require_POST
def check_tileset(request):
    try:
        data = json.loads(request.body or "{}")
        tiles = data.get("tiles", [])
        result = solve_tiling(10, tiles)
        return JsonResponse({"success": True, "can_tile": result})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

def play(request):
    colors = [
        {'id': 0, 'hex': '#dddddd', 'name': 'Gray'},
        {'id': 1, 'hex': '#ff6b6b', 'name': 'Red'},
        {'id': 2, 'hex': '#4ecdc4', 'name': 'Teal'},
        {'id': 3, 'hex': '#ffe66d', 'name': 'Yellow'},
        {'id': 4, 'hex': '#1a535c', 'name': 'Dark Blue'},
        {'id': 5, 'hex': '#ff9f1c', 'name': 'Orange'},
    ]
    return render(request, 'visualizer/play.html', {'colors': colors})