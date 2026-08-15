import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HANDLE = "writeAhead"
BG = "#131722"
LINE = "#8891b8"
FILL = "#3a4160"
TEXT = "#8891b8"
GRID = "#2a3040"

resp = requests.get(f"https://codeforces.com/api/user.rating?handle={HANDLE}", timeout=15)
data = resp.json()

if data.get("status") != "OK":
    raise SystemExit(f"Codeforces API error: {data.get('comment')}")

contests = data["result"]
ratings = [c["newRating"] for c in contests]
labels = list(range(1, len(ratings) + 1))

fig, ax = plt.subplots(figsize=(10, 3.2), dpi=160)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

if ratings:
    ax.plot(labels, ratings, color=LINE, linewidth=2.2, marker="o",
             markersize=3.5, markerfacecolor=FILL, markeredgecolor=LINE)
    ax.fill_between(labels, ratings, min(ratings) - 50, color=FILL, alpha=0.25)
    ax.set_title(f"Codeforces Rating — {HANDLE} (current: {ratings[-1]})",
                 color=TEXT, fontsize=13, pad=12)
else:
    ax.text(0.5, 0.5, "No rated contests yet", color=TEXT,
             ha="center", va="center", fontsize=12)
    ax.set_title(f"Codeforces Rating — {HANDLE}", color=TEXT, fontsize=13, pad=12)

ax.set_xlabel("Contest #", color=TEXT, fontsize=9)
ax.set_ylabel("Rating", color=TEXT, fontsize=9)
ax.tick_params(colors=TEXT, labelsize=8)
ax.grid(True, color=GRID, linewidth=0.6, alpha=0.6)
for spine in ax.spines.values():
    spine.set_color(GRID)

plt.tight_layout()
plt.savefig("codeforces-rating.svg", format="svg", facecolor=BG)
