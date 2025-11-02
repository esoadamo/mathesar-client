"""Mathesar Python Client - Typed, ergonomic client for Mathesar JSON-RPC API.

This package provides both low-level (MathesarClientRaw) and high-level (MathesarClient)
interfaces to the Mathesar API. The high-level client is recommended for most use cases.

Quick Start:
    >>> from mathesar_client import MathesarClient
    >>> 
    >>> # Connect using environment variables or pass credentials
    >>> client = MathesarClient()
    >>> 
    >>> # Navigate the hierarchy: database -> schema -> table
    >>> db = client.database(1)
    >>> schema = db.schema_by_name("public")
    >>> table = schema.table_by_name("users")
    >>> 
    >>> # Query records with column names
    >>> page = table.records_list(limit=10, order_by=[("created_at", "desc")])
    >>> for record in page.results:
    ...     print(record["email"])

Environment Variables:
    MATHESAR_BASE_URL: Base URL of the Mathesar instance
    MATHESAR_USERNAME: Username for basic authentication
    MATHESAR_PASSWORD: Password for basic authentication

Main Components:
    MathesarClient: High-level ergonomic client (recommended)
    MathesarClientRaw: Low-level JSON-RPC client
    MathesarClientError: Exception for API errors
    
    All Pydantic models are also exported for type hints and validation.
"""

from .client_raw import MathesarClientRaw, MathesarClientError
from .client import MathesarClient
from .client_raw_models import (
	# Records
	OrderBy,
	Filter,
	FilterAttnum,
	FilterLiteral,
	Grouping,
	Group,
	GroupingResponse,
	SearchParam,
	RecordList,
	RecordAdded,
	RecordSummaryList,
	SummarizedRecordReference,
	# Analytics
	AnalyticsState,
	AnalyticsReport,
	# Collaborators
	CollaboratorInfo,
	# Columns
	TypeOptions,
	ColumnDefault,
	ColumnInfo,
	CreatablePkColumnInfo,
	CreatableColumnInfo,
	SettableColumnInfo,
	ColumnMetaDataBlob,
	ColumnMetaDataRecord,
	# Configured databases
	ConfiguredDatabaseInfo,
	ConfiguredDatabasePatch,
	# Constraints
	ForeignKeyConstraint,
	PrimaryKeyConstraint,
	UniqueConstraint,
	CreatableConstraintInfo,
	ConstraintInfo,
	# Data modeling
	MappingColumn,
	SplitTableInfo,
	# Databases and privileges
	DatabaseInfo,
	DBPrivileges,
	# Setup
	ConfiguredServerInfo,
	ConfiguredRoleInfo,
	DatabaseConnectionResult,
	# Explorations
	ExplorationInfo,
	ExplorationDef,
	ExplorationResult,
	# Forms
	FieldInfo,
	FormInfo,
	AddOrReplaceFieldDef,
	AddFormDef,
	SettableFormDef,
	# Roles
	RoleMember,
	RoleInfo,
	# Schemas and privileges
	SchemaInfo,
	SchemaPatch,
	SchemaPrivileges,
	# Tables and metadata and privileges
	TableInfo,
	AddedTableInfo,
	SettableTableInfo,
	JoinableTableRecord,
	JoinableTableInfo,
	TableMetaDataBlob,
	TableMetaDataRecord,
	TablePrivileges,
	# Users
	UserInfo,
	UserDef,
)

__all__ = [
	# Client
	"MathesarClientRaw",
	"MathesarClientError",
	"MathesarClient",
	# Records
	"OrderBy",
	"Filter",
	"FilterAttnum",
	"FilterLiteral",
	"Grouping",
	"Group",
	"GroupingResponse",
	"SearchParam",
	"RecordList",
	"RecordAdded",
	"RecordSummaryList",
	"SummarizedRecordReference",
	# Analytics
	"AnalyticsState",
	"AnalyticsReport",
	# Collaborators
	"CollaboratorInfo",
	# Columns
	"TypeOptions",
	"ColumnDefault",
	"ColumnInfo",
	"CreatablePkColumnInfo",
	"CreatableColumnInfo",
	"SettableColumnInfo",
	"ColumnMetaDataBlob",
	"ColumnMetaDataRecord",
	# Configured databases
	"ConfiguredDatabaseInfo",
	"ConfiguredDatabasePatch",
	# Constraints
	"ForeignKeyConstraint",
	"PrimaryKeyConstraint",
	"UniqueConstraint",
	"CreatableConstraintInfo",
	"ConstraintInfo",
	# Data modeling
	"MappingColumn",
	"SplitTableInfo",
	# Databases and privileges
	"DatabaseInfo",
	"DBPrivileges",
	# Setup
	"ConfiguredServerInfo",
	"ConfiguredRoleInfo",
	"DatabaseConnectionResult",
	# Explorations
	"ExplorationInfo",
	"ExplorationDef",
	"ExplorationResult",
	# Forms
	"FieldInfo",
	"FormInfo",
	"AddOrReplaceFieldDef",
	"AddFormDef",
	"SettableFormDef",
	# Roles
	"RoleMember",
	"RoleInfo",
	# Schemas and privileges
	"SchemaInfo",
	"SchemaPatch",
	"SchemaPrivileges",
	# Tables and metadata and privileges
	"TableInfo",
	"AddedTableInfo",
	"SettableTableInfo",
	"JoinableTableRecord",
	"JoinableTableInfo",
	"TableMetaDataBlob",
	"TableMetaDataRecord",
	"TablePrivileges",
	# Users
	"UserInfo",
	"UserDef",
]
