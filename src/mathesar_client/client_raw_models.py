"""Pydantic models mirroring Mathesar API TypedDicts.

This module contains all data models used by the Mathesar JSON-RPC API,
organized by functional area (records, analytics, columns, tables, etc.).
All models use Pydantic v2 for validation and serialization.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Field


# Records models


class OrderBy(BaseModel):
    """Specifies ordering for record queries.
    
    Attributes:
        attnum: Column attribute number to order by.
        direction: Sort direction, either "asc" or "desc".
    """
    attnum: int
    direction: Literal["asc", "desc"]


class FilterAttnum(BaseModel):
    """Filter referencing a column by its attribute number.
    
    Attributes:
        type: Literal "attnum" identifying this filter type.
        value: Column attribute number to filter.
    """
    type: Literal["attnum"] = Field(default="attnum")
    value: int


class FilterLiteral(BaseModel):
    """Filter using a literal value.
    
    Attributes:
        type: Literal "literal" identifying this filter type.
        value: Literal value to use in the filter.
    """
    type: Literal["literal"] = Field(default="literal")
    value: Any


class _Filter(BaseModel):
    """Recursive filter structure for complex query conditions.
    
    Attributes:
        type: Filter operation type (e.g., "and", "or", "equal").
        args: Arguments to the filter, which can be nested filters or values.
    """
    type: str
    args: List[Union["_Filter", FilterAttnum, FilterLiteral]]


# Expose Filter as alias to the recursive model
Filter = _Filter

# Rebuild for self-referencing types
_Filter.model_rebuild()


class Grouping(BaseModel):
    """Specifies grouping for record queries.
    
    Attributes:
        columns: List of column attribute numbers to group by.
        preproc: Optional preprocessing operations to apply.
    """
    columns: List[int]
    preproc: Optional[List[str]] = None


class Group(BaseModel):
    """A single group in a grouping response.
    
    Attributes:
        id: Unique identifier for this group.
        count: Number of records in this group.
        results_eq: Values that define this group.
        result_indices: Indices of records belonging to this group.
    """
    id: int
    count: int
    results_eq: List[Dict[str, Any]]
    result_indices: List[int]


class GroupingResponse(BaseModel):
    """Response containing grouped query results.
    
    Attributes:
        columns: Columns used for grouping.
        preproc: Preprocessing applied.
        groups: List of individual groups.
    """
    columns: List[int]
    preproc: Optional[List[str]] = None
    groups: List[Group]


class SearchParam(BaseModel):
    """Search parameter for text search queries.
    
    Attributes:
        attnum: Column attribute number to search in.
        literal: Search term or value.
    """
    attnum: int
    literal: Any


RecordObject = Dict[str, Any]


class RecordList(BaseModel):
    """List of records returned from a query.
    
    Attributes:
        count: Total number of records matching the query.
        results: List of record objects (dicts with column attnums as keys).
        grouping: Optional grouping information if query was grouped.
        linked_record_summaries: Summaries of linked records by row and column.
        record_summaries: Summaries for records in this result set.
        download_links: Optional download links for file columns.
    """
    count: int
    results: List[RecordObject]
    grouping: Optional[GroupingResponse] = None
    linked_record_summaries: Optional[Dict[str, Dict[str, str]]] = None
    record_summaries: Optional[Dict[str, str]] = None
    download_links: Optional[Dict[str, Any]] = None


class RecordAdded(BaseModel):
    """Response after adding or updating a record.
    
    Attributes:
        results: The added/updated record(s).
        linked_record_summaries: Summaries of linked records.
        record_summaries: Summaries for the returned records.
    """
    results: List[RecordObject]
    linked_record_summaries: Optional[Dict[str, Dict[str, str]]] = None
    record_summaries: Optional[Dict[str, str]] = None


class SummarizedRecordReference(BaseModel):
    """A reference to a record with its display summary.
    
    Attributes:
        key: Primary key or identifier of the referenced record.
        summary: Human-readable summary/display text for the record.
    """
    key: Any
    summary: str


class RecordSummaryList(BaseModel):
    """List of summarized record references.
    
    Attributes:
        count: Total number of summaries.
        results: List of summarized record references.
    """
    count: int
    results: List[SummarizedRecordReference]


# Analytics


class AnalyticsState(BaseModel):
    """Current state of analytics collection.
    
    Attributes:
        enabled: Whether analytics are currently enabled.
    """
    enabled: bool


class AnalyticsReport(BaseModel):
    """Analytics report containing usage statistics.
    
    Attributes:
        installation_id: Unique identifier for this installation.
        mathesar_version: Version of Mathesar running.
        user_count: Total number of users.
        active_user_count: Number of active users.
        configured_role_count: Number of configured database roles.
        connected_database_count: Number of connected databases.
    """
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
    """Information about a database collaborator.
    
    Attributes:
        id: Unique identifier for this collaborator relationship.
        user_id: ID of the user who is a collaborator.
        database_id: ID of the database they have access to.
        configured_role_id: ID of the database role assigned to them.
    """
    id: int
    user_id: int
    database_id: int
    configured_role_id: int


# Columns


class TypeOptions(BaseModel):
    """Options for configuring column data types.
    
    Attributes:
        precision: Numeric precision.
        scale: Numeric scale (decimal places).
        fields: Date/time fields specification.
        length: Character length limit.
        item_type: Type of items in array columns.
    """
    precision: Optional[int] = None
    scale: Optional[int] = None
    fields: Optional[str] = None
    length: Optional[int] = None
    item_type: Optional[str] = None


class ColumnDefault(BaseModel):
    """Default value configuration for a column.
    
    Attributes:
        value: The default value expression.
        is_dynamic: Whether the default is dynamic (e.g., NOW()).
    """
    value: str
    is_dynamic: bool


class ColumnInfo(BaseModel):
    """Complete information about a table column.
    
    Attributes:
        id: Column attribute number (attnum).
        name: Column name.
        type: Column data type.
        type_options: Type-specific configuration options.
        nullable: Whether the column accepts NULL values.
        primary_key: Whether this column is part of the primary key.
        default: Default value configuration.
        has_dependents: Whether other objects depend on this column.
        description: Optional column description/comment.
        current_role_priv: Privileges the current role has on this column.
    """
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
    """Configuration for creating a primary key column.
    
    Attributes:
        name: Optional name for the primary key column (default: 'id').
        type: Type of primary key: 'IDENTITY' (serial) or 'UUIDv4'.
    """
    name: Optional[str] = None
    type: Optional[Literal['IDENTITY', 'UUIDv4']] = None


class CreatableColumnInfo(BaseModel):
    """Configuration for creating a new column.
    
    Attributes:
        name: Column name.
        type: Column data type.
        type_options: Type-specific configuration options.
        nullable: Whether to allow NULL values.
        default: Default value configuration.
        description: Optional column description.
    """
    name: Optional[str] = None
    type: Optional[str] = None
    type_options: Optional[TypeOptions] = None
    nullable: Optional[bool] = None
    default: Optional[ColumnDefault] = None
    description: Optional[str] = None


class SettableColumnInfo(BaseModel):
    """Configuration for updating an existing column.
    
    Attributes:
        id: Column attribute number (attnum) to update.
        name: New column name.
        type: New column data type.
        cast_options: Options for type casting during the change.
        type_options: Type-specific configuration options.
        nullable: Whether to allow NULL values.
        default: Default value configuration.
        description: Column description.
    """
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    cast_options: Optional[Dict[str, Any]] = None
    type_options: Optional[TypeOptions] = None
    nullable: Optional[bool] = None
    default: Optional[ColumnDefault] = None
    description: Optional[str] = None


class ColumnMetaDataBlob(BaseModel):
    """Metadata for customizing column display and behavior.
    
    Attributes:
        attnum: Column attribute number this metadata applies to.
        bool_input: UI widget for boolean columns.
        bool_true: Display text for true values.
        bool_false: Display text for false values.
        num_min_frac_digits: Minimum fractional digits for numbers.
        num_max_frac_digits: Maximum fractional digits for numbers.
        num_grouping: Digit grouping style (e.g., thousands separator).
        num_format: Number format template.
        mon_currency_symbol: Currency symbol for monetary columns.
        mon_currency_location: Where to place currency symbol.
        time_format: Time display format.
        date_format: Date display format.
        duration_min: Minimum unit for duration columns.
        duration_max: Maximum unit for duration columns.
        display_width: Display width hint for UI.
        file_backend: Backend ID for file storage columns.
    """
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
    """Stored column metadata record including database/table identifiers.
    
    Inherits all attributes from ColumnMetaDataBlob plus:
        database_id: Database this column belongs to.
        table_oid: Table OID this column belongs to.
        attnum: Column attribute number.
    """
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
    """Information about a database configured in Mathesar.
    
    Attributes:
        id: Unique identifier for this configured database.
        name: Database name.
        server_id: ID of the server hosting this database.
        last_confirmed_sql_version: Last confirmed PostgreSQL version.
        needs_upgrade_attention: Whether the database needs upgrade attention.
        nickname: Optional user-friendly nickname for the database.
    """
    id: int
    name: str
    server_id: int
    last_confirmed_sql_version: str
    needs_upgrade_attention: bool
    nickname: Optional[str] = None


class ConfiguredDatabasePatch(BaseModel):
    """Fields that can be updated on a configured database.
    
    Attributes:
        name: New database name.
        nickname: New user-friendly nickname.
    """
    name: Optional[str] = None
    nickname: Optional[str] = None


# Constraints


class ForeignKeyConstraint(BaseModel):
    """Foreign key constraint definition.
    
    Attributes:
        type: Constraint type identifier (usually 'f' for foreign key).
        columns: Column attnums in this table participating in the FK.
        fkey_relation_id: OID of the referenced table.
        fkey_columns: Column attnums in the referenced table.
        name: Optional constraint name.
        deferrable: Whether the constraint can be deferred.
        fkey_update_action: Action on UPDATE (e.g., CASCADE, SET NULL).
        fkey_delete_action: Action on DELETE (e.g., CASCADE, SET NULL).
        fkey_match_type: Match type (FULL, PARTIAL, SIMPLE).
    """
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
    """Primary key constraint definition.
    
    Attributes:
        type: Constraint type identifier (usually 'p' for primary key).
        columns: Column attnums participating in the primary key.
        name: Optional constraint name.
        deferrable: Whether the constraint can be deferred.
    """
    type: str
    columns: List[int]
    name: Optional[str] = None
    deferrable: Optional[bool] = None


class UniqueConstraint(BaseModel):
    """Unique constraint definition.
    
    Attributes:
        type: Constraint type identifier (usually 'u' for unique).
        columns: Column attnums that must be unique together.
        name: Optional constraint name.
        deferrable: Whether the constraint can be deferred.
    """
    type: str
    columns: List[int]
    name: Optional[str] = None
    deferrable: Optional[bool] = None


CreatableConstraintInfo = List[Union[ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint]]


class ConstraintInfo(BaseModel):
    """Generic constraint information from the database.
    
    Accepts any fields returned by the server.
    """
    # Accept unknown fields from server response
    # Pydantic v2: use ConfigDict to allow extra
    model_config = dict(extra='allow')


# Data Modeling


class MappingColumn(BaseModel):
    """Column specification for creating a mapping table.
    
    Attributes:
        column_name: Name for the foreign key column.
        referent_table_oid: OID of the table this column references.
    """
    column_name: str
    referent_table_oid: int


class SplitTableInfo(BaseModel):
    """Information about a table split operation result.
    
    Attributes:
        extracted_table_oid: OID of the newly created extracted table.
        new_fkey_attnum: Attnum of the new foreign key column created.
    """
    extracted_table_oid: int
    new_fkey_attnum: int


# Databases and privileges


class DatabaseInfo(BaseModel):
    """Information about a PostgreSQL database.
    
    Attributes:
        oid: Database OID in PostgreSQL.
        name: Database name.
        owner_oid: OID of the database owner role.
        current_role_priv: Privileges the current role has on this database.
        current_role_owns: Whether the current role owns this database.
    """
    oid: int
    name: str
    owner_oid: int
    current_role_priv: List[Literal['CONNECT', 'CREATE', 'TEMPORARY']]
    current_role_owns: bool


class DBPrivileges(BaseModel):
    """Privileges for a specific role on a database.
    
    Attributes:
        role_oid: OID of the role these privileges apply to.
        direct: List of direct privileges granted to this role.
    """
    role_oid: int
    direct: List[Literal['CONNECT', 'CREATE', 'TEMPORARY']]


# Database setup


class ConfiguredServerInfo(BaseModel):
    """Information about a configured PostgreSQL server.
    
    Attributes:
        id: Unique identifier for this server configuration.
        host: Server hostname or IP address.
        port: Server port number.
    """
    id: int
    host: str | None = None
    port: int | None = None


class ConfiguredRoleInfo(BaseModel):
    """Information about a configured database role.
    
    Attributes:
        id: Unique identifier for this role configuration.
        name: Role name in PostgreSQL.
        server_id: ID of the server this role is configured for.
    """
    id: int
    name: str
    server_id: int


class DatabaseConnectionResult(BaseModel):
    """Result of connecting or creating a database.
    
    Attributes:
        server: Information about the connected server.
        database: Information about the connected/created database.
        configured_role: Role used for the connection.
    """
    server: ConfiguredServerInfo
    database: ConfiguredDatabaseInfo
    configured_role: ConfiguredRoleInfo


# Explorations


class ExplorationInfo(BaseModel):
    """Information about a saved exploration (query).
    
    Attributes:
        id: Unique identifier for this exploration.
        database_id: Database containing this exploration.
        name: Exploration name.
        base_table_oid: OID of the base table for this exploration.
        schema_oid: Schema OID containing the base table.
        initial_columns: Initial columns selected in the exploration.
        transformations: Query transformations applied.
        display_options: Display formatting options.
        display_names: Custom display names for columns.
        description: Optional description of this exploration.
    """
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
    """Definition for creating or running an exploration.
    
    Attributes:
        database_id: Database to query.
        name: Exploration name.
        base_table_oid: OID of the base table.
        schema_oid: Schema OID containing the base table.
        initial_columns: Initial columns to select.
        transformations: Query transformations to apply.
        display_options: Display formatting options.
        display_names: Custom display names for columns.
        description: Optional description.
    """
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
    """Result of running an exploration query.
    
    Attributes:
        query: The executed query details.
        records: The resulting records.
        output_columns: Tuple of output column definitions.
        column_metadata: Metadata about the columns.
        limit: Optional limit applied to results.
        offset: Optional offset applied to results.
    """
    query: Dict[str, Any]
    records: Dict[str, Any]
    output_columns: Tuple[Any, ...]
    column_metadata: Dict[str, Any]
    limit: Optional[int] = None
    offset: Optional[int] = None


# Forms


class FieldInfo(BaseModel):
    """Information about a form field.
    
    Attributes:
        id: Unique identifier for this field.
        key: Field key for referencing in submissions.
        form_id: ID of the form this field belongs to.
        index: Display order index of this field.
        label: Display label for the field.
        help: Help text for the field.
        kind: Field type (scalar_column or foreign_key).
        column_attnum: Column attnum if this is a scalar column field.
        related_table_oid: Related table OID if this is a foreign key field.
        fk_interaction_rule: How foreign keys are handled in this field.
        parent_field_id: Parent field ID if this is a nested field.
        styling: Custom styling options.
        is_required: Whether this field is required.
        child_fields: Nested child fields if any.
    """
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
    """Complete information about a form.
    
    Attributes:
        id: Unique identifier for this form.
        created_at: Timestamp when form was created.
        updated_at: Timestamp when form was last updated.
        token: Unique token for accessing this form.
        name: Form name.
        description: Optional form description.
        version: Version number of the form.
        database_id: Database this form operates on.
        schema_oid: Schema OID containing the target table.
        base_table_oid: Table OID this form submits to.
        associated_role_id: Optional role ID associated with form.
        header_title: Form header title (can be internationalized).
        header_subtitle: Optional header subtitle.
        publish_public: Whether form is publicly accessible.
        submit_message: Message shown after submission.
        submit_redirect_url: URL to redirect to after submission.
        submit_button_label: Label for the submit button.
        fields: List of form fields.
    """
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
    """Definition for adding or replacing a form field.
    
    Attributes:
        key: Field key for referencing in submissions.
        index: Display order index.
        label: Display label.
        help: Help text.
        kind: Field type (scalar_column or foreign_key).
        column_attnum: Column attnum if scalar column field.
        related_table_oid: Related table OID if foreign key field.
        fk_interaction_rule: How foreign keys are handled.
        styling: Custom styling options.
        is_required: Whether field is required.
        child_fields: Nested child field definitions.
    """
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
    """Definition for creating a new form.
    
    Attributes:
        name: Form name.
        description: Optional description.
    """
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
    """Definition for updating an existing form.
    
    Inherits all fields from AddFormDef plus:
        id: Form ID to update.
        version: Current version number.
    """
    id: int
    version: int


# Roles and configured roles


class RoleMember(BaseModel):
    """Information about a role member.
    
    Attributes:
        oid: OID of the member role.
        admin: Whether the member has admin privileges.
    """
    oid: int
    admin: bool


class RoleInfo(BaseModel):
    """Complete information about a PostgreSQL role.
    
    Attributes:
        oid: Role OID.
        name: Role name.
        super: Whether role is a superuser.
        inherits: Whether role inherits privileges.
        create_role: Whether role can create other roles.
        create_db: Whether role can create databases.
        login: Whether role can log in.
        description: Optional role description.
        members: List of roles that are members of this role.
    """
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
    """Information about a database schema.
    
    Attributes:
        oid: Schema OID.
        name: Schema name.
        description: Optional description.
        owner_oid: OID of the schema owner role.
        current_role_priv: Privileges the current role has on this schema.
        current_role_owns: Whether the current role owns this schema.
        table_count: Number of tables in this schema.
    """
    oid: int
    name: str
    description: Optional[str] = None
    owner_oid: int
    current_role_priv: List[Literal['USAGE', 'CREATE']]
    current_role_owns: bool
    table_count: int


class SchemaPatch(BaseModel):
    """Fields that can be updated on a schema.
    
    Attributes:
        name: New schema name.
        description: New description.
    """
    name: Optional[str] = None
    description: Optional[str] = None


class SchemaPrivileges(BaseModel):
    """Privileges for a specific role on a schema.
    
    Attributes:
        role_oid: OID of the role these privileges apply to.
        direct: List of direct privileges granted.
    """
    role_oid: int
    direct: List[Literal['USAGE', 'CREATE']]


# Tables and metadata and privileges


class TableInfo(BaseModel):
    """Information about a database table.
    
    Attributes:
        oid: Table OID.
        name: Table name.
        schema: Schema OID containing this table.
        description: Optional table description.
        owner_oid: OID of the table owner role.
        current_role_priv: Privileges the current role has on this table.
        current_role_owns: Whether the current role owns this table.
    """
    oid: int
    name: str
    schema: int
    description: Optional[str] = None
    owner_oid: int
    current_role_priv: List[Literal['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE', 'REFERENCES', 'TRIGGER']]
    current_role_owns: bool


class AddedTableInfo(BaseModel):
    """Information about a newly created table.
    
    Attributes:
        oid: Table OID.
        name: Table name.
        renamed_columns: Map of original to renamed column names.
    """
    oid: int
    name: str
    renamed_columns: Optional[Dict[str, Any]] = None


class SettableTableInfo(BaseModel):
    """Fields that can be updated on a table.
    
    Attributes:
        name: New table name.
        description: New description.
        columns: Column updates to apply.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    columns: Optional[List[SettableColumnInfo]] = None


class JoinableTableRecord(BaseModel):
    """Information about a table that can be joined.
    
    Attributes:
        base: Base table OID.
        target: Target table OID that can be joined.
        join_path: Path of joins to reach the target.
        fkey_path: Foreign key path to the target.
        depth: Join depth (number of hops).
        multiple_results: Whether join produces multiple results.
    """
    base: int
    target: int
    join_path: List[Any]
    fkey_path: List[Any]
    depth: int
    multiple_results: bool


class JoinableTableInfo(BaseModel):
    """List of tables that can be joined with a base table.
    
    Attributes:
        joinable_tables: List of joinable table records.
        target_table_info: Information about target tables.
    """
    joinable_tables: List[JoinableTableRecord]
    target_table_info: List[Any]


class TableMetaDataBlob(BaseModel):
    """Metadata for customizing table behavior.
    
    Attributes:
        data_file_id: ID of the file this table was imported from.
        import_verified: Whether import has been verified.
        column_order: Custom column display order.
        record_summary_template: Template for generating record summaries.
        mathesar_added_pkey_attnum: Attnum of primary key added by Mathesar.
    """
    data_file_id: Optional[int] = None
    import_verified: Optional[bool] = None
    column_order: Optional[List[int]] = None
    record_summary_template: Optional[Dict[str, Union[str, List[int]]]] = None
    mathesar_added_pkey_attnum: Optional[int] = None


class TableMetaDataRecord(BaseModel):
    """Stored table metadata record including identifiers.
    
    Inherits all fields from TableMetaDataBlob plus:
        id: Metadata record ID.
        database_id: Database this table belongs to.
        table_oid: Table OID this metadata applies to.
    """
    id: int
    database_id: int
    table_oid: int
    data_file_id: Optional[int] = None
    import_verified: Optional[bool] = None
    column_order: Optional[List[int]] = None
    record_summary_template: Optional[Dict[str, Union[str, List[int]]]] = None
    mathesar_added_pkey_attnum: Optional[int] = None


class TablePrivileges(BaseModel):
    """Privileges for a specific role on a table.
    
    Attributes:
        role_oid: OID of the role these privileges apply to.
        direct: List of direct privileges granted.
    """
    role_oid: int
    direct: List[Literal['INSERT', 'SELECT', 'UPDATE', 'DELETE', 'TRUNCATE', 'REFERENCES', 'TRIGGER']]


# Users


class UserInfo(BaseModel):
    """Information about a Mathesar user.
    
    Attributes:
        id: Unique user ID.
        username: Username for login.
        is_superuser: Whether user has superuser privileges.
        email: User email address.
        full_name: User's full name.
        display_language: Preferred display language.
    """
    id: int
    username: str
    is_superuser: bool
    email: str
    full_name: str
    display_language: str


class UserDef(BaseModel):
    """Definition for creating or updating a user.
    
    Attributes:
        username: Username for login.
        password: User password.
        is_superuser: Whether user should have superuser privileges.
        email: User email address.
        full_name: User's full name.
        display_language: Preferred display language.
    """
    username: str
    password: str
    is_superuser: bool
    email: Optional[str] = None
    full_name: Optional[str] = None
    display_language: Optional[str] = None
