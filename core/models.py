from django.db import models
from image_cropping.fields import ImageCropField, ImageRatioField
from model_utils.models import TimeStampedModel


class Shape(TimeStampedModel):
    """
    A generic puzzle piece with a particular shape, but no orientation or pattern.
    """
    key = models.CharField(null=False, blank=False, max_length=255, unique=True)
    name = models.CharField(null=False, blank=True, max_length=255)
    heads = models.IntegerField(null=True, blank=False, default=None)
    image = ImageCropField(null=False, blank=True, upload_to='shapes')

    def __str__(self) -> str:
        return self.name


class Piece(TimeStampedModel):
    """
    A physical puzzle piece that can be placed in the grid.
    """
    class Meta:
        ordering = ('shape', 'num')

    shape = models.ForeignKey(Shape, null=False, blank=False, on_delete=models.CASCADE)
    num = models.IntegerField(null=False, blank=False)
    image = ImageCropField(null=False, blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image', '500x500', free_crop=True, size_warning=True)
    w = models.CharField(null=False, blank=True, max_length=255)
    nw = models.CharField(null=False, blank=True, max_length=255)
    n = models.CharField(null=False, blank=True, max_length=255)
    ne = models.CharField(null=False, blank=True, max_length=255)
    e = models.CharField(null=False, blank=True, max_length=255)
    se = models.CharField(null=False, blank=True, max_length=255)
    s = models.CharField(null=False, blank=True, max_length=255)
    sw = models.CharField(null=False, blank=True, max_length=255)

    @property
    def cell(self):
        return self.cell_set.first()

    def save(self):
        super().save()
    
    def __str__(self) -> str:
        shape = self.shape
        shape_key = '?' if not shape else shape.key
        used_in = ''
        if cell := self.cell:
            used_in = f" ({cell.coords})"
        return f"{shape_key}-{self.num}{used_in}"

    def get_pattern(self, side):
        if (cell := self.cell) is None:
            return
        n = [self.n, self.w, self.s, self.e]
        e = [self.e, self.n, self.w, self.s]
        s = [self.s, self.e, self.n, self.w]
        w = [self.w, self.s, self.e, self.n]
        ne = [self.ne, self.nw, self.sw, self.se]
        se = [self.se, self.ne, self.nw, self.sw]
        sw = [self.sw, self.se, self.ne, self.nw]
        nw = [self.nw, self.sw, self.se, self.ne]
        turns = cell.turns
        haves = dict(
            n=n[turns],
            s=s[turns],
            e=e[turns],
            w=w[turns],
            ne=ne[turns],
            se=se[turns],
            sw=sw[turns],
            nw=nw[turns],
        )
        return haves[side]


class Cell(TimeStampedModel):
    """
    A specific space for a puzzle piece. May or may not be filled with an actual piece.
    """
    shape = models.ForeignKey(Shape, null=False, blank=False, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, null=True, blank=True, on_delete=models.CASCADE)
    turns = models.IntegerField(null=False, blank=True, default=0)
    c = models.IntegerField(null=False, blank=False)
    r = models.IntegerField(null=False, blank=False)

    @property
    def coords(self):
        return f"{self.c},{self.r}"
    
    def save(self):
        if not self.shape and self.piece:
            self.shape = self.piece.shape
        super().save()

    def clear(self):
        self.shape = self.piece = None
        self.turns = 0
        self.save()

    def __str__(self) -> str:
        return f"{self.coords} - {self.piece}"
