from src.Helpers.helper import request_get
from config import RPC_EXPLOLER
from time import sleep


def get_txn_list_from_address(address, offset):
    attempt = 1
    url = (f'https://api.lineascan.build/api?module=account&action=txlist'
           f'&address={address}'
           f'&startblock=0'
           f'&endblock=99999999'
           f'&page=1'
           f'&offset={offset}'
           f'&sort=desc'
           f'&apikey={RPC_EXPLOLER}')
    while attempt < 4:
        attempt += 1
        r = request_get(url, None, None)
        sleep(0.21)
        if r.status_code == 200:
            res = [r.json()]
            if res[0]['message'] == 'OK':
                txn_list = res[0]['result']
                return txn_list
    return []


def check_txn_existence(address:str, txn_list, contract_address:str, method_id):
    for txn in txn_list:
        if (txn['from'] == address.lower() and
                txn['to'] == contract_address.lower() and
                txn['methodId'] == method_id and
                txn['isError'] != 1):
            return txn
    return None
