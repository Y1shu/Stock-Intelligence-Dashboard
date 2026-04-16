import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Standard CORS setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STOCKS = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "WIPRO.NS"]

@app.get("/companies")
def get_companies():
    return {"available_companies": STOCKS}

@app.get("/data/{symbol}")
def get_stock_details(symbol: str):
    try:
        # Downloading minimal data to ensure speed and stability
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1mo")
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")

        # Resetting index to access Date
        df = df.reset_index()
        
        chart_data = []
        for i in range(len(df)):
            # Extracting values as simple Python primitives to avoid 'Series' errors
            date_str = str(df['Date'].iloc[i]).split()[0]
            close_price = float(df['Close'].iloc[i])
            
            chart_data.append({
                "Date": date_str,
                "Close": round(close_price, 2)
            })
            
        return chart_data

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)