# Phonepe-Transaction-Insights

# Problem Statement:

With the increasing reliance on digital payment systems like PhonePe, understanding the dynamics of transactions, user engagement, and insurance-related data is crucial for improving services and targeting users effectively. This project aims to analyze and visualize aggregated values of payment categories, create maps for total values at state and district levels, and identify top-performing states, districts, and pin codes.

# Business Use Case:

**1. Decoding Transaction Dynamics on PhonePe**

**Scenario:**

PhonePe, a leading digital payments platform, has recently identified significant variations in transaction behavior across states, quarters, and payment categories. While some regions and transaction types demonstrate consistent growth, others show stagnation or decline. The leadership team seeks a deeper understanding of these patterns to drive targeted business strategies.

**2. Insurance Penetration and Growth Potential Analysis**

**Scenario**

PhonePe has ventured into the insurance domain, providing users with options to secure various policies. With increasing transactions in this segment, the company seeks to analyze its growth trajectory and identify untapped opportunities for insurance adoption at the state level. This data will help prioritize regions for marketing efforts and partnerships with insurers.

**3. Transaction Analysis for Market Expansion**

**Scenario**

PhonePe operates in a highly competitive market, and understanding transaction dynamics at the state level is crucial for strategic decision-making. With a growing number of transactions across different regions, the company seeks to analyze its transaction data to identify trends, opportunities, and potential areas for expansion.

**4. Insurance Engagement Analysis**

**Scenario**

PhonePe aims to analyze insurance transactions across various states and districts to understand the uptake of insurance services among users. This analysis will provide insights into user behavior, market demand, and potential areas for growth in insurance offerings.

**5. Transaction Analysis Across States and Districts**

**Scenario**

PhonePe is conducting an analysis of transaction data to identify the top-performing states, districts, and pin codes in terms of transaction volume and value. This analysis will help understand user engagement patterns and identify key areas for targeted marketing efforts..

**6. Insurance Transactions Analysis**

**Scenario**

PhonePe aims to analyze insurance transactions to identify the top states, districts, and pin codes where the most insurance transactions occurred during a specific year-quarter combination. This analysis will help in understanding user engagement in the insurance sector and informing strategic decisions.

# Approach:

    1. Data Extraction: Clone the GitHub repository containing PhonePe transaction data and load it into a SQL database.
    2. SQL Database and Table Creation: Set up a SQL database using a relational database management system (e.g., MySQL, PostgreSQL). Create tables to store data from the different folders:
        Aggregated Tables:
          Aggregated_user: Holds aggregated user-related data.
          Aggregated_transaction : Contains aggregated values for map-related data.
          Aggregated_insurance: Stores aggregated insurance-related data.
        Map Tables:
          Map_user: Contains mapping information for users.
          Map_map: Holds mapping values for total amounts at state and district levels.
          Map_insurance: Includes mapping information related to insurance.
        Top Tables:
          Top_user: Lists totals for the top users.
          Top_map: Contains totals for the top states, districts, and pin codes.
          Top_insurance: Lists totals for the top insurance categories.
      3. SQL Queries for Data Analysis after selecting the relevant business use cases:
      4. Data Analysis Using Python:  Utilize Python libraries (e.g., Pandas, Matplotlib, Seaborn) to analyze the results from the SQL queries.
      5. Create visualizations (bar charts, pie charts) to display aggregated values and top performers.
      6. Dashboard Creation: Develop an interactive dashboard using Streamlit and  Power BI, or Tableau to present the analysis results. Ensure the dashboard integrates visualizations for real-time data exploration and insights.

# Insights Generation:
  
    1. Summarize key findings from the analysis and visualizations.
    2. Provide actionable recommendations based on the insights gained.

# Technology Used:

    Python, SQL, PowerBI, Streamlit Library
