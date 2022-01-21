from SMWinservice import SMWinservice
import time
from mainFile import MontaBackup, leitor
import uvicorn
from multiprocessing import Process, freeze_support
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from apscheduler.workers.sync import SyncWorker
from setup_logger import logger
import API_Control

"""
Para instalar com o PyInstaller, rodar o comando
pyinstaller --onefile --uac-admin --hidden-import=win32timezone --name arc_srv ServicoManager.py
"""


class PythonService(SMWinservice):
    _svc_name_ = 'RCloneServiceTest'
    _svc_display_name_ = 'RCloneServiceTest'
    _svc_description_ = 'RClone Servico de backup do Fabricio'

    def start(self):
        logger.info("************************************")
        logger.info(f"Iniciando o servico: {self._svc_name_}")
        logger.info("************************************")
        self.isrunning = True

    def stop(self):
        logger.info("************************************")
        logger.info(f"Parando o servico: {self._svc_name_}")
        logger.info("************************************")
        self.stop_API()
        self.isrunning = False

    def create_jobs(self):
        """ Criar e agendar os serviçõs segundo as configurações """
        # schedule = BackgroundScheduler(daemon=True)
        # schedule.add_job(main.main, 'interval', minutes=1, id="Test_Job")
        # run_date=datetime(2021, 5, 21, 17, 15, 10)
        schedule = BackgroundScheduler()
        schedule.start()

        self.info_processos, self.backup_confs = leitor()
        # Oque vai ser recebido pelo leitor sao as seguintes informações:
        # [config[backup_num]['metodo'],        - ITEM 0 NA LISTA
        # config[backup_num]['remote_name'],    - ITEM 1 NA LISTA
        # config[backup_num]['arquivo_log'],    - ITEM 2 NA LISTA
        # config[backup_num]['pasta_servidor'], - ITEM 3 NA LISTA
        # config[backup_num]['pasta_nuvem'],    - ITEM 4 NA LISTA
        # config['times'],          - ITEM 5 NA LISTA
        # config['conf_path']       - ITEM 6 NA LISTA
        # ])
        schedule.add_job(self.start_Processes, id="Iniciar_Servico")
        self.backup_confs[0] = self.backup_confs[0].split(',')
        x = 0
        for time_backup in self.backup_confs[0]:
            hora, minuto = time_backup.split(':')
            logger.info(f"Perfil de backup '{self.info_processos[0][4]}' agendado para as {hora}:{minuto}.")
            schedule.add_job(self.start_Processes, 'cron', hour=int(hora), minute=int(minuto), id=f"Tarefa-{str(x)}")
            x += 1

    def start_API(self):
        """ Inicializar a API como um processo em outro nucleo """
        self.API = Process(target=uvicorn.run,
                           kwargs={
                               "app": "API_Control:app",
                               "host": "0.0.0.0",
                               "port": 80,
                               "log_level": "info"})
        self.API.daemon = True
        self.API.start()
        logger.info(f'API iniciada em: {self.API} porta 80')

    def stop_API(self):
        """ Matar o processo da API criado em start_API() """
        self.API.terminate()
        time.sleep(0.1)
        if not self.API.is_alive():
            self.API.join(timeout=1.0)

    def start_Processes(self):
        logger.info("Iniciando BACKUPS")
        # logger.info(f"Configurações carregadas para 'rclone.conf' do usuario: {self.path_rclone_config_file}")
        processos = []
        # Processos armazena todos os dados necessarios que foram coletador do arquivo de configuração
        # ex: ("metodo": "sync", "nuvem": "backup", "arquivo_log": "RcloneSyncLOG.txt", "pasta_servidor": "\\\\192.168.0.91\\Softgran", "pasta_nuvem": "Servidor_Antigo_Softgran")
        # Inicia cada processo de backup(contidos em config.json) com um nucleo diferente
        for p in self.info_processos:
            try:
                key_words = {
                    'metodo': p[0], 'remote_name': p[1], 'arquivo_log': p[2],
                    'pasta_servidor': p[3], 'pasta_nuvem': p[4], 'conf_path': self.backup_confs[1]
                    }
                mp = Process(target=MontaBackup, kwargs=key_words)
                processos.append(mp)
                mp.start()
                logger.info(f"Processo {p[1]}:{p[4]} PID:{mp.pid} está iniciando...")
            except Exception as e:
                logger.error(f"O processo {p[1]}:{p[4]} PID:{mp.pid} executou com falha... É necessario verificar seus parametros... Erro: {e}")

        # Entram na fila de espera...
        for i in processos:
            try:
                i.join()
            except Exception as e:
                logger.error(f"{i[1]} PID:{i.pid} encontrou dificuldades para entrar fila. Erro: {e}")

        # Assim que todos os processos de rclone forem finalizados, o programa terminará...
        logger.info("Os backups finalizaram! Finalizando o sistema de backups... Aguardando novas ordens")

    def main(self):
        self.create_jobs()
        self.start_API()
        while self.isrunning:
            try:
                time.sleep(2)
            except Exception:
                self.scheduler.shutdown()
                break


if __name__ == '__main__':
    freeze_support()
    PythonService.parse_command_line()
