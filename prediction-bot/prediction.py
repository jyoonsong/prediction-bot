from typing import Dict
from .openai_utils import run_openai
from .utils import log

def make_final_prediction(event: Dict[str, any], research_reports: str, market_descriptions: str) -> str:
    # Make final market predictions based on research reports
    prompt =f"""The following are markets under the event titled "{event.get('title', '')}". The markets can resolve before the scheduled close date.
{market_descriptions}

The following are research reports related to the markets:
{research_reports}

# Instructions
Given all you know and the research reports above, make the best possible prediction for whether each of these markets will resolve to Yes. Format your predictions as an array of objects, where each object corresponds to a market. The length of your array must be {len(event.get('markets', []))}. Include ALL markets, even if you think they will resolve to No. Each object should have the following structure:
- "ticker": "KXWTAMATCH-25JUN30KALSTO-STO" // market ticker copied exactly from the market metadata
- "reasoning": "A brief explanation of how you arrived at the prediction",
- "confidence": 0.85 // a number between 0 and 1 indicating your confidence in the prediction,
- "decision": "buy" or "sell" // a decision of "buy" indicates a prediction that the market will resolve to Yes, while "sell" indicates a prediction that the market will resolve to No."""
    
    log("---### Final Prediction Prompt Start ###---")
    log(f"Making final prediction for event {event['event_ticker']} with prompt:\n{prompt}")
    log("---### Final Prediction Prompt End ###---")
    
    output = run_openai(prompt)
    return output.strip()