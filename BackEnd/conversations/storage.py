import json
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent.parent / "test" / "conversations"

def save_conversation(conversation):
    BASE_PATH.mkdir(parents=True, exist_ok=True)

    path = BASE_PATH / f"{conversation.test_id}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(conversation.to_dict(), f, indent=2, ensure_ascii=False)

    return path