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


# Analytics


class AnalyticsState(BaseModel):
    enabled: bool


class AnalyticsReport(BaseModel):
    installation_id: Optional[str]
    mathesar_version: str
    user_count: int
    active_user_count: int
    configured_role_count: int
    connected_database_count: int
    connected_database_schema_count: int
    connected_database_table_count: int
    connected_database_record_count: int
    exploration_count: int
    form_count: int
    public_form_count: int


# Collaborators


class CollaboratorInfo(BaseModel):
    id: int
    user_id: int
    database_id: int
    configured_role_id: int


# Columns


class TypeOptions(BaseModel):
    precision: Optional[int] = None
    scale: Optional[int] = None
    fields: Optional[str] = None
    length: Optional[int] = None
    item_type: Optional[str] = None


class ColumnDefault(BaseModel):
    value: str
    is_dynamic: bool


class ColumnInfo(BaseModel):
    id: int
    name: str
    type: str
    type_options: Optional[TypeOptions] = None
    nullable: bool
    primary_key: bool
    default: Optional[ColumnDefault] = None
    has_dependents: bool
    description: Optional[str] = None
    current_role_priv: List[Literal['SELECT', 'INSERT', 'UPDATE', 'REFERENCES']]


class CreatablePkColumnInfo(BaseModel):
    name: Optional[str] = None
    type: Optional[Literal['IDENTITY', 'UUIDv4']] = None


class CreatableColumnInfo(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    type_options: Optional[TypeOptions] = None
    nullable: Optional[bool] = None
    default: Optional[ColumnDefault] = None
    description: Optional[str] = None


class SettableColumnInfo(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    cast_options: Optional[Dict[str, Any]] = None
    type_options: Optional[TypeOptions] = None
    nullable: Optional[bool] = None
    default: Optional[ColumnDefault] = None
    description: Optional[str] = None


class ColumnMetaDataBlob(BaseModel):
    attnum: int
    bool_input: Optional[Literal['dropdown', 'checkbox']] = None
    bool_true: Optional[str] = None
    bool_false: Optional[str] = None
    num_min_frac_digits: Optional[int] = None
    num_max_frac_digits: Optional[int] = None
    num_grouping: Optional[str] = None
    num_format: Optional[str] = None
    mon_currency_symbol: Optional[str] = None
    mon_currency_location: Optional[Literal['after-minus', 'end-with-space']] = None
    time_format: Optional[str] = None
    date_format: Optional[str] = None
    duration_min: Optional[str] = None
    duration_max: Optional[str] = None
    display_width: Optional[int] = None
    file_backend: Optional[int] = None


class ColumnMetaDataRecord(BaseModel):
    database_id: int
    table_oid: int
    attnum: int
    bool_input: Optional[Literal['dropdown', 'checkbox']] = None
    bool_true: Optional[str] = None
    bool_false: Optional[str] = None
    num_min_frac_digits: Optional[int] = None
    num_max_frac_digits: Optional[int] = None
    num_grouping: Optional[str] = None
    num_format: Optional[str] = None
    mon_currency_symbol: Optional[str] = None
    mon_currency_location: Optional[Literal['after-minus', 'end-with-space']] = None
    time_format: Optional[str] = None
    date_format: Optional[str] = None
    duration_min: Optional[str] = None
    duration_max: Optional[str] = None
    display_width: Optional[int] = None
    file_backend: Optional[int] = None


# Configured Databases


class ConfiguredDatabaseInfo(BaseModel):
    id: int
    name: str
    server_id: int
    last_confirmed_sql_version: str
    needs_upgrade_attention: bool
    nickname: Optional[str] = None


class ConfiguredDatabasePatch(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None


# Constraints


class ForeignKeyConstraint(BaseModel):
    type: str
    columns: List[int]
    fkey_relation_id: int
    fkey_columns: List[int]
    name: Optional[str] = None
    deferrable: Optional[bool] = None
    fkey_update_action: Optional[str] = None
    fkey_delete_action: Optional[str] = None
    fkey_match_type: Optional[str] = None


class PrimaryKeyConstraint(BaseModel):
    type: str
    columns: List[int]
    name: Optional[str] = None
    deferrable: Optional[bool] = None


class UniqueConstraint(BaseModel):
    type: str
    columns: List[int]
    name: Optional[str] = None
    deferrable: Optional[bool] = None


CreatableConstraintInfo = List[Union[ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint]]


class ConstraintInfo(BaseModel):
    # Accept unknown fields from server response
    # Pydantic v2: use ConfigDict to allow extra
    model_config = dict(extra='allow')


# Data Modeling


class MappingColumn(BaseModel):
    column_name: str
    referent_table_oid: int


class SplitTableInfo(BaseModel):
    extracted_table_oid: int
    new_fkey_attnum: int


# Databases and privileges


class DatabaseInfo(BaseModel):
    oid: int
    name: str
    owner_oid: int
    current_role_priv: List[Literal['CONNECT', 'CREATE', 'TEMPORARY']]
    current_role_owns: bool


class DBPrivileges(BaseModel):
    role_oid: int
    direct: List[Literal['CONNECT', 'CREATE', 'TEMPORARY']]


# Database setup


class ConfiguredServerInfo(BaseModel):
    id: int
    host: str | None = None
    port: int | None = None


class ConfiguredRoleInfo(BaseModel):
    id: int
    name: str
    server_id: int


class DatabaseConnectionResult(BaseModel):
    server: ConfiguredServerInfo
    database: ConfiguredDatabaseInfo
    configured_role: ConfiguredRoleInfo


# Explorations


class ExplorationInfo(BaseModel):
    id: int
    database_id: int
    name: str
    base_table_oid: int
    schema_oid: int
    initial_columns: List[Any]
    transformations: Optional[List[Any]] = None
    display_options: Optional[List[Any]] = None
    display_names: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ExplorationDef(BaseModel):
    database_id: int
    name: str
    base_table_oid: int
    schema_oid: int
    initial_columns: List[Any]
    transformations: Optional[List[Any]] = None
    display_options: Optional[List[Any]] = None
    display_names: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ExplorationResult(BaseModel):
    query: Dict[str, Any]
    records: Dict[str, Any]
    output_columns: Tuple[Any, ...]
    column_metadata: Dict[str, Any]
    limit: Optional[int] = None
    offset: Optional[int] = None


# Forms


class FieldInfo(BaseModel):
    id: int
    key: str
    form_id: int
    index: int
    label: Optional[str] = None
    help: Optional[str] = None
    kind: Literal['scalar_column', 'foreign_key']
    column_attnum: Optional[int] = None
    related_table_oid: Optional[int] = None
    fk_interaction_rule: Literal['must_pick', 'can_pick_or_create', 'must_create']
    parent_field_id: Optional[int] = None
    styling: Optional[Dict[str, Any]] = None
    is_required: bool
    child_fields: Optional[List['FieldInfo']] = None


FieldInfo.model_rebuild()


class FormInfo(BaseModel):
    id: int
    created_at: str
    updated_at: str
    token: str
    name: str
    description: Optional[str] = None
    version: int
    database_id: int
    schema_oid: int
    base_table_oid: int
    associated_role_id: Optional[int] = None
    header_title: Dict[str, Any]
    header_subtitle: Optional[Dict[str, Any]] = None
    publish_public: bool
    submit_message: Optional[Dict[str, Any]] = None
    submit_redirect_url: Optional[str] = None
    submit_button_label: Optional[str] = None
    fields: List[FieldInfo]


class AddOrReplaceFieldDef(BaseModel):
    key: str
    index: int
    label: Optional[str] = None
    help: Optional[str] = None
    kind: Literal['scalar_column', 'foreign_key']
    column_attnum: Optional[int] = None
    related_table_oid: Optional[int] = None
    fk_interaction_rule: Literal['must_pick', 'can_pick_or_create', 'must_create']
    styling: Optional[Dict[str, Any]] = None
    is_required: Optional[bool] = None
    child_fields: Optional[List['AddOrReplaceFieldDef']] = None


AddOrReplaceFieldDef.model_rebuild()


class AddFormDef(BaseModel):
    name: str
    description: Optional[str] = None
    version: int
    database_id: int
    schema_oid: int
    base_table_oid: int
    associated_role_id: Optional[int] = None
    header_title: Dict[str, Any]
    header_subtitle: Optional[Dict[str, Any]] = None
    submit_message: Optional[Dict[str, Any]] = None
    submit_redirect_url: Optional[str] = None
    submit_button_label: Optional[str] = None
    fields: List[AddOrReplaceFieldDef]


class SettableFormDef(AddFormDef):
    id: int
    version: int


# Roles and configured roles


class RoleMember(BaseModel):
    oid: int
    admin: bool


class RoleInfo(BaseModel):
    oid: int
    name: str
    super: bool
    inherits: bool
    create_role: bool
    create_db: bool
    login: bool
    description: Optional[str] = None
    members: Optional[List[RoleMember]] = None


# Schemas and privileges


class SchemaInfo(BaseModel):
    oid: int
    name: str
    description: Optional[str] = None
    owner_oid: int
    current_role_priv: List[Literal['USAGE', 'CREATE']]
    current_role_owns: bool
    table_count: int


class SchemaPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SchemaPrivileges(BaseModel):
    role_oid: int
    direct: List[Literal['USAGE', 'CREATE']]


# Tables and metadata and privileges


class TableInfo(BaseModel):
    oid: int
    name: str
    schema: int
    description: Optional[str] = None
    owner_oid: int
    current_role_priv: List[Literal['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE', 'REFERENCES', 'TRIGGER']]
    current_role_owns: bool


class AddedTableInfo(BaseModel):
    oid: int
    name: str
    renamed_columns: Optional[Dict[str, Any]] = None


class SettableTableInfo(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    columns: Optional[List[SettableColumnInfo]] = None


class JoinableTableRecord(BaseModel):
    base: int
    target: int
    join_path: List[Any]
    fkey_path: List[Any]
    depth: int
    multiple_results: bool


class JoinableTableInfo(BaseModel):
    joinable_tables: List[JoinableTableRecord]
    target_table_info: List[Any]


class TableMetaDataBlob(BaseModel):
    data_file_id: Optional[int] = None
    import_verified: Optional[bool] = None
    column_order: Optional[List[int]] = None
    record_summary_template: Optional[Dict[str, Union[str, List[int]]]] = None
    mathesar_added_pkey_attnum: Optional[int] = None


class TableMetaDataRecord(BaseModel):
    id: int
    database_id: int
    table_oid: int
    data_file_id: Optional[int] = None
    import_verified: Optional[bool] = None
    column_order: Optional[List[int]] = None
    record_summary_template: Optional[Dict[str, Union[str, List[int]]]] = None
    mathesar_added_pkey_attnum: Optional[int] = None


class TablePrivileges(BaseModel):
    role_oid: int
    direct: List[Literal['INSERT', 'SELECT', 'UPDATE', 'DELETE', 'TRUNCATE', 'REFERENCES', 'TRIGGER']]


# Users


class UserInfo(BaseModel):
    id: int
    username: str
    is_superuser: bool
    email: str
    full_name: str
    display_language: str


class UserDef(BaseModel):
    username: str
    password: str
    is_superuser: bool
    email: Optional[str] = None
    full_name: Optional[str] = None
    display_language: Optional[str] = None
