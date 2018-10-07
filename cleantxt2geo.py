import sys
import re
from functools import partial

from shapely import ops
from shapely.geometry import Polygon, Point
from shapely.validation import explain_validity
from shapely_geojson import dumps, Feature, FeatureCollection
import pyproj

txt = open(sys.argv[1], 'r')

poly = None

check = re.compile(r'^([A-Z])?: ([0-9]{1,3})° ([0-5]?[0-9])\' ([0-5]?[0-9](,[0-9]{1,3})?)" ([EO]) / ([0-9]{1,2})° ([0-5]?[0-9])\' ([0-5]?[0-9](,[0-9]{1,3})?)" ([NS])( (.*)km)?$')  ## noqa


def dms2d(deg, min, sec, cardinal):
    degres = float(deg) + float(min)/60 + float(sec.replace(',', '.')) / 3600
    if cardinal in ['O', 'S']:
        return(-degres)
    else:
        return(degres)


def pts2feature(pts, nom):
    poly = []
    km = None
    for pt in pts:
        lon = dms2d(pt[1], pt[2], pt[3], pt[4])
        lat = dms2d(pt[5], pt[6], pt[7], pt[8])
        poly.append((lon, lat))
        km = pt[9]
    if km:
        # calcule un cercle en projection Lambert 93
        zone_local = ops.transform(
            partial(
                pyproj.transform,
                pyproj.Proj(init='EPSG:4326'),  # EPSG:4326 est WGS 84
                pyproj.Proj(init='EPSG:2154')
            ),
            Point(poly[0])
        ).buffer(float(km.replace(',', '.'))*1000, resolution=36)
        zone = ops.transform(
            partial(
                pyproj.transform,
                pyproj.Proj(init='EPSG:2154'),
                pyproj.Proj(init='EPSG:4326')  # EPSG:4326 est WGS 84
            ),
            zone_local
        )
        return(Feature(zone, {'nom': nom, 'distance': km}))
    else:
        valid = explain_validity(Polygon(poly))
        if valid != 'Valid Geometry':
            print('ERREUR:', nom, valid)
            exit()
        if Polygon(poly).area > 0.01 and nom not in ['CSG KOUROU 1']:
            print('ERREUR:', nom, 'emprise trop importante')
            exit()
        return(Feature(Polygon(poly), {'nom': nom}))


pts = []
nom = None
features = []

for ligne in txt:
    ligne = ligne[:-1]
    match = re.match(check, ligne)
    if match:
        pts.append(match.group(1, 2, 3, 4, 6, 7, 8, 9, 11, 13))
    else:
        if nom:
            features.append(pts2feature(pts, nom))
            nom = None
        if ligne != '':
            nom = ligne
            pts = []

if nom:
    features.append(pts2feature(pts, nom))

print(dumps(FeatureCollection(features)))
