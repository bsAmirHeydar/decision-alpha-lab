import argparse,json
from .fixtures import candidate,bar,registry
from .engine import OutcomeEngine
from .models import SimulationPolicy

def main():
    p=argparse.ArgumentParser();p.add_argument("--ambiguity",choices=["stop","target","exclude"],default="stop");a=p.parse_args()
    policy=SimulationPolicy();engine=OutcomeEngine(policy,registry(0.05),"sf09.cost.fixture","1.0.0");engine.register(candidate(),1000)
    engine.process(bar(1,2000,100,101,99.5,100.5));engine.process(bar(2,3000,100.5,104.5,100,104));out=engine.pop()
    print(json.dumps({"outcome_id":out.outcome_id,"gross_r":out.gross_r,"net_r":out.net_r,"mfe_r":out.mfe_r,"mae_r":out.mae_r},indent=2))
if __name__=="__main__":main()
