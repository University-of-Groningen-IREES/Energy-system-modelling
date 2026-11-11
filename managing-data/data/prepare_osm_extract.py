"""Refresh a small classroom OSM extract. Existing output will be replaced.

Data: © OpenStreetMap contributors, ODbL.
https://www.openstreetmap.org/copyright
Run only when a new class snapshot is needed, not once per student.
Requires osmnx (which depends on requests).
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import hashlib
from datetime import datetime, timezone
import requests
import osmnx as ox

output = Path(__file__).resolve().parent
bbox = '6.563,53.218,6.571,53.222'
url = 'https://api.openstreetmap.org/api/0.6/map'
response = requests.get(url, params={'bbox': bbox}, timeout=60,
                        headers={'User-Agent': 'RenewableEnergyTeaching/1.0'})
response.raise_for_status()
with TemporaryDirectory() as tmp:
    source = Path(tmp) / 'groningen.osm'
    source.write_bytes(response.content)
    raw = ox.features_from_xml(source, tags={'building': True})
    buildings = raw.loc[
        raw.geometry.notna() & ~raw.geometry.is_empty
        & raw.geometry.is_valid
        & raw.geom_type.isin(['Polygon', 'MultiPolygon'])
    ].copy()
    buildings['osm_id'] = [f'{kind}/{ident}' for kind, ident in buildings.index]
    buildings = buildings.reset_index(drop=True)
    for col in ['building', 'name', 'building:levels']:
        if col not in buildings:
            buildings[col] = None
        buildings[col] = buildings[col].map(
            lambda value: str(value) if value is not None and not isinstance(value, float) else None)
    columns = ['osm_id', 'building', 'name', 'building:levels', 'geometry']
    buildings[columns].to_file(output / 'groningen-centre-buildings.geojson',
                               driver='GeoJSON', index=False)
metadata = {
    'retrieved_utc': datetime.now(timezone.utc).isoformat(),
    'source_url': response.url,
    'raw_xml_sha256': hashlib.sha256(response.content).hexdigest(),
    'osmnx_version': ox.__version__,
    'mapped_polygon_elements': len(buildings),
    'licence': 'ODbL-1.0',
    'attribution': '© OpenStreetMap contributors',
}
(output / 'retrieval-metadata.json').write_text(json.dumps(metadata, indent=2))
print(f'Wrote {len(buildings)} mapped polygon elements. Record the new date in the lesson.')
