# Sales Performance Dashboard

**Business question:** Which reps, products, and regions are driving revenue — and where are the opportunities?

## Dataset
Chocolate sales transactions including rep name, country, product, date, revenue, and boxes shipped. *(Update with row count and date range after loading your data.)*

## Key Insights
- **Trend:** Revenue peaked in January ($896K), dipped through April, then recovered to a second high in June ($865K) — suggesting a mid-year seasonal pattern across an 8-month window.
- **Top performers:** The top 5 reps are tightly clustered ($311K–$321K). Rafaelita Blaksland has the best deal quality at $48.93/box despite mid-table revenue — she likely targets premium accounts.
- **Opportunity:** Karlen McCaffrey ships the most boxes (9,658) at the lowest $/box ($23.18) — coaching toward higher-value products could lift her revenue significantly. Peanut Butter Cubes is the most balanced product: high volume and strong margins.

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Drop your data file
# → sales_dashboard/data/chocolate_sales.csv

# Launch the interactive dashboard
streamlit run app.py

# Or open the analysis notebook
jupyter notebook notebooks/01_eda_and_insights.ipynb
```

## Skills Demonstrated
- Data cleaning and feature engineering with **pandas**
- Interactive visualizations with **Plotly Express**
- Multi-page dashboard with filters using **Streamlit**
- EDA storytelling structured around business questions
