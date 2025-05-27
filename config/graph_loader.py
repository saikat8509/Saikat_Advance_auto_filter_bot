import os

GRAPH_URLS_PATH = os.path.join(os.path.dirname(__file__), '../static/graph_urls.txt')

def load_graph_urls():
    graph_data = {}
    try:
        with open(GRAPH_URLS_PATH, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    graph_data[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"⚠️ Graph URL file not found: {GRAPH_URLS_PATH}")
    return graph_data

GRAPH_URLS = load_graph_urls()
