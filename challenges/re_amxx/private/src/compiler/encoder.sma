#include <amxmodx>

// increase mem size because db_results_ready is crashing :(
#pragma dynamic 16384

#include "utils.inl"
#include "opcodes.inl"

public do_nothing(){
	// put external functions here if you are going to use them in patched code
	// because order of sysreq's matters
	
	new tmp[2];
	TrieGetCell(TrieCreate(), fmt("ignoreme"), tmp[0]);
	get_user_name(0, tmp, charsmax(tmp));
	get_cvar_num("ignoreme");
	get_function_bytes(1, tmp, 1);
	dump_function(1, tmp, 1);
}

native db_get(key[]);
forward db_results_ready(key[], bytecode[], len, func_base);

new code_keys[3][] = {
	"stage1",
	"stage2",
	"stage3",
}

new encode2_fmt[] = "%02x";
new encode3_cvar_name[] = "encoder_random_value";

new Trie:parts;
new amx_base;

public plugin_init(){
	register_plugin("Super-encryptor 4001", "0.01 pre-alpha", "RiviT");
	register_cvar("encoder_random_value", "1337");

	read_regions();
	set_task(2.0, "prepare_plugin");
}

public plugin_end(){
	TrieDestroy(parts);
}

public plugin_natives(){
	register_native("encode_password", "encode_password", 1);
}

public encode_password(id, password[], len, output[], out_len){
	param_convert(2);
	param_convert(4);

	new local_copy[256];
	copy(local_copy, len, password);

	new new_len = len;
	new_len = encode1(id, local_copy, new_len);
	new_len = encode2(local_copy, new_len);
	new_len = encode3(local_copy, new_len);

	copy(output, out_len, local_copy);
	return new_len;
}

stock encode1_(id, password[], password_len){
	new name[33];
	new nick_len = get_user_name(id, name, charsmax(name));

	for(new i = 0, j = 0; i < password_len; i++){
		password[i] ^= name[j++];
		j %= nick_len;
	}

	for(new i = 0; i+1 < password_len; i += 2){
		password[i] ^= password[i+1];
		password[i+1] ^= password[i];
		password[i] ^= password[i+1];
	}

	return password_len;
}

public encode1(id, password[], password_len){
	log_amx("encode1");

	new name[33];
	new nick_len = get_user_name(id, name, charsmax(name));

	for(new i = 0; i < password_len; i++){
		if(i % 3 == 0) continue;
		new v = password[i];
		v += 3;
		v ^= 0x55;
		v *= 2;
		v &= 0xff
		password[i] = v
	}

	for(new i = 0; i < password_len; i++){
		if(i % 2 == 0) continue;
		new v = password[i];
		v ^= i;
		v ^= nick_len;
		v ^= name[0];
		v &= 0xff
		password[i] = v;
	}

	return password_len;
}

stock encode2_(password[], password_len){
	new v;
	for(new i = 0; i < password_len; i++){
		TrieGetCell(parts, fmt(encode2_fmt, password[i]), v);
		password[i] = v;
	}

	return password_len;
}

public encode2(password[], password_len){
	log_amx("encode2");

	new key[64];
	for(new i = 0; i < password_len; i++){
		formatex(key, charsmax(key), encode2_fmt, password[i]);
		new trie_size = TrieGetSize(parts);
		password[i] = (password[i] * trie_size) & 0xff;
	}

	return password_len;
}

stock encode3_(password[], password_len){
	new b = get_cvar_num(encode3_cvar_name);
	for(new i = 0; i < password_len; i++){
		b += password[i] * 0xDEAD;
		b += 1;
		b %= 0x1000
		password[i] = b;
	}

	return password_len;
}

public encode3(password[], password_len){
	log_amx("encode3");

	new b = get_cvar_num(encode3_cvar_name);
	for(new i = 0; i < password_len; i++){
		if(i % 5 == 0) continue;
		b += password[i] * 18 + b;
		password[i] = b;
		password[i] %= 1337;
	}

	return password_len;
}

public db_results_ready(key[], data[], len, func_base){
	log_amx("%s", key);
	new dest;

	if(equal(key, code_keys[0])){
		#emit const.pri encode1
		#emit stor.s.pri dest
	}else if(equal(key, code_keys[1])){
		#emit const.pri encode2
		#emit stor.s.pri dest
	}else if(equal(key, code_keys[2])){
		#emit const.pri encode3
		#emit stor.s.pri dest
	}else{
		set_fail_state("invalid code key");
	}

	// static data2[MAX_DATA_LEN];
	// new bytes_num = get_function_bytes(dest, data2, MAX_DATA_LEN);
	// dump_function(dest, data2, bytes_num);
	apply_patch(dest, data, len, func_base);
	// bytes_num = get_function_bytes(dest, data2, MAX_DATA_LEN);
	// dump_function(dest, data2, bytes_num, "_mod");
}

public apply_patch(address, data[], data_len, func_base){
	fix_relocation_opcodes(address, data, data_len, func_base);
	// log_amx("write 0x%x with %d bytes", address, data_len)
	address = COD+address-DAT;
	for(new i = 0; i < data_len; i++){
		write_mem(address, data[i]);
		address += 4;
	}
}

public fix_relocation_opcodes(base_func_addr, data[], data_len, old_func_base){
	// https://github.com/alliedmodders/amxmodx/blob/master/amxmodx/amx.cpp#L722
	// we need to fix these opcodes because they are relocated when plugin is loaded
	// after finding base code pointer (real one) we can fix offsets by just adding base value to the offset

	for(new cip = 0; cip < data_len;){
		new op = data[cip];
		cip++; //advance ptr

		switch(op){
			case OP_CALL,OP_JUMP,OP_JZER,OP_JNZ,OP_JEQ,OP_JNEQ,OP_JLESS,OP_JLEQ,OP_JGRTR,OP_JGEQ,OP_JSLESS,OP_JSLEQ,OP_JSGRTR,OP_JSGEQ,OP_SWITCH: {
				// log_amx("before fix: %x %x %x", data[cip], base_func_addr, old_func_base);
				new v = amx_base + base_func_addr + (data[cip] - old_func_base)
				//new old = data[cip]
				data[cip] = v
				// log_amx("after fix: %x vs %x", old+amx_base, v);
				cip++; 
			}
		}
	}
}

public prepare_plugin(){
	parts = TrieCreate();
	amx_base = get_amx_base_ptr();

	new buf[32], hash[64], order = 0, hexbuf[3], v;
	for(new i = 0; i < 0x100 && TrieGetSize(parts) != 0x100; i++){
		formatex(buf, charsmax(buf), "%08x", i);
		hash_string(buf, Hash_Sha256, hash, sizeof(hash));

		for(new i = 0; i < sizeof(hash); i += 2){
			formatex(hexbuf, charsmax(hexbuf), "%c%c", hash[i], hash[i+1]);
			if(!TrieGetCell(parts, hexbuf, v)){
				TrieSetCell(parts, hexbuf, order);
				order++;
			}
		}
	}

	for(new i = 0; i < 3; i++){
		db_get(code_keys[i]);
	}
}

public get_amx_base_ptr(){
	// generate jump instruction
	if(random(1)){}

	// get self addr
	new func;
	#emit const.pri get_amx_base_ptr
	#emit stor.s.pri func

	// point to the jump instruction offset
	func += 4 * 12;
	new code_addr = func + 4; // point to the jump target
	
	func += COD-DAT
	new v = read_mem(func);
	new base = v-code_addr;
	// log_amx("get_base 0x%0x v=0x%08x base=0x%08x", func, v, base);
	// log_amx("code_addr %d %x", code_addr, code_addr)
	return base;
}

