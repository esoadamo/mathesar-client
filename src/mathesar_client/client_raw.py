from typing import Any, Dict, List, Optional, Literal
from requests import post
from os import environ
from urllib.parse import urljoin
from random import randint
from .client_raw_models import (
    # Records
    OrderBy,
    Filter,
    Grouping,
    SearchParam,
    RecordList,
    RecordAdded,
    RecordSummaryList,
    # Analytics
    AnalyticsState,
    AnalyticsReport,
    # Collaborators
    CollaboratorInfo,
    # Columns
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
    ConstraintInfo,
    CreatableConstraintInfo,
    # Data modeling
    MappingColumn,
    SplitTableInfo,
    # Databases & privileges
    DatabaseInfo,
    DBPrivileges,
    # Setup
    DatabaseConnectionResult,
    # Explorations
    ExplorationInfo,
    ExplorationDef,
    ExplorationResult,
    # Forms
    FormInfo,
    AddFormDef,
    SettableFormDef,
    # Roles
    RoleInfo,
    ConfiguredRoleInfo,
    # Schemas & privileges
    SchemaInfo,
    SchemaPatch,
    SchemaPrivileges,
    # Tables & metadata & privileges
    TableInfo,
    AddedTableInfo,
    SettableTableInfo,
    JoinableTableInfo,
    TableMetaDataBlob,
    TableMetaDataRecord,
    TablePrivileges,
    # Users
    UserInfo,
    UserDef,
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

    # Analytics
    def analytics_get_state(self) -> AnalyticsState:
        result = self._post("analytics.get_state", {})
        return AnalyticsState.model_validate(result)

    def analytics_initialize(self) -> None:
        self._post("analytics.initialize", {})
        return None

    def analytics_disable(self) -> None:
        self._post("analytics.disable", {})
        return None

    def analytics_view_report(self) -> AnalyticsReport:
        result = self._post("analytics.view_report", {})
        return AnalyticsReport.model_validate(result)

    def analytics_upload_feedback(self, *, message: str) -> None:
        self._post("analytics.upload_feedback", {"message": message})
        return None

    # Collaborators
    def collaborators_list(self, *, database_id: Optional[int] = None) -> List[CollaboratorInfo]:
        params: Dict[str, Any] = {}
        if database_id is not None:
            params["database_id"] = database_id
        result = self._post("collaborators.list", params)
        return [CollaboratorInfo.model_validate(x) for x in result]

    def collaborators_add(self, *, database_id: int, user_id: int, configured_role_id: int) -> None:
        self._post(
            "collaborators.add",
            {"database_id": database_id, "user_id": user_id, "configured_role_id": configured_role_id},
        )
        return None

    def collaborators_delete(self, *, collaborator_id: int) -> None:
        self._post("collaborators.delete", {"collaborator_id": collaborator_id})
        return None

    def collaborators_set_role(self, *, collaborator_id: int, configured_role_id: int) -> None:
        self._post(
            "collaborators.set_role",
            {"collaborator_id": collaborator_id, "configured_role_id": configured_role_id},
        )
        return None

    # Columns
    def columns_list(self, *, table_oid: int, database_id: int) -> List[ColumnInfo]:
        result = self._post("columns.list", {"table_oid": table_oid, "database_id": database_id})
        return [ColumnInfo.model_validate(x) for x in result]

    def columns_add(
        self,
        *,
        column_data_list: List[CreatableColumnInfo],
        table_oid: int,
        database_id: int,
    ) -> List[int]:
        data = {
            "column_data_list": [c.model_dump(mode="json") for c in column_data_list],
            "table_oid": table_oid,
            "database_id": database_id,
        }
        return self._post("columns.add", data)

    def columns_add_primary_key_column(
        self,
        *,
        pkey_type: Literal['IDENTITY', 'UUIDv4'],
        table_oid: int,
        database_id: int,
        drop_existing_pkey_column: bool = False,
        name: str = "id",
    ) -> None:
        data = {
            "pkey_type": pkey_type,
            "table_oid": table_oid,
            "database_id": database_id,
            "drop_existing_pkey_column": drop_existing_pkey_column,
            "name": name,
        }
        self._post("columns.add_primary_key_column", data)
        return None

    def columns_patch(
        self,
        *,
        column_data_list: List[SettableColumnInfo],
        table_oid: int,
        database_id: int,
    ) -> int:
        data = {
            "column_data_list": [c.model_dump(mode="json") for c in column_data_list],
            "table_oid": table_oid,
            "database_id": database_id,
        }
        return self._post("columns.patch", data)

    def columns_delete(self, *, column_attnums: List[int], table_oid: int, database_id: int) -> int:
        data = {
            "column_attnums": column_attnums,
            "table_oid": table_oid,
            "database_id": database_id,
        }
        return self._post("columns.delete", data)

    def columns_reset_mash(self, *, column_attnum: int, table_oid: int, database_id: int) -> None:
        data = {
            "column_attnum": column_attnum,
            "table_oid": table_oid,
            "database_id": database_id,
        }
        self._post("columns.reset_mash", data)
        return None

    def columns_list_with_metadata(self, *, table_oid: int, database_id: int) -> List[ColumnInfo]:
        result = self._post("columns.list_with_metadata", {"table_oid": table_oid, "database_id": database_id})
        return [ColumnInfo.model_validate(x) for x in result]

    def columns_metadata_list(self, *, table_oid: int, database_id: int) -> List[ColumnMetaDataRecord]:
        result = self._post("columns.metadata.list", {"table_oid": table_oid, "database_id": database_id})
        return [ColumnMetaDataRecord.model_validate(x) for x in result]

    def columns_metadata_set(
        self, *, column_meta_data_list: List[ColumnMetaDataBlob], table_oid: int, database_id: int
    ) -> None:
        data = {
            "column_meta_data_list": [m.model_dump(mode="json") for m in column_meta_data_list],
            "table_oid": table_oid,
            "database_id": database_id,
        }
        self._post("columns.metadata.set", data)
        return None

    # Configured Databases
    def databases_configured_list(self, *, server_id: Optional[int] = None) -> List[ConfiguredDatabaseInfo]:
        params: Dict[str, Any] = {}
        if server_id is not None:
            params["server_id"] = server_id
        result = self._post("databases.configured.list", params)
        return [ConfiguredDatabaseInfo.model_validate(x) for x in result]

    def databases_configured_patch(self, *, database_id: int, patch: ConfiguredDatabasePatch) -> ConfiguredDatabaseInfo:
        data = {"database_id": database_id, "patch": patch.model_dump(mode="json")}
        result = self._post("databases.configured.patch", data)
        return ConfiguredDatabaseInfo.model_validate(result)

    def databases_configured_disconnect(
        self,
        *,
        database_id: int,
        schemas_to_remove: Optional[List[str]] = None,
        strict: bool = True,
        role_name: Optional[str] = None,
        password: Optional[str] = None,
        disconnect_db_server: bool = False,
    ) -> None:
        data: Dict[str, Any] = {
            "database_id": database_id,
            "strict": strict,
            "disconnect_db_server": disconnect_db_server,
        }
        if schemas_to_remove is not None:
            data["schemas_to_remove"] = schemas_to_remove
        if role_name is not None:
            data["role_name"] = role_name
        if password is not None:
            data["password"] = password
        self._post("databases.configured.disconnect", data)
        return None

    # Constraints
    def constraints_list(self, *, table_oid: int, database_id: int) -> List[ConstraintInfo]:
        result = self._post("constraints.list", {"table_oid": table_oid, "database_id": database_id})
        return [ConstraintInfo.model_validate(x) for x in result]

    def constraints_add(
        self, *, table_oid: int, constraint_def_list: CreatableConstraintInfo, database_id: int
    ) -> List[int]:
        data = {
            "table_oid": table_oid,
            "constraint_def_list": [c.model_dump(mode="json") for c in constraint_def_list],
            "database_id": database_id,
        }
        return self._post("constraints.add", data)

    def constraints_delete(self, *, table_oid: int, constraint_oid: int, database_id: int) -> str:
        data = {"table_oid": table_oid, "constraint_oid": constraint_oid, "database_id": database_id}
        return self._post("constraints.delete", data)

    # Data Modeling
    def data_modeling_add_foreign_key_column(
        self, *, column_name: str, referrer_table_oid: int, referent_table_oid: int, database_id: int
    ) -> None:
        data = {
            "column_name": column_name,
            "referrer_table_oid": referrer_table_oid,
            "referent_table_oid": referent_table_oid,
            "database_id": database_id,
        }
        self._post("data_modeling.add_foreign_key_column", data)
        return None

    def data_modeling_add_mapping_table(
        self,
        *,
        table_name: str,
        mapping_columns: List[MappingColumn],
        schema_oid: int,
        database_id: int,
    ) -> None:
        data = {
            "table_name": table_name,
            "mapping_columns": [m.model_dump(mode="json") for m in mapping_columns],
            "schema_oid": schema_oid,
            "database_id": database_id,
        }
        self._post("data_modeling.add_mapping_table", data)
        return None

    def data_modeling_suggest_types(self, *, table_oid: int, database_id: int) -> Dict[str, str]:
        return self._post("data_modeling.suggest_types", {"table_oid": table_oid, "database_id": database_id})

    def data_modeling_split_table(
        self,
        *,
        table_oid: int,
        column_attnums: List[int],
        extracted_table_name: str,
        database_id: int,
        relationship_fk_column_name: Optional[str] = None,
    ) -> SplitTableInfo:
        data: Dict[str, Any] = {
            "table_oid": table_oid,
            "column_attnums": column_attnums,
            "extracted_table_name": extracted_table_name,
            "database_id": database_id,
        }
        if relationship_fk_column_name is not None:
            data["relationship_fk_column_name"] = relationship_fk_column_name
        result = self._post("data_modeling.split_table", data)
        return SplitTableInfo.model_validate(result)

    def data_modeling_move_columns(
        self, *, source_table_oid: int, target_table_oid: int, move_column_attnums: List[int], database_id: int
    ) -> None:
        data = {
            "source_table_oid": source_table_oid,
            "target_table_oid": target_table_oid,
            "move_column_attnums": move_column_attnums,
            "database_id": database_id,
        }
        self._post("data_modeling.move_columns", data)
        return None

    # Databases
    def databases_get(self, *, database_id: int) -> DatabaseInfo:
        result = self._post("databases.get", {"database_id": database_id})
        return DatabaseInfo.model_validate(result)

    def databases_delete(self, *, database_oid: int, database_id: int) -> None:
        self._post("databases.delete", {"database_oid": database_oid, "database_id": database_id})
        return None

    def databases_upgrade_sql(
        self, *, database_id: int, username: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        data: Dict[str, Any] = {"database_id": database_id}
        if username is not None:
            data["username"] = username
        if password is not None:
            data["password"] = password
        self._post("databases.upgrade_sql", data)
        return None

    # Database privileges
    def databases_privileges_list_direct(self, *, database_id: int) -> List[DBPrivileges]:
        result = self._post("databases.privileges.list_direct", {"database_id": database_id})
        return [DBPrivileges.model_validate(x) for x in result]

    def databases_privileges_replace_for_roles(
        self, *, privileges: List[DBPrivileges], database_id: int
    ) -> List[DBPrivileges]:
        data = {
            "privileges": [p.model_dump(mode="json") for p in privileges],
            "database_id": database_id,
        }
        result = self._post("databases.privileges.replace_for_roles", data)
        return [DBPrivileges.model_validate(x) for x in result]

    def databases_privileges_transfer_ownership(self, *, new_owner_oid: int, database_id: int) -> DatabaseInfo:
        result = self._post(
            "databases.privileges.transfer_ownership", {"new_owner_oid": new_owner_oid, "database_id": database_id}
        )
        return DatabaseInfo.model_validate(result)

    # Database setup
    def databases_setup_create_new(
        self, *, database: str, sample_data: Optional[List[str]] = None, nickname: Optional[str] = None
    ) -> DatabaseConnectionResult:
        data: Dict[str, Any] = {"database": database}
        if sample_data is not None:
            data["sample_data"] = sample_data
        if nickname is not None:
            data["nickname"] = nickname
        result = self._post("databases.setup.create_new", data)
        return DatabaseConnectionResult.model_validate(result)

    def databases_setup_connect_existing(
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
        data: Dict[str, Any] = {
            "host": host,
            "database": database,
            "role": role,
            "password": password,
        }
        if port is not None:
            data["port"] = port
        if sample_data is not None:
            data["sample_data"] = sample_data
        if nickname is not None:
            data["nickname"] = nickname
        result = self._post("databases.setup.connect_existing", data)
        return DatabaseConnectionResult.model_validate(result)

    # Explorations
    def explorations_list(self, *, database_id: int, schema_oid: Optional[int] = None) -> List[ExplorationInfo]:
        data: Dict[str, Any] = {"database_id": database_id}
        if schema_oid is not None:
            data["schema_oid"] = schema_oid
        result = self._post("explorations.list", data)
        return [ExplorationInfo.model_validate(x) for x in result]

    def explorations_get(self, *, exploration_id: int) -> ExplorationInfo:
        result = self._post("explorations.get", {"exploration_id": exploration_id})
        return ExplorationInfo.model_validate(result)

    def explorations_add(self, *, exploration_def: ExplorationDef) -> ExplorationInfo:
        result = self._post("explorations.add", {"exploration_def": exploration_def.model_dump(mode="json")})
        return ExplorationInfo.model_validate(result)

    def explorations_delete(self, *, exploration_id: int) -> None:
        self._post("explorations.delete", {"exploration_id": exploration_id})
        return None

    def explorations_replace(self, *, new_exploration: ExplorationInfo) -> ExplorationInfo:
        result = self._post("explorations.replace", {"new_exploration": new_exploration.model_dump(mode="json")})
        return ExplorationInfo.model_validate(result)

    def explorations_run(
        self, *, exploration_def: ExplorationDef, limit: int = 100, offset: int = 0
    ) -> ExplorationResult:
        data = {
            "exploration_def": exploration_def.model_dump(mode="json"),
            "limit": limit,
            "offset": offset,
        }
        result = self._post("explorations.run", data)
        return ExplorationResult.model_validate(result)

    def explorations_run_saved(self, *, exploration_id: int, limit: int = 100, offset: int = 0) -> ExplorationResult:
        data = {"exploration_id": exploration_id, "limit": limit, "offset": offset}
        result = self._post("explorations.run_saved", data)
        return ExplorationResult.model_validate(result)

    # Forms
    def forms_list(self, *, database_id: int, schema_oid: int) -> List[FormInfo]:
        result = self._post("forms.list", {"database_id": database_id, "schema_oid": schema_oid})
        return [FormInfo.model_validate(x) for x in result]

    def forms_get(self, *, form_token: str) -> FormInfo:
        result = self._post("forms.get", {"form_token": form_token})
        return FormInfo.model_validate(result)

    def forms_add(self, *, form_def: AddFormDef) -> FormInfo:
        result = self._post("forms.add", {"form_def": form_def.model_dump(mode="json")})
        return FormInfo.model_validate(result)

    def forms_delete(self, *, form_id: int) -> None:
        self._post("forms.delete", {"form_id": form_id})
        return None

    def forms_regenerate_token(self, *, form_id: int) -> str:
        return self._post("forms.regenerate_token", {"form_id": form_id})

    def forms_patch(self, *, update_form_def: SettableFormDef) -> FormInfo:
        result = self._post("forms.patch", {"update_form_def": update_form_def.model_dump(mode="json")})
        return FormInfo.model_validate(result)

    def forms_set_publish_public(self, *, form_id: int, publish_public: bool) -> bool:
        return self._post("forms.set_publish_public", {"form_id": form_id, "publish_public": publish_public})

    def forms_submit(self, *, form_token: str, values: Dict[str, Any]) -> None:
        self._post("forms.submit", {"form_token": form_token, "values": values})
        return None

    def forms_list_related_records(
        self,
        *,
        form_token: str,
        field_key: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> RecordSummaryList:
        data: Dict[str, Any] = {"form_token": form_token, "field_key": field_key}
        if limit is not None:
            data["limit"] = limit
        if offset is not None:
            data["offset"] = offset
        if search is not None:
            data["search"] = search
        result = self._post("forms.list_related_records", data)
        return RecordSummaryList.model_validate(result)

    # Roles
    def roles_list(self, *, database_id: int) -> List[RoleInfo]:
        result = self._post("roles.list", {"database_id": database_id})
        return [RoleInfo.model_validate(x) for x in result]

    def roles_add(
        self, *, rolename: str, database_id: int, password: Optional[str] = None, login: Optional[bool] = None
    ) -> RoleInfo:
        data: Dict[str, Any] = {"rolename": rolename, "database_id": database_id}
        if password is not None:
            data["password"] = password
        if login is not None:
            data["login"] = login
        result = self._post("roles.add", data)
        return RoleInfo.model_validate(result)

    def roles_delete(self, *, role_oid: int, database_id: int) -> None:
        self._post("roles.delete", {"role_oid": role_oid, "database_id": database_id})
        return None

    def roles_get_current_role(self, *, database_id: int) -> Dict[str, Any]:
        return self._post("roles.get_current_role", {"database_id": database_id})

    def roles_set_members(self, *, parent_role_oid: int, members: List[int], database_id: int) -> RoleInfo:
        data = {"parent_role_oid": parent_role_oid, "members": members, "database_id": database_id}
        result = self._post("roles.set_members", data)
        return RoleInfo.model_validate(result)

    # Roles configured
    def roles_configured_list(self, *, server_id: int) -> List[ConfiguredRoleInfo]:
        result = self._post("roles.configured.list", {"server_id": server_id})
        return [ConfiguredRoleInfo.model_validate(x) for x in result]

    def roles_configured_add(self, *, server_id: int, name: str, password: str) -> ConfiguredRoleInfo:
        result = self._post("roles.configured.add", {"server_id": server_id, "name": name, "password": password})
        return ConfiguredRoleInfo.model_validate(result)

    def roles_configured_delete(self, *, configured_role_id: int) -> None:
        self._post("roles.configured.delete", {"configured_role_id": configured_role_id})
        return None

    def roles_configured_set_password(self, *, configured_role_id: int, password: str) -> None:
        self._post("roles.configured.set_password", {"configured_role_id": configured_role_id, "password": password})
        return None

    # Schemas
    def schemas_list(self, *, database_id: int) -> List[SchemaInfo]:
        result = self._post("schemas.list", {"database_id": database_id})
        return [SchemaInfo.model_validate(x) for x in result]

    def schemas_get(self, *, schema_oid: int, database_id: int) -> SchemaInfo:
        result = self._post("schemas.get", {"schema_oid": schema_oid, "database_id": database_id})
        return SchemaInfo.model_validate(result)

    def schemas_add(
        self, *, name: str, database_id: int, owner_oid: Optional[int] = None, description: Optional[str] = None
    ) -> SchemaInfo:
        data: Dict[str, Any] = {"name": name, "database_id": database_id}
        if owner_oid is not None:
            data["owner_oid"] = owner_oid
        if description is not None:
            data["description"] = description
        result = self._post("schemas.add", data)
        return SchemaInfo.model_validate(result)

    def schemas_delete(self, *, schema_oids: List[int], database_id: int) -> None:
        self._post("schemas.delete", {"schema_oids": schema_oids, "database_id": database_id})
        return None

    def schemas_patch(self, *, schema_oid: int, database_id: int, patch: SchemaPatch) -> SchemaInfo:
        data = {"schema_oid": schema_oid, "database_id": database_id, "patch": patch.model_dump(mode="json")}
        result = self._post("schemas.patch", data)
        return SchemaInfo.model_validate(result)

    # Schema privileges
    def schemas_privileges_list_direct(self, *, schema_oid: int, database_id: int) -> List[SchemaPrivileges]:
        result = self._post("schemas.privileges.list_direct", {"schema_oid": schema_oid, "database_id": database_id})
        return [SchemaPrivileges.model_validate(x) for x in result]

    def schemas_privileges_replace_for_roles(
        self, *, privileges: List[SchemaPrivileges], schema_oid: int, database_id: int
    ) -> List[SchemaPrivileges]:
        data = {
            "privileges": [p.model_dump(mode="json") for p in privileges],
            "schema_oid": schema_oid,
            "database_id": database_id,
        }
        result = self._post("schemas.privileges.replace_for_roles", data)
        return [SchemaPrivileges.model_validate(x) for x in result]

    def schemas_privileges_transfer_ownership(
        self, *, schema_oid: int, new_owner_oid: int, database_id: int
    ) -> SchemaInfo:
        data = {"schema_oid": schema_oid, "new_owner_oid": new_owner_oid, "database_id": database_id}
        result = self._post("schemas.privileges.transfer_ownership", data)
        return SchemaInfo.model_validate(result)

    # Tables
    def tables_list(self, *, schema_oid: int, database_id: int) -> List[TableInfo]:
        result = self._post("tables.list", {"schema_oid": schema_oid, "database_id": database_id})
        return [TableInfo.model_validate(x) for x in result]

    def tables_get(self, *, table_oid: int, database_id: int) -> TableInfo:
        result = self._post("tables.get", {"table_oid": table_oid, "database_id": database_id})
        return TableInfo.model_validate(result)

    def tables_add(
        self,
        *,
        schema_oid: int,
        database_id: int,
        table_name: Optional[str] = None,
        pkey_column_info: Optional[CreatablePkColumnInfo] = None,
        column_data_list: Optional[List[CreatableColumnInfo]] = None,
        constraint_data_list: Optional[List[CreatableConstraintInfo]] = None,
        owner_oid: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> AddedTableInfo:
        data: Dict[str, Any] = {"schema_oid": schema_oid, "database_id": database_id}
        if table_name is not None:
            data["table_name"] = table_name
        if pkey_column_info is not None:
            data["pkey_column_info"] = pkey_column_info.model_dump(mode="json")
        if column_data_list is not None:
            data["column_data_list"] = [c.model_dump(mode="json") for c in column_data_list]
        if constraint_data_list is not None:
            data["constraint_data_list"] = [c.model_dump(mode="json") for c in constraint_data_list]
        if owner_oid is not None:
            data["owner_oid"] = owner_oid
        if comment is not None:
            data["comment"] = comment
        result = self._post("tables.add", data)
        return AddedTableInfo.model_validate(result)

    def tables_delete(self, *, table_oid: int, database_id: int, cascade: bool = False) -> str:
        return self._post("tables.delete", {"table_oid": table_oid, "database_id": database_id, "cascade": cascade})

    def tables_patch(self, *, table_oid: int, table_data_dict: SettableTableInfo, database_id: int) -> str:
        data = {
            "table_oid": table_oid,
            "table_data_dict": table_data_dict.model_dump(mode="json"),
            "database_id": database_id,
        }
        return self._post("tables.patch", data)

    def tables_import(
        self,
        *,
        data_file_id: int,
        schema_oid: int,
        database_id: int,
        table_name: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> AddedTableInfo:
        data: Dict[str, Any] = {
            "data_file_id": data_file_id,
            "schema_oid": schema_oid,
            "database_id": database_id,
        }
        if table_name is not None:
            data["table_name"] = table_name
        if comment is not None:
            data["comment"] = comment
        result = self._post("tables.import", data)
        return AddedTableInfo.model_validate(result)

    def tables_get_import_preview(
        self,
        *,
        table_oid: int,
        columns: List[SettableColumnInfo],
        database_id: int,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        data = {
            "table_oid": table_oid,
            "columns": [c.model_dump(mode="json") for c in columns],
            "database_id": database_id,
            "limit": limit,
        }
        return self._post("tables.get_import_preview", data)

    def tables_list_joinable(self, *, table_oid: int, database_id: int, max_depth: int = 3) -> JoinableTableInfo:
        data = {"table_oid": table_oid, "database_id": database_id, "max_depth": max_depth}
        result = self._post("tables.list_joinable", data)
        return JoinableTableInfo.model_validate(result)

    def tables_list_with_metadata(self, *, schema_oid: int, database_id: int) -> List[Dict[str, Any]]:
        return self._post("tables.list_with_metadata", {"schema_oid": schema_oid, "database_id": database_id})

    def tables_get_with_metadata(self, *, table_oid: int, database_id: int) -> Dict[str, Any]:
        return self._post("tables.get_with_metadata", {"table_oid": table_oid, "database_id": database_id})

    # Tables metadata
    def tables_metadata_list(self, *, database_id: int) -> List[TableMetaDataRecord]:
        result = self._post("tables.metadata.list", {"database_id": database_id})
        return [TableMetaDataRecord.model_validate(x) for x in result]

    def tables_metadata_set(self, *, table_oid: int, metadata: TableMetaDataBlob, database_id: int) -> None:
        data = {"table_oid": table_oid, "metadata": metadata.model_dump(mode="json"), "database_id": database_id}
        self._post("tables.metadata.set", data)
        return None

    # Tables privileges
    def tables_privileges_list_direct(self, *, table_oid: int, database_id: int) -> List[TablePrivileges]:
        result = self._post("tables.privileges.list_direct", {"table_oid": table_oid, "database_id": database_id})
        return [TablePrivileges.model_validate(x) for x in result]

    def tables_privileges_replace_for_roles(
        self, *, privileges: List[TablePrivileges], table_oid: int, database_id: int
    ) -> List[TablePrivileges]:
        data = {
            "privileges": [p.model_dump(mode="json") for p in privileges],
            "table_oid": table_oid,
            "database_id": database_id,
        }
        result = self._post("tables.privileges.replace_for_roles", data)
        return [TablePrivileges.model_validate(x) for x in result]

    def tables_privileges_transfer_ownership(self, *, table_oid: int, new_owner_oid: int, database_id: int) -> TableInfo:
        data = {"table_oid": table_oid, "new_owner_oid": new_owner_oid, "database_id": database_id}
        result = self._post("tables.privileges.transfer_ownership", data)
        return TableInfo.model_validate(result)

    # Users
    def users_list(self) -> List[UserInfo]:
        result = self._post("users.list", {})
        return [UserInfo.model_validate(x) for x in result]

    def users_get(self, *, user_id: int) -> UserInfo:
        result = self._post("users.get", {"user_id": user_id})
        return UserInfo.model_validate(result)

    def users_add(self, *, user_def: UserDef) -> UserInfo:
        result = self._post("users.add", {"user_def": user_def.model_dump(mode="json")})
        return UserInfo.model_validate(result)

    def users_delete(self, *, user_id: int) -> None:
        self._post("users.delete", {"user_id": user_id})
        return None

    def users_patch_self(
        self, *, username: str, email: str, full_name: str, display_language: str
    ) -> UserInfo:
        data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "display_language": display_language,
        }
        result = self._post("users.patch_self", data)
        return UserInfo.model_validate(result)

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
        data = {
            "user_id": user_id,
            "username": username,
            "is_superuser": is_superuser,
            "email": email,
            "full_name": full_name,
            "display_language": display_language,
        }
        result = self._post("users.patch_other", data)
        return UserInfo.model_validate(result)

    def users_replace_own(self, *, old_password: str, new_password: str) -> None:
        self._post("users.replace_own", {"old_password": old_password, "new_password": new_password})
        return None

    def users_revoke(self, *, user_id: int, new_password: str) -> None:
        self._post("users.revoke", {"user_id": user_id, "new_password": new_password})
        return None


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
