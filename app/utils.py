import pandas as pd

# Top restaurants by Order Total
def top_restaurants_by_order_value(df, top_n=10):
    if 'Restaurant Name' in df.columns and 'Order Total' in df.columns:
        top_df = df.groupby('Restaurant Name')['Order Total'].sum().reset_index()
        top_df = top_df.sort_values(by='Order Total', ascending=False).head(top_n)
        return top_df
    else:
        return pd.DataFrame()

# Monthly Sales Summary
def monthly_sales(df):
    if 'Order Date' in df.columns and 'Order Total' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df = df.dropna(subset=['Order Date'])
        df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
        monthly_df = df.groupby('Month')['Order Total'].sum().reset_index()
        return monthly_df
    else:
        return pd.DataFrame()
