import pandas as pd
import dash
from dash import Dash, dcc, html
import plotly.express as px
import numpy as np

# Load your data
account_share = pd.read_csv("./data/company_shares_in_south_africa.csv")
investment = pd.read_csv("./data/global_investments.csv")
forecasting_ai = pd.read_csv("./data/market_size_forecasting_generative_ai.csv")
outsourcing = pd.read_csv("./data/outsourcing_it.csv")
revenue_forecast = pd.read_csv("./data/revenue_forecast_it_south_africa.csv")
topcompanies = pd.read_csv("./data/top_ai_companies.csv")

# Data preprocessing steps
account_share.columns = ['brand', 'sharepercentage', 'market'] 

def ConvertToMillions(value):
    if 'm' in value:
        return float(value.replace('m', ''))
    elif 'b' in value:
        return float(value.replace('b', '')) * 1000
    else:
        return float(value)

investment['total_investment(in Millions)'] = investment['total_investment'].apply(ConvertToMillions)
simplified_investment = investment.drop(columns=['total_investment'])
simplified_investment.to_csv("./data/simplified_global_investment.csv", index=False)

outsourcing.columns = outsourcing.columns.str.lower()
revenue_forecast.columns = revenue_forecast.columns.str.lower()
topcompanies.columns = topcompanies.columns.str.lower().str.replace(' ', '_')
topcompanies.rename(columns={'market_cap(as_of_march_2024)': 'market_cap_march2024'}, inplace=True)
cleaned_topcompanies = topcompanies.dropna()
cleaned_topcompanies.to_csv("./data/cleaned_topcompanies.csv", index=False)

outsourcing['insource'][2] = '23%'
outsourcing_fixed = outsourcing.fillna('77%')
outsourcing_fixed.to_csv('./data/fixed_outsourcing.csv', index=False)

fig1 = px.bar(outsourcing_fixed, x="area", y="insource", title="Insourcing in each area")
fig2 = px.bar(outsourcing_fixed.sort_values(by="outsource", ascending=True), x="area", y="outsource", title="Outsourcing in each area")

rf_melted = revenue_forecast.melt(id_vars=['area'], var_name='years', value_name="values")
rf_pivoted = rf_melted.pivot(index="years", columns="area", values="values").reset_index()
rf_pivoted.columns = rf_pivoted.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

fig8 = px.bar(rf_pivoted, x="years", y="it_administration_outsourcing", text="it_administration_outsourcing", title="IT Administration Outsourcing forecast")
fig9 = px.bar(rf_pivoted, x="years", y="it_application_outsourcing", text="it_application_outsourcing", title="IT Application Outsourcing forecast")
fig10 = px.bar(rf_pivoted, x="years", y="it_other_it_outsourcing", text="it_other_it_outsourcing", title="Other IT Outsourcing forecast")
fig11 = px.bar(rf_pivoted, x="years", y="it_web_hosting", text="it_web_hosting", title="IT Web Hosting forecast")

fig14 = px.bar(cleaned_topcompanies, x="company", y="market_cap_march2024", title="Market cap of Top AI Companies (As of March 2024)")
fig15 = px.bar(simplified_investment, x="year", y="total_investment(in Millions)", title="Total Investment each year (in millions)", text="total_investment(in Millions)")
fig16 = px.bar(account_share, x='brand', y='sharepercentage', title='Percentage Share of brands in South Africa', range_y=[0, 80], text="sharepercentage")

fig17 = px.bar(account_share[account_share['market'].isin(['generative AI(text)', 'generative AI(image)'])], x='brand', y='sharepercentage', title='Share Percentage of Brands that are working with AI in South Africa',
               color='brand', color_discrete_map={brand: f'rgba({np.random.randint(0, 256)}, {np.random.randint(0, 256)}, {np.random.randint(0, 256)}, 0.8)' for brand in account_share['brand'].unique()}, range_y=[0, 80], text="sharepercentage")

graph1 = dcc.Graph(figure=fig1)
graph2 = dcc.Graph(figure=fig2)

app = dash.Dash()
app.layout = html.Div([
    html.H1('GRAPHS', style={'textAlign': 'center', 'color': '#636EFA'}),
    html.Img(src='/assets/1.png', style={'width': '50%'})
])
if __name__ == '__main__':
    app.run_server(port=8192)
server=app.server
