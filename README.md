# Assignment Backend-developer at {COMPANY NAME}

This is an assignment for a technical job interview at a company that deals with geopositional data. The task is to use the Django Rest Framework to make operations with data having geographical features. GeoDjango allows to build GIS applications. 


### Data
Data consisting of 355 items with geographical features was shared in a geojson file. The data follows the [GEOJSON ](https://en.wikipedia.org/wiki/GeoJSON) standard. 

```
{
  "type": "FeatureCollection",
  "name": "municipalities_nl",
  "crs": { 
    "type": "name", 
    "properties": { 
      "name": "urn:ogc:def:crs:OGC:1.3:CRS84" 
    } 
  },
  "features": [
    { "type": "Feature", 
      "properties": 
        { "name": "Appingedam"}, 
      "geometry": { 
        "type": "MultiPolygon", 
        "coordinates": [ [ [ [ 6.885405186403255, 
        53.345128040081015 ] ....., ]]]
      }
    }
  ]
}
```

### Tasks
1. Create a CRUD REST API.
2. Limit the number of GEO feauters returned to 100 through pagination.
3. Filter items by a bounding box.
4. POST GEOJSON data with a python script.
5. Use JWT for authentication.
6. Implement appropiate tests.
7. TODO: Provide a Dockerfile and docker-compose.yml files for deployment. 

### Setup
1. Install Postgresql with postgis extension.
```
sudo apt install postgresql-17, postgresql-17-postgis-3, postgresql-server-dev-17

source venv/bin/activate  # initiate your environment if you haven't (see below)
```
2. Prepare python env
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install psycopg[binary]

```
2. Prepare DB - create the DB
```
sudo service postgresql status # to check status of your db server
sudo service postgresql start # to start the db server

createdb  <db name>

```
3. Prepare DB - install the extension and create db user

```
$ psql <db name>
> CREATE EXTENSION postgis;
> CREATE USER admin PASSWORD 'admin';
```
remember the `;` at the end of the extension creation!

4. Clone the repository.
```
git clone ...
```
5. Install the dependencies.
```

pip install -r requirements.txt
```
### Steps to Run locally
1. Navigate to the project directory. And run the migrations

```
cd assignment
python manage.py migrate
```
2. Create a user.
```
python manage.py createsuperuser --username admin --email admin@example.com
```

3. Run the server.
```
python manage.py runserver
```

4. Get refresh and access tokens
```
python manage.py shell

> from django.contrib.auth.models import User
> from rest_framework_simplejwt.tokens import RefreshToken
> user = User.objects.get(username='admin')
> refresh = RefreshToken.for_user(user)
> print(f'Refresh: {refresh.refresh}')
> print(f'Access: {refresh.access_token}')
```

5. Test the API.
Go to `http://127.0.0.1:8000/api/` in your browser or tool.

`http://127.0.0.1:8000/api/municipalities/?in_bbox=xmin,ymin,xmax,ymax`

Get new token by passing user and password and POST to `http://127.0.0.1:8000/api/token/`

Run tests with `python manage.py test`


### Upload data
``` 
cd assignment
python load_data.py
```


