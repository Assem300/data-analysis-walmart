import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Walmart Sales Dashboard", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #4A90E2;'>📊 Walmart Sales Analysis Dashboard</h1>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data

def load_data():
    return pd.read_csv("Walmart_Cleaned_Advanced3_Modified.csv")

df = load_data()

# إنشاء التبويبات
tabs = st.tabs([
    "Top Products", "Sales Trends", "Store Performance", "Promotions", "Stockouts", 
    "Customer Age", "Loyalty Program", "Weather Impact", "Holiday Sales", 
    "Categories", "Payment Methods", "Lead Time", "Reorder Analysis", "Top Customers",
    "Sales by Weekday", "Transactions by Hour"
])

with tabs[0]:
    st.subheader("Top-Selling Products")
    col1, col2 = st.columns(2)
    with col1:
        top_products_quantity = df.groupby('product_name')['quantity_sold'].sum().nlargest(5).reset_index()
        fig1 = px.bar(top_products_quantity, x='product_name', y='quantity_sold', title='By Quantity')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        top_products_revenue = df.groupby('product_name')['total_sales'].sum().nlargest(5).reset_index()
        fig2 = px.bar(top_products_revenue, x='product_name', y='total_sales', title='By Revenue')
        st.plotly_chart(fig2, use_container_width=True)

with tabs[1]:
    st.subheader("Monthly Sales Trends")
    monthly_sales = df.groupby('transaction_month')['total_sales'].sum().reset_index()
    fig3 = px.line(monthly_sales, x='transaction_month', y='total_sales', title='Monthly Sales')
    st.plotly_chart(fig3, use_container_width=True)

with tabs[2]:
    st.subheader("Best Performing Stores")
    store_performance = df.groupby('store_location')['total_sales'].sum().nlargest(5).reset_index()
    fig4 = px.bar(store_performance, x='store_location', y='total_sales', title='Top Stores')
    st.plotly_chart(fig4, use_container_width=True)

with tabs[3]:
    st.subheader("Impact of Promotions")
    promotion_sales = df.groupby('promotion_applied')['total_sales'].sum().reset_index()
    fig5 = px.pie(promotion_sales, values='total_sales', names='promotion_applied', title='Promotions Share')
    st.plotly_chart(fig5, use_container_width=True)

with tabs[4]:
    st.subheader("Stockout Analysis")
    stockout_products = df[df['stockout_indicator'] == 1].groupby('product_name').size().reset_index(name='stockout_count')
    fig6 = px.bar(stockout_products, x='product_name', y='stockout_count', title='Stockout Frequency')
    st.plotly_chart(fig6, use_container_width=True)

with tabs[5]:
    st.subheader("Customer Age Spending")
    age_spending = df.groupby('customer_age')['total_sales'].mean().reset_index()
    fig7 = px.scatter(age_spending, x='customer_age', y='total_sales', title='Avg Spend by Age')
    st.plotly_chart(fig7, use_container_width=True)

with tabs[6]:
    st.subheader("Loyalty Program Effectiveness")
    loyalty_spending = df.groupby('customer_loyalty_level')['total_sales'].mean().reset_index()
    fig8 = px.bar(loyalty_spending, x='customer_loyalty_level', y='total_sales', title='Avg Spend by Loyalty Level')
    st.plotly_chart(fig8, use_container_width=True)

with tabs[7]:
    st.subheader("Weather Impact on Sales")
    weather_sales = df.groupby('weather_conditions')['total_sales'].sum().reset_index()
    fig9 = px.bar(weather_sales, x='weather_conditions', y='total_sales', title='Sales by Weather Condition')
    st.plotly_chart(fig9, use_container_width=True)

with tabs[8]:
    st.subheader("Holiday vs Non-Holiday Sales")
    holiday_sales = df.groupby('holiday_indicator')['total_sales'].sum().reset_index()
    fig10 = px.pie(holiday_sales, values='total_sales', names='holiday_indicator', title='Holiday Sales Distribution')
    st.plotly_chart(fig10, use_container_width=True)

with tabs[9]:
    st.subheader("Top Product Categories")
    category_performance = df.groupby('category')['total_sales'].sum().nlargest(5).reset_index()
    fig11 = px.bar(category_performance, x='category', y='total_sales', title='Top Categories')
    st.plotly_chart(fig11, use_container_width=True)

with tabs[10]:
    st.subheader("Payment Method Preferences")
    payment_methods = df.groupby('payment_method')['total_sales'].sum().reset_index()
    fig12 = px.pie(payment_methods, values='total_sales', names='payment_method', title='Payment Preferences')
    st.plotly_chart(fig12, use_container_width=True)

with tabs[11]:
    st.subheader("Supplier Lead Time & Stockouts")
    lead_time_stockouts = df.groupby('supplier_lead_time')['stockout_indicator'].sum().reset_index()
    fig13 = px.bar(lead_time_stockouts, x='supplier_lead_time', y='stockout_indicator', title='Lead Time vs Stockouts')
    st.plotly_chart(fig13, use_container_width=True)

with tabs[12]:
    st.subheader("Reorder Point Analysis")
    reorder_analysis = df[df['inventory_level'] < df['reorder_point']].groupby('product_name').size().reset_index(name='low_stock_count')
    fig14 = px.bar(reorder_analysis, x='product_name', y='low_stock_count', title='Products Below Reorder Point')
    st.plotly_chart(fig14, use_container_width=True)

with tabs[13]:
    st.subheader("Top High-Value Customers")
    top_customers = df.groupby('customer_id')['total_sales'].sum().nlargest(10).reset_index()
    fig15 = px.bar(top_customers, x='customer_id', y='total_sales', title='Top 10 Customers by Spend')
    st.plotly_chart(fig15, use_container_width=True)

with tabs[14]:
    st.subheader("Sales by Day of the Week")
    # إنشاء عمود يوم الأسبوع
    weekday_map = {
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    }
    df['transaction_weekday'] = pd.to_datetime(
        df['transaction_year'].astype(str) + '-' +
        df['transaction_month'].astype(str).str.zfill(2) + '-' +
        df['transaction_day'].astype(str).str.zfill(2),
        errors='coerce'
    ).dt.weekday.map(weekday_map)

    weekday_sales = df.groupby('transaction_weekday')['total_sales'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).reset_index()

    fig16 = px.bar(weekday_sales, x='transaction_weekday', y='total_sales', title='Sales by Weekday')
    st.plotly_chart(fig16, use_container_width=True)

with tabs[15]:
    st.subheader("Transactions by Hour")
    df['transaction_hour'] = df['transaction_hour'].astype(int)
    hourly_sales = df.groupby('transaction_hour')['total_sales'].sum().reset_index()
    fig17 = px.line(hourly_sales, x='transaction_hour', y='total_sales', markers=True, title='Sales by Hour of Day')
    st.plotly_chart(fig17, use_container_width=True)

st.success("✅ Dashboard loaded successfully!")
