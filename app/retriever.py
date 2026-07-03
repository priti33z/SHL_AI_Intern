import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Project root path
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folder path
DATA_DIR = BASE_DIR / "data"

INDEX_PATH = DATA_DIR / "shl.index"
CATALOG_PATH = DATA_DIR / "catalog.pkl"

print("Loading FAISS Index...")

index = faiss.read_index(str(INDEX_PATH))

with open(CATALOG_PATH, "rb") as file:
    catalog = pickle.load(file)


def search(query, top_k=5):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(catalog[idx])

    return results


# Test only when running this file directly
if __name__ == "__main__":

    while True:

        query = input("\nEnter Query : ")

        if query.lower() == "exit":
            break

        results = search(query)

        print("\nTop Recommendations\n")

        for assessment in results:

            print("=" * 60)
            print("Name :", assessment["name"])
            print("URL :", assessment["link"])
            print("Duration :", assessment["duration"])
            print("Job Levels :", ", ".join(assessment["job_levels"]))
            print("Categories :", ", ".join(assessment["keys"]))
            print("Description :", assessment["description"])