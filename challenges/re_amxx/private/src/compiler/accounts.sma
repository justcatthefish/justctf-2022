#include <amxmodx>
#include <nvault>

// #pragma compress 1 // anti amxxdump

#include "utils.inl"

native encode_password(id, password[], len, out[], out_len);

enum kPlayerState {
	NONE = 0,
	IN_REGISTER,
	IN_LOGIN,
	LOGGED
};

#define KICK_TASKID 54321

new g_nvault;
new bool:logged[33];
new kPlayerState:player_state[33];
new account_menu;

public plugin_init(){
	register_plugin("Account system", "21.37", "RiviT");

	register_clcmd("say /menu", "cmd_menu");
	register_clcmd("say /login", "cmd_menu");
	register_clcmd("say /register", "cmd_menu");
	register_clcmd("radio1", "cmd_menu");
	// register_clcmd("say /gen", "generate_entries");

	register_clcmd("passwd", "handle_password_input");

	g_nvault = nvault_open("accounts");

	create_menu();
}

stock create_menu(){
	account_menu = menu_create("Account system", "menu_handle");
	menu_additem(account_menu, "Login");
	menu_additem(account_menu, "Register");
}

public plugin_end(){
	nvault_close(g_nvault);
}

public client_putinserver(id){
	logged[id] = false;
	player_state[id] = NONE;
	set_task(120.0, "kick", KICK_TASKID+id);
}

public client_disconnect(id){
	logged[id] = false;
	player_state[id] = NONE;
	remove_task(KICK_TASKID+id);
}

public kick_player(id){
	return kick(id + KICK_TASKID);
}

public kick(id) {
	id -= KICK_TASKID;
	if(!is_user_connected(id)){
		return 0;
	}

	return server_cmd(fmt("kick #%d", get_user_userid(id)));
}

public cmd_menu(id){
	if(player_state[id] == LOGGED){
		return client_print(id, 3, "Already logged in");
	}
	return menu_display(id, account_menu);
}

public cmd_login(id){
	if(player_state[id] != NONE){
		return 1;
	}

	new vault_data[512];
	new was_found = nvault_get(g_nvault, fmt("%n", id), vault_data, charsmax(vault_data));
	if(!was_found){
		client_print(id, 3, "Account with username: %n not found", id);
		return 1;
	}

	player_state[id] = IN_LOGIN;
	client_cmd(id, "messagemode passwd");
	return 1;
}

public cmd_register(id){
	if(player_state[id] != NONE){
		return 1;
	}

	new vault_data[512];
	new was_found = nvault_get(g_nvault, fmt("%n", id), vault_data, charsmax(vault_data));
	if(was_found){
		client_print(id, 3, "Account with username: %n already exists", id);
		return 1;
	}

	player_state[id] = IN_REGISTER;
	client_cmd(id, "messagemode passwd");
	return 1;
}

public menu_handle(id, menu, item){
	if(item == MENU_EXIT || !is_user_connected(id)){
		return 0;
	}

	return item == 0 ? cmd_login(id) : cmd_register(id);
}

public handle_password_input(id){
	if(player_state[id] != IN_REGISTER && player_state[id] != IN_LOGIN){
		return 1;
	}

	remove_task(id + KICK_TASKID);

	new password[192], vault_data[512], encoded[512], bytes_str[512];
	new name[33];
	get_user_name(id, name, charsmax(name));
	new password_len = read_argv(1, password, charsmax(password));
	new was_found = nvault_get(g_nvault, name, vault_data, charsmax(vault_data));
	new encoded_len = encode_password(id, password, password_len, encoded, charsmax(encoded));
	words_to_str(encoded, encoded_len, bytes_str, charsmax(bytes_str));

	switch(player_state[id]){
		case IN_LOGIN: {
			if(!was_found){
				player_state[id] = NONE;
				return client_print(id, 3, "Account with username: %n not found", id);
			}

			if(!equal(vault_data, bytes_str)){
				client_print(id, 3, "Wrong password");
				player_state[id] = NONE;
				return kick_player(id);
			}
			
			client_print(id, 3, "Login OK");
			player_state[id] = LOGGED;
		}

		case IN_REGISTER: {
			if(was_found){
				player_state[id] = NONE;
				return client_print(id, 3, "Account with username: %n already exists", id);
			}

			if(password_len < 8){
				player_state[id] = NONE;
				return client_print(id, 3, "Password too short!");
			}

			if(password_len > 32){
				player_state[id] = NONE;
				return client_print(id, 3, "Password too long!");
			}

			nvault_set(g_nvault, name, bytes_str);
			client_print(id, 3, "Register OK");
			player_state[id] = LOGGED;
		}
	}

	return 1;
}


// stock generate_entries(id){
// 	enum kLoginData {
// 		GEN_LOGIN[32],
// 		GEN_PASSWD[128]
// 	}
// 	new kLoginData:nicks[][kLoginData] = {
// 		{"Joe", "08ce0d1901640a1802cc0b800434087f0cca057e0e3206e6"},
// 		{"Botman", "048106ed0b540ddc022a065c01f1081e"},
// 		{"Fragnatic", "080a0d3804d4008509900e670da10d9f"},
// 		{"Campers Death", "0f890c6e040a08e102b30b9f0d0c0cb6"},
// 		{"Headshot Deluxe", "0797080805980012065809c30871086f0554037002530fca0d250e3e"},
// 		{"Pr0g4m3r", "0ec80d920582039e07950164007f02940e290e97038d08670cd108630bce02de0566079a02f4012c08ac04950aa60f0d0c81"},
// 		{"L33t", "021608eb067b093b0c170c88053c098a"},
// 		{"Dredd", "0efd057e09b003820d380f340ae502d50a71"},
// 		{"Rivit", "0f5401c00a740b8d0dc10407081d0c8700ee"},
// 		{"Wujek", "04f10c8a0a1a095404ae0985092f0e98"},
// 		{"shw", "0ec80d76021800c6043101fc01360a220905"},
// 		{"rumcajs", "07b6052d07ed0724036104070b300f7b"},
// 		{"fex", "05100a060efc0ea60e500346083c0d320cdc"}
// 	}

// 	for(new i = 0; i < sizeof(nicks); i++){
// 		nvault_set(g_nvault, fmt("%s", nicks[i][GEN_LOGIN]), fmt("%s", nicks[i][GEN_PASSWD]));
// 	}
// }
