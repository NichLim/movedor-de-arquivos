import json
import shutil
import os
import sys
import time
import logging

timestr = time.strftime('%d.%m.%Y %H.%M.%S')
logger = logging.getLogger("main") # inicializa o arquivo de Log
#configura o logger e a formatação da mensagem para inclusão de hora/data nas mensagens
logging.basicConfig(filename = "Log - %s.log" %timestr, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S') 

logger.info('Inicializando')

with open('config.json') as config: #extraindo as informações de whitelist, origem e destino do arquivo config.json da pasta do programa
    config_from_JSON = json.load(config)
    logger.info('Carregando informações do JSON')
    
    logger.info('Validando Pasta de Origem')
    if os.path.exists(config_from_JSON["origem"]):  #Verifica se o endereço original dentro do JSON é um caminho válido no Sistema
        origem = config_from_JSON["origem"]
        logger.info('Endereço de Origem %s válido', origem)
    else:
        logger.warning('Origem Inválida. Por favor, verifique o arquivo config.json')
        logger.error('Um erro foi encontrado durante a execução do programa, por favor verifique o Log')
        sys.exit(0)
    
    logger.info('Validando Pasta de Destino')
    if os.path.exists(config_from_JSON["destino"]):  #Verifica se o endereço de destino dentro do JSON é um caminho válido no Sistema
        destino = config_from_JSON["destino"]
        logger.info('Endereço de Destino %s válido', origem)
    else:
        logger.warning('Origem Inválida. Por favor, verifique o arquivo config.json')
        logger.error('Um erro foi encontrado durante a execução do programa, por favor verifique o Log')
        sys.exit(0)

    logger.info('Verificando Whitelist')
    if isinstance(config_from_JSON["whitelist"], list): #Verifica se a Whitelist é uma Lista Python válida (arrays são resolvidos como Listas quando são importados)
        whitelist = config_from_JSON["whitelist"]
        logger.info('Whitelist Válida: %s', whitelist)
    else:
        logger.warning('Whitelist Inválida. Por favor verifique o arquivo config.json')
        logger.error('Um erro foi encontrado durante a execução do programa, por favor verifique o Log')
        sys.exit(0)
    config.close()


arquivos = list(set(os.listdir(origem)) - set(whitelist)) #lista com os arquivos da pasta sem os arquivos da whitelist

if len(arquivos) == 0:  #Checa se há algo para transferir
    logger.warning('Não há arquivos a serem transferidos')

for a, arquivo in enumerate(arquivos):
    shutil.move(os.path.join(origem, arquivo), os.path.join(destino, arquivo))
    logger.info('Transferindo %s', arquivo)
    if a == len(arquivos) - 1 : #Checa se está no último arquivo da lista de arquivos
        logger.info('Transferencia Completa.')