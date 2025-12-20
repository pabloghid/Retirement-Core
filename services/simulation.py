def summarize_sim(response):

    first = response[0]
    last = response[-1]

    # Indexa investimentos iniciais
    initial_map = {
        f"{i['asset']}:{i['type']}": i["balance"]
        for i in first["by_type"]
    }

    investments_summary = []

    for item in last["by_type"]:
        key = f"{item['asset']}:{item['type']}"
        initial = initial_map.get(key, 0)
        final = item["balance"]

        gain_percent = (
            ((final - initial) / initial) * 100
            if initial > 0 else 0
        )

        investments_summary.append({
            "asset": item["asset"],
            "type": item["type"],
            "initial": initial,
            "final": final,
            "gain_percent": str(round(gain_percent, 2)) + "%"
        })

    total_gain_percent = (
        ((last["total"] - first["total"]) / first["total"]) * 100
        if first["total"] > 0 else 0
    )

    return {
        "investments": investments_summary,
        "total": {
            "initial": first["total"],
            "final": last["total"],
            "gain_percent": str(round(total_gain_percent, 2)) + "%"
        }
    }