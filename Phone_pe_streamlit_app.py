import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="PhonePe Dashboard")

# MySQL Database Connection
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="17562dentsu",
    database="phonepay"
)
cursor = conn.cursor()

# Navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Select Page:", ["Home Page", "Business Use Cases"])

if page_selection == "Home Page":
    st.title("🏦 PhonePe Dashboard - India")

    # Fetch Data from MySQL
    cursor.execute("SELECT SUM(Transaction_Count) FROM Aggregated_Transactions")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(Registered_Users) FROM Aggregated_Users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(Insurance_count), 0), COALESCE(SUM(Insurance_amount), 0) FROM Aggregated_Insurance")
    total_insurance, total_insurance_amount = cursor.fetchone()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Transactions", value=f"{total_transactions:,}")
    with col2:
        st.metric(label="Total Users", value=f"{total_users:,}")
    with col3:
        st.metric(label="Total Insurance Policies", value=f"{total_insurance:,}")
    with col4:
        st.metric(label="Total Insurance Amount", value=f"₹{total_insurance_amount:,.2f}")

    # Selection Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        show_transactions = st.button("💰 Show Transactions")
    with col2:
        show_users = st.button("🧑‍🤝‍🧑 Show Users")
    with col3:
        show_insurance = st.button("📝 Show Insurance")

    # Define default metric
    metric_selection = "Total Transactions"
    color_scale = "Sunset"
    label = "Total Transactions"
    query = """
        SELECT State, SUM(Transaction_Count) AS Value
        FROM Aggregated_Transactions
        GROUP BY State
    """

    # Update metric based on button click
    if show_users:
        metric_selection = "Total Users"
        color_scale = "Blues"
        label = "Total Users"
        query = """
            SELECT State, SUM(Registered_Users) AS Value
            FROM Aggregated_Users
            GROUP BY State
        """
    elif show_insurance:
        metric_selection = "Total Insurance Policies"
        color_scale = "Tealrose"
        label = "Total Insurance Policies"
        query = """
            SELECT State, SUM(Insurance_count) AS Value
            FROM Aggregated_Insurance
            GROUP BY State
        """

    # Fetch Data from MySQL
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["State", "Value"])

    # Convert Value column to numeric
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # State Mapping
    map_state = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chandigarh': 'Chandigarh',
        'chhattisgarh': 'Chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'delhi': 'Delhi',
        'goa': 'Goa',
        'gujarat': 'Gujarat',
        'haryana': 'Haryana',
        'himachal-pradesh': 'Himachal Pradesh',
        'jammu-&-kashmir': 'Jammu & Kashmir',
        'jharkhand': 'Jharkhand',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'ladakh': 'Ladakh',
        'madhya-pradesh': 'Madhya Pradesh',
        'maharashtra': 'Maharashtra',
        'manipur': 'Manipur',
        'meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram',
        'nagaland': 'Nagaland',
        'odisha': 'Odisha',
        'puducherry': 'Puducherry',
        'punjab': 'Punjab',
        'rajasthan': 'Rajasthan',
        'sikkim': 'Sikkim',
        'tamil-nadu': 'Tamil Nadu',
        'telangana': 'Telangana',
        'tripura': 'Tripura',
        'uttar-pradesh': 'Uttar Pradesh',
        'uttarakhand': 'Uttarakhand',
        'west-bengal': 'West Bengal'
    }

    df["State"] = df["State"].str.lower().map(map_state)

    # Load GeoJSON and Create Map
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Value",
        color_continuous_scale=color_scale,
        labels={'Value': label},
        hover_name="State",
        hover_data={"Value": True, "State": False}  # ✅ Display value & hide redundant state name
    )

    # ✅ Fix: Zoom in on India & Hide World Map
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
    )

    # ✅ Remove color scale (legend)
    fig.update_layout(
        width=1200,
        height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=True , # ✅ Hides the color scale completely
        legend=dict(orientation="v", x=1, y=0.5)  # ✅ Move legend to right
    )
    # Show India Map
    st.plotly_chart(fig, use_container_width=True)

    # 🏆 **Separate Top 10 Buttons**
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("🏆 Show Top 10 Transactions"):
            cursor.execute("""
                SELECT State, SUM(Transaction_Count) AS Value
                FROM Aggregated_Transactions
                GROUP BY State
                ORDER BY Value DESC
                LIMIT 10
            """)
            top_10_transactions = pd.DataFrame(cursor.fetchall(), columns=["State", "Value"])
            st.subheader("🏆 Top 10 States by Transactions")
            st.table(top_10_transactions)

    with col5:
        if st.button("🏆 Show Top 10 Users"):
            cursor.execute("""
                SELECT State, SUM(Registered_Users) AS Value
                FROM Aggregated_Users
                GROUP BY State
                ORDER BY Value DESC
                LIMIT 10
            """)
            top_10_users = pd.DataFrame(cursor.fetchall(), columns=["State", "Value"])
            st.subheader("🏆 Top 10 States by Users")
            st.table(top_10_users)

    with col6:
        if st.button("🏆 Show Top 10 Insurance Policies"):
            cursor.execute("""
                SELECT State, SUM(Insurance_count) AS Value
                FROM Aggregated_Insurance
                GROUP BY State
                ORDER BY Value DESC
                LIMIT 10
            """)
            top_10_insurance = pd.DataFrame(cursor.fetchall(), columns=["State", "Value"])
            st.subheader("🏆 Top 10 States by Insurance Policies")
            st.table(top_10_insurance)

elif page_selection == "Business Use Cases":
    st.title("Business Use Cases Analysis")
    business_cases = [
        "Decoding Transaction Dynamics on PhonePe",
        "Insurance Penetration and Growth Potential Analysis",
        "Transaction Analysis for Market Expansion",
        "Insurance Engagement Analysis",
        "Transaction Analysis Across States and Districts",
        "Insurance Transactions Analysis"
    ]
    selected_case = st.selectbox("Select a Business Use Case", business_cases)
    st.write(f"### Analysis for: {selected_case}")
    st.write("(Detailed insights will be displayed based on the selected business use case)")
    
    if selected_case == "Decoding Transaction Dynamics on PhonePe":
        st.write(f"### Scenario:")
        st.write(f"PhonePe, a leading digital payments platform, has recently identified significant variations in transaction behavior across states, quarters, and payment categories. While some regions and transaction types demonstrate consistent growth, others show stagnation or decline. The leadership team seeks a deeper understanding of these patterns to drive targeted business strategies.")
        query = """
            SELECT Year,State, Quarter, Transaction_Type, SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS Total_Amount
            FROM Aggregated_Transactions
            GROUP BY Year,State, Quarter, Transaction_Type
        """
        cursor.execute(query)
        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=["Year", "State", "Quarter", "Transaction_Type", "Total Transactions", "Total Amount"])

        # Convert Total Transactions to numeric
        df["Total Transactions"] = pd.to_numeric(df["Total Transactions"], errors="coerce")
                
        st.subheader("Transaction Trends Across States")
        fig = px.bar(df, x="State", y="Total Transactions", color="Transaction_Type", barmode="group",
                     title="Transaction Count by State and Payment Category")
        st.plotly_chart(fig)

        # Convert Year and Quarter to Period format
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", states)
        df_filtered = df[df["State"] == selected_state]
        
        # Line Chart for Yearly and Quarterly Trends
        st.subheader("Yearly and Quarterly Trends for State Wise Selection")
        fig_line = px.line(df_filtered, x="Period", y="Total Transactions", title=f"Transaction Trends in {selected_state}", markers=True)
        st.plotly_chart(fig_line)

        # Pie Chart for Payment Category
        st.subheader("Transaction Distribution by Payment Category")
        df_pie = df_filtered.groupby("Transaction_Type")["Total Transactions"].sum().reset_index()
        fig_pie = px.pie(df_pie, names="Transaction_Type", values="Total Transactions", title=f"Payment Category Distribution in {selected_state}")
        st.plotly_chart(fig_pie)
        
    elif selected_case == "Insurance Penetration and Growth Potential Analysis":
        st.write(f"### Scenario:")
        st.write(f"PhonePe has ventured into the insurance domain, providing users with options to secure various policies. With increasing transactions in this segment, the company seeks to analyze its growth trajectory and identify untapped opportunities for insurance adoption at the state level. This data will help prioritize regions for marketing efforts and partnerships with insurers.")
        query = """
            SELECT Year, State, Quarter, SUM(Insurance_Count) AS Total_Policy, SUM(Insurance_Amount) AS Total_Amount
            FROM Aggregated_Insurance
            GROUP BY Year, State, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["Year", "State", "Quarter", "Total_Policy", "Total Amount"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # Bar Chart - Total Insurance Transactions by State
        st.subheader("Total Insurance Transactions Across States")
        fig_bar = px.bar(df.groupby("State")["Total_Policy"].sum().reset_index(), x="State", y="Total_Policy", title="Total Insurance Policy Vs. State", color="Total_Policy")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
            
        # Line Chart - Growth Trend of Insurance Transactions Over Time
        st.subheader(f"Insurance Policy Growth Over Time For {selected_state}")
        fig_line = px.line(df.groupby("Period")["Total_Policy"].sum().reset_index(), x="Period", y="Total_Policy", title="Insurance Transactions Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Bar Chart - Insurance Amount by Year/Quarter
        st.subheader(f"Insurance Amount Trends Over Time For {selected_state}")
        fig_insurance_amount = px.bar(df.groupby("Period")["Total Amount"].sum().reset_index(), x="Period", y="Total Amount", title="Insurance Amount by Year/Quarter", color="Total Amount")
        st.plotly_chart(fig_insurance_amount, use_container_width=True)

    elif selected_case == "Transaction Analysis for Market Expansion":
        st.write(f"### Scenario:")
        st.write(f"PhonePe operates in a highly competitive market, and understanding transaction dynamics at the state level is crucial for strategic decision-making. With a growing number of transactions across different regions, the company seeks to analyze its transaction data to identify trends, opportunities, and potential areas for expansion.")
        query = """
            SELECT State, Transaction_Type, SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS Total_Amount, Year, Quarter
            FROM Map_Transactions
            GROUP BY State, Transaction_Type, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["State", "District", "Total Transactions", "Total Amount", "Year", "Quarter"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
        
        # Line Chart - Transaction Trends by Type
        st.subheader(f"Transaction Trends Over Time by District - {selected_state}")
        fig_line = px.line(df, x="Period", y="Total Transactions", color="District", title="Transaction Trends Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Bar Chart - Transactions by Type
        st.subheader(f"Total Transactions by District - {selected_state}")
        fig_bar = px.bar(df, x="District", y="Total Transactions", title="Total Transactions by Type", color="District")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Bubble Chart - Transactions by Type and Amount
        st.subheader(f"Transactions by Type and Amount - {selected_state}")
        fig_bubble = px.scatter(df, x="Total Transactions", y="Total Amount", color="District", size="Total Amount", hover_name="District", title="Transactions by Policy and Amount", size_max=50)
        st.plotly_chart(fig_bubble, use_container_width=True)
    elif selected_case == "Insurance Engagement Analysis":
        st.write(f"### Scenario:")
        st.write(f"PhonePe aims to analyze insurance transactions across various states and districts to understand the uptake of insurance services among users. This analysis will provide insights into user behavior, market demand, and potential areas for growth in insurance offerings.")
        query = """
            SELECT State, District, SUM(Insurance_Count) AS Total_Insurance, SUM(Insurance_Amount) AS Total_Amount, Year, Quarter
            FROM Map_Insurance
            GROUP BY State, District, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["State", "District", "Total Insurance", "Total Amount", "Year", "Quarter"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # Ensure numeric values for aggregation
        df["Total Insurance"] = pd.to_numeric(df["Total Insurance"], errors="coerce").fillna(0)
        df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce").fillna(0)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
        
        # Sunburst Chart - Insurance Distribution by State and District
        st.subheader("Insurance Distribution by State and District")
        fig_sunburst = px.sunburst(df, path=["State", "District"], values="Total Insurance")
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Scatter Plot - Insurance Count vs. Amount by District
        st.subheader("Insurance Count vs. Amount by District")
        fig_scatter = px.scatter(df, x="Total Insurance", y="Total Amount", color="State", hover_name="District")
        st.plotly_chart(fig_scatter, use_container_width=True)

    elif selected_case == "Transaction Analysis Across States and Districts":
        st.write(f"### Scenario:")
        st.write(f"PhonePe is conducting an analysis of transaction data to identify the top-performing states, districts, and pin codes in terms of transaction volume and value. This analysis will help understand user engagement patterns and identify key areas for targeted marketing efforts..")

        query = """
            SELECT State, District, Year, Quarter, SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS Total_Amount
            FROM Top_Transactions
            GROUP BY State, District, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["State", "District", "Year", "Quarter", "Total Transactions", "Total Amount"])
        
        # Top States Visualization by Year/Quarter
        st.subheader("Top States by Transaction Volume and Value (Year/Quarter)")
        selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=0)
        selected_quarter = st.selectbox("Select Quarter", sorted(df["Quarter"].unique()), index=0)
        df_filtered = df[(df["Year"] == selected_year) & (df["Quarter"] == selected_quarter)]
        
        fig_state_bar = px.bar(df_filtered.groupby("State").sum().reset_index().sort_values("Total Transactions", ascending=False).head(10), 
                               x="State", y="Total Transactions",title=f"Top 10 States by Transactions in {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_state_bar, use_container_width=True)
        
        fig_state_pie = px.pie(df_filtered.groupby("State").sum().reset_index().sort_values("Total Transactions", ascending=False).head(10), 
                               names="State", values="Total Transactions", 
                               title=f"Top 10 States by Transaction Share in {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_state_pie, use_container_width=True)
        
        # State Selection Filter
        states = df_filtered["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df_filtered = df_filtered[df_filtered["State"] == selected_state]
        
        # Top Districts Visualization by Year/Quarter
        st.subheader(f"Top Districts in {selected_state if selected_state != 'All' else 'Selected States'} for {selected_year} Q{selected_quarter}")
        fig_district_bar = px.bar(df_filtered.sort_values("Total Transactions", ascending=False).head(10), 
                                  x="District", y="Total Transactions",
                                  title=f"Top 10 Districts by Transactions in {selected_state} - {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_district_bar, use_container_width=True)
        
        fig_district_pie = px.pie(df_filtered.sort_values("Total Transactions", ascending=False).head(10), 
                                  names="District", values="Total Transactions", 
                                  title=f"Top 10 Districts by Transaction Share in {selected_state} - {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_district_pie, use_container_width=True)

    if selected_case == "Insurance Transactions Analysis":
        st.write(f"### Scenario:")
        st.write(f"PhonePe aims to analyze insurance transactions to identify the top states, districts, and pin codes where the most insurance transactions occurred during a specific year-quarter combination. This analysis will help in understanding user engagement in the insurance sector and informing strategic decisions.")
        query = """
            SELECT State, District, Year, Quarter, SUM(Insurance_count) AS Total_Policy, SUM(Insurance_Amount) AS Total_Amount
            FROM Top_Insurance
            GROUP BY State, District, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["State", "District", "Year", "Quarter", "Total_Policy", "Total Amount"])
        
        # Top States Visualization by Year/Quarter
        st.subheader("Top States by Insurance Transaction Volume and Value (Year/Quarter)")
        selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=0)
        selected_quarter = st.selectbox("Select Quarter", sorted(df["Quarter"].unique()), index=0)
        df_filtered = df[(df["Year"] == selected_year) & (df["Quarter"] == selected_quarter)]
        
        fig_state_bar = px.bar(df_filtered.groupby("State").sum().reset_index().sort_values("Total_Policy", ascending=False).head(10), 
                               x="State", y="Total_Policy", title=f"Top 10 States by Insurance Transactions in {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_state_bar, use_container_width=True)
        
        fig_state_pie = px.pie(df_filtered.groupby("State").sum().reset_index().sort_values("Total_Policy", ascending=False).head(10), 
                               names="State", values="Total_Policy", 
                               title=f"Top 10 States by Insurance Transaction Share in {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_state_pie, use_container_width=True)
        
        fig_state_scatter = px.scatter(df_filtered, x="State", y="Total_Policy", size="Total Amount",  
                                       title=f"State-wise Insurance Transaction Trends in {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_state_scatter, use_container_width=True)
        
        # State Selection Filter
        states = df_filtered["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df_filtered = df_filtered[df_filtered["State"] == selected_state]
        
        # Top Districts Visualization by Year/Quarter
        st.subheader(f"Top Districts in {selected_state if selected_state != 'All' else 'Selected States'} for {selected_year} Q{selected_quarter}")
        fig_district_bar = px.bar(df_filtered.sort_values("Total_Policy", ascending=False).head(10), 
                                  x="District", y="Total_Policy",title=f"Top 10 Districts by Insurance Transactions in {selected_state} - {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_district_bar, use_container_width=True)
        
        fig_district_pie = px.pie(df_filtered.sort_values("Total_Policy", ascending=False).head(10), 
                                  names="District", values="Total_Policy", 
                                  title=f"Top 10 Districts by Insurance Transaction Share in {selected_state} - {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_district_pie, use_container_width=True)
        
        fig_district_scatter = px.scatter(df_filtered, x="District", y="Total_Policy", size="Total Amount",  
                                          title=f"District-wise Insurance Transaction Trends in {selected_state} - {selected_year} Q{selected_quarter}")
        st.plotly_chart(fig_district_scatter, use_container_width=True)
        
# Close Database Connection
cursor.close()
conn.close()
