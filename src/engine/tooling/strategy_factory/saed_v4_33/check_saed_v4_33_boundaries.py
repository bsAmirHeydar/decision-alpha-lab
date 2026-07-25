from _common import ROOT
roots=[ROOT/"src/engine/packages/saed_v4_federated_confidential_research"]
forbidden=["MetaTrader5.initialize(","OrderSend(","trade.Buy(","trade.Sell(","live_credentials","socket.connect("]
for base in roots:
    for p in base.rglob("*.py"):
        text=p.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text,f"forbidden token {token} in {p}"
print("V4-33 authority boundaries passed")
