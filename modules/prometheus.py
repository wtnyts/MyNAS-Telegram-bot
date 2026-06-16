import requests

def get_prometheus_metric(query):
    try:
        response = requests.get(
            "http://192.168.1.45:9090/api/v1/query",
            params={"query": query},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data["data"]["result"]:
                value = data["data"]["result"][0]["value"][1]
                return float(value)
    except:
        return None