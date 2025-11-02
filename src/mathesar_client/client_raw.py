from typing import Any, Dict, List, Optional
from requests import post
from os import environ
from urllib.parse import urljoin
from random import randint
from .client_raw_models import (
    OrderBy,
    Filter,
    Grouping,
    SearchParam,
    RecordList,
    RecordAdded,
    RecordSummaryList,
)


class MathesarClientError(Exception):
    pass


class MathesarClientRaw:
    def __init__(self, base_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.__base_url = base_url or environ['MATHESAR_BASE_URL']
        self.__username = username or environ['MATHESAR_USERNAME']
        self.__password = password or environ['MATHESAR_PASSWORD']
        self.__api_url = urljoin(self.__base_url, "api/rpc/v0/")

    def records_list(
        self,
        *,
        database_id: int,
        table_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[List[OrderBy]] = None,
        filter: Optional[Filter] = None,
        grouping: Optional[Grouping] = None,
        return_record_summaries: bool = False,
    ) -> RecordList:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "table_oid": table_id,
            "return_record_summaries": return_record_summaries,
        }
        if limit is not None:
            data["limit"] = limit
        if offset is not None:
            data["offset"] = offset
        if order is not None:
            data["order"] = [o.model_dump(mode="json") for o in order]
        if filter is not None:
            data["filter"] = filter.model_dump(mode="json")
        if grouping is not None:
            data["grouping"] = grouping.model_dump(mode="json")

        result = self._post("records.list", data)
        return RecordList.model_validate(result)

    def records_get(
        self,
        *,
        database_id: int,
        table_id: int,
        record_id: Any,
        return_record_summaries: bool = False,
        table_record_summary_templates: Optional[Dict[str, Any]] = None,
    ) -> RecordList:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "table_oid": table_id,
            "record_id": record_id,
            "return_record_summaries": return_record_summaries,
        }
        if table_record_summary_templates is not None:
            data["table_record_summary_templates"] = table_record_summary_templates
        result = self._post("records.get", data)
        return RecordList.model_validate(result)

    def records_add(
        self,
        *,
        database_id: int,
        table_id: int,
        record_def: Dict[str, Any],
        return_record_summaries: bool = False,
    ) -> RecordAdded:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "table_oid": table_id,
            "record_def": record_def,
            "return_record_summaries": return_record_summaries,
        }
        result = self._post("records.add", data)
        return RecordAdded.model_validate(result)

    def records_patch(
        self,
        *,
        database_id: int,
        table_id: int,
        record_id: Any,
        record_def: Dict[str, Any],
        return_record_summaries: bool = False,
    ) -> RecordAdded:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "table_oid": table_id,
            "record_id": record_id,
            "record_def": record_def,
            "return_record_summaries": return_record_summaries,
        }
        result = self._post("records.patch", data)
        return RecordAdded.model_validate(result)

    def records_delete(
        self,
        *,
        database_id: int,
        table_id: int,
        record_ids: List[Any],
    ) -> List[Any]:
        data = {
            "database_id": database_id,
            "table_oid": table_id,
            "record_ids": record_ids,
        }
        result = self._post("records.delete", data)
        return result

    def records_search(
        self,
        *,
        database_id: int,
        table_id: int,
        search_params: Optional[List[SearchParam]] = None,
        limit: int = 10,
        offset: int = 0,
        return_record_summaries: bool = False,
    ) -> RecordList:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "table_oid": table_id,
            "limit": limit,
            "offset": offset,
            "return_record_summaries": return_record_summaries,
        }
        if search_params is not None:
            data["search_params"] = [p.model_dump(mode="json") for p in search_params]
        result = self._post("records.search", data)
        return RecordList.model_validate(result)

    def records_list_summaries(
        self,
        *,
        database_id: int,
        table_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> RecordSummaryList:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "table_oid": table_id,
        }
        if limit is not None:
            data["limit"] = limit
        if offset is not None:
            data["offset"] = offset
        if search is not None:
            data["search"] = search
        result = self._post("records.list_summaries", data)
        return RecordSummaryList.model_validate(result)


    def _post(self, method: str, data: Dict[str, Any]) -> Any:
        response = post(
            self.__api_url,
            json={
                "id": randint(1, 1000),
                "jsonrpc": "2.0",
                "method": method,
                "params": data
            },
            auth=(self.__username, self.__password)
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise MathesarClientError(data["error"])

        return data["result"]
