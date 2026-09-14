import os, re, time, urllib.request

URL = "https://www.utvs.cvut.cz/vyuka/povinna-volitelna/orientacni-beh"
NTFY = "https://ntfy.sh/" + os.environ["NTFY_TOPIC"]  # subscribe to this topic in the ntfy app
INTERVAL = int(os.environ.get("INTERVAL", 180))


def free_spots(html):
    return int(re.search(r"Volná místa:\s*</strong>\s*(\d+)", html).group(1))


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def notify(msg):
    urllib.request.urlopen(urllib.request.Request(NTFY, data=msg.encode(), headers={"Priority": "high"}), timeout=30)


if __name__ == "__main__":
    last = 0  # ponytail: in-memory, a restart re-notifies once if spots are still free
    while True:
        try:
            n = free_spots(fetch())
            print(time.strftime("%F %T"), "free:", n, flush=True)
            if n > 0 and last == 0:
                notify(f"Orientační běh: {n} volných míst! {URL}")
            last = n
        except Exception as e:
            print(time.strftime("%F %T"), "error:", e, flush=True)
        time.sleep(INTERVAL)
