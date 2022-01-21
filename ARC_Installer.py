import os
"""
pyinstaller --onefile --uac-admin --name installer ARC_Installer.py"
"""


def preliminares():
    """
    Criar as pastas para o funcionamento do aplicativo.
    Depois deste método, o arquivo de log ja esta funcionando!
    """
    diretoriosParaCriar = [r"C:\AutoRClone",
                           r"C:\AutoRClone\LOG",
                           r"C:\AutoRClone\LIB",
                           r"C:\AutoRClone\LIB\Config"]
    try:
        for dir in diretoriosParaCriar:
            if(os.path.exists(dir)):
                print(rf"O diretorio {dir} ja existe.")
                pass
            else:
                print(rf"O diretorio {dir} será criado.")
                os.mkdir(dir)
    except Exception as error:
        print("Houve algum erro ao criar os diretorios...")
        print(f"Erro: {error}")
    finally:
        print("\nOs diretorios foram criados com sucesso!\n")


def verificar_instalacao():
    """
    Primeiramente verifica se a pasta do rclone ja foi criada anteriormente...
    Se sim, entao ele vai sair do programa.
    Se nao, ele vai iniciar a instalacao do programa.
    """
    dir = r'C:\AutoRClone\rclone'
    if os.path.exists(dir):
        # O diretorio ja existe
        """ A DEFINIR OQUE FAZER AQUI """
        print("Ja esta instalado!")
        input("Pressione 'Enter' para sair...")
        exit()
    else:
        # O diretorio ainda nao existe
        preliminares()
        from SetupArchives import InstalarVariaveisAmbiente
        from SetupArchives import InstalarArquivos
        """ Instala os caminhos e dll do python necessarios para rodar o serviço do windows """
        instalador_paths = InstalarVariaveisAmbiente()
        instalador_paths.instalar_paths()

        """ Inicia a instalacao dos arquivos """
        install = InstalarArquivos()
        install.main()


if __name__ == "__main__":
    verificar_instalacao()
