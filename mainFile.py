import time
import subprocess
import json
from setup_logger import logger


class MontaBackup():
    def __init__(self, metodo, remote_name, arquivo_log, pasta_servidor, pasta_nuvem, conf_path, *args, **kwargs):
        """ INICIALIZA E CRIA VARIAVEIS """
        self.tempo_iniciou = time.monotonic()
        self.metodo = metodo
        self.remote_name = remote_name
        self.arquivo_log = arquivo_log
        self.pasta_servidor = rf'{pasta_servidor}'
        self.pasta_nuvem = pasta_nuvem
        self.conf_path = conf_path
        self.caminho_exe_rclone = r'C:\AutoRClone\rclone\rclone.exe'
        self.run()

    def tempos(self):
        """ PROCEDIMENTO PARA LIDAR COM O TEMPO PARA SER UTILIZADO NO LOG """
        # Transforma de decimais para segundos.... E transforma tempo em string para "horario_de_termino_str"
        tempo_estimado = (self.tempo_finalizou - self.tempo_iniciou) / 60
        tempo_estimado_str = f"{tempo_estimado:0.2f}"
        # Armazena minutos e segundos_decimal em variaveis por meio de split
        self.minutos, self.segundos_decimal = (tempo_estimado_str).split(".", 1)
        # Transforma segundos decimal para segundos, multiplicando por segundos/min, link explicativo https://www.calculatorsoup.com/calculators/time/decimal-to-time-calculator.php
        self.segundos = (int(self.segundos_decimal) / 100) * 60

    def run(self):
        """ PROCEDIMENTO PARA CHAMAR O EXECUTAVEL DO RCLONE COM SEUS RESPECTIVOS ARGUMENTOS """
        try:
            # -L: Segue os symbol-links. Arquivos que sao atalhos,serao tratados como o arquivo verdadeiro
            # -q: Escreve menos informações no arquivo de log, um modo 'quiet'
            # rclone_caminho_nuvem = backup:Servidor_Teste
            self.rclone_caminho_nuvem = self.remote_name + ':' + self.pasta_nuvem

            # Exemplo: rclone -v copy C:\\Teste\sample.txt MyGDrive:/ -L -q
            args = [self.caminho_exe_rclone, self.metodo, self.pasta_servidor,
                    self.rclone_caminho_nuvem, "-L", "-q", "--config", self.conf_path,
                    f"--log-file={self.arquivo_log}"]
            comando_processo = subprocess.run(args, capture_output=True, text=True)
        except Exception as e:
            logger.error(f"Houve um erro ao tentar executar 'rclone.exe': {e}")
            logger.error(f"Check_ReturnCode: {comando_processo.check_returncode}")
            logger.error(f"Processo {self.pasta_nuvem} teve um erro, codigo: {comando_processo.returncode}... Saida do erro: {comando_processo.stderr} ||| {comando_processo.stdout}")

        self.tempo_finalizou = time.monotonic()
        self.tempos()
        if comando_processo.returncode == 0:
            logger.info(f"Processo {self.rclone_caminho_nuvem} foi finalizado com SUCESSO em {self.minutos}:{int(self.segundos):02d} minutos, com codigo de saida: {comando_processo.returncode}... RClone Log: {self.arquivo_log}")


"""
LEITURA DO ARQUIVO DE CONFIGURAÇÃO
"""


def leitor():
    """ LE AS INFORMAÇÕES DO ARQUIVO DE CONFIGURAÇÃO config.json """
    dir_config_file = r"C:\AutoRClone\LIB\Config\config.json"
    with open(dir_config_file, 'r') as f:
        config = json.load(f)
    n_backups = 0
    backup_info = []
    backup_confs = []
    # deve contar
    # - metodo = 'sync'
    # - remote_name = 'backupdrive'
    # - arquivo_log = 'C:\\AutoRClone\\RcloneSyncLOG.log'
    # - pasta_servidor = 'C:\\Teste\\File'
    # - pasta_nuvem: 'teste'
    # - times: '12:30,00:30'
    # - conf_path : 'C:\AutoRClone\LIB\Config...'

    # Tenta encontrar os itens na lista até dar erro
    try:
        for x in range(1000):
            # Conta quantos 'backup' tem no arquivo. Por exemplo, vai contar backup0, backup1, backup2...
            # E entao salvar a quantidade em n_backups
            verificador = "backup" + str(n_backups)
            config[verificador]
            n_backups += 1
    except Exception:
        # Apos contas quantos backups existem, começa a adicionar eles em 'backup_info[]'
        for i in range(n_backups):
            backup_num = "backup" + str(i)
            backup_info.append([config[backup_num]['metodo'],
                               config[backup_num]['remote_name'],
                               config[backup_num]['arquivo_log'],
                               config[backup_num]['pasta_servidor'],
                               config[backup_num]['pasta_nuvem']])
        backup_confs.append(config['times'])
        backup_confs.append(config['conf_path'])
    finally:
        return backup_info, backup_confs


if __name__ == "__main__":
    print("Nao deve ser executado diretamente...")
    exit()
