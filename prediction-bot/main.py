from .utils import log
from .events import scrape_kalshi_events
from .rag import get_report, get_market_descriptions
from .prediction import make_final_prediction

def main():
    print("Starting daily report generation...")
    events = scrape_kalshi_events()
    log(f"Fetched {len(events)} events from Kalshi.")


    for event in events:
        market_descriptions = get_market_descriptions(event)
        report = get_report(event, market_descriptions)

        report_filename = f"event_{event['event_ticker']}_report.txt"
        with open(report_filename, "w") as f:
            f.write(report)

        log(f"Saved report for event {event['event_ticker']} to {report_filename}.")

        prediction = make_final_prediction(event, report, market_descriptions)
        log("---### Final Prediction Output Start ###---")
        log(f"Final prediction for event {event['event_ticker']}:\n{prediction}")
        log("---### Final Prediction Output End ###---")

        # use the prediction object to make trading decisions using Kalshi API (not implemented here)

if __name__ == "__main__":
    main()
