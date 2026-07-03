import json

with open("catalog/shl_product_catalog.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)

def search_assessment(query):

    found = False

    for assessment in catalog:

        name = assessment.get("name","")
        description = assessment.get("description","")
        url = assessment.get("url","")

        text = name + " " + description

        if query.lower() in text.lower():

            print("Assessment :", name)
            print("URL :", url)
            print("----------------")

            found = True

    if not found:
        print("No assessment found.")

query = input("Enter skill : ")

search_assessment(query)