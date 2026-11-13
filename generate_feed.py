import json, datetime, pathlib, urllib.request, ssl

FEED_PATH = pathlib.Path('feed.json')
TODAY = datetime.datetime.utcnow().date()
URL = 'https://crates.io/api/v1/crates?page=1&per_page=30&sort=recent-downloads'

def fetch_new_crates():
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(URL, timeout=10, context=ctx) as resp:
        data = json.load(resp)
    today_str = TODAY.isoformat()
    return [c for c in data['crates'] if c['created_at'].startswith(today_str)]

def build_feed(crates):
    items = []
    for c in crates:
        items.append({
            'title': c['name'],
            'description': c.get('description') or '',
            'url': f"https://crates.io/crates/{c['name']}",
            'published': c['created_at']
        })
    return {'generated': datetime.datetime.utcnow().isoformat() + 'Z', 'items': items}

if __name__ == '__main__':
    crates = fetch_new_crates()
    feed = build_feed(crates)
    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEED_PATH.write_text(json.dumps(feed, indent=2))
