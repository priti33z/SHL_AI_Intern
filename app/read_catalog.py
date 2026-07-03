import json
with open("catalog/shl_product_catalog.json","r",
          encoding="utf-8") as file :
    catalog = json.load(file)
print("Total Assessments:", len(catalog))

print("\nFirst Assessment:")
print(catalog[0])

print("\nFirst Assessment Name:")
print(catalog[0]["name"])