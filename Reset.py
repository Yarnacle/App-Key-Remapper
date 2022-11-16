import os,winreg,ctypes,sys,shutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

os.system("title " + 'App Key Reset')

if is_admin():
	scripts_path = f'{os.path.expanduser("~/Documents")}\Keyboard Remap Scripts'
	path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\AppKey\\'
	script_directory_exists = os.path.exists(scripts_path)
	if script_directory_exists:
		os.chdir(scripts_path)
	appkey = input('App key to be reset or leave blank to reset all >>> ')

	if appkey:

		winreg.DeleteValue(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path + appkey,0,winreg.KEY_SET_VALUE),'ShellExecute')

		if os.path.exists(appkey):
			shutil.rmtree(appkey)
		if not any(os.scandir(scripts_path)):
			os.chdir('..')
			os.rmdir(scripts_path)

		print(f'Successfully reset app key {appkey}')

	else:
		hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path)
		try:
			i = 0
			while True:
				try:
					key_number = winreg.EnumKey(hkey,i)
				except:
					break

				try:
					winreg.DeleteValue(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path + key_number,0,winreg.KEY_SET_VALUE),'ShellExecute')
				except:
					pass
				i += 1
		except:
			pass

		if script_directory_exists:
			os.chdir('..')
			shutil.rmtree(scripts_path)
		
		print('Successfully reset all app keys')
	os.system('pause')

else:
	ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable,'"Reset.py"',None ,1)