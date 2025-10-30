import requests, random
from collections import Counter
from .utils import log

base_url_events = "https://api.elections.kalshi.com/trade-api/v2/events"

def fetch_all_events(status=None, with_markets=True):
    """
    Fetch all events (optionally filtered) from Kalshi with pagination.
    Args:
        status (str | None): e.g., 'open' to fetch only open events.
        with_markets (bool): If True, include nested markets in results.
    Returns:
        list[dict]: All fetched events.
    """
    params = {}
    if status:
        params['status'] = status
    if with_markets:
        params['with_nested_markets'] = "true"

    events = []
    cursor = None

    log(f"Fetching all events with status={status} and with_markets={with_markets}")

    while True:
        if cursor:
            params['cursor'] = cursor

        log(f"Requesting events with params: {params}")
        resp = requests.get(base_url_events, params=params)
        if resp.status_code != 200:
            log(f"Failed to fetch events: {resp.status_code}")
            break

        data = resp.json()
        batch_events = data.get("events", [])
        log(f"Fetched {len(batch_events)} events in this batch")
        events.extend(batch_events)

        cursor = data.get("cursor")
        if not cursor:
            break
        if len(events) >= 1000:
            log("Reached 1000 events limit, stopping fetch.")
            break

    log(f"Total events fetched: {len(events)}")
    return events

def stratified_sample_events(events, target=17):
    """Stratified sampling of events across categories."""
    if len(events) <= target:
        return events
    
    random.seed(37)

    # group by category
    categories = {}
    for e in events:
        categories.setdefault(e["category"], []).append(e)
    sampled, remaining = [], target

    # smallest categories first; give each category an equal "share" of remaining slots
    cat_lists = sorted(categories.values(), key=len)
    for i, lst in enumerate(cat_lists):
        slots_left = len(cat_lists) - i
        share = max(1, remaining // slots_left)
        take = len(lst) if len(lst) <= share else share
        sampled += lst if take == len(lst) else random.sample(lst, take)
        remaining -= take

    # print counts of original vs sampled
    orig_counts = Counter(e["category"] for e in events)
    sampled_counts = Counter(e["category"] for e in sampled)
    for cat in orig_counts:
        print(f"{cat}: original={orig_counts[cat]}, sampled={sampled_counts.get(cat, 0)}")
    return sampled


def scrape_kalshi_events():
    """
    Merge current Kalshi events/markets with previously stored JSONs to:
      - keep active items,
      - add new items,
      - move no-longer-active items to resolved,
      - update market price snapshots for active markets.
    Writes four JSONs and returns their paths along with the final active events.
    """
    log("Starting Kalshi event scraping...")

    # Pull current events from Kalshi 
    current_events = fetch_all_events(status='open', with_markets=True)
    sampled_events = stratified_sample_events(current_events, target=17)
    return sampled_events