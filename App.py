import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1e3a8a;
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #475569;
    margin-bottom: 30px;
}
.info-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.metric-card {
    background-color: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}
.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #0f172a;
}
.metric-label {
    color: #64748b;
    font-size: 15px;
}
.section-title {
    color: #1e293b;
    font-size: 25px;
    font-weight: bold;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "data" not in st.session_state:
    st.session_state.data = None


# ---------------- PAGE 1: UPLOAD ----------------
if st.session_state.page == "upload":

    st.markdown("<div class='main-title'>Sales Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Upload your dataset to generate business insights</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>About This Application</h3>
        <p>
        This Sales Dashboard helps businesses analyze their sales performance.
        After uploading a sales dataset, the system automatically generates
        visual insights such as sales trends, category-wise sales,
        region-wise sales, total profit, total orders and top-selling products.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Sales Dataset CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.session_state.data = df

        st.success("Dataset uploaded successfully!")

        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        if st.button("Go to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()


# ---------------- PAGE 2: DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    df = st.session_state.data

    required_columns = [
        "Order ID",
        "Order Date",
        "Region",
        "Category",
        "Product Name",
        "Sales",
        "Profit"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error("Missing required columns:")
        st.write(missing_columns)

    else:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

        st.markdown("<div class='main-title'>Sales Dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Business Insights Dashboard</div>", unsafe_allow_html=True)

        if st.button("Back to Upload Page"):
            st.session_state.page = "upload"
            st.rerun()

        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()
        total_orders = df["Order ID"].nunique()

        st.markdown("<div class='section-title'>Business Summary</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Sales</div>
                <div class="metric-value">${total_sales:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Profit</div>
                <div class="metric-value">${total_profit:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Orders</div>
                <div class="metric-value">{total_orders}</div>
            </div>
            """, unsafe_allow_html=True)

        # Monthly Sales Trend
        st.markdown("<div class='section-title'>Monthly Sales Trend</div>", unsafe_allow_html=True)

        monthly_sales = df.groupby(
            df["Order Date"].dt.to_period("M")
        )["Sales"].sum().reset_index()

        monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

        fig1 = px.line(
            monthly_sales,
            x="Order Date",
            y="Sales",
            markers=True
        )

        st.plotly_chart(fig1, use_container_width=True)

        # Category + Region
        col4, col5 = st.columns(2)

        with col4:
            st.markdown("<div class='section-title'>Category-wise Sales</div>", unsafe_allow_html=True)

            category_sales = df.groupby("Category")["Sales"].sum().reset_index()

            fig2 = px.bar(
                category_sales,
                x="Category",
                y="Sales"
            )

            st.plotly_chart(fig2, use_container_width=True)

        with col5:
            st.markdown("<div class='section-title'>Region-wise Sales</div>", unsafe_allow_html=True)

            region_sales = df.groupby("Region")["Sales"].sum().reset_index()

            fig3 = px.pie(
                region_sales,
                names="Region",
                values="Sales"
            )

            st.plotly_chart(fig3, use_container_width=True)

        # Top Products
        st.markdown("<div class='section-title'>Top 10 Products by Sales</div>", unsafe_allow_html=True)

        top_products = df.groupby("Product Name")["Sales"].sum().reset_index()
        top_products = top_products.sort_values(by="Sales", ascending=False).head(10)

        fig4 = px.bar(
            top_products,
            x="Sales",
            y="Product Name",
            orientation="h"
        )

        st.plotly_chart(fig4, use_container_width=True)

        st.markdown("<div class='section-title'>Complete Dataset</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)