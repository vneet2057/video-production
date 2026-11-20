import json, os, subprocess, urllib.parse
K = os.environ["UNSPLASH_KEY"]
Q = {"jet": ("fighter jet", "landscape"), "dro": ("military drone", "portrait"), "dr2": ("drone flying sky", "landscape")}
meta = {}
for k, (q, o) in Q.items():
    u = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(q)}&orientation={o}&per_page=4&content_filter=high"
    r = json.loads(subprocess.run(["curl", "-sS", "--max-time", "20", "-H", f"Authorization: Client-ID {K}", u], capture_output=True, text=True).stdout)
    for i, p in enumerate(r["results"]):
        f = f"{k}{i}.jpg"
        subprocess.run(["curl", "-sS", "--max-time", "30", "-o", f, p["urls"]["regular"].replace("w=1080", "w=1600")], check=True)
        meta[f] = {"name": p["user"]["name"], "dl": p["links"]["download_location"], "alt": p.get("alt_description")}
json.dump(meta, open("meta.json", "w"), indent=1)
for f, m in meta.items(): print(f, m["name"], "|", m["alt"])
