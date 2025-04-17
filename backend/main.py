from datetime import datetime
from backend.granularity import get_granularity
from backend.solana.fetch import fetch_solana_data
from backend.solana.process import process_solana_data
from backend.news.fetch import fetch_top_headlines
from backend.volatility import compute_volatility
from backend.llm_prompt import prepare_llm_input, get_llm_insight

def analyze(start_date: str, end_date: str) -> dict:
    print(f"\nAnalyzing from {start_date} to {end_date}")

    #parse date inputs
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    #get appropriate time granularity
    granularity = get_granularity(start, end)
    print(f"\nTime granularity selected: {granularity}")

    #fetch and process Solana data
    print("\nFetching Solana data.")
    solana_raw = fetch_solana_data(start, end, granularity)
    solana_df = process_solana_data(solana_raw, granularity)

    #fetch top news headlines
    print("\nFetching headlines.")
    headlines = fetch_top_headlines(start, end)

    #compute volatility
    print("\nComputing volatility.")
    volatility_df = compute_volatility(solana_df)

    #prepare LLM input and get insights
    print("\nPreparing input for LLM.")
    llm_input = prepare_llm_input(volatility_df, headlines)

    print("\nQuerying LLM for insights.")
    insight = get_llm_insight(llm_input)

    #prepare response
    print("\nDone. Returning output.\n")
    return {
        "granularity": granularity,
        "graphs": {
            "price": solana_df[["timestamp", "price"]].to_dict(orient="records"),
            "volume": solana_df[["timestamp", "volume"]].to_dict(orient="records"),
            "volatility": volatility_df[["timestamp", "spike_value"]].to_dict(orient="records")
        },
        "headlines": headlines,
        "insight": insight
    }

# For CLI/debug use only
if __name__ == "__main__":
    result = analyze("2025-03-01", "2025-04-01")
    from pprint import pprint
    pprint(result)
