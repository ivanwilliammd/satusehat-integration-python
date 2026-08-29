from datetime import datetime
from typing import Optional

from src.builder.base_builder import BaseBuilder


class BundleBuilder(BaseBuilder):
    TYPE_DOCUMENT = "document"
    TYPE_BATCH = "batch"
    TYPE_TRANSACTION = "transaction"
    TYPE_HISTORY_COLLECTION = "history-collection"
    TYPE_HISTORY_DOCUMENT = "history-document"
    TYPE_HISTORY_FEED = "history-feed"
    TYPE_SEARCHSET = "searchset"
    TYPE_COLLECTION = "collection"
    TYPE_FEED = "feed"
    TYPE_WRAPPER = "wrapper"

    VALID_TYPES = {
        "document": TYPE_DOCUMENT,
        "batch": TYPE_BATCH,
        "transaction": TYPE_TRANSACTION,
        "history-collection": TYPE_HISTORY_COLLECTION,
        "history-document": TYPE_HISTORY_DOCUMENT,
        "history-feed": TYPE_HISTORY_FEED,
        "searchset": TYPE_SEARCHSET,
        "collection": TYPE_COLLECTION,
        "feed": TYPE_FEED,
        "wrapper": TYPE_WRAPPER,
    }

    def __init__(self, bundle_type: Optional[str] = None):
        super().__init__("Bundle")
        self._timestamp_auto_set = True
        if bundle_type:
            self.set_type(bundle_type)
        if self._timestamp_auto_set:
            self.set_timestamp(datetime.utcnow().isoformat() + "Z")

    def set_type(self, bundle_type: str) -> "BundleBuilder":
        if bundle_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid Bundle type '{bundle_type}'. Valid: {', '.join(self.VALID_TYPES.keys())}")
        self.data["type"] = bundle_type
        return self

    def set_timestamp(self, timestamp: str) -> "BundleBuilder":
        self._timestamp_auto_set = False
        self.data["timestamp"] = timestamp
        return self

    def set_total(self, total: int) -> "BundleBuilder":
        self.data["total"] = total
        return self

    def set_meta(self, meta: dict) -> "BundleBuilder":
        self.data["meta"] = meta
        return self

    def set_id(self, id: str) -> "BundleBuilder":
        self.data["id"] = id
        return self

    def add_link(self, relation: str, url: str) -> "BundleBuilder":
        if "link" not in self.data:
            self.data["link"] = []
        self.data["link"].append({"relation": relation, "url": url})
        return self

    def add_entry(self, resource: dict, full_url: Optional[str] = None) -> "BundleBuilder":
        entry: dict = {"resource": resource}
        if full_url:
            entry["fullUrl"] = full_url
        if "entry" not in self.data:
            self.data["entry"] = []
        self.data["entry"].append(entry)
        return self

    def add_search_entry(
        self,
        resource: dict,
        full_url: Optional[str] = None,
        score: Optional[float] = None,
        search_mode: Optional[str] = None,
    ) -> "BundleBuilder":
        entry: dict = {"resource": resource}
        if full_url:
            entry["fullUrl"] = full_url
        search: dict = {}
        if search_mode:
            search["mode"] = search_mode
        if score is not None:
            search["score"] = score
        if search:
            entry["search"] = search
        if "entry" not in self.data:
            self.data["entry"] = []
        self.data["entry"].append(entry)
        return self

    def add_batch_entry(
        self,
        resource: Optional[dict],
        full_url: str,
        method: str,
        url: str,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        if_none_exist: Optional[str] = None,
    ) -> "BundleBuilder":
        request: dict = {"method": method, "url": url}
        if if_match:
            request["ifMatch"] = if_match
        if if_none_match:
            request["ifNoneMatch"] = if_none_match
        if if_none_exist:
            request["ifNoneExist"] = if_none_exist
        entry: dict = {"fullUrl": full_url, "request": request}
        if resource is not None:
            entry["resource"] = resource
        if "entry" not in self.data:
            self.data["entry"] = []
        self.data["entry"].append(entry)
        return self

    def add_transaction_entry(
        self,
        resource: Optional[dict],
        full_url: str,
        method: str,
        url: str,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        if_none_exist: Optional[str] = None,
    ) -> "BundleBuilder":
        self.set_type(self.TYPE_TRANSACTION)
        return self.add_batch_entry(resource, full_url, method, url, if_match, if_none_match, if_none_exist)

    def add_get_entry(self, full_url: str, url: str, if_none_match: Optional[str] = None) -> "BundleBuilder":
        return self.add_batch_entry(None, full_url, "GET", url, None, if_none_match)

    def add_delete_entry(self, full_url: str, url: str, if_match: Optional[str] = None) -> "BundleBuilder":
        return self.add_batch_entry(None, full_url, "DELETE", url, if_match)

    def validate(self) -> list:
        errors: list = []
        if "type" not in self.data:
            errors.append("Bundle.type is required")
        if "timestamp" not in self.data:
            errors.append("Bundle.timestamp is required")
        return errors
