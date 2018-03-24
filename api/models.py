from django.db import models


"""
Model defining a package
.id - Unique identifier for package, auto generated on insert.
.description - Description of package.
"""
class Package(models.Model):
    description = models.CharField(max_length=140, blank=False)

    class Meta:
        ordering = ('id',)


"""
Status of a package
.created = Server time of the status update
.package = Foreign key relationship to package (package_id)
.latitude = Latitude of package to 8 decimal places
.longitude = Longitude of package to 8 decimal places
.elevation = Vertical elevation of package in metres to 3 decimal places (millimetre)
"""
class Status(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    elevation = models.DecimalField(max_digits=7, decimal_places=3)

    class Meta:
        ordering = ('package_id','created',)
