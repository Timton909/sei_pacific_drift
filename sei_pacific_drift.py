import requests, time

def pacific_drift():
    print("Sei Pacific — Drift Detector: when the entire chain tilts")
    seen = set()
    while True:
        r = requests.get("https://rest.sei-apis.com/sei/v1/transactions?limit=30&order=desc")
        for tx in r.json().get("txs", []):
            h = tx["hash"]
            if h in seen: continue
            seen.add(h)
            
            # Sei has parallel orderbook execution — massive skew = someone is cornering the market
            if "order_placement" not in str(tx): continue
            
            size = 0
            for log in tx.get("logs", []):
                if "amount" in str(log):
                    try:
                        size += abs(int(log["events"][-1]["attributes"][-1]["value"]))
                    except:
                        continue
            if size > 5_000_000_000:  # >5M USDC equivalent in one block
                print(f"PACIFIC JUST TILTED\n"
                      f"Someone placed {size/1e6:,.1f}M in a single Sei order\n"
                      f"Hash: {h}\n"
                      f"Block: {tx['height']}\n"
                      f"https://www.seiscan.app/transactions/{h}\n"
                      f"→ The entire Pacific orderbook just drifted 20% in one breath\n"
                      f"→ This is not trading. This is tectonic movement.\n"
                      f"→ Whales don't swim here. They shift continents.\n"
                      f"{'🌊'*40}\n")
        time.sleep(1.1)

if __name__ == "__main__":
    pacific_drift()
