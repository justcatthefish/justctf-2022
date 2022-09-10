import subprocess
import os
import shutil
import colorama
from colorama import Fore
import sys

def main(fname):
	source = f'{fname}.sma'
	compiled = f'{fname}.amxx'
	compiler_folder = f'.'

	compile_cmds = [
		# f'amxxpc.exe -a {source}',
		f'amxxpc.exe {source}',
	]

	for compile_cmd in compile_cmds:
		print(f"{Fore.LIGHTGREEN_EX}\nCompiling: {compile_cmd}...")
		
		try:
			compile_output = subprocess.check_output(compile_cmd, cwd=f'{compiler_folder}', stderr=subprocess.PIPE, shell=True)
			compile_output = compile_output.decode()
			if '-a' not in compile_cmd:
				print(compile_output)
		except subprocess.CalledProcessError as exc:
			if '-a' not in compile_cmd:
				output = exc.stderr.decode()
				if not output:
					output = exc.stdout.decode()
				print(exc)
				print(f'{Fore.RED}Error!')
				print(f'{output}')

	#install plugin
	print(f"{Fore.LIGHTGREEN_EX}\nInstalling plugin...", end='')
	#shutil.copy(f'{compiler_folder}\{compiled}', f"D:/games/Counter-Strike 1.6 v43/cstrike/addons/amxmodx/plugins/")
	#shutil.copy(f'{compiler_folder}\{compiled}', f"../../for_user/addons/amxmodx/plugins")
	print(f"{Fore.LIGHTBLUE_EX} OK!")

	# with open(f'{compiler_folder}/{fname}.asm', "r+") as f:
	# 	asm = f.read().splitlines()
	# 	f.seek(0)
	# 	f.write('\n'.join(filter(lambda l: 'break' not in l, asm)))
	# 	f.truncate()

	
			
if __name__ == "__main__":
	colorama.init(autoreset=True)
	if len(sys.argv) == 1:
		print("Usage: build.py fname [fname...]")
		exit(2)

	for fname in sys.argv[1:]:
		main(fname)
