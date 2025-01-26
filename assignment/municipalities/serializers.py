from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Municipality

class MunicipalitySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Municipality
        geo_field = 'geom'
        fields = '__all__' # Or specify the fields you need
