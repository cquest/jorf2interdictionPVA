# jorf2interdictionPVA

Scripts d'aide à l'extraction des données géographiques contenues dans les arrêtés publiés au JO listant les zones interdites à la prise de vue aérienne.

Le JO est disponible sous forme PDF, mais les tableaux contenant les limites géographiques y figure en format image.

Il est donc nécessaire de faire une passe d'OCR pour en extraire le plus de texte possible, puis de faire du nettoyage et reformatage du texte obtenu, avant de pouvoir générer un fichier exploitable au geojson.

Tout n'est malheureusement pas automatisé, une phase de correction et vérification manuelle est nécessaire, mais ces scripts permettent de les limiter et de détecter les principales erreurs.

## Fichiers finaux disponibles

### 2017-10.txt

C'est le fichier nettoyé servant à générer le geojson final.

**Si des erreurs sont à corriger dans les coordonnées des zones, c'est ce fichier qu'il faut modifier.** Vos pull-requests ou issues sont les bienvenues !

### 2017-10.geojson

Fichier geojson final, généré par:

`python cleantxt2geo.py 2017-10.txt > 2017-10.geojson`

## Conversion PDF > TIFF > txt

`bash jorf2txt.sh <lefichierpdf>`

Ce script utilise [imagemagick](https://imagemagick.org) pour convertir le PDF en pages uniques après cropping.

[Tesseract](https://tesseract-ocr.github.io/) est ensuite utilisé pour en extraire le texte.

## Nettoyage automatique du texte

`python txt2cleantxt.py <lefichier>`

Ce script python, détecte les lignes contenant des coordonnées géographiques et tente de les remettre sous une forme homogène cohérente.

Les lignes ne pouvant être remises en cohérence dans leur intégralité sont précédées par "ERR", celles remise en cohérence sont modifiées et celles ne contenant pas de coordonnées géographiques sont laissées intactes.

## Nettoyage manuel du texte

Cette phase doit éliminer toutes les lignes de bruit et corriger les lignes de coordonnées avec 'ERR'.

Au final on doit avoir pour chaque site des lignes sour la forme suivante:

```
CIVAUX
A: 000° 39' 13" E / 46° 27' 47" N
B: 000° 39' 49" E / 46° 26' 53" N
```

Pour les sites dont la zone est définit par un cercle autour d'une coordonnée, on utilise:

```
MUNEVILLE LE BINGARD
Z: 001° 30' 16" O / 49° 08' 58" N 0,5km
```

**txt2cleantxt.py** peut être utilisé autant de fois que nécessaire pour cette remise en forme.

## Contrôle et conversion geojson

`python cleantxt2geo.py <lefichier>`

Si des erreurs ou incohérences sont encore détectées, elle sortiront en "ERREUR", sinon un geojson global sera produit.
