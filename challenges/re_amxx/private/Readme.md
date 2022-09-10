# re-amxx

## dekompilatory/disasmy

## amxxdump

### bez zapezbieczen
- wywala sie na d0, d1
- disasm na default

### `pragma compress 1`
- nieczytelne

### `#emit sysreq.c`
- nieczytelne


## Lysis java

### bez zapezbieczen
- pełna dekompilacja

### `pragma compress 1`
- pełna dekompilacja

### `#emit sysreq.c`
- nieczytelne (da się zfixować)

# ASM
![](https://i.imgur.com/rcPXSY1.png)
![](https://i.imgur.com/x5UAZSX.png)


```
	#emit const.pri to_call2
	#emit push.c 12
	#emit push.c 4
	#emit call.pri
```

```
	#emit const.pri to_call2
	#emit push.c 0
	#emit call.pri
```

# anti decompiler

## call.pri
Gdy uzyjemy `call.pri` lysis sie wykłada, `jrel` tak samo.
```
/* ERROR! Unrecognized opcode: jrel */
```

gdy spatchujemy lysisa tak zeby skipowal te instrukcje (traktowal je nopem) to outputy takie:

```
public read_cod()
{
	new ret_addr;
	return ret_addr;
}

public testcmd(id, _arg1, _arg2, _arg3, _arg4, _arg5, _arg6, _arg7, _arg8, _arg9, _arg10, _arg11, _arg12, _arg13, _arg14, _arg15, _arg16, _arg17, _arg18)
{
	new var1 = 4;
	to_call();
	log_amx("lubie %d", var1);
	testcmd(var1);
	return 1;
}
```

## jrel trik

mozemy przeskakiwac kilka instrukcji
```
	#emit const.pri 10
	#emit jrel 8
	#emit add.c 1 // skipowana
	#emit push.pri
	#emit push.c 4
	#emit const.pri to_call2
	#emit call.pri
```

Nic nie daje jak mamy listing asemblera

## fmt

Uzywanie fmt do formatowania powoduje, że output z lysis-java jest taki:
```
	new i;
	while (i < 256)
	{
		new v;
		fmt("%02x", i);

/* ERROR! Can't print expression: Heap */
 function "prepare_plugin" (number 7)
public plugin_end()
{
	TrieDestroy(parts);
	return 0;
}
```

Łatwo fixnąć w dekompilatorze

# Wnioski

- jeśli JIT lub ASM32 jest włączony to sekcja code zawiera kod asemblerowy, zamiast PAWN'owy
- funkcje zewnętrzne są callowane przez opcode `sysreq.c ID` gdzie id to id funkcji. Kolejnosc uzycia wplywa na to, ktora funkcja zostanie uzyta
- można patchować sekcje COD, używając negatywnych offsetów bo COD jest zaraz przed DAT
- żeby czytać adres funkcji musi być ona zadeklarowana wcześniej (wyżej) w pliku .sma 
- niektóre instrukcje np. `jump` muszą być relokowane i dynamiczne patchowanie 
