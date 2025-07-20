import json
import re

# load original sitemap
with open('sitemap_products_1.json') as f:
    items = json.load(f)

output = []
for entry in items['urlset']['url']:
    try:
        url = entry['loc']
        img = entry['image']['loc']['__text']
        # extract the “P###” (or similar) model code from the image filename
        m = re.search(r'Cokin[-_]([A-Za-z\d]+?)[-_\.]', img)
        model = m.group(1) if m else None
        name = entry['image']['title']['__text']

        if model is None:
            print(f"Ignoring {name}")
            continue

        output.append({
            "url": url,
            "model": model,
            "name": name,
            "title": entry['image']['title']['__text'],
            "image_url": entry['image']['loc']['__text']
        })
    except:
        pass

# write out concise JSON
with open('cokin_products_concise.json', 'w') as f:
    json.dump(output, f, indent=2)
