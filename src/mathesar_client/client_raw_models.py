from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Field


# Records models


class OrderBy(BaseModel):
    attnum: int
    direction: Literal["asc", "desc"]


class FilterAttnum(BaseModel):
    type: Literal["attnum"] = Field(default="attnum")
    value: int


class FilterLiteral(BaseModel):
    type: Literal["literal"] = Field(default="literal")
    value: Any


class _Filter(BaseModel):
    type: str
    args: List[Union["_Filter", FilterAttnum, FilterLiteral]]


# Expose Filter as alias to the recursive model
Filter = _Filter

# Rebuild for self-referencing types
_Filter.model_rebuild()


class Grouping(BaseModel):
    columns: List[int]
    preproc: Optional[List[str]] = None


class Group(BaseModel):
    id: int
    count: int
    results_eq: List[Dict[str, Any]]
    result_indices: List[int]


class GroupingResponse(BaseModel):
    columns: List[int]
    preproc: Optional[List[str]] = None
    groups: List[Group]


class SearchParam(BaseModel):
    attnum: int
    literal: Any


RecordObject = Dict[str, Any]


class RecordList(BaseModel):
    count: int
    results: List[RecordObject]
    grouping: Optional[GroupingResponse] = None
    linked_record_smmaries: Optional[Dict[str, Any]] = None
    record_summaries: Optional[Dict[str, str]] = None
    download_links: Optional[Dict[str, Any]] = None


class RecordAdded(BaseModel):
    results: List[RecordObject]
    linked_record_summaries: Optional[Dict[str, Dict[str, str]]] = None
    record_summaries: Optional[Dict[str, str]] = None


class SummarizedRecordReference(BaseModel):
    key: Any
    summary: str


class RecordSummaryList(BaseModel):
    count: int
    results: List[SummarizedRecordReference]
