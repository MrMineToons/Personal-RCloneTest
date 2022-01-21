import subprocess
import os
from shutil import copy, copytree


r"""
COMO EXECUTAR
- python start_pyinstaller.py
- Copiar 'installer.exe', 'API', 'Config', 'Core', 'SetupArchives' para uma pasta separada
- Executar installer.exe

COMO USAR
- Rodar 'C:\AutoRClone\rclone.exe config' no CMD
- Configurar 'C:\AutoRClone\LIB\Config\config.json' com suas necessidade


RODAR MANUALMENTE
pyinstaller --onefile --uac-admin --hidden-import=win32timezone --name arc_srv ServicoManager.py
pyinstaller --onefile --uac-admin --name installer ARC_Installer.py"
"""


def create_Service(root_dir):
    # pyinstaller --onefile --uac-admin --hidden-import=win32timezone --name arc_srv ServicoManager.py
    args = ["pyinstaller", "--onefile", "--uac-admin", "--hidden-import=win32timezone", "--name", "arc_srv", "ServicoManager.py"]
    print("\n")
    print("- Iniciando PYInstaller para Serviço do Windows.")
    try:
        error = False
        comando_processo = subprocess.run(args, capture_output=True, text=True)
    except Exception as e:
        error = True
        print(f"Houve um erro ao tentar gerar um executavel para o Serviço do Windows. Erro: {e}. STDOUT: {comando_processo.stdout}. STDERR: {comando_processo.stderr}")

    if error is False:
        src = root_dir + r"\dist\arc_srv.exe"
        dest = root_dir + r"\LIB\Core\arc_srv.exe"
        copy(src, dest)
        print("- O Serviço do Windows gerou um executavel com sucesso!")


def create_Folders(root_dir):
    # pyinstaller --onefile --uac-admin --name installer ARC_Installer.py
    print("\n")
    print("- Iniciando PYInstaller para o Instalador.")
    args = ["pyinstaller", "--onefile", "--uac-admin", "--name", "installer", "ARC_Installer.py"]
    try:
        error = False
        comando_processo = subprocess.run(args, capture_output=True, text=True)
    except Exception as e:
        error = True
        print(f"Houve um erro ao tentar gerar um executavel para o Instalador. Erro: {e}. STDOUT: {comando_processo.stdout}. STDERR: {comando_processo.stderr}")

    if error is False:
        src = root_dir + r"\dist\installer.exe"
        dest = root_dir + r"\installer.exe"
        copy(src, dest)
        print("- O instalador gerou um executavel com sucesso!")


def save_all_in_Distributable(root_dir):
    """ Cria uma pasta de distribuição da aplicação """
    # Precisa copiar:
    # 'API', 'Config', 'Core' e 'installer.exe'
    folder = root_dir + r'\LIB'
    dest_folders = root_dir + r"\Distributable\LIB"
    try:
        error = False
        copytree(folder, dest_folders, dirs_exist_ok=True)
        # Copiar installer.exe
        src = root_dir + r'\installer.exe'
        dest = root_dir + r'\Distributable'
        copy(src, dest)
    except Exception as e:
        error = True
        print(f"Nao foi possivel criar a pasta de distribuição. Erro: {e}")

    if error is False:
        print(rf"- Pasta de Distribuição criada com SUCESSO! em {root_dir}\Distributable")
        print("\n")


if __name__ == '__main__':
    root_dir = os.getcwd()
    print(root_dir)
    create_Folders(root_dir)
    create_Service(root_dir)
    save_all_in_Distributable(root_dir)
    input("Pressione 'Enter' para sair...")
