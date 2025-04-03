Highly suggested to read:

https://www.backtrader.com/docu/quickstart/quickstart/#adding-a-data-feed

Slide link: https://docs.google.com/presentation/d/15jryxgmqfL5Gp3j_NcYpdpXVFXqDfECFxuId1uZvuKg/edit?slide=id.p#slide=id.p 


/SPY-Trading-Strategies/
│
├── data/                  # Historical SPY and feature data
│
├── strategies/
│   ├── strategy_A.py      # Person 1
│   ├── strategy_B.py      # Person 2
│   ├── strategy_C.py      # Person 3
│   └── strategy_D.py      # Person 4
│
├── backtest/
│   ├── backtester.py      # Shared backtesting logic
│   └── metrics.py         # Common performance metrics
│
├── results/
│   ├── equity_curves/     # PnL plots per strategy
│   ├── performance.csv    # Comparison table (Sharpe, CAGR, etc.)
│
├── report/                # Final team report / presentation
│
└── main.py                # Orchestrates all strategy runs + plots
