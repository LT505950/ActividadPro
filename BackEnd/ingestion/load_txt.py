import os

def load_txt(folder_path: str) -> list[dict]:
    docs = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

                docs.append({
                    "text": text,
                    "source": file,
                    "path": path
                })

    return docs