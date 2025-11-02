"""High-level ergonomic client for Mathesar API.

This module provides a user-friendly client with a hierarchical structure:
MathesarClient → Database → Schema → Table

Features:
- Column name resolution (use names instead of attnums)
- Linked record summary inlining
- Name-based lookups for schemas and tables
- Convenience methods for common operations
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple, Literal
from pydantic import BaseModel

from .client_raw import MathesarClientRaw
from .client_raw_models import (
    # Columns
    ColumnInfo,
    CreatablePkColumnInfo,
    CreatableColumnInfo,
    SettableColumnInfo,
    # Records
    OrderBy,
    RecordList as RawRecordList,
    RecordAdded as RawRecordAdded,
    SearchParam,
    SummarizedRecordReference,
    # Constraints
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
    # Tables
    SettableTableInfo,
    AddedTableInfo,
    JoinableTableInfo,
    TableMetaDataBlob,
    TableMetaDataRecord,
    TablePrivileges,
    # Data modeling
    MappingColumn,
    SplitTableInfo,
    # Explorations
    ExplorationDef,
    ExplorationInfo,
    ExplorationResult,
    # Forms
    AddFormDef,
    SettableFormDef,
    FormInfo,
    # Roles
    RoleInfo,
    ConfiguredRoleInfo,
    # Schemas
    SchemaInfo,
    SchemaPatch,
    SchemaPrivileges,
    # Databases and setup
    DatabaseInfo,
    DBPrivileges,
    ConfiguredDatabaseInfo,
    ConfiguredDatabasePatch,
    DatabaseConnectionResult,
    # Analytics
    AnalyticsState,
    AnalyticsReport,
    # Collaborators
    CollaboratorInfo,
    # Users
    UserInfo,
    UserDef,
)


class LinkedRecordRef(SummarizedRecordReference):
    """A reference to a linked record enriched with summary text.
    
    Used in record results to represent foreign key relationships
    with both the key value and a human-readable summary.
    """
    pass


class RecordsPage(BaseModel):
    """A page of records from a query with enriched column names.
    
    Attributes:
        count: Total number of records matching the query.
        results: List of record dictionaries with column names as keys.
    """
    count: int
    results: List[Dict[str, Any]]


class MathesarClient:
    """High-level ergonomic client for Mathesar API.
    
    This client provides a user-friendly interface with:
    - Hierarchical navigation: database() → schema() → table()
    - Column name resolution (use names instead of attnums)
    - Linked record summary inlining
    - Name-based lookups
    - Convenience methods for common operations
    
    Args:
        raw: Optional MathesarClientRaw instance. If not provided, creates one using
             environment variables (MATHESAR_BASE_URL, MATHESAR_USERNAME, MATHESAR_PASSWORD).
    
    Example:
        >>> client = MathesarClient()
        >>> db = client.database(1)
        >>> schema = db.schema_by_name("public")
        >>> table = schema.table_by_name("users")
        >>> records = table.records_list(limit=10)
    """

    def __init__(self, raw: Optional[MathesarClientRaw] = None):
        self.raw = raw or MathesarClientRaw()

    def database(self, database_id: int) -> Database:
        """Get a Database object for the specified database.
        
        Args:
            database_id: Database ID to work with.
        
        Returns:
            Database instance for performing database-level operations.
        """
        return Database(self.raw, database_id)

    # ----- Analytics -----
    def analytics_get_state(self) -> AnalyticsState:
        """Get the current analytics collection state.
        
        Returns:
            AnalyticsState indicating whether analytics are enabled.
        """
        return self.raw.analytics_get_state()

    def analytics_initialize(self) -> None:
        """Initialize and enable analytics collection."""
        return self.raw.analytics_initialize()

    def analytics_disable(self) -> None:
        """Disable analytics collection."""
        return self.raw.analytics_disable()

    def analytics_view_report(self) -> AnalyticsReport:
        """View the current analytics report.
        
        Returns:
            AnalyticsReport with usage statistics.
        """
        return self.raw.analytics_view_report()

    def analytics_upload_feedback(self, *, message: str) -> None:
        """Upload user feedback to analytics.
        
        Args:
            message: Feedback message to upload.
        """
        return self.raw.analytics_upload_feedback(message=message)

    # ----- Setup (global) -----
    def setup_create_new(
        self, *, database: str, sample_data: Optional[List[str]] = None, nickname: Optional[str] = None
    ) -> DatabaseConnectionResult:
        return self.raw.databases_setup_create_new(database=database, sample_data=sample_data, nickname=nickname)

    def setup_connect_existing(
        self,
        *,
        host: str,
        database: str,
        role: str,
        password: str,
        port: Optional[int] = None,
        sample_data: Optional[List[str]] = None,
        nickname: Optional[str] = None,
    ) -> DatabaseConnectionResult:
        return self.raw.databases_setup_connect_existing(
            host=host,
            database=database,
            role=role,
            password=password,
            port=port,
            sample_data=sample_data,
            nickname=nickname,
        )

    # ----- Configured databases -----
    def configured_databases_list(self, *, server_id: Optional[int] = None) -> List[ConfiguredDatabaseInfo]:
        return self.raw.databases_configured_list(server_id=server_id)

    def configured_databases_patch(
        self, *, database_id: int, patch: ConfiguredDatabasePatch
    ) -> ConfiguredDatabaseInfo:
        return self.raw.databases_configured_patch(database_id=database_id, patch=patch)

    def configured_databases_disconnect(
        self,
        *,
        database_id: int,
        schemas_to_remove: Optional[List[str]] = None,
        strict: bool = True,
        role_name: Optional[str] = None,
        password: Optional[str] = None,
        disconnect_db_server: bool = False,
    ) -> None:
        return self.raw.databases_configured_disconnect(
            database_id=database_id,
            schemas_to_remove=schemas_to_remove,
            strict=strict,
            role_name=role_name,
            password=password,
            disconnect_db_server=disconnect_db_server,
        )

    # ----- Configured roles -----
    def configured_roles_list(self, *, server_id: int) -> List[ConfiguredRoleInfo]:
        return self.raw.roles_configured_list(server_id=server_id)

    def configured_roles_add(self, *, server_id: int, name: str, password: str) -> ConfiguredRoleInfo:
        return self.raw.roles_configured_add(server_id=server_id, name=name, password=password)

    def configured_roles_delete(self, *, configured_role_id: int) -> None:
        return self.raw.roles_configured_delete(configured_role_id=configured_role_id)

    def configured_roles_set_password(self, *, configured_role_id: int, password: str) -> None:
        return self.raw.roles_configured_set_password(configured_role_id=configured_role_id, password=password)

    # ----- Users (global) -----
    def users_list(self) -> List[UserInfo]:
        return self.raw.users_list()

    def users_get(self, *, user_id: int) -> UserInfo:
        return self.raw.users_get(user_id=user_id)

    def users_add(self, *, user_def: UserDef) -> UserInfo:
        return self.raw.users_add(user_def=user_def)

    def users_delete(self, *, user_id: int) -> None:
        return self.raw.users_delete(user_id=user_id)

    def users_patch_self(self, *, username: str, email: str, full_name: str, display_language: str) -> UserInfo:
        return self.raw.users_patch_self(
            username=username, email=email, full_name=full_name, display_language=display_language
        )

    def users_patch_other(
        self,
        *,
        user_id: int,
        username: str,
        is_superuser: bool,
        email: str,
        full_name: str,
        display_language: str,
    ) -> UserInfo:
        return self.raw.users_patch_other(
            user_id=user_id,
            username=username,
            is_superuser=is_superuser,
            email=email,
            full_name=full_name,
            display_language=display_language,
        )

    def users_replace_own(self, *, old_password: str, new_password: str) -> None:
        return self.raw.users_replace_own(old_password=old_password, new_password=new_password)

    def users_revoke(self, *, user_id: int, new_password: str) -> None:
        return self.raw.users_revoke(user_id=user_id, new_password=new_password)


class Database:
    """Database-level operations and navigation.
    
    Provides access to:
    - Schema management and navigation
    - Database-level privileges
    - Explorations, collaborators, and roles
    - Database information and upgrades
    
    Args:
        raw: The underlying raw client.
        database_id: Database ID for this instance.
    
    Example:
        >>> db = client.database(1)
        >>> schemas = db.list_schemas()
        >>> schema = db.schema_by_name("public")
    """
    
    def __init__(self, raw: MathesarClientRaw, database_id: int):
        self._raw = raw
        self.database_id = database_id

    def table(self, table_oid: int) -> Table:
        return Table(self._raw, self.database_id, table_oid)

    # Schemas
    def list_schemas(self):
        return self._raw.schemas_list(database_id=self.database_id)

    def add_schema(
        self,
        *,
        name: str,
        owner_oid: Optional[int] = None,
        description: Optional[str] = None,
    ) -> SchemaInfo:
        return self._raw.schemas_add(name=name, database_id=self.database_id, owner_oid=owner_oid, description=description)

    def get_schema(self, *, schema_oid: int) -> SchemaInfo:
        return self._raw.schemas_get(schema_oid=schema_oid, database_id=self.database_id)

    def delete_schemas(self, *, schema_oids: List[int]) -> None:
        return self._raw.schemas_delete(schema_oids=schema_oids, database_id=self.database_id)

    def patch_schema(self, *, schema_oid: int, patch: SchemaPatch) -> SchemaInfo:
        return self._raw.schemas_patch(schema_oid=schema_oid, database_id=self.database_id, patch=patch)

    def schema(self, schema_oid: int) -> Schema:
        """Get a Schema object for the specified schema.
        
        Args:
            schema_oid: Schema OID to work with.
        
        Returns:
            Schema instance for performing schema-level operations.
        """
        return Schema(self._raw, self.database_id, schema_oid)

    def schema_by_name(self, name: str) -> Schema:
        """Get a Schema object by name.
        
        Args:
            name: Schema name to look up.
        
        Returns:
            Schema instance for the named schema.
        
        Raises:
            ValueError: If no schema with the given name exists.
        """
        schemas = self._raw.schemas_list(database_id=self.database_id)
        for s in schemas:
            if s.name == name:
                return Schema(self._raw, self.database_id, s.oid)
        raise ValueError(f"Schema with name '{name}' not found")

    # Schema privileges
    def schema_privileges_list(self, *, schema_oid: int) -> List[SchemaPrivileges]:
        return self._raw.schemas_privileges_list_direct(schema_oid=schema_oid, database_id=self.database_id)

    def schema_privileges_replace_for_roles(
        self, *, schema_oid: int, privileges: List[SchemaPrivileges]
    ) -> List[SchemaPrivileges]:
        return self._raw.schemas_privileges_replace_for_roles(
            privileges=privileges, schema_oid=schema_oid, database_id=self.database_id
        )

    def schema_transfer_ownership(self, *, schema_oid: int, new_owner_oid: int) -> SchemaInfo:
        return self._raw.schemas_privileges_transfer_ownership(
            schema_oid=schema_oid, new_owner_oid=new_owner_oid, database_id=self.database_id
        )

    # Database info
    def info(self) -> DatabaseInfo:
        return self._raw.databases_get(database_id=self.database_id)

    def delete(self, *, database_oid: int) -> None:
        return self._raw.databases_delete(database_oid=database_oid, database_id=self.database_id)

    def upgrade_sql(self, *, username: Optional[str] = None, password: Optional[str] = None) -> None:
        return self._raw.databases_upgrade_sql(database_id=self.database_id, username=username, password=password)

    # Privileges
    def list_privileges(self) -> List[DBPrivileges]:
        return self._raw.databases_privileges_list_direct(database_id=self.database_id)

    def replace_privileges_for_roles(self, *, privileges: List[DBPrivileges]) -> List[DBPrivileges]:
        return self._raw.databases_privileges_replace_for_roles(
            privileges=privileges, database_id=self.database_id
        )

    def transfer_ownership(self, *, new_owner_oid: int) -> DatabaseInfo:
        return self._raw.databases_privileges_transfer_ownership(new_owner_oid=new_owner_oid, database_id=self.database_id)

    # Explorations
    def explorations_list(self, *, schema_oid: Optional[int] = None) -> List[ExplorationInfo]:
        return self._raw.explorations_list(database_id=self.database_id, schema_oid=schema_oid)

    def exploration(self, exploration_id: int) -> ExplorationInfo:
        return self._raw.explorations_get(exploration_id=exploration_id)

    def explorations_add(self, *, exploration_def: ExplorationDef) -> ExplorationInfo:
        return self._raw.explorations_add(exploration_def=exploration_def)

    def explorations_delete(self, *, exploration_id: int) -> None:
        return self._raw.explorations_delete(exploration_id=exploration_id)

    def explorations_replace(self, *, new_exploration: ExplorationInfo) -> ExplorationInfo:
        return self._raw.explorations_replace(new_exploration=new_exploration)

    def explorations_run(self, *, exploration_def: ExplorationDef, limit: int = 100, offset: int = 0) -> ExplorationResult:
        return self._raw.explorations_run(exploration_def=exploration_def, limit=limit, offset=offset)

    def explorations_run_saved(self, *, exploration_id: int, limit: int = 100, offset: int = 0) -> ExplorationResult:
        return self._raw.explorations_run_saved(exploration_id=exploration_id, limit=limit, offset=offset)

    # Collaborators
    def collaborators_list(self) -> List[CollaboratorInfo]:
        return self._raw.collaborators_list(database_id=self.database_id)

    def collaborators_add(self, *, user_id: int, configured_role_id: int) -> None:
        return self._raw.collaborators_add(database_id=self.database_id, user_id=user_id, configured_role_id=configured_role_id)

    def collaborators_delete(self, *, collaborator_id: int) -> None:
        return self._raw.collaborators_delete(collaborator_id=collaborator_id)

    def collaborators_set_role(self, *, collaborator_id: int, configured_role_id: int) -> None:
        return self._raw.collaborators_set_role(collaborator_id=collaborator_id, configured_role_id=configured_role_id)

    # Roles
    def roles_list(self) -> List[RoleInfo]:
        return self._raw.roles_list(database_id=self.database_id)

    def roles_add(self, *, rolename: str, password: Optional[str] = None, login: Optional[bool] = None) -> RoleInfo:
        return self._raw.roles_add(rolename=rolename, database_id=self.database_id, password=password, login=login)

    def roles_delete(self, *, role_oid: int) -> None:
        return self._raw.roles_delete(role_oid=role_oid, database_id=self.database_id)

    def roles_get_current_role(self) -> Dict[str, Any]:
        return self._raw.roles_get_current_role(database_id=self.database_id)

    def roles_set_members(self, *, parent_role_oid: int, members: List[int]) -> RoleInfo:
        return self._raw.roles_set_members(parent_role_oid=parent_role_oid, members=members, database_id=self.database_id)


class Schema:
    """Schema-level operations and navigation.
    
    Provides access to:
    - Table management and navigation
    - Forms management
    - Data modeling operations (mapping tables)
    
    Args:
        raw: The underlying raw client.
        database_id: Database ID this schema belongs to.
        schema_oid: Schema OID for this instance.
    
    Example:
        >>> schema = db.schema_by_name("public")
        >>> tables = schema.list_tables()
        >>> table = schema.table_by_name("users")
    """
    
    def __init__(self, raw: MathesarClientRaw, database_id: int, schema_oid: int):
        self._raw = raw
        self.database_id = database_id
        self.schema_oid = schema_oid

    # Tables
    def list_tables(self):
        return self._raw.tables_list(schema_oid=self.schema_oid, database_id=self.database_id)

    def add_table(
        self,
        *,
        table_name: Optional[str] = None,
        pkey_type: Optional[Literal["IDENTITY", "UUIDv4"]] = None,
        column_data_list: Optional[List[Dict[str, Any]]] = None,
        owner_oid: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> AddedTableInfo:
        # Convert pkey_type to CreatablePkColumnInfo if provided
        pkey_info = None
        if pkey_type is not None:
            pkey_info = CreatablePkColumnInfo(type=pkey_type)  # default name 'id'
        columns = None
        if column_data_list is not None:
            columns = [CreatableColumnInfo.model_validate(c) for c in column_data_list]
        return self._raw.tables_add(
            schema_oid=self.schema_oid,
            database_id=self.database_id,
            table_name=table_name,
            pkey_column_info=pkey_info,
            column_data_list=columns,
            constraint_data_list=None,
            owner_oid=owner_oid,
            comment=comment,
        )

    def table(self, table_oid: int) -> Table:
        """Get a Table object for the specified table.
        
        Args:
            table_oid: Table OID to work with.
        
        Returns:
            Table instance for performing table-level operations.
        """
        return Table(self._raw, self.database_id, table_oid)

    def table_by_name(self, name: str) -> Table:
        """Get a Table object by name.
        
        Args:
            name: Table name to look up.
        
        Returns:
            Table instance for the named table.
        
        Raises:
            ValueError: If no table with the given name exists.
        """
        tables = self.list_tables()
        for t in tables:
            if t.name == name:
                return Table(self._raw, self.database_id, t.oid)
        raise ValueError(f"Table with name '{name}' not found")

    # Tables with metadata
    def list_tables_with_metadata(self) -> List[Dict[str, Any]]:
        return self._raw.tables_list_with_metadata(schema_oid=self.schema_oid, database_id=self.database_id)

    def import_table(
        self,
        *,
        data_file_id: int,
        table_name: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> AddedTableInfo:
        return self._raw.tables_import(
            data_file_id=data_file_id,
            schema_oid=self.schema_oid,
            database_id=self.database_id,
            table_name=table_name,
            comment=comment,
        )

    # Data modeling (schema-scoped)
    def add_mapping_table(self, *, table_name: str, mapping_columns: List[MappingColumn]) -> None:
        return self._raw.data_modeling_add_mapping_table(
            table_name=table_name,
            mapping_columns=mapping_columns,
            schema_oid=self.schema_oid,
            database_id=self.database_id,
        )

    # Forms (schema-scoped)
    def forms_list(self) -> List[FormInfo]:
        return self._raw.forms_list(database_id=self.database_id, schema_oid=self.schema_oid)

    def forms_add(self, *, form_def: AddFormDef) -> FormInfo:
        return self._raw.forms_add(form_def=form_def)

    def forms_delete(self, *, form_id: int) -> None:
        return self._raw.forms_delete(form_id=form_id)

    def forms_regenerate_token(self, *, form_id: int) -> str:
        return self._raw.forms_regenerate_token(form_id=form_id)

    def forms_patch(self, *, update_form_def: SettableFormDef) -> FormInfo:
        return self._raw.forms_patch(update_form_def=update_form_def)

    def forms_set_publish_public(self, *, form_id: int, publish_public: bool) -> bool:
        return self._raw.forms_set_publish_public(form_id=form_id, publish_public=publish_public)

    def form_get(self, *, form_token: str) -> FormInfo:
        return self._raw.forms_get(form_token=form_token)

    def form_submit(self, *, form_token: str, values: Dict[str, Any]) -> None:
        return self._raw.forms_submit(form_token=form_token, values=values)

    def forms_list_related_records(
        self,
        *,
        form_token: str,
        field_key: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ):
        return self._raw.forms_list_related_records(
            form_token=form_token,
            field_key=field_key,
            limit=limit,
            offset=offset,
            search=search,
        )


class Table:
    """Table-level operations with column name resolution and record enrichment.
    
    Provides:
    - Record operations with column names (instead of attnums)
    - Linked record summary inlining
    - Column management with name-based API
    - Constraint and data modeling operations
    - Table metadata and privileges
    
    This class automatically caches column information and provides mappings
    between column names and attribute numbers (attnums).
    
    Args:
        raw: The underlying raw client.
        database_id: Database ID this table belongs to.
        table_oid: Table OID for this instance.
    
    Example:
        >>> table = schema.table_by_name("users")
        >>> # Query records using column names
        >>> page = table.records_list(
        ...     limit=10,
        ...     order_by=[("created_at", "desc")]
        ... )
        >>> # Add a record using column names
        >>> record = table.record_add({
        ...     "email": "user@example.com",
        ...     "full_name": "John Doe"
        ... })
    """
    
    def __init__(self, raw: MathesarClientRaw, database_id: int, table_oid: int):
        self._raw = raw
        self.database_id = database_id
        self.table_oid = table_oid
        self._columns_cache: Optional[List[ColumnInfo]] = None
        self._attnum_to_name: Optional[Dict[int, str]] = None
        self._name_to_attnum: Optional[Dict[str, int]] = None

    # ----- Columns helpers -----
    def columns(self, use_cache: bool = True) -> List[ColumnInfo]:
        """Get list of columns for this table.
        
        Args:
            use_cache: Whether to use cached column information.
        
        Returns:
            List of ColumnInfo objects.
        """
        if not use_cache or self._columns_cache is None:
            self._columns_cache = self._raw.columns_list(table_oid=self.table_oid, database_id=self.database_id)
            self._attnum_to_name = {c.id: c.name for c in self._columns_cache}
            self._name_to_attnum = {c.name: c.id for c in self._columns_cache}
        return self._columns_cache

    def _ensure_column_maps(self):
        """Ensure column name/attnum mappings are loaded."""
        if self._attnum_to_name is None or self._name_to_attnum is None:
            self.columns(use_cache=False)

    def _attnum_to_colname(self, attnum: int) -> str:
        self._ensure_column_maps()
        assert self._attnum_to_name is not None
        return self._attnum_to_name.get(attnum, str(attnum))

    def _colname_to_attnum(self, name: str) -> int:
        self._ensure_column_maps()
        assert self._name_to_attnum is not None
        if name not in self._name_to_attnum:
            raise KeyError(f"Unknown column name: {name}")
        return self._name_to_attnum[name]

    def _map_names_or_attnums(self, values: Iterable[int | str]) -> List[int]:
        mapped: List[int] = []
        for v in values:
            if isinstance(v, int):
                mapped.append(v)
            else:
                mapped.append(self._colname_to_attnum(v))
        return mapped

    # ----- Record transforms -----
    def _order_by_from_names(self, order_by: Optional[List[Tuple[str, Literal["asc", "desc"]]]]) -> Optional[List[OrderBy]]:
        if not order_by:
            return None
        return [
            OrderBy(attnum=self._colname_to_attnum(name), direction=direction)
            for name, direction in order_by
        ]

    @staticmethod
    def _pick_linked_map(record_list: RawRecordList) -> Optional[Dict[str, Dict[str, str]]]:
        return getattr(record_list, "linked_record_summaries", None)

    def _enrich_records(self, record_list: RawRecordList) -> RecordsPage:
        att_to_name = {c.id: c.name for c in self.columns()}
        linked_map = self._pick_linked_map(record_list) or {}
        enriched: List[Dict[str, Any]] = []
        for idx, rec in enumerate(record_list.results):
            row: Dict[str, Any] = {}
            # keys may be string attnums; normalize to ints when possible
            for k, v in rec.items():
                try:
                    att = int(k)
                except Exception:
                    # unexpected key, keep as-is
                    row[k] = v
                    continue
                colname = att_to_name.get(att, str(att))
                # If we have linked summary for this row and column, wrap it
                row_linked = linked_map.get(str(idx)) or linked_map.get(idx) or {}
                summary = row_linked.get(str(att))
                if summary is not None and v is not None:
                    row[colname] = LinkedRecordRef(key=v, summary=summary)
                else:
                    row[colname] = v
            enriched.append(row)
        return RecordsPage(count=record_list.count, results=enriched)

    # ----- Records API (high-level) -----
    def records_list(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Tuple[str, Literal["asc", "desc"]]]] = None,
        return_record_summaries: bool = True,
    ) -> RecordsPage:
        """List records from this table with enriched column names.
        
        This method returns records with column names as keys (instead of attnums)
        and inlines linked record summaries when requested.
        
        Args:
            limit: Maximum number of records to return.
            offset: Number of records to skip.
            order_by: List of (column_name, direction) tuples for sorting.
                     Example: [("created_at", "desc"), ("name", "asc")]
            return_record_summaries: Whether to include summaries of linked records.
        
        Returns:
            RecordsPage with count and enriched results.
        
        Example:
            >>> page = table.records_list(
            ...     limit=10,
            ...     order_by=[("created_at", "desc")]
            ... )
            >>> for record in page.results:
            ...     print(record["email"], record["full_name"])
        """
        order = self._order_by_from_names(order_by)
        raw = self._raw.records_list(
            database_id=self.database_id,
            table_id=self.table_oid,
            limit=limit,
            offset=offset,
            order=order,
            return_record_summaries=return_record_summaries,
        )
        return self._enrich_records(raw)

    def records_search(
        self,
        *,
        search_params: Optional[List[SearchParam]] = None,
        limit: int = 10,
        offset: int = 0,
        return_record_summaries: bool = True,
    ) -> RecordsPage:
        """Search records in this table.
        
        Args:
            search_params: List of SearchParam for full-text search.
            limit: Maximum number of records to return.
            offset: Number of records to skip.
            return_record_summaries: Whether to include summaries of linked records.
        
        Returns:
            RecordsPage with matching records.
        """
        raw = self._raw.records_search(
            database_id=self.database_id,
            table_id=self.table_oid,
            search_params=search_params,
            limit=limit,
            offset=offset,
            return_record_summaries=return_record_summaries,
        )
        return self._enrich_records(raw)

    def record_get(self, *, record_id: Any, return_record_summaries: bool = True) -> Dict[str, Any]:
        """Get a single record by ID.
        
        Args:
            record_id: Primary key value of the record.
            return_record_summaries: Whether to include summaries of linked records.
        
        Returns:
            Record dictionary with column names as keys.
        
        Raises:
            ValueError: If record is not found.
        """
        raw = self._raw.records_get(
            database_id=self.database_id,
            table_id=self.table_oid,
            record_id=record_id,
            return_record_summaries=return_record_summaries,
        )
        page = self._enrich_records(raw)
        if not page.results:
            raise ValueError("Record not found")
        return page.results[0]

    def record_add(self, *, record_def_by_name: Dict[str, Any], return_record_summaries: bool = True) -> Dict[str, Any]:
        """Add a new record to the table.
        
        Args:
            record_def_by_name: Dictionary mapping column names to values.
            return_record_summaries: Whether to include summaries of linked records.
        
        Returns:
            The added record as a dictionary with column names as keys.
        
        Example:
            >>> record = table.record_add({
            ...     "email": "user@example.com",
            ...     "full_name": "Jane Doe",
            ...     "active": True
            ... })
        """
        # Convert column names to attnums
        self._ensure_column_maps()
        record_def: Dict[str, Any] = {
            str(self._colname_to_attnum(k)): v for k, v in record_def_by_name.items()
        }
        raw: RawRecordAdded = self._raw.records_add(
            database_id=self.database_id,
            table_id=self.table_oid,
            record_def=record_def,
            return_record_summaries=return_record_summaries,
        )
        # RawRecordAdded has a single record in results
        temp_list = RawRecordList(count=1, results=raw.results, record_summaries=raw.record_summaries, linked_record_summaries=getattr(raw, "linked_record_summaries", None))  # type: ignore[arg-type]
        page = self._enrich_records(temp_list)
        return page.results[0]

    def record_patch(
        self,
        *,
        record_id: Any,
        record_def_by_name: Dict[str, Any],
        return_record_summaries: bool = True,
    ) -> Dict[str, Any]:
        """Update an existing record.
        
        Args:
            record_id: Primary key value of the record to update.
            record_def_by_name: Dictionary mapping column names to new values.
            return_record_summaries: Whether to include summaries of linked records.
        
        Returns:
            The updated record as a dictionary with column names as keys.
        
        Example:
            >>> updated = table.record_patch(
            ...     record_id=123,
            ...     record_def_by_name={"active": False}
            ... )
        """
        self._ensure_column_maps()
        record_def: Dict[str, Any] = {
            str(self._colname_to_attnum(k)): v for k, v in record_def_by_name.items()
        }
        raw: RawRecordAdded = self._raw.records_patch(
            database_id=self.database_id,
            table_id=self.table_oid,
            record_id=record_id,
            record_def=record_def,
            return_record_summaries=return_record_summaries,
        )
        temp_list = RawRecordList(count=1, results=raw.results, record_summaries=raw.record_summaries, linked_record_summaries=getattr(raw, "linked_record_summaries", None))  # type: ignore[arg-type]
        page = self._enrich_records(temp_list)
        return page.results[0]

    def records_delete(self, *, record_ids: List[Any]) -> List[Any]:
        return self._raw.records_delete(
            database_id=self.database_id,
            table_id=self.table_oid,
            record_ids=record_ids,
        )

    # ----- Columns API (high-level) -----
    def columns_add(self, *, columns: List[Dict[str, Any]]) -> List[int]:
        cols = [CreatableColumnInfo.model_validate(c) for c in columns]
        return self._raw.columns_add(column_data_list=cols, table_oid=self.table_oid, database_id=self.database_id)

    def columns_patch(self, *, columns: List[Dict[str, Any]]) -> int:
        # Allow users to specify 'name' in entries, we map it to id if needed.
        self._ensure_column_maps()
        patched: List[Dict[str, Any]] = []
        for c in columns:
            c2 = dict(c)
            if "id" not in c2 and "name" in c2:
                c2["id"] = self._colname_to_attnum(c2["name"])  # ensure id present
            patched.append(c2)
        return self._raw.columns_patch(
            column_data_list=[SettableColumnInfo.model_validate(p) for p in patched],
            table_oid=self.table_oid,
            database_id=self.database_id,
        )

    def columns_delete(self, *, column_names_or_attnums: List[int | str]) -> int:
        attnums = self._map_names_or_attnums(column_names_or_attnums)
        return self._raw.columns_delete(column_attnums=attnums, table_oid=self.table_oid, database_id=self.database_id)

    def add_primary_key_column(
        self, *, pkey_type: Literal["IDENTITY", "UUIDv4"], drop_existing_pkey_column: bool = False, name: str = "id"
    ) -> None:
        return self._raw.columns_add_primary_key_column(
            pkey_type=pkey_type,
            table_oid=self.table_oid,
            database_id=self.database_id,
            drop_existing_pkey_column=drop_existing_pkey_column,
            name=name,
        )

    def reset_file_mash(self, *, column: int | str) -> None:
        attnum = self._map_names_or_attnums([column])[0]
        return self._raw.columns_reset_mash(column_attnum=attnum, table_oid=self.table_oid, database_id=self.database_id)

    def list_columns_with_metadata(self) -> List[ColumnInfo]:
        return self._raw.columns_list_with_metadata(table_oid=self.table_oid, database_id=self.database_id)

    # ----- Constraints API (high-level) -----
    def constraints_list(self):
        return self._raw.constraints_list(table_oid=self.table_oid, database_id=self.database_id)

    def add_primary_key_constraint(self, *, columns: List[int | str], name: Optional[str] = None, deferrable: Optional[bool] = None) -> List[int]:
        cols = self._map_names_or_attnums(columns)
        pk = PrimaryKeyConstraint(type="p", columns=cols, name=name, deferrable=deferrable)
        return self._raw.constraints_add(table_oid=self.table_oid, constraint_def_list=[pk], database_id=self.database_id)

    def add_unique_constraint(self, *, columns: List[int | str], name: Optional[str] = None, deferrable: Optional[bool] = None) -> List[int]:
        cols = self._map_names_or_attnums(columns)
        uq = UniqueConstraint(type="u", columns=cols, name=name, deferrable=deferrable)
        return self._raw.constraints_add(table_oid=self.table_oid, constraint_def_list=[uq], database_id=self.database_id)

    def add_foreign_key_constraint(
        self,
        *,
        columns: List[int | str],
        fkey_relation_id: int,
        fkey_columns: List[int | str],
        name: Optional[str] = None,
        deferrable: Optional[bool] = None,
        fkey_update_action: Optional[str] = None,
        fkey_delete_action: Optional[str] = None,
        fkey_match_type: Optional[str] = None,
    ) -> List[int]:
        cols = self._map_names_or_attnums(columns)
        ref_cols = fkey_columns  # referent table columns are specified against the referent table
        fk = ForeignKeyConstraint(
            type="f",
            columns=cols,
            fkey_relation_id=fkey_relation_id,
            fkey_columns=ref_cols,  # assume ints here; if names needed, user should map via another Table instance
            name=name,
            deferrable=deferrable,
            fkey_update_action=fkey_update_action,
            fkey_delete_action=fkey_delete_action,
            fkey_match_type=fkey_match_type,
        )
        return self._raw.constraints_add(table_oid=self.table_oid, constraint_def_list=[fk], database_id=self.database_id)

    def constraints_delete(self, *, constraint_oid: int) -> str:
        return self._raw.constraints_delete(table_oid=self.table_oid, constraint_oid=constraint_oid, database_id=self.database_id)

    # ----- Data modeling -----
    def add_foreign_key_column(self, *, column_name: str, referent_table_oid: int) -> None:
        return self._raw.data_modeling_add_foreign_key_column(
            column_name=column_name,
            referrer_table_oid=self.table_oid,
            referent_table_oid=referent_table_oid,
            database_id=self.database_id,
        )

    def suggest_types(self) -> Dict[str, str]:
        return self._raw.data_modeling_suggest_types(table_oid=self.table_oid, database_id=self.database_id)

    def split_table(
        self,
        *,
        column_names_or_attnums: List[int | str],
        extracted_table_name: str,
        relationship_fk_column_name: Optional[str] = None,
    ) -> SplitTableInfo:
        attnums = self._map_names_or_attnums(column_names_or_attnums)
        return self._raw.data_modeling_split_table(
            table_oid=self.table_oid,
            column_attnums=attnums,
            extracted_table_name=extracted_table_name,
            database_id=self.database_id,
            relationship_fk_column_name=relationship_fk_column_name,
        )

    def move_columns(
        self, *, target_table_oid: int, move_column_names_or_attnums: List[int | str]
    ) -> None:
        attnums = self._map_names_or_attnums(move_column_names_or_attnums)
        return self._raw.data_modeling_move_columns(
            source_table_oid=self.table_oid,
            target_table_oid=target_table_oid,
            move_column_attnums=attnums,
            database_id=self.database_id,
        )

    # ----- Tables management -----
    def info(self) -> Dict[str, Any]:
        return self._raw.tables_get_with_metadata(table_oid=self.table_oid, database_id=self.database_id)

    def get_import_preview(self, *, columns: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
        return self._raw.tables_get_import_preview(
            table_oid=self.table_oid, columns=[SettableColumnInfo.model_validate(c) for c in columns], database_id=self.database_id, limit=limit
        )

    def list_joinable(self, *, max_depth: int = 3) -> JoinableTableInfo:
        return self._raw.tables_list_joinable(table_oid=self.table_oid, database_id=self.database_id, max_depth=max_depth)

    def patch(self, *, table_data: SettableTableInfo) -> str:
        return self._raw.tables_patch(table_oid=self.table_oid, table_data_dict=table_data, database_id=self.database_id)

    def delete(self, *, cascade: bool = False) -> str:
        return self._raw.tables_delete(table_oid=self.table_oid, database_id=self.database_id, cascade=cascade)

    # ----- Tables metadata -----
    def list_metadata(self) -> List[TableMetaDataRecord]:
        return self._raw.tables_metadata_list(database_id=self.database_id)

    def set_metadata(self, *, metadata: TableMetaDataBlob) -> None:
        return self._raw.tables_metadata_set(table_oid=self.table_oid, metadata=metadata, database_id=self.database_id)

    # ----- Tables privileges -----
    def list_privileges(self) -> List[TablePrivileges]:
        return self._raw.tables_privileges_list_direct(table_oid=self.table_oid, database_id=self.database_id)

    def replace_privileges_for_roles(self, *, privileges: List[TablePrivileges]) -> List[TablePrivileges]:
        return self._raw.tables_privileges_replace_for_roles(
            privileges=privileges, table_oid=self.table_oid, database_id=self.database_id
        )

    def transfer_ownership(self, *, new_owner_oid: int):
        return self._raw.tables_privileges_transfer_ownership(
            table_oid=self.table_oid, new_owner_oid=new_owner_oid, database_id=self.database_id
        )
