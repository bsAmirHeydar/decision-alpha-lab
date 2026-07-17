import copy,json
from _common import EX
from saed_v4_federated_confidential_research.service import run
x=json.loads((EX/"FULL_REFERENCE_INPUT.JSON").read_text());a=run(x);b=run(copy.deepcopy(x));assert a["replay"]["deterministic"] and a==b
future=copy.deepcopy(x);future["local_updates"].append({"update_id":"UPD-FUTURE","cell_id":"CELL-AMS-001","round_id":"ROUND-001","known_time":"2027-01-01T00:00:00Z","sample_count":999999,"vector":[99,99,99],"local_loss_before":9.0,"local_loss_after":0.0,"synthetic_fixture":True})
c=run(future);assert a["global_model"]["global_model_hash"]==c["global_model"]["global_model_hash"]
print("V4-33 deterministic replay and future-suffix invariance passed")
