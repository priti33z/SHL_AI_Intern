import json
import pickle
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading SHL catalog...")

with open("catalog/shl_product_catalog.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)

documents = []

for assessment in catalog:

    text = f"""
    Name: {assessment.get("name","")}

    Description: {assessment.get("description","")}

    Job Levels: {" ".join(assessment.get("job_levels",[]))}

    Languages: {" ".join(assessment.get("languages",[]))}

    Duration: {assessment.get("duration","")}

    Categories: {" ".join(assessment.get("keys",[]))}

    Adaptive: {assessment.get("adaptive","")}

    Remote: {assessment.get("remote","")}
    """

    documents.append(text)

print("Creating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

os.makedirs("data", exist_ok=True)

faiss.write_index(index, "data/shl.index")

with open("data/catalog.pkl", "wb") as file:
    pickle.dump(catalog, file)

print("=====================================")
print("Index Created Successfully")
print("Total Assessments :", len(catalog))
print("=====================================")