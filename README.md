# Sales-performance-dashboard

**Business question:** Which reps, products, and regions are driving revenue — and where are the opportunities?

[View Repository](#)

### Business Context
A chocolate sales company needs visibility into rep performance, product margins, and regional trends to make informed decisions about where to coach, invest, and expand. This interactive dashboard replaces static reports with a filterable, real-time view of the business.

### Dataset
- Chocolate sales transactions including rep name, country, product, date, revenue, and boxes shipped

### Approach
1. **Data Cleaning:** Standardized date formats, handled missing values, engineered revenue-per-box metric
2. **EDA:** Identified seasonal trends, rep performance clusters, and product margin profiles
3. **Dashboard:** Multi-page Streamlit app with dynamic filters by country, rep, and date range

### Key Insights
- Revenue peaked in January ($896K), dipped mid-year, then recovered to $865K in June — indicating a recurring seasonal pattern
- Top 5 reps are tightly clustered ($311K–$321K); Rafaelita Blaksland leads in deal quality at $48.93/box despite mid-table revenue — she targets premium accounts
- Karlen McCaffrey ships the most boxes (9,658) at the lowest $/box ($23.18) — a coaching opportunity to shift toward higher-margin products
- Peanut Butter Cubes is the most balanced product: high volume with strong margins

### Skills Demonstrated
- Data cleaning and feature engineering with **pandas**
- Interactive visualizations with **Plotly Express**
- Multi-page dashboard with dynamic filters using **Streamlit**
- EDA structured around business questions, not just statistics
