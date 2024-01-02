import re
import os

from core.models import Cell, Piece, Shape
from django.conf import settings
from django.core.management.base import BaseCommand

KEY_ALL = '__ALL__'

class Command(BaseCommand):
    help = "Insert shapes and blank pieces."

    def add_arguments(self, parser):
        parser.add_argument('--skip-grid', action='store_true', help="Don't seed the grid cells")
        parser.add_argument('--skip-shapes', action='store_true', help="Don't seed the shapes")

    def handle(self, *args, **options):
        if not options['skip_shapes']:
            self.seed_shapes()
        if not options['skip_grid']:
            self.seed_grid()
        
        print("Seeding pieces...")
        for file in os.listdir(settings.UPLOADED_IMAGES_PATH):
            if re.match(r"^[^.]+\.([^.]+)$", file):
                shape_key, num = (file.split('.')[0]).split('-')
                shape = Shape.objects.get(key=shape_key)
                piece = Piece(
                    shape=shape,
                    num=int(num),
                    image=os.path.join(settings.UPLOADED_IMAGES_PATH, file),
                )
                if not Piece.objects.filter(shape__key=shape_key, num=num).exists():
                    print(f"Seeding {shape_key}-{num}")
                    piece.save()
        print("Done")

    def seed_shapes(self):
        print("Seeding shapes...")
        for s in settings.PIECE_SHAPES:
            shape = Shape(**s)
            if not Shape.objects.filter(key=shape.key).exists():
                print("Seeding shape", shape)
                shape.image = f"images/shapes/{shape.key}.png"
                shape.save()
        print("Done")

    def seed_grid(self):
        shape_cache = {}
        for shape in Shape.objects.all():
            shape_cache[shape.key] = shape
        print("Seeding grid cells...")
        for y, row in enumerate(settings.GRID):
            r = y + 1 # need 1-based
            for x, piece_key in enumerate(row):
                c = x + 1 # need 1-based
                if not piece_key:
                    continue
                # If no rotation is specified, add it as 0 degrees
                if '+' not in piece_key:
                    piece_key = piece_key + '+0'
                shape_key, turns = piece_key.split('+')
                cell = Cell.objects.filter(r=r, c=c).first()
                if not cell:
                    cell = Cell(
                        r=r,
                        c=c,
                        shape=shape_cache.get(shape_key),
                        turns=int(turns),
                    )
                    print("Seeding cell", cell)
                    cell.save()
        print("Done")
