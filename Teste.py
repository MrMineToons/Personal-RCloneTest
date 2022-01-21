import json

def leitor():
    """ LE AS INFORMAÇÕES DO ARQUIVO DE CONFIGURAÇÃO config.json """
    dir_config_file = r"C:\AutoRClone\LIB\Config\config.json"
    with open(dir_config_file, 'r') as f:
        config = json.load(f)
    n_backups = 0
    backup_info = []
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
            print(config[backup_num]['metodo'])
            print(config[backup_num]['remote_name'])
            print(config[backup_num]['arquivo_log'])
            print(config[backup_num]['pasta_servidor'])
            print(config[backup_num]['pasta_nuvem'])
            print(config['times'])
            print(config['conf_path'])
            backup_info.append([config[backup_num]['metodo'],
                               config[backup_num]['remote_name'],
                               config[backup_num]['arquivo_log'],
                               config[backup_num]['pasta_servidor'],
                               config[backup_num]['pasta_nuvem']])
            backup_info.append(config['times'])
            backup_info.append(config['conf_path'])
    finally:
        print(backup_info)
        return backup_info


if __name__ == "__main__":
    leitor()
