from core.models import Cell, Piece, Shape
from django.contrib import admin
from image_cropping import ImageCroppingMixin


class ShapeAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('__str__', 'key', 'heads', 'image')

class CellAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('__str__', 'c', 'r', 'shape', 'turns')
    list_filter = ('c', 'r')
    ordering = ('r', 'c')

class PieceAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('__str__', 'shape', 'image', 'num', 'w', 'nw', 'n', 'ne', 'e', 'se', 's', 'sw')
    list_filter = ('shape', 'num')
    ordering = ('shape', 'num')

admin.site.register(Shape, ShapeAdmin)
admin.site.register(Cell, CellAdmin)
admin.site.register(Piece, PieceAdmin)
