from py_setenv import setenv
import os
import sys
import threading
### Este arquivo tem a funcao de adicionar os paths necessarios para que o servico do windows funcione corretamente.
## Paths necessarios para o funcionamento:
# C:\Users\Fabricio Softgran\AppData\Local\Programs\Python\Python39\
# C:\Users\Fabricio Softgran\AppData\Local\Programs\Python\Python39\Scripts\
# C:\Users\Fabricio Softgran\AppData\Local\Programs\Python\Python39\lib\site-packages\pywin32_system32


class InstalarVariaveisAmbiente:
    def instalar_paths(self):
        path_python = []
        path_python.append(os.path.dirname(sys.executable))  # C:\Users\Fabricio Softgran\AppData\Local\Programs\Python\Python39\
        path_python.append(os.path.dirname(sys.executable) + r"\Scripts")  # C:\Users\Fabricio Softgran\AppData\Local\Programs\Python\Python39\Scripts\
        path_python.append(os.path.dirname(sys.executable) + r"\lib\site-packages\pywin32_system32")  # C:\Users\Fabricio Softgran\AppData\Local\Programs\Python\Python39\lib\site-packages\pywin32_system32

        ## Define Paths do User e do System
        paths_existentes_user = setenv("path", user=True, suppress_echo=True)
        paths_existentes_system = setenv("path", suppress_echo=True)
        print("Instalando PATHS")
        try:
            for path in path_python:
                ## Verifica se existe os paths no usuario, e entao adiciona caso nao exista.
                if not (path in paths_existentes_user):
                    t = threading.Thread(
                                target=setenv,
                                daemon=True,
                                kwargs={
                                    'value': path,
                                    'append': True,
                                    'user': True,
                                    'suppress_echo': True
                                })
                    t.start()
                    # t.join()
                    # setenv("path", value=path, append=True, user=True, suppress_echo=False)

                ## Verifica se existe os paths no usuario, e entao adiciona caso nao exista.
                if not (path in paths_existentes_system):
                    t2 = threading.Thread(
                                target=setenv,
                                daemon=True,
                                kwargs={
                                    'value': path,
                                    'append': True,
                                    'suppress_echo': True
                                 })
                    t2.start()
                    # t2.join()
                    # setenv("path", value=path, append=True, suppress_echo=False)
        except Exception as e:
            print(f"Houve um erro ao tentar adicionar {path} nas variaveis de ambiente. Erro: {e} Por favor verifique!")
        finally:
            print("Paths instalados!\n")


if __name__ == "__main__":
    install = InstalarVariaveisAmbiente()
    install.instalar_paths()
