from typing import Optional

from src.builder.base_builder import BaseBuilder


class ListBuilder(BaseBuilder):
    def __init__(self):
        super().__init__("List")

    def set_status(self, status: str) -> "ListBuilder":
        self.data["status"] = status
        return self

    def set_mode(self, mode: str) -> "ListBuilder":
        self.data["mode"] = mode
        return self

    def set_title(self, title: str) -> "ListBuilder":
        self.data["title"] = title
        return self

    def set_code(self, code: str) -> "ListBuilder":
        self.data["code"] = {"text": code}
        return self

    def set_subject(self, subject_ref: str) -> "ListBuilder":
        self.data["subject"] = {"reference": subject_ref}
        return self

    def set_encounter(self, enc_ref: str) -> "ListBuilder":
        self.data["encounter"] = {"reference": enc_ref}
        return self

    def set_date(self, date: str) -> "ListBuilder":
        self.data["date"] = date
        return self

    def set_source(self, source_ref: str) -> "ListBuilder":
        self.data["source"] = {"reference": source_ref}
        return self

    def add_entry(self, item_ref: str) -> "ListBuilder":
        if "entry" not in self.data:
            self.data["entry"] = []
        entry: dict = {}
        if item_ref:
            entry["item"] = {"reference": item_ref}
        self.data["entry"].append(entry)
        return self
