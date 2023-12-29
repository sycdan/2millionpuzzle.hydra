from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Cell, Piece, Shape

KEY_ALL = '__ALL__'

class Command(BaseCommand):
    help = "Insert shapes and blank pieces."

    def add_arguments(self, parser):
        parser.add_argument('--grid', action='store_true', help="Seed the grid cells")
        parser.add_argument('--key', type=str, default=KEY_ALL, help="Which shape type to seed")
        # parser.add_argument('end', type=int, help='Last piece number')
        # parser.add_argument('heads', type=int, help="Number of head (1, 2, 3, 4, 0)")
        # parser.add_argument('style', type=str, help="eb")

    def handle(self, *args, **options):
        self.seed_shapes(options['key'])
        if options['grid']:
            self.seed_grid()
        # TODO: fix this up to work for seeding real pieces
        # style = options['style']
        # heads = options['heads']
        # for i in range(options['end']):
        #     x = i + 1
        #     print(heads, style, x)
        #     p = None
        #     for _p in Piece.objects.filter(x=x, heads=heads):
        #         if _p.style == style:
        #             p = _p
        #             print("Found", p)
        #             break
        #     if p is None:
        #         print("Creating")
        #         p = Piece(x=x, heads=heads, style=style)
        #     if not p.image:
        #         p.image = f"uploaded_images/{style}-{x}.JPG"
        #     p.save()
        print("Done")

    def seed_shapes(self, key):
        print("Seeding shapes...")
        for s in settings.PIECE_SHAPES:
            if key != KEY_ALL and s['key'] != key:
                continue
            shape = Shape.objects.filter(key=s['key']).first()
            if not shape:
                shape = Shape(**s)
            print("Seeding shape", shape)
            shape.image = f"images/shapes/{shape.key}.png"
            shape.save()

    def seed_grid(self):
        print("Seeding grid cells...")
        for y, row in enumerate(settings.GRID):
            r = y + 1 # need 1-based
            for x, key in enumerate(row):
                c = x + 1 # need 1-based
                # If no rotation is specified, add it as 0 degrees
                if '+' not in key:
                    key = key + '+0'
                shape_key, turns = key.split('+')
                cell = Cell.objects.filter(r=r, c=c).first()
                if not cell:
                    cell = Cell(r=r, c=c)
                print("Seeding cell", cell)
                cell.shape = Shape.objects.filter(key=shape_key).first()
                cell.turns = int(turns)
                cell.save()
