from django.test import TestCase
from municipalities.models import Municipality
from django.contrib.gis.geos import Polygon, GeometryCollection
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class MunicipalityViewTestCase(TestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        try:
            user = User.objects.get(id=1)
        except:
            user = User.objects.create_user(username='test', password='test', email='test@test.com')
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}

    def setUp(self):
        def create_multipolygon(base):
            """returns a multipolygon based on a base coordinate"""
            poly = Polygon(((base, base), (base, base + 1), (base + 1, base + 1), (base, base)))
            poly_2 = Polygon(((base + 1, base + 1), (base + 1, base + 2), (base + 2, base + 2), (base + 1, base + 1)))
            gc = GeometryCollection(poly, poly_2)
            return gc
        
        gc = create_multipolygon(0)
        number_of_municipalities = 150
        for n in range(number_of_municipalities):
            Municipality.objects.create(name='Test 1', geom=gc)

        gc = create_multipolygon(4)
        Municipality.objects.create(name='Test 2', geom=gc)
        

    def test_jwt_authentication(self):
        # checks if authentication is required
        response = self.client.get('/api/municipalities/')
        self.assertNotEqual(response.status_code, 200)


    def test_pagination(self):
        # checks if pagination works
        page_size = 100
        response = self.client.get('/api/municipalities/', **self.bearer_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('features')), page_size)

    def test_in_bbox_filter(self):
        # filters a single feature
        bbox = '3,3,7,7'
        response = self.client.get(f'/api/municipalities/?in_bbox={bbox}', **self.bearer_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('features')), 1)

        # check if pagination works when filtering
        bbox = '-1,-1,3,3'
        response = self.client.get(f'/api/municipalities/?in_bbox={bbox}', **self.bearer_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('features')), 100)