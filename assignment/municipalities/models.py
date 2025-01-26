from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry

class Municipality(models.Model):
    name = models.CharField(max_length=255)
    geom = models.GeometryField()  # PostGIS geometry field

    def __str__(self):
        return self.name
    