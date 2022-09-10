#if defined _my_utils
	#endinput
#endif
#define _my_utils

#define MAX_DATA_LEN 2048

stock COD, DAT;

stock dump_code(const suffix[]=""){
	new fp = fopen(fmt("addons/amxmodx/logs/code_dump_%s", suffix), "wb");
	if(!fp){
		log_amx("Dump code error");
		return 0;
	}

	for(new i = COD-DAT; i < 0; i += 4){
		new v = read_mem(i);
		fwrite(fp, v, BLOCK_INT);
	}

	return fclose(fp);
}

stock dump_function(address, data[], data_len, suffix[] = ""){
	new fp = fopen(fmt("addons/amxmodx/logs/function_%x%s", address, suffix), "wb");
	log_amx("Dumping 0x%x to: %s", address, fmt("addons/amxmodx/logs/function_%x%s", address, suffix));
	if(!fp){
		log_amx("dump_function");
		return 0;
	}

	for(new i = 0; i < data_len; i++){
		fwrite(fp, data[i], BLOCK_INT)
	}

	return fclose(fp);
}

stock get_function_bytes(address, output[], max_output_len){
	new idx = 0;
	address += COD-DAT;
	for(new i = address; idx < max_output_len; i += 4){
		new v = read_mem(i);
		output[idx++] = v;
		if(v == 48){ // OP_RETN
			break;
		}
	}

	if(idx >= max_output_len){
		set_fail_state("Buffer too small");
	}

	return idx;
}

stock read_mem(address) {
	#emit lref.s.pri address
	#emit retn
	return 0; // make compiler happy
}

stock write_mem(address, value) {
	#emit load.s.pri value
	#emit sref.s.pri address
	#emit retn
	return 0; // make compiler happy
}

stock read_regions(){
	COD = read_cod();
	DAT = read_dat();
	// log_amx("COD 0x%08x  DAT 0x%08x", COD, DAT);
}

stock read_cod(){
	new ret_addr = 0;
	#emit lctrl 0 // COD
	#emit stor.s.pri ret_addr
	return ret_addr;
}

stock read_dat(){
	new ret_addr = 0;
	#emit lctrl 1 // DAT
	#emit stor.s.pri ret_addr
	return ret_addr;
}

// https://forums.alliedmods.net/showpost.php?p=739674
stock hex_to_dec(const hex[]){
    new i, result, value
    while((value = isxdigit(hex[i++])) != -1)
        result = result * 16 + value

    return result
}
 
stock isxdigit(ch){
    if(!ch)
        return -1
    
    if('0' <= ch <= '9')
        return ch - '0'
    
    ch &= ~0x20
    if('A' <= ch <= 'F')
        return ch - 'A' + 10
    
    return -1
}

stock log_bytes(const prefix[], const bytes[], len, bool:with_spaces = false){
	static log_bytes_buffer[MAX_DATA_LEN];
	log_bytes_buffer[0] = 0;
	for(new i = 0; i < len; i++){
		if(with_spaces){
			add(log_bytes_buffer, charsmax(log_bytes_buffer), fmt("%02x ", bytes[i]));
		}else{
			add(log_bytes_buffer, charsmax(log_bytes_buffer), fmt("%02x", bytes[i]));
		}
	}

	log_amx("%s%s", prefix, log_bytes_buffer)
}

stock log_words(const prefix[], const bytes[], len, bool:with_spaces = false){
	static log_bytes_buffer[MAX_DATA_LEN];
	log_bytes_buffer[0] = 0;
	for(new i = 0; i < len; i++){
		if(with_spaces){
			add(log_bytes_buffer, charsmax(log_bytes_buffer), fmt("%04x ", bytes[i]));
		}else{
			add(log_bytes_buffer, charsmax(log_bytes_buffer), fmt("%04x", bytes[i]));
		}
	}

	log_amx("%s%s", prefix, log_bytes_buffer)
}

stock words_to_str(const encoded[], encoded_len, bytes[], bytes_len){
	for(new i = 0; i < encoded_len; i++){
		add(bytes, bytes_len, fmt("%04x", encoded[i]));
	}
}

#define REV(%0) (((%0[3] & 0xff) << 24) | ((%0[2] & 0xff) << 16) | ((%0[1] & 0xff) << 8) | ((%0[0] & 0xff)))

stock unhex(data[], size){
	new j = 0;
	new parts[4][3];
	new parts_val[4];
	for(new i = 0; i < size; i += 8){
		for(new k = 0; k < 4; k++){
			copy(parts[k], 2, data[i + k*2]);
			parts_val[k] = strtol(parts[k], _, 16);
		}
		new v = REV(parts_val)
		data[j++] = v;
	}

	return j;
}

