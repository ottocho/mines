
import logging
logger = logging.getLogger(__name__)

import json
import random
import datetime
import collections
from operator import or_
from functools import reduce

from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q

from . import helper
from mines_api.models import Game, Brick

def _get_nearby_bricks(height, width, x, y):
    '''
    check the bounary of the board and return avaliable nearby bricks

    positions:
        x-1,y-1 | x-1,y  | x-1,y+1
        x,y-1   | (x,y)  | x,y+1
        x+1,y-1 | x+1,y  | x+1,y+1
    '''
    pos = []
    if y > 0:
        pos.append((x, y-1))
    if y < width-1:
        pos.append((x, y+1))
    if x > 0:
        pos.append((x-1, y))
    if x < height-1:
        pos.append((x+1, y))
    if x > 0 and y > 0:
        pos.append((x-1, y-1))
    if x < height-1 and y < width-1:
        pos.append((x+1, y+1))
    if x > 0 and y < width-1:
        pos.append((x-1, y+1))
    if x < height-1 and y > 0:
        pos.append((x+1, y-1))
    return pos

def _get_new_empty_brick(x, y):
    '''
    return a default empty brick structure
    '''
    return {
        'x': x,
        'y': y,
        'isMine': False,
        'nNearbyMines': 0,
        'isDug': False,
        'isFlagged': False,
        'isMarked': False,
    }

def _put_mines(bricks_data, height, width, n_mines_all):
    '''
    initialize mines randomly in the game board
    '''
    _mn = 0
    while _mn < n_mines_all:
        _mx = random.randrange(0, height, 1)
        _my = random.randrange(0, width, 1)
        if not bricks_data[_mx][_my]['isMine']:
            bricks_data[_mx][_my]['isMine'] = True
            _mn = _mn + 1
    return bricks_data

def _update_brick_nearby_mines(bricks_data, height, width):
    '''
    update the `nNearbyMines` of every brick
    '''
    for x in range(height):
        for y in range(width):
            nearby_bricks_pos = _get_nearby_bricks(height, width, x, y)
            _n = sum([ 1 for (_x, _y) in nearby_bricks_pos
                         if bricks_data[_x][_y]['isMine'] ])
            bricks_data[x][y]['nNearbyMines'] = _n
    return bricks_data

def _get_game_data(game_id):
    '''
    fetch whole data of game and return it in a dictionary format
    '''
    game = Game.objects.get(pk=game_id)
    # fetch bricks data TODO query exception
    brick_objects = game.brick_set.order_by('x', 'y').iterator()
    bricks_data = []
    for x in range(game.height):
        new_bricks_row = []
        for y in range(game.width):
            _o = next(brick_objects)
            _d = {
                'x': _o.x,
                'y': _o.y,
                'isMine': _o.is_mine,
                'nNearbyMines': _o.n_nearby_mines,
                'isDug': _o.is_dug,
                'isFlagged': _o.is_flagged,
                'isMarked': _o.is_marked,
            }
            new_bricks_row.append(_d)
        bricks_data.append(new_bricks_row)
    game_data  = {
        'id': game_id,
        'userName': game.user_name,
        'startTime': game.start_time.isoformat(),
        'height': game.height,
        'width': game.width,
        'nMinesAll': game.n_mines_all,
        'nMinesLeft': game.n_mines_left,
        'status': game.status,
        'bricks': bricks_data,
    }
    return game_data


def _explore_dig(game_id, x, y):
    '''
    when dig on a brick whose neighbouring 8 bricks are all not mines, this
    digging should propagate to neighbouring bricks untils the boundary
    '''
    result = []
    # TODO fetch whole game data for spread, can be optimized
    game_data = _get_game_data(game_id)
    height = game_data['height']
    width = game_data['width']
    bricks_data = game_data['bricks']
    bricks_data[x][y]['isDug'] = True
    stack = []
    nearby_bricks_pos = _get_nearby_bricks(height, width, x, y)
    stack.extend(nearby_bricks_pos)
    while stack:
        _x, _y = stack.pop()
        _bk = bricks_data[_x][_y]
        if not _bk['isFlagged'] and not _bk['isDug'] and not _bk['isMine']:
            result.append((_x, _y))
            bricks_data[_x][_y]['isDug'] = True
            if _bk['nNearbyMines'] == 0:
                stack.extend(_get_nearby_bricks(height, width, _x, _y))
    logger.debug("(%d, %d) explore to %s" % (x, y, str(result)))
    return result

@require_http_methods(["GET"])
@transaction.atomic
def game_get(request, game_id):
    '''
    GET /api/game/get/:game_id

    fetch game infomation
    '''
    result = helper.get_new_result()

    try:
        game_data = _get_game_data(game_id)
    except ObjectDoesNotExist:
        result['ret'] = 60
        result['text'] = 'game %d not existed' % game_id
        return JsonResponse(result)
    result['ret'] = 0
    result['value'] = game_data
    return JsonResponse(result)

@require_http_methods(["POST"])
@transaction.atomic
def game_new(request):
    '''
    POST /api/game/new
    params:
        userName
        height
        width
        nMinesAll
    '''
    result = helper.get_new_result()

    _g = json.loads(request.body)
    # TODO check the post parameter if valid
    user_name = _g.get('userName', None)
    height = int(_g.get('height', None))
    width = int(_g.get('width', None))
    n_mines_all = int(_g.get('nMinesAll', None))

    new_game = Game(user_name=user_name,
                    height=height,
                    width=width,
                    n_mines_all=n_mines_all,
                    n_mines_left=n_mines_all,
                    status=Game.PLAYING)
    new_game.save()

    # build new bricks
    bricks_data = [] # 2D array for bricks' board
    for x in range(height):
        new_bricks_row = []
        for y in range(width):
            new_brick = _get_new_empty_brick(x, y)
            new_bricks_row.append(new_brick)
        bricks_data.append(new_bricks_row)
    # put mines in the bricks
    _put_mines(bricks_data, height, width, n_mines_all)
    # update the attr `nNearbyMines` of each brick
    _update_brick_nearby_mines(bricks_data, height, width)

    # store to db
    for x in range(height):
        for y in range(width):
            _b = bricks_data[x][y]
            new_brick = Brick(game=new_game,
                              x=x,
                              y=y,
                              is_mine=_b['isMine'],
                              n_nearby_mines=_b['nNearbyMines'],
                              is_dug=_b['isDug'],
                              is_flagged=_b['isFlagged'],
                              is_marked=_b['isMarked'])
            new_brick.save()

    game_id = new_game.id
    result['ret'] = 0
    result['value'] = dict(gameId=game_id)
    return JsonResponse(result)

@require_http_methods(["POST"])
@transaction.atomic
def game_right_click(request, game_id, x, y):
    '''
    POST /api/game/:game_id/right_click/:x/:y
    '''
    result = helper.get_new_result()
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        result['ret'] = 20
        result['text'] = 'game(%d) not existed' % game_id
        return JsonResponse(result)
    if game.status != Game.PLAYING:
        result['ret'] = 0
        result['text'] = 'game finished'
        return JsonResponse(result)
    try:
        brick = game.brick_set.get(x=x, y=y)
    except ObjectDoesNotExist:
        result['ret'] = 30
        result['text'] = 'game(%d) does not have brick(%d,%d)' % (game_id, x, y)
        return JsonResponse(result)
    # invalid click when brick is dug
    if brick.is_dug:
        result['ret'] = 0
        result['text'] = 'dug click'
        return JsonResponse(result)
    if brick.is_flagged:
        brick.is_flagged = False
        game.n_mines_left += 1
    else:
        brick.is_flagged = True
        game.n_mines_left -= 1
    brick.save()
    game.save()
    result['ret'] = 0
    result['text'] = 'game finished'
    result['value'] = {
        'brick': {
            'x': x,
            'y': y,
            'isFlagged': brick.is_flagged,
        },
        'game': {
            'nMinesLeft': game.n_mines_left
        },
    }
    return JsonResponse(result)

@require_http_methods(["POST"])
@transaction.atomic
def game_left_click(request, game_id, x, y):
    '''
    POST /api/game/:game_id/left_click/:x/:y
    '''
    result = helper.get_new_result()
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        result['ret'] = 40
        result['text'] = 'game(%d) not existed' % game_id
        return JsonResponse(result)
    if game.status != Game.PLAYING:
        result['ret'] = 0
        result['text'] = 'game finished'
        return JsonResponse(result)
    try:
        brick = game.brick_set.get(x=x, y=y)
    except ObjectDoesNotExist:
        result['ret'] = 50
        result['text'] = 'game(%d) does not have brick(%d,%d)' % (game_id, x, y)
        return JsonResponse(result)
    # invalid click when brick is dug or flagged
    if brick.is_dug:
        result['ret'] = 0
        result['text'] = 'dug click'
        return JsonResponse(result)
    if brick.is_flagged:
        result['ret'] = 0
        result['text'] = 'flagged click'
        return JsonResponse(result)
    brick.is_dug = True
    brick.save()
    # click on a mine: lost
    if brick.is_mine:
        game.status = Game.LOST
        game.save()
        result['ret'] = 0
        result['value'] = {
            'bricks': [
                {
                    'x': x,
                    'y': y,
                    'isDug': True
                },
            ],
            'game': {
                'status': Game.LOST
            },
        }
        return JsonResponse(result)
    dug_bricks = [(x, y)]
    if brick.n_nearby_mines == 0:
        _s = _explore_dig(game_id, x, y)
        dug_bricks.extend(_s)
    # update the dug bricks
    logger.debug("before qs: " + datetime.datetime.now().isoformat())
    qs = ((Q(x=_x) & Q(y=_y)) for (_x, _y) in dug_bricks)
    q = Q(game_id=game_id) & reduce(or_, qs)
    Brick.objects.filter(q).update(is_dug=True)
    logger.debug("after qs: " + datetime.datetime.now().isoformat())
    # check if won
    dug_count = Brick.objects.filter(game_id=game_id, is_dug=True).count()
    if dug_count + game.n_mines_all == game.height * game.width:
        new_status = Game.WON
        game.status = new_status
        game.save()
    else:
        new_status = Game.PLAYING
    result['ret'] = 0
    result['value'] = {
        'bricks': [
            dict(x=_x, y=_y, isDug=True) for (_x, _y) in dug_bricks
        ],
        'game': {
            'status': new_status,
        },
    }
    return JsonResponse(result)

