import base64
import csv
import io
import json
import os
import re
from collections import defaultdict

from core.models import Cell, Piece, Shape
from django.conf import settings
from django.core.management.base import BaseCommand

KEY_ALL = '__ALL__'

class Command(BaseCommand):
    help = "Outputs a JSON representation of the shape layout."

    def add_arguments(self, parser):
        parser.add_argument('--compact', action='store_true', help="Remove separator spaces from JSON data")
        parser.add_argument('--no-encode', action='store_true', help="Don't base-64 the output")

    def handle(self, *args, **options):
        data = defaultdict(list)
        for cell in Cell.objects.all():
            data[cell.r].append(f"{cell.shape.key}+{cell.turns}")
        
        grid = []
        for r in sorted(data.keys()):
            grid.append(data[r])
        
        output = json.dumps(grid, separators=(",", ":") if options['compact'] else (", ", ": "))
        if not options['no_encode']:
            json_bytes = output.encode('utf-8')
            output = base64.b64encode(json_bytes).decode('utf-8')
            print("Copy the data below into your .env file")
            print("-" * 80)
            print("GRID=", end='')
        print(output)
