from core.models import Cell, Shape
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Insert shapes and blank pieces."

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help="Overwrite existing data (except placed pieces).")

    def handle(self, *args, **options):
        shapes = self.seed_shapes(options['force'])
        self.seed_grid(shapes, options['force'])

    def seed_shapes(self, force):
        print("Seeding shapes...")
        shapes = {}
        for s in settings.PIECE_SHAPES:
            shape = Shape.objects.filter(key=s['key']).first()
            if not shape:
                shape = Shape(**s)
            if force or not shape.image:
                print("Seeding shape", shape)
                shape.image = f"images/shapes/{shape.key}.png"
                shape.save()
            shapes[shape.key] = shape
        print("Done")
        return shapes

    def seed_grid(self, shapes, force):
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
                if force or not cell:
                    cell = Cell(
                        id=cell.id if cell else None,
                        r=r,
                        c=c,
                        piece=cell.piece,
                        shape=shapes[shape_key],
                        turns=int(turns),
                    )
                    print("Seeding cell", cell.coords)
                    cell.save()
        print("Done")
