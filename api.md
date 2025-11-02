# Methods - Mathesar Documentation
API Methods
---------------------------------------------

Analytics
-----------------------------------------

Classes and functions exposed to the RPC endpoint for managing analytics.

### analytics.get\_state 

Returns:



* Type:                   AnalyticsState            
  * Description:               A boolean to identify if analytics is enabled.            


### analytics.initialize 

Initialize analytics collection and reporting in Mathesar

If initialized, analytics are gathered to a local model once per day, and uploaded.

### analytics.disable 

Disable analytics collection and reporting in Mathesar

Disabling analytics amounts to (for now) simply deleting the Installation ID, ensuring that it’s impossible to save analytics reports. Any reports currently saved are removed when the Installation ID is deleted.

### analytics.view\_report 

View an example analytics report, prepared with the same function that creates real reports that would be saved and uploaded.

Returns:


|Type                                         |Description                                   |
|---------------------------------------------|----------------------------------------------|
|                  AnalyticsReport            |              An analytics report.            |


### analytics.upload\_feedback 

Upload a feedback message to Mathesar’s servers.

Parameters:



* Name:                 message            
  * Type:                   str            
  * Description:               The feedback message to send.            
  * Default:                 required            


### analytics.AnalyticsReport 

Bases: `TypedDict`

A report with some statistics about the data accessible by Mathesar.

Attributes:



* Name: installation_id
  * Type:                   Optional[str]            
  * Description:               A unique ID for this Mathesar installation.            
* Name: mathesar_version
  * Type:                   str            
  * Description:               The version of Mathesar.            
* Name: user_count
  * Type:                   int            
  * Description:               The number of configured users in Mathesar.            
* Name: active_user_count
  * Type:                   int            
  * Description:               The number of users who have recently logged in.            
* Name: configured_role_count
  * Type:                   int            
  * Description:               The number of DB roles configured.            
* Name: connected_database_count
  * Type:                   int            
  * Description:               The number of databases configured.            
* Name: connected_database_schema_count
  * Type:                   int            
  * Description:               The number of all schemas inall connected databases.            
* Name: connected_database_table_count
  * Type:                   int            
  * Description:               The total number of tables inall connected databasees.            
* Name: connected_database_record_count
  * Type:                   int            
  * Description:               The total number of records inall connected databasees (approximated)            
* Name: exploration_count
  * Type:                   int            
  * Description:               The number of explorations.            
* Name: form_count
  * Type:                   int            
  * Description:               The number of forms.            
* Name: public_form_count
  * Type:                   int            
  * Description:               The number of published forms.            


### analytics.AnalyticsState 

Bases: `TypedDict`

Returns the current state of analytics.

Attributes:



* Name: enabled
  * Type:                   bool            
  * Description:               A boolean representing if analytics is enabled.            


Collaborators
-------------------------------------------------

### collaborators.list\_ 

```
list_(*, database_id=None, **kwargs)

```


List information about collaborators. Exposed as `list`.

If called with no `database_id`, all collaborators for all databases are listed.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database associated with the collaborators.            
  * Default:                   None            


Returns:



* Type:                   list[CollaboratorInfo]            
  * Description:               A list of collaborators.            


### collaborators.add 

```
add(*, database_id, user_id, configured_role_id, **kwargs)

```


Set up a new collaborator for a database.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the Database to associate with the collaborator.            
  * Default:                 required            
* Name:                 user_id            
  * Type:                   int            
  * Description:               The Django id of the User model instance who’d be the collaborator.            
  * Default:                 required            
* Name:                 configured_role_id            
  * Type:                   int            
  * Description:               The Django id of the ConfiguredRole model instance to associate with the collaborator.            
  * Default:                 required            


### collaborators.delete 

```
delete(*, collaborator_id, **kwargs)

```


Delete a collaborator from a database.

Parameters:



* Name:                 collaborator_id            
  * Type:                   int            
  * Description:               The Django id of the UserDatabaseRoleMap model instance of the collaborator.            
  * Default:                 required            


### collaborators.set\_role 

```
set_role(*, collaborator_id, configured_role_id, **kwargs)

```


Set the role of a collaborator for a database.

Parameters:



* Name:                 collaborator_id            
  * Type:                   int            
  * Description:               The Django id of the UserDatabaseRoleMap model instance of the collaborator.            
  * Default:                 required            
* Name:                 configured_role_id            
  * Type:                   int            
  * Description:               The Django id of the ConfiguredRole model instance to associate with the collaborator.            
  * Default:                 required            


### collaborators.CollaboratorInfo 

Bases: `TypedDict`

Information about a collaborator.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               the Django ID of the UserDatabaseRoleMap model instance.            
* Name: user_id
  * Type:                   int            
  * Description:               The Django ID of the User model instance of the collaborator.            
* Name: database_id
  * Type:                   int            
  * Description:               the Django ID of the Database model instance for the collaborator.            
* Name: configured_role_id
  * Type:                   int            
  * Description:               The Django ID of the ConfiguredRole model instance for the collaborator.            


Columns
-------------------------------------

### columns.list\_ 

```
list_(*, table_oid, database_id, **kwargs)

```


List information about columns for a table. Exposed as `list`.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[ColumnInfo]            
  * Description:               A list of column details.            


### columns.add 

```
add(*, column_data_list, table_oid, database_id, **kwargs)

```


Add columns to a table.

There are defaults for both the name and type of a column, and so passing `[{}]` for `column_data_list` would add a single column of type `CHARACTER VARYING`, with an auto-generated name.

Parameters:



* Name:                 column_data_list            
  * Type:                   list[CreatableColumnInfo]            
  * Description:               A list describing desired columns to add.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table to which we’ll add columns.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[int]            
  * Description:               An array of the attnums of the new columns.            


### columns.add\_primary\_key\_column 

```
add_primary_key_column(
    *,
    pkey_type,
    table_oid,
    database_id,
    drop_existing_pkey_column=False,
    name="id",
    **kwargs
)

```


Add a primary key column to a table of a predefined type.

The column will be added, set as the primary key, and also filled for each preexisting row, using the default generating function or method associated with the given `pkey_type`.

If there is a name collision for the new primary key column, we automatically generate a non-colliding name for the new primary key column, and leave the existing table column names as they are.

Primary key types - ‘UUIDv4’: This results in a `uuid` primary key column, with default values generated by the `get_random_uuid()` function provided by PostgreSQL. This amounts to UUIDv4 uuid definitions. - ‘IDENTITY’: This results in an `integer` primary key column with default values created via an identity sequence, i.e., using `GENERATED BY DEFAULT AS IDENTITY`.

Parameters:



* Name:                 pkey_type            
  * Type:                   Literal['IDENTITY', 'UUIDv4']            
  * Description:               Defines the type and default of the primary key.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               The OID of the table getting a primary key.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 drop_existing_pkey_column            
  * Type:                   bool            
  * Description:               Whether to drop the old pkey column.            
  * Default:                   False            
* Name:                 name            
  * Type:                   str            
  * Description:               A custom name for the added primary key column.            
  * Default:                   'id'            


### columns.patch 

```
patch(
    *, column_data_list, table_oid, database_id, **kwargs
)

```


Alter details of preexisting columns in a table.

Does not support altering the type or type options of array columns.

Parameters:



* Name:                 column_data_list            
  * Type:                   list[SettableColumnInfo]            
  * Description:               A list describing desired column alterations.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table whose columns we’ll modify.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:


|Type                             |Description                                             |
|---------------------------------|--------------------------------------------------------|
|                  int            |              The number of columns altered.            |


### columns.delete 

```
delete(*, column_attnums, table_oid, database_id, **kwargs)

```


Delete columns from a table.

Parameters:



* Name:                 column_attnums            
  * Type:                   list[int]            
  * Description:               A list of attnums of columns to delete.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:


|Type                             |Description                                             |
|---------------------------------|--------------------------------------------------------|
|                  int            |              The number of columns dropped.            |


### columns.reset\_mash 

```
reset_mash(
    *, column_attnum, table_oid, database_id, **kwargs
)

```


Resets the outdated “mash” for a given file column.

Parameters:



* Name:                 column_attnum            
  * Type:                   int            
  * Description:               attnum of the file column whose mashes need to be reset.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table containing the file column.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


### columns.list\_with\_metadata 

```
list_with_metadata(*, table_oid, database_id, **kwargs)

```


List information about columns for a table, along with the metadata associated with each column. Args: table\_oid: Identity of the table in the user’s database. database\_id: The Django id of the database containing the table. Returns: A list of column details.

### columns.ColumnInfo 

Bases: `TypedDict`

Information about a column. Extends the settable fields.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The attnum of the column in the table.            
* Name: name
  * Type:                   str            
  * Description:               The name of the column.            
* Name: type
  * Type:                   str            
  * Description:               The type of the column on the database.            
* Name: type_options
  * Type:                   TypeOptions            
  * Description:               The options applied to the column type.            
* Name: nullable
  * Type:                   bool            
  * Description:               Whether or not the column is nullable.            
* Name: primary_key
  * Type:                   bool            
  * Description:               Whether the column is in the primary key.            
* Name: default
  * Type:                   ColumnDefault            
  * Description:               The default value and whether it’s dynamic.            
* Name: has_dependents
  * Type:                   bool            
  * Description:               Whether the column has dependent objects.            
* Name: description
  * Type:                   str            
  * Description:               The description of the column.            
* Name: current_role_priv
  * Type:                   list[Literal['SELECT', 'INSERT', 'UPDATE', 'REFERENCES']]            
  * Description:               The privileges available to the user for the column.            


### columns.CreatablePkColumnInfo 

Bases: `TypedDict`

Information needed to add a new PK column.

No keys are required.

Attributes:



* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the column.            
* Name: type
  * Type:                   Optional[Literal['IDENTITY', 'UUIDv4']]            
  * Description:               The type of the pk column on the database.            


### columns.CreatableColumnInfo 

Bases: `TypedDict`

Information needed to add a new column.

No keys are required.

Attributes:



* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the column.            
* Name: type
  * Type:                   Optional[str]            
  * Description:               The type of the column on the database.            
* Name: type_options
  * Type:                   Optional[TypeOptions]            
  * Description:               The options applied to the column type.            
* Name: nullable
  * Type:                   Optional[bool]            
  * Description:               Whether or not the column is nullable.            
* Name: default
  * Type:                   Optional[ColumnDefault]            
  * Description:               The default value.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the column.            


### columns.PreviewableColumnInfo 

Bases: `TypedDict`

Information needed to preview a column.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The attnum of the column in the table.            
* Name: type
  * Type:                   Optional[str]            
  * Description:               The new type to be applied to a column.            
* Name: type_options
  * Type:                   Optional[TypeOptions]            
  * Description:               The options to be applied to the column type.            


### columns.SettableColumnInfo 

Bases: `TypedDict`

Information about a column, restricted to settable fields.

When possible, Passing `null` for a key will clear the underlying setting. E.g.,

*   `default = null` clears the column default setting.
*   `type_options = null` clears the type options for the column.
*   `description = null` clears the column description.

Setting any of `name`, `type`, or `nullable` is a noop.

Only the `id` key is required.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The attnum of the column in the table.            
* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the column.            
* Name: type
  * Type:                   Optional[str]            
  * Description:               The type of the column on the database.            
* Name: cast_options
  * Type:                   Optional[dict]            
  * Description:               Suggestions to be used while type casting.            
* Name: type_options
  * Type:                   Optional[TypeOptions]            
  * Description:               The options applied to the column type.            
* Name: nullable
  * Type:                   Optional[bool]            
  * Description:               Whether or not the column is nullable.            
* Name: default
  * Type:                   Optional[ColumnDefault]            
  * Description:               The default value.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the column.            


### columns.TypeOptions 

Bases: `TypedDict`

Options applied to a type. All attributes are optional.

Take special care with the difference between numeric and date/time types w.r.t. precision. The attribute has a different meaning depending on the type to which it’s being applied.

Attributes:



* Name: precision
  * Type:                   int            
  * Description:               For numeric types, the number of significant digits.       For date/time types, the number of fractional digits.            
* Name: scale
  * Type:                   int            
  * Description:               For numeric types, the number of fractional digits.            
* Name: fields
  * Type:                   str            
  * Description:               Which time fields are stored. See Postgres docs.            
* Name: length
  * Type:                   int            
  * Description:               The maximum length of a character-type field.            
* Name: item_type
  * Type:                   str            
  * Description:               The member type for arrays.            


### columns.ColumnDefault 

Bases: `TypedDict`

A dictionary describing the default value for a column.

Attributes:



* Name: value
  * Type:                   str            
  * Description:               An SQL expression giving the default value.            
* Name: is_dynamic
  * Type:                   bool            
  * Description:               Whether the value is possibly dynamic.            


Classes and functions exposed to the RPC endpoint for managing column metadata.

### columns.metadata.list\_ 

```
list_(*, table_oid, database_id, **kwargs)

```


List metadata associated with columns for a table. Exposed as `list`.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[ColumnMetaDataRecord]            
  * Description:               A list of column meta data objects.            


### columns.metadata.set\_ 

```
set_(
    *,
    column_meta_data_list,
    table_oid,
    database_id,
    **kwargs
)

```


Set metadata associated with columns of a table for a database. Exposed as `set`.

Parameters:



* Name:                 column_meta_data_list            
  * Type:                   list[ColumnMetaDataBlob]            
  * Description:               A list describing desired metadata alterations.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table whose metadata we’ll modify.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


### columns.metadata.ColumnMetaDataRecord 

Bases: `TypedDict`

Metadata for a column in a table.

Only the `database`, `table_oid`, and `attnum` keys are required.

Attributes:



* Name: database_id
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
* Name: table_oid
  * Type:                   int            
  * Description:               The OID of the table containing the column.            
* Name: attnum
  * Type:                   int            
  * Description:               The attnum of the column in the table.            
* Name: bool_input
  * Type:                   Optional[Literal['dropdown', 'checkbox']]            
  * Description:               How the input for a boolean column should be shown.            
* Name: bool_true
  * Type:                   Optional[str]            
  * Description:               A string to display for true values.            
* Name: bool_false
  * Type:                   Optional[str]            
  * Description:               A string to display for false values.            
* Name: num_min_frac_digits
  * Type:                   Optional[int]            
  * Description:               Minimum digits shown after the decimal point.            
* Name: num_max_frac_digits
  * Type:                   Optional[int]            
  * Description:               Maximum digits shown after the decimal point.            
* Name: num_grouping
  * Type:                   Optional[str]            
  * Description:               Specifies how grouping separators are displayed for numeric values.            
* Name: num_format
  * Type:                   Optional[str]            
  * Description:               Specifies the locale-specific format for displaying numeric values.            
* Name: mon_currency_symbol
  * Type:                   Optional[str]            
  * Description:               The currency symbol shown for money value.            
* Name: mon_currency_location
  * Type:                   Optional[Literal['after-minus', 'end-with-space']]            
  * Description:               Where the currency symbol should be shown.            
* Name: time_format
  * Type:                   Optional[str]            
  * Description:               A string representing the format of time values.            
* Name: date_format
  * Type:                   Optional[str]            
  * Description:               A string representing the format of date values.            
* Name: duration_min
  * Type:                   Optional[str]            
  * Description:               The smallest unit for displaying durations.            
* Name: duration_max
  * Type:                   Optional[str]            
  * Description:               The largest unit for displaying durations.            
* Name: display_width
  * Type:                   Optional[int]            
  * Description:               The pixel width of the column            
* Name: file_backend
  * Type:                   Optional[int]            
  * Description:               The name of a backend for storing file attachments.            


### columns.metadata.ColumnMetaDataBlob 

Bases: `TypedDict`

The metadata fields which can be set for a column in a table.

Attributes:



* Name: attnum
  * Type:                   int            
  * Description:               The attnum of the column in the table.            
* Name: bool_input
  * Type:                   Optional[Literal['dropdown', 'checkbox']]            
  * Description:               How the input for a boolean column should be shown.            
* Name: bool_true
  * Type:                   Optional[str]            
  * Description:               A string to display for true values.            
* Name: bool_false
  * Type:                   Optional[str]            
  * Description:               A string to display for false values.            
* Name: num_min_frac_digits
  * Type:                   Optional[int]            
  * Description:               Minimum digits shown after the decimal point.            
* Name: num_max_frac_digits
  * Type:                   Optional[int]            
  * Description:               Maximum digits shown after the decimal point.            
* Name: num_grouping
  * Type:                   Optional[str]            
  * Description:               Specifies how grouping separators are displayed for numeric values.            
* Name: num_format
  * Type:                   Optional[str]            
  * Description:               Specifies the locale-specific format for displaying numeric values.            
* Name: mon_currency_symbol
  * Type:                   Optional[str]            
  * Description:               The currency symbol shown for money value.            
* Name: mon_currency_location
  * Type:                   Optional[Literal['after-minus', 'end-with-space']]            
  * Description:               Where the currency symbol should be shown.            
* Name: time_format
  * Type:                   Optional[str]            
  * Description:               A string representing the format of time values.            
* Name: date_format
  * Type:                   Optional[str]            
  * Description:               A string representing the format of date values.            
* Name: duration_min
  * Type:                   Optional[str]            
  * Description:               The smallest unit for displaying durations.            
* Name: duration_max
  * Type:                   Optional[str]            
  * Description:               The largest unit for displaying durations.            
* Name: display_width
  * Type:                   Optional[int]            
  * Description:               The pixel width of the column.            
* Name: file_backend
  * Type:                   Optional[int]            
  * Description:               The name of a backend for storing file attachments.            


Configured Databases
---------------------------------------------------------------

### databases.configured.list\_ 

```
list_(*, server_id=None, **kwargs)

```


List information about databases for a server. Exposed as `list`.

If called with no `server_id`, all databases for all servers are listed.

Parameters:



* Name:                 server_id            
  * Type:                   int            
  * Description:               The Django id of the server containing the databases.            
  * Default:                   None            


Returns:



* Type:                   list[ConfiguredDatabaseInfo]            
  * Description:               A list of database details.            


### databases.configured.patch 

```
patch(*, database_id, patch, **kwargs)

```


Patch a configured database, given its id.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database            
  * Default:                 required            
* Name:                 patch            
  * Type:                   ConfiguredDatabasePatch            
  * Description:               An object containing the fields to update.            
  * Default:                 required            


Returns:



* Type:                   ConfiguredDatabaseInfo            
  * Description:               An object describing the database.            


### databases.configured.disconnect 

```
disconnect(
    *,
    database_id,
    schemas_to_remove=["msar", "__msar", "mathesar_types"],
    strict=True,
    role_name=None,
    password=None,
    disconnect_db_server=False
)

```


Disconnect a configured database, after removing Mathesar SQL from it.

If no `role_name` and `password` are submitted, we will determine the role which owns the `msar` schema on the database, then use that role for the SQL removal.

All removals are performed safely, and without `CASCADE`. This is to make sure the user can’t accidentally lose data calling this function.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            
* Name:                 schemas_to_remove            
  * Type:                   list[str]            
  * Description:               Mathesar schemas we should remove SQL from.            
  * Default:                   ['msar', '__msar', 'mathesar_types']            
* Name:                 strict            
  * Type:                   bool            
  * Description:               If True, we throw an exception and roll back changes ifwe fail to remove any objects which we expected to remove.            
  * Default:                   True            
* Name:                 role_name            
  * Type:                   str            
  * Description:               the username of the role used for upgrading.            
  * Default:                   None            
* Name:                 password            
  * Type:                   str            
  * Description:               the password of the role used for upgrading.            
  * Default:                   None            
* Name:                 disconnect_db_server            
  * Type:                   bool            
  * Description:               If True, will delete the stored servermetadata(host, port, role credentials) from Mathesar.This is intended for optional use while disconnecting thelast database on the server.            
  * Default:                   False            


### databases.configured.ConfiguredDatabaseInfo 

Bases: `TypedDict`

Information about a database.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               the Django ID of the database model instance.            
* Name: name
  * Type:                   str            
  * Description:               The name of the database on the server.            
* Name: server_id
  * Type:                   int            
  * Description:               the Django ID of the server model instance for the database.            
* Name: last_confirmed_sql_version
  * Type:                   str            
  * Description:               The last version of the SQL scripts whichwere confirmed to have been run on this database.            
* Name: needs_upgrade_attention
  * Type:                   bool            
  * Description:               This is True if the SQL version isn’t thesame as the service version.            
* Name: nickname
  * Type:                   Optional[str]            
  * Description:               A optional user-configurable name for the database.            


### databases.configured.ConfiguredDatabasePatch 

Bases: `TypedDict`

Information to be changed about a configured database

Attributes:



* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the database on the server.            
* Name: nickname
  * Type:                   Optional[str]            
  * Description:               A optional user-configurable name for the database.            


Constraints
---------------------------------------------

Classes and functions exposed to the RPC endpoint for managing table constraints.

### constraints.list\_ 

```
list_(*, table_oid, database_id, **kwargs)

```


List information about constraints in a table. Exposed as `list`.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               The oid of the table to list constraints for.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[ConstraintInfo]            
  * Description:               A list of constraint details.            


### constraints.add 

```
add(
    *, table_oid, constraint_def_list, database_id, **kwargs
)

```


Add constraint(s) on a table in bulk.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table to delete constraint for.            
  * Default:                 required            
* Name:                 constraint_def_list            
  * Type:                   CreatableConstraintInfo            
  * Description:               A list describing the constraints to add.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[int]            
  * Description:               The oid(s) of all the constraints on the table.            


### constraints.delete 

```
delete(*, table_oid, constraint_oid, database_id, **kwargs)

```


Delete a constraint from a table.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table to delete constraint for.            
  * Default:                 required            
* Name:                 constraint_oid            
  * Type:                   int            
  * Description:               The OID of the constraint to delete.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:


|Type                             |Description                                                  |
|---------------------------------|-------------------------------------------------------------|
|                  str            |              The name of the dropped constraint.            |


### constraints.ForeignKeyConstraint 

Bases: `TypedDict`

Information about a foreign key constraint.

Attributes:



* Name: type
  * Type:                   str            
  * Description:               The type of the constraint('f' for foreign key constraint).            
* Name: columns
  * Type:                   list[int]            
  * Description:               List of columns to set a foreign key on.            
* Name: fkey_relation_id
  * Type:                   int            
  * Description:               The OID of the referent table.            
* Name: fkey_columns
  * Type:                   list[int]            
  * Description:               List of referent column(s).            
* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the constraint.            
* Name: deferrable
  * Type:                   Optional[bool]            
  * Description:               Whether to postpone constraint checking until the end of the transaction.            
* Name: fkey_update_action
  * Type:                   Optional[str]            
  * Description:               Specifies what action should be taken when the referenced key is updated.Valid options include 'a'(no action)(default behavior), 'r'(restrict), 'c'(cascade), 'n'(set null), 'd'(set default)            
* Name: fkey_delete_action
  * Type:                   Optional[str]            
  * Description:               Specifies what action should be taken when the referenced key is deleted.Valid options include 'a'(no action)(default behavior), 'r'(restrict), 'c'(cascade), 'n'(set null), 'd'(set default)            
* Name: fkey_match_type
  * Type:                   Optional[str]            
  * Description:               Specifies how the foreign key matching should be performed.Valid options include 'f'(full match), 's'(simple match)(default behavior).            


### constraints.PrimaryKeyConstraint 

Bases: `TypedDict`

Information about a primary key constraint.

Attributes:



* Name: type
  * Type:                   str            
  * Description:               The type of the constraint('p' for primary key constraint).            
* Name: columns
  * Type:                   list[int]            
  * Description:               List of columns to set a primary key on.            
* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the constraint.            
* Name: deferrable
  * Type:                   Optional[bool]            
  * Description:               Whether to postpone constraint checking until the end of the transaction.            


### constraints.UniqueConstraint 

Bases: `TypedDict`

Information about a unique constraint.

Attributes:



* Name: type
  * Type:                   str            
  * Description:               The type of the constraint('u' for unique constraint).            
* Name: columns
  * Type:                   list[int]            
  * Description:               List of columns to set a unique constraint on.            
* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the constraint.            
* Name: deferrable
  * Type:                   Optional[bool]            
  * Description:               Whether to postpone constraint checking until the end of the transaction.            


### constraints.CreatableConstraintInfo `module-attribute` 

```
CreatableConstraintInfo = list[
    Union[
        ForeignKeyConstraint,
        PrimaryKeyConstraint,
        UniqueConstraint,
    ]
]

```


Type alias for a list of creatable constraints which can be unique, primary key, or foreign key constraints.

Data Modeling
-------------------------------------------------

Classes and functions exposed to the RPC endpoint for managing data models.

### data\_modeling.add\_foreign\_key\_column 

```
add_foreign_key_column(
    *,
    column_name,
    referrer_table_oid,
    referent_table_oid,
    database_id,
    **kwargs
)

```


Add a foreign key column to a table.

The foreign key column will be newly created, and will reference the `id` column of the referent table.

Parameters:



* Name:                 column_name            
  * Type:                   str            
  * Description:               The name of the column to create.            
  * Default:                 required            
* Name:                 referrer_table_oid            
  * Type:                   int            
  * Description:               The OID of the table getting the new column.            
  * Default:                 required            
* Name:                 referent_table_oid            
  * Type:                   int            
  * Description:               The OID of the table being referenced.            
  * Default:                 required            


### data\_modeling.add\_mapping\_table 

```
add_mapping_table(
    *,
    table_name,
    mapping_columns,
    schema_oid,
    database_id,
    **kwargs
)

```


Add a mapping table to give a many-to-many link between referents.

The foreign key columns in the mapping table will reference the `id` column of the referent tables.

Parameters:



* Name:                 table_name            
  * Type:                   str            
  * Description:               The name for the new mapping table.            
  * Default:                 required            
* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the schema for the mapping table.            
  * Default:                 required            
* Name:                 mapping_columns            
  * Type:                   list[MappingColumn]            
  * Description:               The foreign key columns to create in themapping table.            
  * Default:                 required            


### data\_modeling.suggest\_types 

```
suggest_types(*, table_oid, database_id, **kwargs)

```


Infer the best type for each column in the table.

Currently we only suggest different types for columns which originate as type `text`.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               The OID of the table whose columns we’re inferring types for.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


The response JSON will have attnum keys, and values will be the result of `format_type` for the inferred type of each column, i.e., the canonical string referring to the type.

### data\_modeling.split\_table 

```
split_table(
    *,
    table_oid,
    column_attnums,
    extracted_table_name,
    database_id,
    relationship_fk_column_name=None,
    **kwargs
)

```


Extract columns from a table to create a new table, linked by a foreign key.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               The OID of the table whose columns we’ll extract.            
  * Default:                 required            
* Name:                 column_attnums            
  * Type:                   list            
  * Description:               A list of the attnums of the columns to extract.            
  * Default:                 required            
* Name:                 extracted_table_name            
  * Type:                   str            
  * Description:               The name of the new table to be made from the extracted columns.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 relationship_fk_column_name            
  * Type:                   str            
  * Description:               The name to give the new foreign key column in the remainder table (optional)            
  * Default:                   None            


Returns:



* Type:                   SplitTableInfo            
  * Description:               The SplitTableInfo object describing the details for the created table as a result of column extraction.            


### data\_modeling.move\_columns 

```
move_columns(
    *,
    source_table_oid,
    target_table_oid,
    move_column_attnums,
    database_id,
    **kwargs
)

```


Extract columns from a table to a referent table, linked by a foreign key.

Parameters:



* Name:                 source_table_oid            
  * Type:                   int            
  * Description:               The OID of the source table whose column(s) we’ll extract.            
  * Default:                 required            
* Name:                 target_table_oid            
  * Type:                   int            
  * Description:               The OID of the target table where the extracted column(s) will be added.            
  * Default:                 required            
* Name:                 move_column_attnums            
  * Type:                   list[int]            
  * Description:               The list of attnum(s) to move from source table to the target table.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


### data\_modeling.MappingColumn 

Bases: `TypedDict`

An object defining a foreign key column in a mapping table.

Attributes:



* Name: column_name
  * Type:                   str            
  * Description:               The name of the foreign key column.            
* Name: referent_table_oid
  * Type:                   int            
  * Description:               The OID of the table the column references.            


### data\_modeling.SplitTableInfo 

Bases: `TypedDict`

Information about a table, created from column extraction.

Attributes:



* Name: extracted_table_oid
  * Type:                   int            
  * Description:               The OID of the table that is created from column extraction.            
* Name: new_fkey_attnum
  * Type:                   int            
  * Description:               The attnum of the newly created foreign key column             referring the extracted_table on the original table.            


Databases
-----------------------------------------

### databases.get 

```
get(*, database_id, **kwargs)

```


Get information about a database.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            


Returns:



* Type:                   DatabaseInfo            
  * Description:               Information about the database, and the current user privileges.            


### databases.delete 

```
delete(*, database_oid, database_id, **kwargs)

```


Drop a database from the server.

Parameters:



* Name:                 database_oid            
  * Type:                   int            
  * Description:               The OID of the database to delete on the database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database to connect to.            
  * Default:                 required            


### databases.upgrade\_sql 

```
upgrade_sql(*, database_id, username=None, password=None)

```


Install, Upgrade, or Reinstall the Mathesar SQL on a database.

If no `username` and `password` are submitted, we will determine the role which owns the `msar` schema on the database, then use that role for the upgrade.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            
* Name:                 username            
  * Type:                   str            
  * Description:               The username of the role used for upgrading.            
  * Default:                   None            
* Name:                 password            
  * Type:                   str            
  * Description:               The password of the role used for upgrading.            
  * Default:                   None            


### databases.DatabaseInfo 

Bases: `TypedDict`

Information about a database current user privileges on it.

Attributes:



* Name: oid
  * Type:                   int            
  * Description:               The oid of the database on the server.            
* Name: name
  * Type:                   str            
  * Description:               The name of the database on the server.            
* Name: owner_oid
  * Type:                   int            
  * Description:               The oid of the owner of the database.            
* Name: current_role_priv
  * Type:                   list[Literal['CONNECT', 'CREATE', 'TEMPORARY']]            
  * Description:               A list of privileges available to the user.            
* Name: current_role_owns
  * Type:                   bool            
  * Description:               Whether the user is an owner of the database.            


Database Privileges
-------------------------------------------------------------

### databases.privileges.list\_direct 

```
list_direct(*, database_id, **kwargs)

```


List database privileges for non-inherited roles.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            


Returns:



* Type:                   list[DBPrivileges]            
  * Description:               A list of database privileges.            


### databases.privileges.replace\_for\_roles 

```
replace_for_roles(*, privileges, database_id, **kwargs)

```


Replace direct database privileges for roles.

Possible privileges are `CONNECT`, `CREATE`, and `TEMPORARY`.

Only roles which are included in a passed `DBPrivileges` object are affected.

WARNING: Any privilege included in the `direct` list for a role is GRANTed, and any privilege not included is REVOKEd.

Attributes:


|Name       |Type        |Description                                                |
|-----------|------------|-----------------------------------------------------------|
|privileges |            |              The new privilege sets for roles.            |
|database_id|            |              The Django id of the database.               |


Returns:



* Type:                   list[DBPrivileges]            
  * Description:               A list of all non-default privileges on the database after the            
* Type:                   list[DBPrivileges]            
  * Description:               operation.            


### databases.privileges.transfer\_ownership 

```
transfer_ownership(*, new_owner_oid, database_id, **kwargs)

```


Transfers ownership of the current database to a new owner.

Attributes:



* Name: new_owner_oid
  * Type:             
  * Description:               The OID of the role whom we want to be the new owner of the current database.            
* Name: database_id
  * Type:             
  * Description:               The Django id of the database whose ownership is to be transferred.            


To successfully transfer ownership of a database to a new owner the current user must:

*   Be a Superuser/Owner of the current database.
*   Be a `MEMBER` of the new owning role. i.e. The current role should be able to `SET ROLE` to the new owning role.
*   Have `CREATEDB` privilege.

Returns:



* Type:                   DatabaseInfo            
  * Description:               Information about the database, and the current user privileges.            


### databases.privileges.DBPrivileges 

Bases: `TypedDict`

Information about database privileges.

Attributes:



* Name: role_oid
  * Type:                   int            
  * Description:               The oid of the role on the database server.            
* Name: direct
  * Type:                   list[Literal['CONNECT', 'CREATE', 'TEMPORARY']]            
  * Description:               A list of database privileges for the aforementioned role_oid.            


Database Setup
---------------------------------------------------

RPC functions for setting up database connections.

### databases.setup.create\_new 

```
create_new(
    *, database, sample_data=[], nickname=None, **kwargs
)

```


Set up a new database on the internal server.

The calling user will get access to that database using the default role stored in Django settings.

Parameters:



* Name:                 database            
  * Type:                   str            
  * Description:               The name of the new database.            
  * Default:                 required            
* Name:                 sample_data            
  * Type:                   list[str]            
  * Description:               A list of strings requesting that some example datasets be installed on the underlying database. Valid listmembers are:- ‘bike_shop’- ‘hardware_store’- ‘ice_cream_employees’- ‘library_management’- ‘library_makerspace’- ‘movie_rentals’- ‘museum_exhibits’- ‘nonprofit_grants’            
  * Default:                   []            
* Name:                 nickname            
  * Type:                   Optional[str]            
  * Description:               An optional nickname for the database.            
  * Default:                   None            


### databases.setup.connect\_existing 

```
connect_existing(
    *,
    host,
    port=None,
    database,
    role,
    password,
    sample_data=[],
    nickname=None,
    **kwargs
)

```


Connect Mathesar to an existing database on a server.

The calling user will get access to that database using the credentials passed to this function.

Parameters:



* Name:                 host            
  * Type:                   str            
  * Description:               The host of the database server.            
  * Default:                 required            
* Name:                 port            
  * Type:                   Optional[int]            
  * Description:               The port of the database server.            
  * Default:                   None            
* Name:                 database            
  * Type:                   str            
  * Description:               The name of the database on the server.            
  * Default:                 required            
* Name:                 role            
  * Type:                   str            
  * Description:               The role on the server to use for the connection.            
  * Default:                 required            
* Name:                 password            
  * Type:                   str            
  * Description:               A password valid for the role.            
  * Default:                 required            
* Name:                 sample_data            
  * Type:                   list[str]            
  * Description:               A list of strings requesting that some example datasets be installed on the underlying database. Valid listmembers are:- ‘bike_shop’- ‘hardware_store’- ‘ice_cream_employees’- ‘library_management’- ‘library_makerspace’- ‘movie_rentals’- ‘museum_exhibits’- ‘nonprofit_grants’            
  * Default:                   []            
* Name:                 nickname            
  * Type:                   Optional[str]            
  * Description:               An optional nickname for the database.            
  * Default:                   None            


### databases.setup.DatabaseConnectionResult 

Bases: `TypedDict`

Info about the objects resulting from calling the setup functions.

These functions will get or create an instance of the Server, Database, and ConfiguredRole models, as well as a UserDatabaseRoleMap entry.

Attributes:



* Name: server
  * Type:                   ConfiguredServerInfo            
  * Description:               Information on the Server model instance.            
* Name: database
  * Type:                   ConfiguredDatabaseInfo            
  * Description:               Information on the Database model instance.            
* Name: configured_role
  * Type:                   ConfiguredRoleInfo            
  * Description:               Information on the ConfiguredRole model instance.            


Explorations
-----------------------------------------------

Classes and functions exposed to the RPC endpoint for managing explorations.

### explorations.list\_ 

```
list_(*, database_id, schema_oid=None, **kwargs)

```


List information about explorations for a database. Exposed as `list`.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the explorations.            
  * Default:                 required            
* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the schema containing the base table(s) of the exploration(s).(optional)            
  * Default:                   None            


Returns:



* Type:                   list[ExplorationInfo]            
  * Description:               A list of exploration details.            


### explorations.get 

```
get(*, exploration_id, **kwargs)

```


List information about an exploration.

Parameters:



* Name:                 exploration_id            
  * Type:                   int            
  * Description:               The Django id of the exploration.            
  * Default:                 required            


Returns:



* Type:                   ExplorationInfo            
  * Description:               Exploration details for a given exploration_id.            


### explorations.add 

Add a new exploration.

Parameters:



* Name:                 exploration_def            
  * Type:                   ExplorationDef            
  * Description:               A dict describing the exploration to create.            
  * Default:                 required            


Returns:



* Type:                   ExplorationInfo            
  * Description:               The exploration details for the newly created exploration.            


### explorations.delete 

```
delete(*, exploration_id, **kwargs)

```


Delete an exploration.

Parameters:



* Name:                 exploration_id            
  * Type:                   int            
  * Description:               The Django id of the exploration to delete.            
  * Default:                 required            


### explorations.replace 

```
replace(*, new_exploration)

```


Replace a saved exploration.

Parameters:



* Name:                 new_exploration            
  * Type:                   ExplorationInfo            
  * Description:               A dict describing the exploration to replace, including the updated fields.            
  * Default:                 required            


Returns:



* Type:                   ExplorationInfo            
  * Description:               The exploration details for the replaced exploration.            


### explorations.run 

```
run(*, exploration_def, limit=100, offset=0, **kwargs)

```


Run an exploration.

Parameters:



* Name:                 exploration_def            
  * Type:                   ExplorationDef            
  * Description:               A dict describing an exploration to run.            
  * Default:                 required            
* Name:                 limit            
  * Type:                   int            
  * Description:               The max number of rows to return.(default 100)            
  * Default:                   100            
* Name:                 offset            
  * Type:                   int            
  * Description:               The number of rows to skip.(default 0)            
  * Default:                   0            


Returns:



* Type:                   ExplorationResult            
  * Description:               The result of the exploration run.            


### explorations.run\_saved 

```
run_saved(*, exploration_id, limit=100, offset=0, **kwargs)

```


Run a saved exploration.

Parameters:



* Name:                 exploration_id            
  * Type:                   int            
  * Description:               The Django id of the exploration to run.            
  * Default:                 required            
* Name:                 limit            
  * Type:                   int            
  * Description:               The max number of rows to return.(default 100)            
  * Default:                   100            
* Name:                 offset            
  * Type:                   int            
  * Description:               The number of rows to skip.(default 0)            
  * Default:                   0            


Returns:



* Type:                   ExplorationResult            
  * Description:               The result of the exploration run.            


### explorations.ExplorationInfo 

Bases: `TypedDict`

Information about an exploration.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The Django id of an exploration.            
* Name: database_id
  * Type:                   int            
  * Description:               The Django id of the database containing the exploration.            
* Name: name
  * Type:                   str            
  * Description:               The name of the exploration.            
* Name: base_table_oid
  * Type:                   int            
  * Description:               The OID of the base table of the exploration on the database.            
* Name: schema_oid
  * Type:                   int            
  * Description:               The OID of the schema containing the base table of the exploration.            
* Name: initial_columns
  * Type:                   list            
  * Description:               A list describing the columns to be included in the exploration.            
* Name: transformations
  * Type:                   Optional[list]            
  * Description:               A list describing the transformations to be made on the included columns.            
* Name: display_options
  * Type:                   Optional[list]            
  * Description:               A list describing metadata for the columns in the explorations.            
* Name: display_names
  * Type:                   Optional[dict]            
  * Description:               A map between the actual column names on the database and the alias to be displayed(if any).            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the exploration.            


### explorations.ExplorationDef 

Bases: `TypedDict`

Definition about a runnable exploration.

Attributes:



* Name: database_id
  * Type:                   int            
  * Description:               The Django id of the database containing the exploration.            
* Name: name
  * Type:                   str            
  * Description:               The name of the exploration.            
* Name: base_table_oid
  * Type:                   int            
  * Description:               The OID of the base table of the exploration on the database.            
* Name: schema_oid
  * Type:                   int            
  * Description:               The OID of the schema containing the base table of the exploration.            
* Name: initial_columns
  * Type:                   list            
  * Description:               A list describing the columns to be included in the exploration.            
* Name: transformations
  * Type:                   Optional[list]            
  * Description:               A list describing the transformations to be made on the included columns.            
* Name: display_options
  * Type:                   Optional[list]            
  * Description:               A list describing metadata for the columns in the explorations.            
* Name: display_names
  * Type:                   Optional[dict]            
  * Description:               A map between the actual column names on the database and the alias to be displayed(if any).            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the exploration.            


### explorations.ExplorationResult 

Bases: `TypedDict`

Result of an exploration run.

Attributes:



* Name: query
  * Type:                   dict            
  * Description:               A dict describing the exploration that ran.            
* Name: records
  * Type:                   dict            
  * Description:               A dict describing the total count of records along with the contents of those records.            
* Name: output_columns
  * Type:                   tuple            
  * Description:               A tuple describing the names of the columns included in the exploration.            
* Name: column_metadata
  * Type:                   dict            
  * Description:               A dict describing the metadata applied to included columns.            
* Name: limit
  * Type:                   Optional[int]            
  * Description:               Specifies the max number of rows returned.(default 100)            
* Name: offset
  * Type:                   Optional[int]            
  * Description:               Specifies the number of rows skipped.(default 0)            


Forms
---------------------------------

Classes and functions exposed to the RPC endpoint for managing forms.

### forms.list\_ 

```
list_(*, database_id, schema_oid, **kwargs)

```


List information about forms for a database. Exposed as `list`.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the form.            
  * Default:                 required            
* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the schema containing the base table(s) of the forms(s).            
  * Default:                 required            


Returns:


|Type                                  |Description                                   |
|--------------------------------------|----------------------------------------------|
|                  FormInfo            |              A list of form info.            |


### forms.get 

```
get(*, form_token, **kwargs)

```


List information about a form.

Parameters:



* Name:                 form_token            
  * Type:                   str            
  * Description:               The unique token of the form.            
  * Default:                 required            


Returns:



* Type:                   FormInfo            
  * Description:               Form details for a given form_token.            


### forms.add 

```
add(*, form_def, **kwargs)

```


Add a new form.

Parameters:



* Name:                 form_def            
  * Type:                   AddFormDef            
  * Description:               A dict describing the form to create.            
  * Default:                 required            


Returns:



* Type:                   FormInfo            
  * Description:               The details for the newly created form.            


### forms.delete 

```
delete(*, form_id, **kwargs)

```


Delete a form.

Parameters:



* Name:                 form_id            
  * Type:                   int            
  * Description:               The Django id of the form to delete.            
  * Default:                 required            


### forms.regenerate\_token 

```
regenerate_token(*, form_id, **kwargs)

```


Regenerate the unique token for a form.

Parameters:



* Name:                 form_id            
  * Type:                   int            
  * Description:               The Django id of the form.            
  * Default:                 required            


Returns:


|Type                             |Description                                          |
|---------------------------------|-----------------------------------------------------|
|                  str            |              The new token for the form.            |


### forms.patch 

```
patch(*, update_form_def, **kwargs)

```


Update a form.

Parameters:



* Name:                 update_form_def            
  * Type:                   SettableFormDef            
  * Description:               A dict describing the form to update, including the updated fields.            
  * Default:                 required            


Returns:



* Type:                   FormInfo            
  * Description:               The form info for the updated form.            


### forms.set\_publish\_public 

```
set_publish_public(*, form_id, publish_public, **kwargs)

```


Set/Unset the form to be publicly shareable.

Parameters:



* Name:                 form_id            
  * Type:                   int            
  * Description:               The Django id of the form.            
  * Default:                 required            
* Name:                 publish_public            
  * Type:                   bool            
  * Description:               Specify whether to share the form publicly.            
  * Default:                 required            


Returns:



* Type:                   bool            
  * Description:               The updated state of public sharing for the form.            


### forms.submit 

```
submit(*, form_token, values, **kwargs)

```


Submit a form.

Parameters:



* Name:                 form_token            
  * Type:                   str            
  * Description:               The unique token of the form.            
  * Default:                 required            
* Name:                 values            
  * Type:                   dict            
  * Description:               A dict describing the values to insert.            
  * Default:                 required            


```
list_related_records(
    *,
    form_token,
    field_key,
    limit=None,
    offset=None,
    search=None,
    **kwargs
)

```


List records for selection via the row seeker

Parameters:



* Name:                 form_token            
  * Type:                   str            
  * Description:               The unique token of the form.            
  * Default:                 required            
* Name:                 field_key            
  * Type:                   str            
  * Description:               The key of the foreign key field for which to list related records.            
  * Default:                 required            
* Name:                 limit            
  * Type:                   Optional[int]            
  * Description:               Optional limit on the number of records to return.            
  * Default:                   None            
* Name:                 offset            
  * Type:                   Optional[int]            
  * Description:               Optional offset for pagination.            
  * Default:                   None            
* Name:                 search            
  * Type:                   Optional[str]            
  * Description:               Optional search term to filter records.            
  * Default:                   None            


Returns:



* Type:                   RecordSummaryList            
  * Description:               The requested records, along with some metadata.            


### forms.FormInfo 

Bases: `TypedDict`

Information about a form.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The Django id of the Form on the database.            
* Name: created_at
  * Type:                   str            
  * Description:               The time at which the form model got created.            
* Name: updated_at
  * Type:                   str            
  * Description:               The time at which the form model was last updated.            
* Name: token
  * Type:                   str            
  * Description:               A UUIDv4 object used to identify a form uniquely.            
* Name: name
  * Type:                   str            
  * Description:               The name of the form.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the form.            
* Name: version
  * Type:                   int            
  * Description:               The version of the form for reconciliation of json fields.            
* Name: database_id
  * Type:                   int            
  * Description:               The Django id of the database containing the Form.            
* Name: schema_oid
  * Type:                   int            
  * Description:               The OID of the schema where within which form exists.            
* Name: base_table_oid
  * Type:                   int            
  * Description:               The table OID based on which a form will be created.            
* Name: associated_role_id
  * Type:                   Optional[int]            
  * Description:               The Django id of the configured role to be used while submitting a form.            
* Name: header_title
  * Type:                   dict            
  * Description:               The title of the rendered form.            
* Name: header_subtitle
  * Type:                   Optional[dict]            
  * Description:               The subtitle of the rendered form.            
* Name: publish_public
  * Type:                   bool            
  * Description:               Specifies whether the form is publicly accessible.            
* Name: submit_message
  * Type:                   Optional[dict]            
  * Description:               Message to be displayed upon submission.            
* Name: submit_redirect_url
  * Type:                   Optional[str]            
  * Description:               Redirect path after submission.            
* Name: submit_button_label
  * Type:                   Optional[str]            
  * Description:               Text to be displayed on the submit button.            
* Name: fields
  * Type:                   list[FieldInfo]            
  * Description:               Definition of Fields within the form.            


### forms.FieldInfo 

Bases: `TypedDict`

Information about a form field.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The Django id of the Field on the database.            
* Name: key
  * Type:                   str            
  * Description:               A unique string identifier for the field within a form.            
* Name: form_id
  * Type:                   int            
  * Description:               The Django id of the Form on the database.            
* Name: index
  * Type:                   int            
  * Description:               The order in which the field should be displayed.            
* Name: label
  * Type:                   Optional[str]            
  * Description:               The text to be displayed for the field input.            
* Name: help
  * Type:                   Optional[str]            
  * Description:               The help text to be displayed for the field input.            
* Name: kind
  * Type:                   Literal['scalar_column', 'foreign_key']            
  * Description:               Type of the selected column (scalar_column, foreign_key).            
* Name: column_attnum
  * Type:                   Optional[int]            
  * Description:               The attnum of column to be selected as a field. Applicable for scalar_column and foreign_key fields.            
* Name: related_table_oid
  * Type:                   Optional[int]            
  * Description:               The oid of the related table. Applicable for foreign_key fields.            
* Name: fk_interaction_rule
  * Type:                   Literal['must_pick', 'can_pick_or_create', 'must_create']            
  * Description:               Determines user interaction with a foreign_key field’s related record (must_pick, can_pick_or_create, must_create).            
* Name: parent_field_id
  * Type:                   Literal['must_pick', 'can_pick_or_create', 'must_create']            
  * Description:               The Django id of the Field set as parent for related fields.            
* Name: styling
  * Type:                   Optional[dict]            
  * Description:               Information about the visual appearance of the field.            
* Name: is_required
  * Type:                   bool            
  * Description:               Specifies whether a value for the field is mandatory.            
* Name: child_fields
  * Type:                   Optional[list[FieldInfo]]            
  * Description:               List of definitions of child fields. Applicable for foreign_key fields.            


### forms.AddFormDef 

Bases: `TypedDict`

Definition needed to add a form.

Attributes:



* Name: name
  * Type:                   str            
  * Description:               The name of the form.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the form.            
* Name: version
  * Type:                   int            
  * Description:               The version of the form for reconciliation of json fields.            
* Name: database_id
  * Type:                   int            
  * Description:               The Django id of the database containing the Form.            
* Name: schema_oid
  * Type:                   int            
  * Description:               The OID of the schema where within which form exists.            
* Name: base_table_oid
  * Type:                   int            
  * Description:               The table OID based on which a form will be created.            
* Name: associated_role_id
  * Type:                   Optional[int]            
  * Description:               The Django id of the configured role to be used while submitting a form.            
* Name: header_title
  * Type:                   dict            
  * Description:               The title of the rendered form.            
* Name: header_subtitle
  * Type:                   Optional[dict]            
  * Description:               The subtitle of the rendered form.            
* Name: submit_message
  * Type:                   Optional[dict]            
  * Description:               Message to be displayed upon submission.            
* Name: submit_redirect_url
  * Type:                   Optional[str]            
  * Description:               Redirect path after submission.            
* Name: submit_button_label
  * Type:                   Optional[str]            
  * Description:               Text to be displayed on the submit button.            
* Name: fields
  * Type:                   list[AddOrReplaceFieldDef]            
  * Description:               Definition of Fields within the form.            


### forms.AddOrReplaceFieldDef 

Bases: `TypedDict`

FormField definition needed while adding or replacing a form.

Attributes:



* Name: key
  * Type:                   str            
  * Description:               A unique string identifier for the field within a form.            
* Name: index
  * Type:                   int            
  * Description:               The order in which the field should be displayed.            
* Name: label
  * Type:                   Optional[str]            
  * Description:               The text to be displayed for the field input.            
* Name: help
  * Type:                   Optional[str]            
  * Description:               The help text to be displayed for the field input.            
* Name: kind
  * Type:                   Literal['scalar_column', 'foreign_key']            
  * Description:               Type of the selected column (scalar_column, foreign_key).            
* Name: column_attnum
  * Type:                   Optional[int]            
  * Description:               The attnum of column to be selected as a field. Applicable for scalar_column and foreign_key fields.            
* Name: related_table_oid
  * Type:                   Optional[int]            
  * Description:               The oid of the related table. Applicable for foreign_key fields.            
* Name: fk_interaction_rule
  * Type:                   Literal['must_pick', 'can_pick_or_create', 'must_create']            
  * Description:               Determines user interaction with a foreign_key field’s related record (must_pick, can_pick_or_create, must_create).            
* Name: styling
  * Type:                   Optional[dict]            
  * Description:               Information about the visual appearance of the field.            
* Name: is_required
  * Type:                   Optional[bool]            
  * Description:               Specifies whether a value for the field is mandatory.            
* Name: child_fields
  * Type:                   Optional[list[AddOrReplaceFieldDef]]            
  * Description:               List of definitions of child fields. Applicable for foreign_key fields.            


### forms.SettableFormDef 

Bases: `[AddFormDef](#forms.AddFormDef "forms.AddFormDef")`

Definition needed to update a form.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The Django id of the Form on the database.            
* Name: name
  * Type:                   str            
  * Description:               The name of the form.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the form.            
* Name: version
  * Type:                   int            
  * Description:               The version of the form.            
* Name: associated_role_id
  * Type:                   Optional[int]            
  * Description:               The Django id of the configured role to be used while submitting a form.            
* Name: header_title
  * Type:                   dict            
  * Description:               The title of the rendered form.            
* Name: header_subtitle
  * Type:                   Optional[dict]            
  * Description:               The subtitle of the rendered form.            
* Name: submit_message
  * Type:                   Optional[dict]            
  * Description:               Message to be displayed upon submission.            
* Name: submit_redirect_url
  * Type:                   Optional[str]            
  * Description:               Redirect path after submission.            
* Name: submit_button_label
  * Type:                   Optional[str]            
  * Description:               Text to be displayed on the submit button.            
* Name: fields
  * Type:                   list[AddOrReplaceFieldDef]            
  * Description:               Definition of Fields within the form.            


Records
-------------------------------------

Classes and functions exposed to the RPC endpoint for managing table records.

### records.list\_ 

```
list_(
    *,
    table_oid,
    database_id,
    limit=None,
    offset=None,
    order=None,
    filter=None,
    grouping=None,
    return_record_summaries=False,
    **kwargs
)

```


List records from a table, and its row count. Exposed as `list`.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 limit            
  * Type:                   int            
  * Description:               The maximum number of rows we’ll return.            
  * Default:                   None            
* Name:                 offset            
  * Type:                   int            
  * Description:               The number of rows to skip before returning records fromfollowing rows.            
  * Default:                   None            
* Name:                 order            
  * Type:                   list[OrderBy]            
  * Description:               An array of ordering definition objects.            
  * Default:                   None            
* Name:                 filter            
  * Type:                   Filter            
  * Description:               An array of filter definition objects.            
  * Default:                   None            
* Name:                 grouping            
  * Type:                   Grouping            
  * Description:               An array of group definition objects.            
  * Default:                   None            
* Name:                 return_record_summaries            
  * Type:                   bool            
  * Description:               Whether to return summaries of retrievedrecords.            
  * Default:                   False            


Returns:



* Type:                   RecordList            
  * Description:               The requested records, along with some metadata.            


### records.get 

```
get(
    *,
    record_id,
    table_oid,
    database_id,
    return_record_summaries=False,
    table_record_summary_templates=None,
    **kwargs
)

```


Get single record from a table by its primary key.

Parameters:



* Name:                 record_id            
  * Type:                   Any            
  * Description:               The primary key value of the record to be gotten.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 return_record_summaries            
  * Type:                   bool            
  * Description:               Whether to return summaries of theretrieved record.            
  * Default:                   False            
* Name:                 table_record_summary_templates            
  * Type:                   dict[str, Any]            
  * Description:               A dict of record summary templates.If none are provided, then the templates will be take from theDjango metadata. Any templates provided will take precedence on aper-table basis over the stored metadata templates. The purpose ofthis function parameter is to allow clients to generate recordsummary previews without persisting any metadata.            
  * Default:                   None            


Returns: The requested record, along with some metadata.

### records.add 

```
add(
    *,
    record_def,
    table_oid,
    database_id,
    return_record_summaries=False,
    **kwargs
)

```


Add a single record to a table.

The form of the `record_def` is determined by the underlying table. Keys should be attnums, and values should be the desired value for that column in the created record. Missing keys will use default values (if set on the DB), and explicit `null` values will set null for that value regardless of default (with obvious exceptions where that would violate some constraint)

Parameters:



* Name:                 record_def            
  * Type:                   dict            
  * Description:               An object representing the record to be added.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 return_record_summaries            
  * Type:                   bool            
  * Description:               Whether to return summaries of the addedrecord.            
  * Default:                   False            


Returns:



* Type:                   RecordAdded            
  * Description:               The created record, along with some metadata.            


### records.patch 

```
patch(
    *,
    record_def,
    record_id,
    table_oid,
    database_id,
    return_record_summaries=False,
    **kwargs
)

```


Modify a record in a table.

The form of the `record_def` is determined by the underlying table. Keys should be attnums, and values should be the desired value for that column in the modified record. Explicit `null` values will set null for that value (with obvious exceptions where that would violate some constraint).

Parameters:



* Name:                 record_def            
  * Type:                   dict            
  * Description:               An object representing the record to be added.            
  * Default:                 required            
* Name:                 record_id            
  * Type:                   Any            
  * Description:               The primary key value of the record to modify.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 return_record_summaries            
  * Type:                   bool            
  * Description:               Whether to return summaries of themodified record.            
  * Default:                   False            


Returns:



* Type:                   RecordAdded            
  * Description:               The modified record, along with some metadata.            


### records.delete 

```
delete(*, record_ids, table_oid, database_id, **kwargs)

```


Delete records from a table by primary key.

Parameters:



* Name:                 record_ids            
  * Type:                   list[Any]            
  * Description:               The primary key values of the records to be deleted.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               The identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[Any]            
  * Description:               The primary key values of the records deleted.            


### records.search 

```
search(
    *,
    table_oid,
    database_id,
    search_params=[],
    limit=10,
    offset=0,
    return_record_summaries=False,
    **kwargs
)

```


List records from a table according to `search_params`.

Literals will be searched for in a basic way in string-like columns, but will have to match exactly in non-string-like columns.

Records are assigned a score based on how many matches, and of what quality, they have with the passed search parameters.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 search_params            
  * Type:                   list[SearchParam]            
  * Description:               Results are ranked and filtered according to the           objects passed here.            
  * Default:                   []            
* Name:                 limit            
  * Type:                   int            
  * Description:               The maximum number of rows we’ll return.            
  * Default:                   10            
* Name:                 offset            
  * Type:                   int            
  * Description:               The number of rows to skip before returning records fromfollowing rows.            
  * Default:                   0            
* Name:                 return_record_summaries            
  * Type:                   bool            
  * Description:               Whether to return summaries of retrievedrecords.            
  * Default:                   False            


Returns:



* Type:                   RecordList            
  * Description:               The requested records, along with some metadata.            


### records.list\_summaries 

```
list_summaries(
    *,
    table_oid,
    database_id,
    limit=None,
    offset=None,
    search=None,
    **kwargs
)

```


List record summaries and keys for each record. Primarily used for selection via the Row seeker.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 limit            
  * Type:                   Optional[int]            
  * Description:               Optional limit on the number of records to return.            
  * Default:                   None            
* Name:                 offset            
  * Type:                   Optional[int]            
  * Description:               Optional offset for pagination.            
  * Default:                   None            
* Name:                 search            
  * Type:                   Optional[str]            
  * Description:               Optional search term to filter records.            
  * Default:                   None            


Returns:



* Type:                   RecordSummaryList            
  * Description:               A list of objects, each containing a record summary and key pertaining to a record.            


### records.RecordList 

Bases: `TypedDict`

Records from a table, along with some meta data

The form of the objects in the `results` array is determined by the underlying records being listed. The keys of each object are the attnums of the retrieved columns. The values are the value for the given row, for the given column.

Attributes:



* Name: count
  * Type:                   int            
  * Description:               The total number of records in the table.            
* Name: results
  * Type:                   list[dict]            
  * Description:               An array of record objects.            
* Name: grouping
  * Type:                   GroupingResponse            
  * Description:               Information for displaying grouped records.            
* Name: linked_record_summaries
  * Type:                   GroupingResponse            
  * Description:               Information for previewing foreign keyvalues, provides a map of foreign key to a text summary.            
* Name: record_summaries
  * Type:                   dict[str, str]            
  * Description:               Information for previewing returned records.            
* Name: download_links
  * Type:                   Optional[dict]            
  * Description:               Information for viewing or downloading fileattachments.            


### records.RecordAdded 

Bases: `TypedDict`

Record from a table, along with some meta data

The form of the object in the `results` array is determined by the underlying records being listed. The keys of each object are the attnums of the retrieved columns. The values are the value for the given row, for the given column.

Attributes:



* Name: results
  * Type:                   list[dict]            
  * Description:               An array of a single record objects (the one added).            
* Name: linked_record_summaries
  * Type:                   dict[str, dict[str, str]]            
  * Description:               Information for previewing foreign keyvalues, provides a map of foreign key to a text summary.            
* Name: record_summaries
  * Type:                   dict[str, str]            
  * Description:               Information for previewing an added record.            


### records.OrderBy 

Bases: `TypedDict`

An object defining an `ORDER BY` clause.

Attributes:



* Name: attnum
  * Type:                   int            
  * Description:               The attnum of the column to order by.            
* Name: direction
  * Type:                   Literal['asc', 'desc']            
  * Description:               The direction to order by.            


### records.Filter 

Bases: `TypedDict`

An object defining a filter to be used in a `WHERE` clause.

For valid `type` values, see the `msar.filter_templates` table defined in `mathesar/db/sql/05_msar.sql`.

Attributes:



* Name: type
  * Type:                   str            
  * Description:               a function or operator to be used in filtering.            
* Name: args
  * Type:                   list[Union[Filter, FilterAttnum, FilterLiteral]]            
  * Description:               The ordered arguments for the function or operator.            


### records.FilterAttnum 

Bases: `TypedDict`

An object choosing a column for a filter.

Attributes:



* Name: type
  * Type:                   Literal['attnum']            
  * Description:               Must be "attnum"            
* Name: value
  * Type:                   int            
  * Description:               The attnum of the column to filter by            


### records.FilterLiteral 

Bases: `TypedDict`

An object defining a literal for an argument to a filter.

Attributes:



* Name: type
  * Type:                   Literal['literal']            
  * Description:               must be "literal".            
* Name: value
  * Type:                   Any            
  * Description:               The value of the literal.            


### records.Grouping 

Bases: `TypedDict`

Grouping definition.

The table involved must have a single column primary key.

Attributes:



* Name: columns
  * Type:                   list[int]            
  * Description:               The columns to be grouped by.            
* Name: preproc
  * Type:                   list[str]            
  * Description:               The preprocessing functions to apply (if any).            


### records.Group 

Bases: `TypedDict`

Group definition.

Note that the `count` is over all rows in the group, whether returned or not. However, `result_indices` is restricted to only the rows returned. This is to avoid potential problems if there are many rows in the group (e.g., the whole table), but we only return a few.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The id of the group. Consistent for same input.            
* Name: count
  * Type:                   int            
  * Description:               The number of items in the group.            
* Name: results_eq
  * Type:                   list[dict]            
  * Description:               The value the results of the group equal.            
* Name: result_indices
  * Type:                   list[int]            
  * Description:               The 0-indexed positions of group members in theresults array.            


### records.GroupingResponse 

Bases: `TypedDict`

Grouping response object. Extends Grouping with actual groups.

Attributes:



* Name: columns
  * Type:                   list[int]            
  * Description:               The columns to be grouped by.            
* Name: preproc
  * Type:                   list[str]            
  * Description:               The preprocessing functions to apply (if any).            
* Name: groups
  * Type:                   list[Group]            
  * Description:               The groups applicable to the records being returned.            


### records.SearchParam 

Bases: `TypedDict`

Search definition for a single column.

Attributes:



* Name: attnum
  * Type:                   int            
  * Description:               The attnum of the column in the table.            
* Name: literal
  * Type:                   Any            
  * Description:               The literal to search for in the column.            


### records.RecordSummaryList 

Bases: `TypedDict`

Response for listing record summaries.

Attributes:



* Name: count
  * Type:                   int            
  * Description:               The total number of records matching the criteria.            
* Name: results
  * Type:                   list[SummarizedRecordReference]            
  * Description:               A list of summarized record references, each containing a key and a summary.            


### records.SummarizedRecordReference 

Bases: `TypedDict`

A summarized reference to a record, typically used in foreign key fields.

Attributes:



* Name: key
  * Type:                   Any            
  * Description:               A unique identifier for the record.            
* Name: summary
  * Type:                   str            
  * Description:               The record summary            


Roles
---------------------------------

### roles.list\_ 

```
list_(*, database_id, **kwargs)

```


List information about roles for a database server. Exposed as `list`. Requires a database id inorder to connect to the server.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            


Returns:



* Type:                   list[RoleInfo]            
  * Description:               A list of roles present on the database server.            


### roles.add 

```
add(
    *,
    rolename,
    database_id,
    password=None,
    login=None,
    **kwargs
)

```


Add a new login/non-login role on a database server.

Parameters:



* Name:                 rolename            
  * Type:                   str            
  * Description:               The name of the role to be created.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            
* Name:                 password            
  * Type:                   str            
  * Description:               The password for the rolename to set.            
  * Default:                   None            
* Name:                 login            
  * Type:                   bool            
  * Description:               Whether the role to be created could login.            
  * Default:                   None            


Returns:



* Type:                   RoleInfo            
  * Description:               A dict describing the created role.            


### roles.delete 

```
delete(*, role_oid, database_id, **kwargs)

```


Drop a role on a database server.

Parameters:



* Name:                 role_oid            
  * Type:                   int            
  * Description:               The OID of the role to drop on the database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            


### roles.get\_current\_role 

```
get_current_role(*, database_id, **kwargs)

```


Get information about the current role and all the parent role(s) whose privileges are immediately available to current role without doing SET ROLE.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database.            
  * Default:                 required            


Returns:


|Type                              |Description                                                  |
|----------------------------------|-------------------------------------------------------------|
|                  dict            |              A dict describing the current role.            |


### roles.set\_members 

```
set_members(
    *, parent_role_oid, members, database_id, **kwargs
)

```


Grant/Revoke direct membership to/from roles.

Parameters:



* Name:                 parent_role_oid            
  * Type:                   int            
  * Description:               The OID of role whose membership will be granted/revoked to/from other roles.            
  * Default:                 required            
* Name:                 members            
  * Type:                   list            
  * Description:               An array of role OID(s) whom we want to grant direct membership of the parent role.       Only the OID(s) present in the array will be granted membership of parent role,       Membership will be revoked for existing members not present in this array.            
  * Default:                 required            


Returns:



* Type:                   RoleInfo            
  * Description:               A dict describing the updated information of the parent role.            


### roles.RoleInfo 

Bases: `TypedDict`

Information about a role.

Attributes:



* Name: oid
  * Type:                   int            
  * Description:               The OID of the role.            
* Name: name
  * Type:                   str            
  * Description:               Name of the role.            
* Name: super
  * Type:                   bool            
  * Description:               Whether the role has SUPERUSER status.            
* Name: inherits
  * Type:                   bool            
  * Description:               Whether the role has INHERIT attribute.            
* Name: create_role
  * Type:                   bool            
  * Description:               Whether the role has CREATEROLE attribute.            
* Name: create_db
  * Type:                   bool            
  * Description:               Whether the role has CREATEDB attribute.            
* Name: login
  * Type:                   bool            
  * Description:               Whether the role has LOGIN attribute.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               A description of the role            
* Name: members
  * Type:                   Optional[list[RoleMember]]            
  * Description:               The member roles that directly inherit the role.            


Refer PostgreSQL documentation on

*   [pg\_roles table](https://www.postgresql.org/docs/current/view-pg-roles.html).
*   [Role attributes](https://www.postgresql.org/docs/current/role-attributes.html)
*   [Role membership](https://www.postgresql.org/docs/current/role-membership.html)

### roles.RoleMember 

Bases: `TypedDict`

Information about a member role of a directly inherited role.

Attributes:



* Name: oid
  * Type:                   int            
  * Description:               The OID of the member role.            
* Name: admin
  * Type:                   bool            
  * Description:               Whether the member role has ADMIN option on the inherited role.            


Roles Configured
-------------------------------------------------------

### roles.configured.list\_ 

```
list_(*, server_id, **kwargs)

```


List information about roles configured in Mathesar. Exposed as `list`.

Parameters:



* Name:                 server_id            
  * Type:                   int            
  * Description:               The Django id of the Server containing the configured roles.            
  * Default:                 required            


Returns:



* Type:                   list[ConfiguredRoleInfo]            
  * Description:               A list of configured roles.            


### roles.configured.add 

```
add(*, server_id, name, password, **kwargs)

```


Configure a role in Mathesar for a database server.

Parameters:



* Name:                 server_id            
  * Type:                   int            
  * Description:               The Django id of the Server to contain the configured role.            
  * Default:                 required            
* Name:                 name            
  * Type:                   str            
  * Description:               The name of the role.            
  * Default:                 required            
* Name:                 password            
  * Type:                   str            
  * Description:               The password for the role.            
  * Default:                 required            


Returns:



* Type:                   ConfiguredRoleInfo            
  * Description:               The newly configured role.            


### roles.configured.delete 

```
delete(*, configured_role_id, **kwargs)

```


Delete a configured role for a server.

Parameters:



* Name:                 configured_role_id            
  * Type:                   int            
  * Description:               The Django id of the ConfiguredRole model instance.            
  * Default:                 required            


### roles.configured.set\_password 

```
set_password(*, configured_role_id, password, **kwargs)

```


Set the password of a configured role for a server.

Parameters:



* Name:                 configured_role_id            
  * Type:                   int            
  * Description:               The Django id of the ConfiguredRole model instance.            
  * Default:                 required            
* Name:                 password            
  * Type:                   str            
  * Description:               The password for the role.            
  * Default:                 required            


### roles.configured.ConfiguredRoleInfo 

Bases: `TypedDict`

Information about a role configured in Mathesar.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               the Django ID of the ConfiguredRole model instance.            
* Name: name
  * Type:                   str            
  * Description:               The name of the role.            
* Name: server_id
  * Type:                   int            
  * Description:               The Django ID of the Server model instance for the role.            


Schemas
-------------------------------------

### schemas.list\_ 

```
list_(*, database_id, **kwargs)

```


List information about schemas in a database. Exposed as `list`.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[SchemaInfo]            
  * Description:               A list of SchemaInfo objects            


### schemas.get 

```
get(*, schema_oid, database_id, **kwargs)

```


Get information about a schema in a database.

Parameters:



* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the schema to get.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   SchemaInfo            
  * Description:               The SchemaInfo describing the user-defined schema in the database.            


### schemas.add 

```
add(
    *,
    name,
    database_id,
    owner_oid=None,
    description=None,
    **kwargs
)

```


Add a schema

Parameters:



* Name:                 name            
  * Type:                   str            
  * Description:               The name of the schema to add.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the schema.            
  * Default:                 required            
* Name:                 owner_oid            
  * Type:                   int            
  * Description:               The OID of the role who will own the new schema.If owner_oid is None, the current role will be the owner of the new schema.            
  * Default:                   None            
* Name:                 description            
  * Type:                   Optional[str]            
  * Description:               A description of the schema            
  * Default:                   None            


Returns:



* Type:                   SchemaInfo            
  * Description:               The SchemaInfo describing the user-defined schema in the database.            


### schemas.delete 

```
delete(*, schema_oids, database_id, **kwargs)

```


Safely drop all objects in each schema, then the schemas themselves.

Does not work on the internal `msar` schema.

If any passed schema doesn’t exist, an exception will be raised. If any object exists in a schema which isn’t passed, but which depends on an object in a passed schema, an exception will be raised.

Parameters:



* Name:                 schema_oids            
  * Type:                   list[int]            
  * Description:               The OIDs of the schemas to delete.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the schema.            
  * Default:                 required            


### schemas.patch 

```
patch(*, schema_oid, database_id, patch, **kwargs)

```


Patch a schema, given its OID.

Parameters:



* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the schema to delete.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the schema.            
  * Default:                 required            
* Name:                 patch            
  * Type:                   SchemaPatch            
  * Description:               A SchemaPatch object containing the fields to update.            
  * Default:                 required            


Returns:



* Type:                   SchemaInfo            
  * Description:               The SchemaInfo describing the user-defined schema in the database.            


### schemas.SchemaInfo 

Bases: `TypedDict`

Information about a schema

Attributes:



* Name: oid
  * Type:                   int            
  * Description:               The OID of the schema            
* Name: name
  * Type:                   str            
  * Description:               The name of the schema            
* Name: description
  * Type:                   Optional[str]            
  * Description:               A description of the schema            
* Name: owner_oid
  * Type:                   int            
  * Description:               The OID of the owner of the schema            
* Name: current_role_priv
  * Type:                   list[Literal['USAGE', 'CREATE']]            
  * Description:               All privileges available to the calling roleon the schema.            
* Name: current_role_owns
  * Type:                   bool            
  * Description:               Whether the current role is the owner of theschema (even indirectly).            
* Name: table_count
  * Type:                   int            
  * Description:               The number of tables in the schema            


### schemas.SchemaPatch 

Bases: `TypedDict`

Attributes:



* Name: name
  * Type:                   Optional[str]            
  * Description:               The name of the schema            
* Name: description
  * Type:                   Optional[str]            
  * Description:               A description of the schema            


Schema Privileges
---------------------------------------------------------

### schemas.privileges.list\_direct 

```
list_direct(*, schema_oid, database_id, **kwargs)

```


List direct schema privileges for roles.

Parameters:



* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the schema whose privileges we’ll list.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the schema.            
  * Default:                 required            


Returns:



* Type:                   list[SchemaPrivileges]            
  * Description:               A list of schema privileges.            


### schemas.privileges.replace\_for\_roles 

```
replace_for_roles(
    *, privileges, schema_oid, database_id, **kwargs
)

```


Replace direct schema privileges for roles.

Possible privileges are `USAGE` and `CREATE`.

Only roles which are included in a passed `SchemaPrivileges` object are affected.

WARNING: Any privilege included in the `direct` list for a role is GRANTed, and any privilege not included is REVOKEd.

Parameters:



* Name:                 privileges            
  * Type:                   list[SchemaPrivileges]            
  * Description:               The new privilege sets for roles.            
  * Default:                 required            
* Name:                 schema_oid            
  * Type:                   int            
  * Description:               The OID of the affected schema.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the schema.            
  * Default:                 required            


Returns:



* Type:                   list[SchemaPrivileges]            
  * Description:               A list of all non-default privileges on the schema after the            
* Type:                   list[SchemaPrivileges]            
  * Description:               operation.            


### schemas.privileges.transfer\_ownership 

```
transfer_ownership(
    *, schema_oid, new_owner_oid, database_id, **kwargs
)

```


Transfers ownership of a given schema to a new owner.

Attributes:



* Name: schema_oid
  * Type:             
  * Description:               The OID of the schema to transfer.            
* Name: new_owner_oid
  * Type:             
  * Description:               The OID of the role whom we want to be the new owner of the schema.            


To successfully transfer ownership of a schema to a new owner the current user must:

*   Be a Superuser/Owner of the schema.
*   Be a `MEMBER` of the new owning role. i.e. The current role should be able to `SET ROLE` to the new owning role.
*   Have `CREATE` privilege for the database.

Returns:



* Type:                   SchemaInfo            
  * Description:               Information about the schema, and the current user privileges.            


### schemas.privileges.SchemaPrivileges 

Bases: `TypedDict`

Information about schema privileges for a role.

Attributes:



* Name: role_oid
  * Type:                   int            
  * Description:               The oid of the role.            
* Name: direct
  * Type:                   list[Literal['USAGE', 'CREATE']]            
  * Description:               A list of schema privileges for the aforementioned role_oid.            


Servers
-------------------------------------

Tables
-----------------------------------

### tables.list\_ 

```
list_(*, schema_oid, database_id, **kwargs)

```


List information about tables for a schema. Exposed as `list`.

Parameters:



* Name:                 schema_oid            
  * Type:                   int            
  * Description:               Identity of the schema in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:


|Type                                         |Description                                       |
|---------------------------------------------|--------------------------------------------------|
|                  list[TableInfo]            |              A list of table details.            |


### tables.get 

```
get(*, table_oid, database_id, **kwargs)

```


List information about a table for a schema.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   TableInfo            
  * Description:               Table details for a given table oid.            


### tables.add 

```
add(
    *,
    schema_oid,
    database_id,
    table_name=None,
    pkey_column_info={},
    column_data_list=[],
    constraint_data_list=[],
    owner_oid=None,
    comment=None,
    **kwargs
)

```


Add a table with a default id column.

Parameters:



* Name:                 schema_oid            
  * Type:                   int            
  * Description:               Identity of the schema in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 table_name            
  * Type:                   str            
  * Description:               Name of the table to be created.            
  * Default:                   None            
* Name:                 pkey_column_info            
  * Type:                   CreatablePkColumnInfo            
  * Description:               A dict describing the primary key column to be created for the new table.            
  * Default:                   {}            
* Name:                 column_data_list            
  * Type:                   list[CreatableColumnInfo]            
  * Description:               A list describing columns to be created for the new table, in order.            
  * Default:                   []            
* Name:                 constraint_data_list            
  * Type:                   list[CreatableConstraintInfo]            
  * Description:               A list describing constraints to be created for the new table.            
  * Default:                   []            
* Name:                 owner_oid            
  * Type:                   int            
  * Description:               The OID of the role who will own the new table.If owner_oid is None, the current role will be the owner of the new table.            
  * Default:                   None            
* Name:                 comment            
  * Type:                   str            
  * Description:               The comment for the new table.            
  * Default:                   None            


Returns:



* Type:                   int            
  * Description:               The oid, name, and renamed_columns of the created table.            


### tables.delete 

```
delete(*, table_oid, database_id, cascade=False, **kwargs)

```


Delete a table from a schema.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 cascade            
  * Type:                   bool            
  * Description:               Whether to drop the dependent objects.            
  * Default:                   False            


Returns:


|Type                             |Description                                             |
|---------------------------------|--------------------------------------------------------|
|                  str            |              The name of the dropped table.            |


### tables.patch 

```
patch(*, table_oid, table_data_dict, database_id, **kwargs)

```


Alter details of a preexisting table in a database.

Parameters:



* Name:                 table_oid            
  * Type:                   str            
  * Description:               Identity of the table whose name, description or columns we’ll modify.            
  * Default:                 required            
* Name:                 table_data_dict            
  * Type:                   SettableTableInfo            
  * Description:               A list describing desired table alterations.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:


|Type                             |Description                                             |
|---------------------------------|--------------------------------------------------------|
|                  str            |              The name of the altered table.            |


### tables.import\_ 

```
import_(
    *,
    data_file_id,
    schema_oid,
    database_id,
    table_name=None,
    comment=None,
    **kwargs
)

```


Import a CSV/TSV into a table.

Parameters:



* Name:                 data_file_id            
  * Type:                   int            
  * Description:               The Django id of the DataFile containing desired CSV/TSV.            
  * Default:                 required            
* Name:                 schema_oid            
  * Type:                   int            
  * Description:               Identity of the schema in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 table_name            
  * Type:                   Optional[str]            
  * Description:               Name of the table to be imported.            
  * Default:                   None            
* Name:                 comment            
  * Type:                   Optional[str]            
  * Description:               The comment for the new table.            
  * Default:                   None            


Returns:



* Type:                   AddedTableInfo            
  * Description:               The oid, name, and renamed_columns of the created table.            


### tables.get\_import\_preview 

```
get_import_preview(
    *, table_oid, columns, database_id, limit=20, **kwargs
)

```


Preview an imported table.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the imported table in the user’s database.            
  * Default:                 required            
* Name:                 columns            
  * Type:                   list[PreviewableColumnInfo]            
  * Description:               List of settings describing the casts to be applied to the columns.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 limit            
  * Type:                   int            
  * Description:               The upper limit for the number of records to return.            
  * Default:                   20            


Returns:



* Type:                   list[dict]            
  * Description:               The records from the specified columns of the table.            


### tables.list\_joinable 

```
list_joinable(
    *, table_oid, database_id, max_depth=3, **kwargs
)

```


List details for joinable tables.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               Identity of the table to get joinable tables for.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            
* Name:                 max_depth            
  * Type:                   int            
  * Description:               Specifies how far to search for joinable tables.            
  * Default:                   3            


Returns:



* Type:                   JoinableTableInfo            
  * Description:               Joinable table details for a given table.            


### tables.list\_with\_metadata 

```
list_with_metadata(*, schema_oid, database_id, **kwargs)

```


List tables in a schema, along with the metadata associated with each table

Parameters:



* Name:                 schema_oid            
  * Type:                   int            
  * Description:               PostgreSQL OID of the schema containing the tables.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list            
  * Description:               A list of table details along with metadata.            


### tables.get\_with\_metadata 

```
get_with_metadata(*, table_oid, database_id, **kwargs)

```


Get information about a table in a schema, along with the associated table metadata.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               The OID of the table in the user’s database.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   dict            
  * Description:               A dict describing table details along with its metadata.            


### tables.TableInfo 

Bases: `TypedDict`

Information about a table.

Attributes:



* Name: oid
  * Type:                   int            
  * Description:               The oid of the table in the schema.            
* Name: name
  * Type:                   str            
  * Description:               The name of the table.            
* Name: schema
  * Type:                   int            
  * Description:               The oid of the schema where the table lives.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the table.            
* Name: owner_oid
  * Type:                   int            
  * Description:               The OID of the direct owner of the table.            
* Name: current_role_priv
  * Type:                   list[Literal['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE', 'REFERENCES', 'TRIGGER']]            
  * Description:               The privileges available to the user on the table.            
* Name: current_role_owns
  * Type:                   bool            
  * Description:               Whether the current role owns the table.            


### tables.AddedTableInfo 

Bases: `TypedDict`

Information about a newly created table.

Attributes:



* Name: oid
  * Type:                   int            
  * Description:               The oid of the table in the schema.            
* Name: name
  * Type:                   str            
  * Description:               The name of the table.            
* Name: renamed_columns
  * Type:                   Optional[dict]            
  * Description:               A dictionary giving the names of columns whichwere renamed due to collisions.            


### tables.SettableTableInfo 

Bases: `TypedDict`

Information about a table, restricted to settable fields.

When possible, Passing `null` for a key will clear the underlying setting. E.g.,

*   `description = null` clears the table description.

Setting any of `name`, `columns` to `null` is a noop.

Attributes:



* Name: name
  * Type:                   Optional[str]            
  * Description:               The new name of the table.            
* Name: description
  * Type:                   Optional[str]            
  * Description:               The description of the table.            
* Name: columns
  * Type:                   Optional[list[SettableColumnInfo]]            
  * Description:               A list describing desired column alterations.            


### tables.JoinableTableRecord 

Bases: `TypedDict`

Information about a singular joinable table.

Attributes:



* Name: base
  * Type:                   int            
  * Description:               The OID of the table from which the paths start            
* Name: target
  * Type:                   int            
  * Description:               The OID of the table where the paths end.            
* Name: join_path
  * Type:                   list            
  * Description:                               A list describing joinable paths in the following form:[  [[L_oid0, L_attnum0], [R_oid0, R_attnum0]],  [[L_oid1, L_attnum1], [R_oid1, R_attnum1]],  [[L_oid2, L_attnum2], [R_oid2, R_attnum2]],  …]Here, [L_oidN, L_attnumN] represents the left column of a join, and [R_oidN, R_attnumN] the right.                          
* Name: fkey_path
  * Type:                   list            
  * Description:                               Same as join_path expressed in terms of foreign key constraints in the following form:[    [constraint_id0, reversed],    [constraint_id1, reversed],]In this form, constraint_idN is a foreign key constraint, and reversed is a boolean givingwhether to travel from referrer to referent (when False) or from referent to referrer (when True).                          
* Name: depth
  * Type:                   int            
  * Description:               Specifies how far to search for joinable tables.            
* Name: multiple_results
  * Type:                   bool            
  * Description:               Specifies whether the path included is reversed.            


### tables.JoinableTableInfo 

Bases: `TypedDict`

Information about joinable table(s).

Attributes:



* Name: joinable_tables
  * Type:                   list[JoinableTableRecord]            
  * Description:               List of reachable joinable table(s) from a base table.            
* Name: target_table_info
  * Type:                   list            
  * Description:               Additional info about target table(s) and its column(s).            


Classes and functions exposed to the RPC endpoint for managing table metadata.

### tables.metadata.list\_ 

```
list_(*, database_id, **kwargs)

```


List metadata associated with tables for a database.

Parameters:



* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[TableMetaDataRecord]            
  * Description:               Metadata object for a given table oid.            


### tables.metadata.set\_ 

```
set_(*, table_oid, metadata, database_id, **kwargs)

```


Set metadata for a table.

Parameters:



* Name:                 table_oid            
  * Type:                   int            
  * Description:               The PostgreSQL OID of the table.            
  * Default:                 required            
* Name:                 metadata            
  * Type:                   TableMetaDataBlob            
  * Description:               A TableMetaDataBlob object describing desired table metadata to set.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


### tables.metadata.TableMetaDataBlob 

Bases: `TypedDict`

The metadata fields which can be set on a table

Attributes:



* Name: data_file_id
  * Type:                   Optional[int]            
  * Description:               Specifies the DataFile model id used for the import.            
* Name: import_verified
  * Type:                   Optional[bool]            
  * Description:               Specifies whether a file has been successfully imported into a table.            
* Name: column_order
  * Type:                   Optional[list[int]]            
  * Description:               The order in which columns of a table are displayed.            
* Name: record_summary_template
  * Type:                   Optional[dict[str, Union[str, list[int]]]]            
  * Description:               The record summary template            
* Name: mathesar_added_pkey_attnum
  * Type:                   Optional[int]            
  * Description:               The attnum of the most recently-set pkey column.            


### tables.metadata.TableMetaDataRecord 

Bases: `TypedDict`

Metadata for a table in a database.

Only the `database` and `table_oid` keys are required.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The Django id of the TableMetaData object.            
* Name: database_id
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
* Name: table_oid
  * Type:                   int            
  * Description:               The OID of the table in the database.            
* Name: data_file_id
  * Type:                   Optional[int]            
  * Description:               Specifies the DataFile model id used for the import.            
* Name: import_verified
  * Type:                   Optional[bool]            
  * Description:               Specifies whether a file has been successfully imported into a table.            
* Name: column_order
  * Type:                   Optional[list[int]]            
  * Description:               The order in which columns of a table are displayed.            
* Name: record_summary_template
  * Type:                   Optional[dict[str, Union[str, list[int]]]]            
  * Description:               The record summary template.            
* Name: mathesar_added_pkey_attnum
  * Type:                   Optional[int]            
  * Description:               The attnum of the most recently-set pkey column.            


Table Privileges
-------------------------------------------------------

### tables.privileges.list\_direct 

```
list_direct(*, table_oid, database_id, **kwargs)

```


List direct table privileges for roles. Args: table\_oid: The OID of the table whose privileges we’ll list. database\_id: The Django id of the database containing the table. Returns: A list of table privileges.

### tables.privileges.replace\_for\_roles 

```
replace_for_roles(
    *, privileges, table_oid, database_id, **kwargs
)

```


Replace direct table privileges for roles.

Possible privileges are `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES` and `TRIGGER`.

Only roles which are included in a passed `TablePrivileges` object are affected.

WARNING: Any privilege included in the `direct` list for a role is GRANTed, and any privilege not included is REVOKEd.

Parameters:



* Name:                 privileges            
  * Type:                   list[TablePrivileges]            
  * Description:               The new privilege sets for roles.            
  * Default:                 required            
* Name:                 table_oid            
  * Type:                   int            
  * Description:               The OID of the affected table.            
  * Default:                 required            
* Name:                 database_id            
  * Type:                   int            
  * Description:               The Django id of the database containing the table.            
  * Default:                 required            


Returns:



* Type:                   list[TablePrivileges]            
  * Description:               A list of all non-default privileges on the table after the            
* Type:                   list[TablePrivileges]            
  * Description:               operation.            


### tables.privileges.transfer\_ownership 

```
transfer_ownership(
    *, table_oid, new_owner_oid, database_id, **kwargs
)

```


Transfers ownership of a given table to a new owner.

Attributes:



* Name: table_oid
  * Type:             
  * Description:               The OID of the table to transfer.            
* Name: new_owner_oid
  * Type:             
  * Description:               The OID of the role whom we want to be the new owner of the table.            


To successfully transfer ownership of a table to a new owner the current user must:

*   Be a Superuser/Owner of the table.
*   Be a `MEMBER` of the new owning role. i.e. The current role should be able to `SET ROLE` to the new owning role.
*   Have `CREATE` privilege on the table’s schema.

Returns:



* Type:                   TableInfo            
  * Description:               Information about the table, and the current user privileges.            


### tables.privileges.TablePrivileges 

Bases: `TypedDict`

Information about table privileges for a role. Attributes: role\_oid: The `oid` of the role. direct: A list of table privileges for the aforementioned role\_oid.

Users
---------------------------------

Classes and functions exposed to the RPC endpoint for managing mathesar users.

### users.list\_ 

List information about all mathesar users. Exposed as `list`.

Returns:



* Type:                   list[UserInfo]            
  * Description:               A list of information about mathesar users.            


### users.get 

List information about a mathesar user.

Parameters:



* Name:                 user_id            
  * Type:                   int            
  * Description:               The Django id of the user.            
  * Default:                 required            


Returns:



* Type:                   UserInfo            
  * Description:               User information for a given user_id.            


### users.add 

Add a new mathesar user.

Parameters:



* Name:                 user_def            
  * Type:                   UserDef            
  * Description:               A dict describing the user to create.            
  * Default:                 required            


Privileges

This endpoint requires the caller to be a superuser.

Returns:



* Type:                   UserInfo            
  * Description:               The information of the created user.            


### users.delete 

Delete a mathesar user.

Parameters:



* Name:                 user_id            
  * Type:                   int            
  * Description:               The Django id of the user to delete.            
  * Default:                 required            


Privileges

This endpoint requires the caller to be a superuser.

### users.patch\_self 

```
patch_self(
    *,
    username,
    email,
    full_name,
    display_language,
    **kwargs
)

```


Alter details of currently logged in mathesar user.

Parameters:



* Name:                 username            
  * Type:                   str            
  * Description:               The username of the user.            
  * Default:                 required            
* Name:                 email            
  * Type:                   str            
  * Description:               The email of the user.            
  * Default:                 required            
* Name:                 full_name            
  * Type:                   str            
  * Description:               The full name of the user.            
  * Default:                 required            
* Name:                 display_language            
  * Type:                   str            
  * Description:               Specifies the display language for the user, can be set to either en or ja.            
  * Default:                 required            


Returns:



* Type:                   UserInfo            
  * Description:               Updated user information of the caller.            


### users.patch\_other 

```
patch_other(
    *,
    user_id,
    username,
    is_superuser,
    email,
    full_name,
    display_language
)

```


Alter details of a mathesar user, given its user\_id.

Parameters:



* Name:                 user_id            
  * Type:                   int            
  * Description:               The Django id of the user.            
  * Default:                 required            
* Name:                 username            
  * Type:                   str            
  * Description:               The username of the user.            
  * Default:                 required            
* Name:                 email            
  * Type:                   str            
  * Description:               The email of the user.            
  * Default:                 required            
* Name:                 is_superuser            
  * Type:                   bool            
  * Description:               Specifies whether to set the user as a superuser.            
  * Default:                 required            
* Name:                 full_name            
  * Type:                   str            
  * Description:               The full name of the user.            
  * Default:                 required            
* Name:                 display_language            
  * Type:                   str            
  * Description:               Specifies the display language for the user, can be set to either en or ja.            
  * Default:                 required            


Privileges

This endpoint requires the caller to be a superuser.

Returns:



* Type:                   UserInfo            
  * Description:               Updated user information for a given user_id.            


### users.replace\_own 

```
replace_own(*, old_password, new_password, **kwargs)

```


Alter password of currently logged in mathesar user.

Parameters:



* Name:                 old_password            
  * Type:                   str            
  * Description:               Old password of the currently logged in user.            
  * Default:                 required            
* Name:                 new_password            
  * Type:                   str            
  * Description:               New password of the user to set.            
  * Default:                 required            


### users.revoke 

```
revoke(*, user_id, new_password)

```


Alter password of a mathesar user, given its user\_id.

Parameters:



* Name:                 user_id            
  * Type:                   int            
  * Description:               The Django id of the user.            
  * Default:                 required            
* Name:                 new_password            
  * Type:                   str            
  * Description:               New password of the user to set.            
  * Default:                 required            


Privileges

This endpoint requires the caller to be a superuser.

### users.UserInfo 

Bases: `TypedDict`

Information about a mathesar user.

Attributes:



* Name: id
  * Type:                   int            
  * Description:               The Django id of the user.            
* Name: username
  * Type:                   str            
  * Description:               The username of the user.            
* Name: is_superuser
  * Type:                   bool            
  * Description:               Specifies whether the user is a superuser.            
* Name: email
  * Type:                   str            
  * Description:               The email of the user.            
* Name: full_name
  * Type:                   str            
  * Description:               The full name of the user.            
* Name: display_language
  * Type:                   str            
  * Description:               Specifies the display language for the user, can be either en or ja.            


### users.UserDef 

Bases: `TypedDict`

Definition for creating a mathesar user.

Attributes:



* Name: username
  * Type:                   str            
  * Description:               The username of the user.            
* Name: password
  * Type:                   str            
  * Description:               The password of the user.            
* Name: is_superuser
  * Type:                   bool            
  * Description:               Whether the user is a superuser.            
* Name: email
  * Type:                   Optional[str]            
  * Description:               The email of the user.            
* Name: full_name
  * Type:                   Optional[str]            
  * Description:               The full name of the user.            
* Name: display_language
  * Type:                   Optional[str]            
  * Description:               Specifies the display language for the user, can be set to either en or ja.            
