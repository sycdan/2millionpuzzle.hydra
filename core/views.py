import logging

from core.models import Cell, Piece, Shape
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def index(request, *args, **kwrgs):
    # Load the selected cell from the query string
    selected_cell_id = int(request.GET.get('cell_id') or 0)
    selected_cell = Cell.objects.get(pk=selected_cell_id) if selected_cell_id else None

    # If a new shape was picked, apply it before loading the grid
    if shape_id := request.POST.get('shape_id'):
        if shape := Shape.objects.get(pk=int(shape_id)):
            if shape != selected_cell.shape:
                selected_cell.shape = shape
                selected_cell.save()

    # Same for turns
    if turns := request.POST.get('turns'):
        turns = int(turns)
        if turns != selected_cell.turns:
            selected_cell.turns = turns
            selected_cell.save()

    # If placing a piece, refresh the view afterwards
    if selected_cell:
        if place_piece_id := request.POST.get('place_piece_id'):
            if place_piece_id == '0':
                selected_cell.clear()
            elif place_piece := Piece.objects.get(pk=place_piece_id):
                if selected_cell.piece != place_piece:
                    selected_cell.piece = place_piece
                    selected_cell.save()
                # Clear any other cell the piece was in
                for cell in place_piece.cell_set.all():
                    if cell != selected_cell:
                        cell.piece = None
                        cell.save()
                return redirect('/')

    # Build an empty grid, then fill it with all known cell info, while recording used pieces
    used_pieces = []
    grid = list([None for _ in range(settings.GRID_COLS)] for _ in range(settings.GRID_ROWS))
    for cell in Cell.objects.filter():
        grid[cell.r - 1][cell.c - 1] = cell
        if cell.piece:
            used_pieces.append(cell.piece)

    # Set up the basic template data
    data = dict(
        grid=grid,
        used_pieces=used_pieces,
        selected_cell=selected_cell,
        shapes=list(Shape.objects.all()) if selected_cell else [],
    )

    # Attempt to figure out initial filters
    data.update(scrape_wants(selected_cell, grid))

    # Update the context data with the results of processing the form, if it was submitted
    if form := request.POST:
        data.update(process_form(form, **data))

    return render(request, 'index.html', data)


def process_form(form, selected_cell, used_pieces, grid, **kwargs):
    heada = form.get('heada', '')
    headb = form.get('headb', '')
    headc = form.get('headc', '')
    headd = form.get('headd', '')
    limba = form.get('limba', '')
    limbb = form.get('limbb', '')
    limbc = form.get('limbc', '')
    limbd = form.get('limbd', '')
    piece_num = form.get('piece_num', '')
    include_used = int(form.get('include_used') or 0)
    
    if piece_num:
        heada = ''
        headb = ''
        headc = ''
        headd = ''
        limba = ''
        limbb = ''
        limbc = ''
        limbd = ''

    matched_pieces = []
    if selected_cell:
        pieces_query = Piece.objects.filter(shape=selected_cell.shape)

        if piece_num:
            pieces_query = pieces_query.filter(num=piece_num)

        head_wants = [heada, headb, headc, headd]
        limb_wants = [limba, limbb, limbc, limbd]
        if pieces_query.count() <= settings.PIECE_QUERY_LIMIT or selected_cell.shape or piece_num or any(x for x in head_wants) or any(x for x in limb_wants):
            for piece in pieces_query:
                if piece_matches(piece, settings.HEAD_SEQUENCES, head_wants) and piece_matches(piece, settings.LIMB_SEQUENCES, limb_wants):
                    matched_pieces.append(piece)

    # Throw out any used pieces that were not matched
    used_pieces = list(filter(lambda x: x in matched_pieces, used_pieces))

    # Then optionally include the used matched pieces
    if not include_used:
        matched_pieces = list(filter(lambda x: x not in used_pieces, matched_pieces))

    return dict(
        piece_num=piece_num,
        pieces=matched_pieces,
        heada=heada,
        headb=headb,
        headc=headc,
        headd=headd,
        limba=limba,
        limbb=limbb,
        limbc=limbc,
        limbd=limbd,
        used_pieces=used_pieces,
        include_used=include_used,
    )


def piece_matches(piece, sequences, wants):
    # If there are no wants, just shortcut to a match
    if not any(x for x in wants if x):
        return True

    logger.debug("Checking if %s has %s in %s", piece, wants, sequences)
    # Sequences is e.g. nesw, eswn, etc.
    for sequence in sequences:
        haves = []
        for s in sequence:
            haves.append(getattr(piece, s))
        if haves_matches_wants(haves, wants):
            return True
    return False

                    
def haves_matches_wants(haves, wants):
    # Iterate all the sets of requested symbols...
    for i, want in enumerate(wants):
        # If nothing specific was wanted, match anything
        if not want:
            continue
        for w in want:
            # If this wanted symbol does not exists on the side in question, we're done...
            if w not in haves[i]:
                return False
    return True

def scrape_wants(cell, grid):
    # Look in the surrounding cells
    wants = {}
    return wants
    for adj in [
        [0, -1, ['sw', 'se']], # n
        # [+1, 0, ['nw', 'sw']], # e
        # [0, +1, ['ne', 'nw']], # s
        # [-1, 0, ['ne', 'nw']], # w
    ]:
        try:
            adj_cell = grid[cell.r + adj[1] - 1][cell.c + adj[0] - 1]
        except IndexError:
            adj_cell = None
        # if adj_cell and adj_cell.piece:
        #     haves = [adj_cell.piece.get_pattern(x) for x in adj[2]]
        pass
    return wants
