import os
import re

from core.models import Piece, Shape
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Insert the pieces with their pictures."

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help="Overwrite existing data.")

    def handle(self, *args, **options):
        if Shape.objects.count() != len(settings.PIECE_SHAPES):
            raise CommandError("Run `seedgrid` first.")
        self.seed_pieces(options['force'])

    def seed_pieces(self, force):
        print("Seeding pieces...")
        for file in os.listdir(settings.UPLOADED_IMAGES_PATH):
            if re.match(r"^[^.]+\.([^.]+)$", file):
                shape_key, num = (file.split('.')[0]).split('-')
                shape = Shape.objects.get(key=shape_key)
                piece = Piece.objects.filter(shape__key=shape_key, num=num).first()
                if not piece:
                    piece = Piece(
                        shape=shape,
                        num=int(num),
                    )
                if force or not piece.pk:
                    piece.image = os.path.join(settings.UPLOADED_IMAGES_PATH, file)
                    print(f"Seeding piece {piece}")
                    piece.save()
        print("Done")
