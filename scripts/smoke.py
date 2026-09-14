import json, re, time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text()
KEY = re.search(r'^ACCOUNT_1_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
DEPLOYMENT = json.loads((ROOT / "deployment.json").read_text())
ACCOUNT = create_account(account_private_key=KEY)
CLIENT = create_client(chain=studionet, account=ACCOUNT)
ADDRESS = DEPLOYMENT["contractAddress"]


def send(method, args):
    tx = CLIENT.write_contract(address=ADDRESS, function_name=method, args=args)
    print(method, tx, flush=True)
    CLIENT.wait_for_transaction_receipt(
        transaction_hash=tx, status=TransactionStatus.FINALIZED, retries=180, interval=5000
    )
    info = CLIENT.get_transaction(transaction_hash=tx)
    receipts = (info.get("consensus_data") or {}).get("leader_receipt") or []
    if info.get("status_name") != "FINALIZED" or not any(
        item.get("execution_result") == "SUCCESS" for item in receipts
    ):
        raise RuntimeError({"tx": tx, "status": info.get("status_name"), "receipts": receipts})
    return tx


route_id = "RR-" + str(int(time.time()))
opened = send(
    "open_route",
    [
        route_id,
        ACCOUNT.address,
        "A public HTTP service needs a standards-grounded remediation path for inconsistent request semantics.",
        [
            "Align request handling and documentation with RFC 9110 HTTP semantics.",
            "Replace the HTTP interface with an unrelated SMTP workflow.",
        ],
        "https://www.rfc-editor.org/rfc/rfc9110.txt",
        "https://datatracker.ietf.org/doc/html/rfc9110",
        3600,
    ],
)
selected = send("select_remedy", [route_id])
state = CLIENT.read_contract(address=ADDRESS, function_name="get_route", args=[route_id])
print(json.dumps(state, indent=2), flush=True)
assert state["state"] == "REMEDY_OPEN"
assert state["completion_window"] == 3600
assert state["completion_deadline"] > 0
proof = {
    "routeId": route_id,
    "transactions": {"openRoute": opened, "selectRemedy": selected},
    "state": state,
}
(ROOT / "network-run.json").write_text(json.dumps(proof, indent=2))
print(json.dumps(proof, indent=2))
