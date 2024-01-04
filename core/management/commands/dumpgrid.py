import base64
import json

from core.models import Cell
from core.utils import get_head_bits, rotate_heads
from django.conf import settings
from django.core.management.base import BaseCommand


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cell):
            return f"{obj.shape.key}+{obj.turns}"
        return json.JSONEncoder.default(self, obj)


class Command(BaseCommand):
    help = "Outputs a JSON representation of the shape layout."

    def add_arguments(self, parser):
        parser.add_argument('--no-compact', action='store_true', help="Don't remove separator spaces from JSON data")
        parser.add_argument('--no-encode', action='store_true', help="Don't base-64 the output")
        parser.add_argument('--no-validate', action='store_true', help="Don't check whether the grid is valid")
        parser.add_argument('--line-length', type=int, default=0, help="Add line break every x characters (0 = one line)")

    def handle(self, *args, **options):
        # Load all the cells in row, column order
        grid = []
        for cell in Cell.objects.all().order_by('-r', 'c'):
            while len(grid) < cell.r:
                grid.append([])
            grid[cell.r - 1].append(cell)

        if not options['no_validate']:
            if errors := self.validate_grid(grid):
                print("Your grid is invalid!")
                for error in errors:
                    print(error)
                return

        output = json.dumps(
            grid,
            separators=(", ", ": ") if options['no_compact'] else (",", ":"),
            cls=JsonEncoder,
        )
        if not options['no_encode']:
            json_bytes = output.encode('utf-8')
            output = base64.b64encode(json_bytes).decode('utf-8')
            print("Copy the data below into your .env file")
            print("-" * 80)
            print("GRID=", end='')
        line_length = options['line_length'] or 1024 * 1024
        for i in range(0, len(output), line_length):
            print(output[i:i+line_length])

    def validate_grid(self, grid):
        errors = []
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                heads = rotate_heads(cell.shape.heads, cell.turns)
                bits = get_head_bits(heads)
                # For each of this piece's heads, does the piece in that direction have a hole and vice-versa
                for i, adj in enumerate([
                    [0, -1], # n
                    [+1, 0], # e
                    [0, +1], # s
                    [-1, 0], # w
                ]):
                    adj_x = x + adj[0]
                    adj_y = y + adj[1]
                    if adj_x < 0 or adj_y < 0 or adj_x > settings.GRID_COLS - 1 or adj_y > settings.GRID_ROWS - 1:
                        continue
                    adj_cell = grid[adj_y][adj_x]
                    adj_heads = rotate_heads(adj_cell.shape.heads, adj_cell.turns)
                    adj_bits = get_head_bits(adj_heads)
                    # Find the opposing hole side (e.g. s -> n, w -> e)
                    if bits[i] == adj_bits[settings.OPPOSING_SIDES[i]]:
                        errors.append(f"Cell {cell.coords} does not match all adjacent cells")
        return errors
