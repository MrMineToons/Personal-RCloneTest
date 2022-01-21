import subprocess
import os
import zipfile
import requests
import io
import shutil
import glob
import threading
import json
# from setup_logger import logger


class InstalarArquivos():
    """
    INSTALACAO DOS ARQUIVOS NO DISCO C:
    """

    def instala_servico_windows(self):
        """ Copia o executavel arc_srv e instala o mesmo como um serviço do windows """
        # Copiar .exe para o disco C:\
        loc = str(os.getcwd() + r"\LIB\Core")
        src = loc
        dest = r"C:\AutoRClone\LIB\Core"
        print("")
        print(fr"- Copiando 'Core' para {dest}")
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print("- 'Core' copiado.")

        print("- Instalando o serviço do windows.")
        # Inicia a instalacao do serviço chamando o .exe
        try:
            error = False
            # C:\AutoRClone\LIB\Core\arc_srv.exe
            args = [r'C:\AutoRClone\LIB\Core\arc_srv.exe', '--startup', 'delayed', 'install']
            install_service = subprocess.run(args, capture_output=True, text=True)
        except Exception as e:
            error = True
            print(f"Houve um erro ao instalar o serviço do windows: {e}. STDOUT= {install_service.stdout} || STDERR= {install_service.stderr}")

        if error is False:
            print("- Serviço do Windows instalado com sucesso. Nome do Serviço: RCloneServiceTest.\n\n")

    def instalar_API(self):
        """ Copia os arquivos necessarios para o funcionamento da API para a raiz no disco C """
        loc = str(os.getcwd() + r"\LIB\API")
        src = loc
        dest = r"C:\AutoRClone\LIB\API"
        print(fr"- Copiando 'template' e 'static' e outras dependencias para {dest}")
        try:
            error = False
            shutil.copytree(src, dest, dirs_exist_ok=True)
        except Exception as e:
            error = True
            print(f"Houve um erro ao tentar copiar 'template' e 'static': {e}")

        if error is False:
            print("- 'template' e 'static' copiados com sucesso!")

    def instala_Configs_No_Disco_C(self):
        """ Copias os arquivos de configuracao no disco C """
        error = False
        dir_config = r"C:\AutoRClone\LIB\Config"
        self.dir_config_file = dir_config + r"\config.json"

        loc = str(os.getcwd() + r"\LIB\Config")
        src = loc
        dest = r"C:\AutoRClone\LIB\Config"
        try:
            print(fr"- Copiando 'Config' e outras dependencias para {dest}")
            shutil.copytree(src, dest, dirs_exist_ok=True)
        except Exception as e:
            error = True
            print(f"Houve um erro ao copiar 'Config'. Erro: {e}")

        if error is False:
            print("- 'Config' copiado com sucesso!")

    def verifica_rclone_config_file(self):
        comando = [r'C:\AutoRClone\rclone\rclone.exe', 'config', 'file']
        rodar_rclone_config = subprocess.run(comando, capture_output=True, text=True)
        self.config_path_rclone = rodar_rclone_config.stdout
        self.config_path_rclone = self.config_path_rclone.split('\n')[1]
        with open(self.dir_config_file, 'r') as file:
            self.backup_file = json.load(file)

        with open(self.dir_config_file, 'w') as file2:
            self.backup_file['conf_path'] = self.config_path_rclone
            # Aqui sera recebido uma mensagem com o seguinte conteudo: Configuration file is stored at: \nC:\\Users\MaquinaFOrmatadazz.config\\rclone\\rclone.conf\n
            json.dump(self.backup_file, file2, indent=4)

    def path_existe(self):
        """ Verifica se o RClone ja foi baixado antes. Se sim substitui pelo mais recente """
        # for name in glob.glob(r"C:\AutoRClone\*.py"):
        if os.path.exists(r'C:\AutoRClone\rclone'):
            try:
                print(fr"- Encontrado {name} em C:\AutoRClone. Deletando a pasta e substituindo pela mais recente.")
                shutil.rmtree(name)
            except Exception as e:
                print(fr"Por algum motivo, eu nao tive sucesso em excluir ou verificar a existencia da pasta C:\AutoRClone... Erro: {e}")

        self.download_RClone_and_Unzip()

    def renomeia_download_do_Rclone(self):
        print("- Renomeando arquivo do RClone")
        if(os.path.exists(r"C:\AutoRClone\rclone")):
            shutil.rmtree(r"C:\AutoRClone\rclone")
        ## Renomeia o diretorio para utilizar com mais facilidade
        error = False
        for name in glob.glob(r"C:\AutoRClone\rclone*"):
            try:
                os.rename(name, r"C:\AutoRClone\rclone")
            except Exception as e:
                error = True
                print(f"Ocorreu um erro ao renomear a pasta do RCLone, por favor verifique a sua instalacao, ou renomeia manualmente a pasta. Erro: {e}")
            finally:
                print(rf"- Pasta {name} renomeada para 'C:\AutoRClone\rclone'")

        if error is False:
            print("- Renomeado com sucesso!")

    def download_RClone_and_Unzip(self):
        """ Faz download e extrai o .zip do rclone para o direitorio principal """
        rclone_download = "https://downloads.rclone.org/rclone-current-windows-amd64.zip"
        try:
            print(f"- Iniciando o download do rclone em {rclone_download}")
            r = requests.get(rclone_download)
        except Exception as e:
            print(f"Ocorreu algum erro ao tentar fazer o download do RClone, Execute o setup novamente... Erro: {e}")
        finally:
            print("- Download Concluido.")

        ## Zipar e extrair
        try:
            print("- Iniciando extracao da .zip do RClone")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(r"C:\AutoRClone")
        except Exception as e:
            print(f"Houve um erro ao extrair o conteudo de RClone. Erro: {e}")
        finally:
            print("- Extracao Concluida.")
            self.renomeia_download_do_Rclone()

    def main(self):
        """ Instala as pastas e arquivos necessarios para o funcionamento do AutoRClone em C:/AutoRClone """
        try:
            download_install_RCLONE = threading.Thread(target=self.path_existe)  # Faz o download do RClone e renomeia para ser utilizado
            download_install_RCLONE.start()
            self.instala_Configs_No_Disco_C()  # Copia a pasta CONFIG para C:/
            self.instalar_API()  # Copia a pasta API para C:/
            self.instala_servico_windows()  # Copia o .exe do serviço, e inicia ele
        except Exception as e:
            print(f"Houve um erro ao tentar executar ARC_setup. Erro: {e}")
        finally:
            print("Ainda concluindo o download de RClone... Aguarde por favor")
            download_install_RCLONE.join()
            self.verifica_rclone_config_file()
            input("Concluido! Pressione 'Enter' para sair...")


if __name__ == "__main__":
    instalar = InstalarArquivos()
    instalar.main()
