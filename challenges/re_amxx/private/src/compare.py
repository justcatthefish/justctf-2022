from pathlib import Path
import subprocess
import os
import shutil
import colorama
from colorama import Fore
import sys



def save_data(path, content):
	path = path.replace("\\", "_")
	path = Path(path).absolute()
	print(path)
	os.makedirs(path.parent, exist_ok=True)
	with open(path, 'wt', newline='') as f:
		f.write(content)

def main(fname):
	source = f'{fname}.sma'
	compiled = f'{fname}.amxx'
	compiler_folder = f'compiler'

	compile_cmds = [
		(f'{compiler_folder}/amxxpc.exe {source}', compiled),
	]

	for i in range(0):
		compiled_out = f'{fname}-d{i}.amxx'
		compile_cmds.append((f'{compiler_folder}/amxxpc.exe -d{i} -o{compiled_out} {source}', compiled_out))

	methods = [
		# f'amxx_uncompress1.1/amxx_uncompress.exe {fname}',
		('amxxdump', 'amxxdump', f'amxxdump.exe -d'),
		# ('Lysis', f'Lysis.exe'),
		('lysis-patched', '../solver', f'java -jar patched-lysis-decompiler.jar'),
	]

	results_folder = f'results/{fname}'
	shutil.rmtree(results_folder, ignore_errors=True)
	os.makedirs(results_folder, exist_ok=True)

	for compile_cmd, compiled_file in compile_cmds:
		print(f"{Fore.LIGHTGREEN_EX}\nCompiling: {compile_cmd}...")
		
		compile_output = subprocess.check_output(compile_cmd, cwd=f'{compiler_folder}')
		compile_output = compile_output.decode()
		print(compile_output)
		if 'compile failed' in compile_output:
			exit(1)

		for mname, cwd, decompile_cmd in methods:
			shutil.copy(f'{compiler_folder}/{compiled_file}', cwd)
			results_path = f'{results_folder}/{mname}_{compiled_file.removesuffix(".amxx")}'
			decompile_cmd = f'{decompile_cmd} {compiled_file}'
			print(f"{Fore.LIGHTBLUE_EX}Executing: {decompile_cmd}... ", end='')
			try:
				output = subprocess.check_output(decompile_cmd, cwd=f'{cwd}', stderr=subprocess.PIPE, shell=True)
				output = output.decode()
				# print(f'\n{output}')
			except subprocess.CalledProcessError as exc:
				output = exc.stderr.decode()
				if not output:
					output = exc.stdout.decode()
				print(f'{Fore.RED}Error!')
				print(f'{output}')
			
			save_data(results_path, output)
			Path(f'{cwd}/{compiled_file}').unlink()

			

if __name__ == "__main__":
	colorama.init(autoreset=True)
	if len(sys.argv) == 1:
		print("Usage: build.py fname [fname...]")
		exit(2)

	os.makedirs('results', exist_ok=True)
	for fname in sys.argv[1:]:
		main(fname)

