import json,re
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
root=Path(__file__).parents[1]; env=(root.parents[3]/'accounts.env').read_text(); key=re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',env,re.M).group(1).strip()
client=create_client(chain=studionet,account=create_account(account_private_key=key)); tx=client.deploy_contract(code=(root/'contracts/contract.py').read_text(),args=[]); print('deploy_tx='+str(tx),flush=True)
receipt=client.wait_for_transaction_receipt(transaction_hash=tx,status='ACCEPTED',retries=120,interval=10000)
def find(x):
 if isinstance(x,dict):
  if x.get('contract_address') or x.get('contractAddress'): return x.get('contract_address') or x.get('contractAddress')
  if x.get('recipient') and str(x.get('tx_execution_result',''))=='1': return x['recipient']
  for y in x.values():
   z=find(y)
   if z:return z
 if isinstance(x,list):
  for y in x:
   z=find(y)
   if z:return z
address=find(receipt)
if not address:raise RuntimeError(receipt)
print(json.dumps({'contract':address,'deploymentTx':tx,'network':'StudioNet','receipt':receipt},default=str),flush=True)
