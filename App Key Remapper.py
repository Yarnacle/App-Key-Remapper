import os,winreg,ctypes,sys,re

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
	appkey = input('App Key to be remapped >>> ')

	map_type = input('Map App Key to (k)ey input or (c)ustom script >>> ')
	while map_type not in ['k','c']:
		print('Please choose (k) or (c)')
		map_type = input('Map App Key to (k)ey input or (c)ustom script >>> ')

	if map_type == 'k':
		scripts_path = f'{os.path.expanduser("~/Documents")}\Keyboard Remap Scripts'

		if not os.path.exists(scripts_path):
			os.makedirs(scripts_path)
		os.chdir(scripts_path)

		if not os.path.exists(appkey):
			os.makedirs(appkey)
		os.chdir(appkey)
		scripts_path = f'{scripts_path}\{appkey}'

		def make_script(extension,content):
			script = open(f'{appkey}.{extension}','w')
			script.write(content)
			script.close()
		
		new_key = input('New keycode >>> ')

		make_script('bat',f'powershell -ExecutionPolicy RemoteSigned -File "{scripts_path}\{appkey}.ps1"')
		make_script('ps1',f'$wshShell = new-object -com wscript.shell\n$wshShell.SendKeys([char]{new_key})')
		make_script('vbs',f'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "{scripts_path}\{appkey}.bat" & Chr(34),0\nSet WshShell = Nothing')
		shell_script_path = f'{scripts_path}\{appkey}.vbs'

	else:
		shell_script_path = input('Path to custom script >>> ')

	reg_key = winreg.OpenKey(
		winreg.HKEY_LOCAL_MACHINE,
		r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\AppKey\\' + appkey,
		0,winreg.KEY_SET_VALUE
	)
	winreg.SetValueEx(reg_key,'ShellExecute',0,winreg.REG_SZ,f'"{shell_script_path}"')
	print('Key successfully remapped')
	os.system('pause')

else:
	ctypes.windll.shell32.ShellExecuteW(None,"runas", sys.executable,'remapper.py',None, 1)