import json
import os
import random


class home_todo:
    def __init__(self, name, path="data/todos.json"):
        self.name = name
        self.path = path
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, items):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    def all(self):
        return self._load()

    def random_todo(self):
        items = self._load()
        if not items:
            return None
        return random.choice(items)

    def add(self, text):
        items = self._load()
        items.append(text.strip())
        self._save(items)

    def delete(self, index):
        items = self._load()
        if index < 0 or index >= len(items):
            return None
        removed = items.pop(index)
        self._save(items)
        return removed

    def format(self):
        item = self.random_todo()
        return item if item else "Список дел пуст"