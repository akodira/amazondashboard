import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
df = pd.read_csv('final_amazon_sales_report.csv', low_memory=False)

# Calculate the required metrics
Total_Profit = round(df['Amount'].sum(), 2)
Total_Qty = df['Qty'].sum()

st.set_page_config(page_title="Amazon Sales dashboard",layout='wide')
st.markdown("<h1 style='text-align: center; color: red;'>Amazon Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")
st.sidebar.title('Filter Pane')

# User selections in the sidebar
selected_year = st.sidebar.selectbox('Select Year', options=['Select'] + list(df['Order_Year'].unique()))
selected_month = st.sidebar.multiselect('Select Month', options=sorted(df['Order_Month'].unique()))
selected_quarter = st.sidebar.selectbox('Select Quarter', options=['Select'] + sorted(df['quarter'].unique()))
selected_day = st.sidebar.multiselect('Select Day', options=sorted(df['Order_Day'].unique()))
selected_season = st.sidebar.selectbox('Select Season', options=['Select'] + list(df['season'].unique()))
selected_Category = st.sidebar.multiselect('Select Category', options=list(df['Category'].unique()))
selected_Size = st.sidebar.multiselect('Select Size', options=list(df['Size'].unique()))


# Start with a copy of the original data
filtered_data = df.copy()

# Apply filters based on user selections
if selected_year != 'Select':  # 'Select' acts as a placeholder for no selection
    filtered_data = filtered_data[filtered_data['Order_Year'] == selected_year]

if selected_month:  # Will only filter if a month is selected
    filtered_data = filtered_data[filtered_data['Order_Month'].isin(selected_month)]

if selected_quarter != 'Select':
    filtered_data = filtered_data[filtered_data['quarter'] == selected_quarter]

if selected_day:  # Will only filter if a day is selected
    filtered_data = filtered_data[filtered_data['Order_Day'].isin(selected_day)]

if selected_season != 'Select':
    filtered_data = filtered_data[filtered_data['season'] == selected_season]




# Create four columns
col1, col2, col3 = st.columns(3)


with col1:
    Total_Profit = round(filtered_data['Amount'].sum(), 2)  
    profit_value = f"${Total_Profit:,.2f}"  
    st.markdown(f"<h3 style='color: black; font-size: 18px; text-align: center;'>Total Profit</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 24px; text-align: center; font-weight: bold;'>{profit_value}</p>", unsafe_allow_html=True)

with col2:
    Total_Quantity = round(filtered_data['Qty'].sum(), 0) 
    qty_value = f"{Total_Quantity:,.0f}"  
    st.markdown(f"<h3 style='color: black; font-size: 18px; text-align: center;'>Total_Quantity</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 24px; text-align: center; font-weight: bold;'>{qty_value}</p>", unsafe_allow_html=True)

with col3:
    Total_Orders = round(filtered_data['Qty'].count(), 0) 
    order_value = f"{Total_Orders:,.0f}"  
    st.markdown(f"<h3 style='color: black; font-size: 18px; text-align: center;'>Total_Orders</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: red; font-size: 24px; text-align: center; font-weight: bold;'>{order_value}</p>", unsafe_allow_html=True)


def page1():
    col1, col2 = st.columns(2)

    with col1:


        profit_by_year = filtered_data.groupby('Order_Year')['Amount'].sum().reset_index()
        max_year_profit = profit_by_year['Amount'].max()
        min_year_profit = profit_by_year['Amount'].min()
        year_colors = ['green' if value == max_year_profit else 'red' if value == min_year_profit else 'lightgray' for value in profit_by_year['Amount']]
        
        st.plotly_chart(px.bar(data_frame=profit_by_year, x='Order_Year', y='Amount', text_auto=True)
                 .update_traces(marker_color=year_colors)
                 .update_layout(
                     title_text='Total Profit by Year',
                     showlegend=False,
                     xaxis=dict(
                         tickmode='array',
                         tickvals=profit_by_year['Order_Year'],
                         ticktext=profit_by_year['Order_Year'].astype(str)
                     ),
                     yaxis={'showticklabels': False}
                 ))
    

        profit_by_quarter =  filtered_data.groupby('quarter')['Amount'].sum().reset_index()
        max_quarter_profit = profit_by_quarter['Amount'].max()
        min_quarter_profit = profit_by_quarter['Amount'].min()
        quarter_colors = ['green' if value == max_quarter_profit else 'red' if value == min_quarter_profit else 'lightgray' for value in profit_by_quarter['Amount']]
    
        st.plotly_chart(px.pie(data_frame=profit_by_quarter, 
                                names='quarter', 
                                values='Amount', 
                                title='Total Profit by Quarter',
                                hole=0.3,  #
                                color_discrete_sequence=quarter_colors)
                         .update_traces(textposition='inside', textinfo='label+percent')  
                         .update_layout(title_text='Total Profit by Quarter'))


    with col2:
        
        profit_by_month = filtered_data.groupby('Order_Month')['Amount'].sum().reset_index()
        max_month_profit = profit_by_month['Amount'].max()
        min_month_profit = profit_by_month['Amount'].min()
        month_colors = ['green' if value == max_month_profit else 'red' if value == min_month_profit else 'lightgray' for value in profit_by_month['Amount']]
        
        profit_by_month['Formatted_Text'] = profit_by_month['Amount'].apply(
        lambda x: f"<b><span style='color:green;'>{x:,.0f}</span></b>" if x == max_month_profit else
              f"<b><span style='color:red;'>{x:,.0f}</span></b>" if x == min_month_profit else
              f"{x:,.0f}"
        )

        # Create the line chart
        fig = px.line(
        data_frame=profit_by_month,
        x='Order_Month',
        y='Amount',
        text='Formatted_Text'
        )

        # Update the line chart with customizations
        fig.update_traces(
        line=dict(color='grey'),  # Line color
        marker=dict(size=8, color='blue'),  # Marker size and color
        textposition='top center'  # Position the text above the markers
        )

        fig.update_layout(
        title_text='Total Profit by Month',
        showlegend=False,
        xaxis=dict(
        tickmode='array',
        tickvals=profit_by_month['Order_Month'],
        ticktext=profit_by_month['Order_Month'].astype(str),
        tickangle=-45  # Rotate labels for better readability
        ),
        yaxis=dict(
        showticklabels=False,  # Hide Y-axis labels
        title='',  # Remove Y-axis title
            )
        )

        # Display the line chart
        st.plotly_chart(fig)
        
    
        
        profit_by_day_name = filtered_data.groupby('Order_Day')['Amount'].sum().reset_index()
        max_day_profit = profit_by_day_name['Amount'].max()
        min_day_profit = profit_by_day_name['Amount'].min()
        day_colors = ['green' if value == max_day_profit else 'red' if value == min_day_profit else 'lightgray' for value in profit_by_day_name['Amount']]
        
        st.plotly_chart(px.bar(data_frame=profit_by_day_name, x='Order_Day', y='Amount', text_auto=True)
                         .update_traces(marker_color=day_colors)  
                         .update_layout(title_text='Total Profit by Day', showlegend=False)  # Hide legend
                         .update_layout(yaxis={'showticklabels': False}))

def page2():
    tab1, tab2, tab3, tab4 = st.tabs(['SKU', 'Category', 'Size', 'Style'])
       
    with tab1:
         # Top-selling products by quantity
        top_quantity = df.groupby('SKU')['Qty'].sum().sort_values(ascending=False).head(10).reset_index()

        # Create a bar chart
        fig = px.bar(
        data_frame=top_quantity,
        x='SKU',
        y='Qty',
        text='Qty',  
        title='Top 10 SKUs by Quantity',
        )

        # Customize the chart
        fig.update_traces(
        texttemplate='%{text}',  
        textposition='outside',  
        marker_color='blue'  
        )

        fig.update_layout(
        xaxis=dict(
        title='SKU',
        tickmode='linear'  
        ),
        yaxis=dict(
        title='Quantity'
        ),
        title={
        'x': 0.5  
            }
        )

        st.plotly_chart(fig)


        # Top-selling products by revenue
        top_revenue = df.groupby('SKU')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()

        # Create a bar chart
        fig = px.bar(
        data_frame=top_revenue,
        x='SKU',
        y='Amount',
        text='Amount',  
        title='Top 10 SKUs by Revenue',
        )

        # Customize the chart
        fig.update_traces(
        texttemplate='%{text:.2s}',  
        textposition='outside',  
        marker_color='green'  
        )

        fig.update_layout(
        xaxis=dict(
        title='SKU',
        tickmode='linear'  
        ),
        yaxis=dict(
        title='Revenue'
        ),
        title={
        'x': 0.5  
            }
        )

        st.plotly_chart(fig)

    with tab2:
        # Top categories by quantity
        top_qty_by_category = df.groupby('Category')['Qty'].sum().sort_values(ascending=False).reset_index()

        # Create a bar chart
        fig = px.bar(
        data_frame=top_qty_by_category,
        x='Category',
        y='Qty',
        text='Qty',  
        title='Qty by Category',
        )

        # Customize the chart
        fig.update_traces(
        texttemplate='%{text:.2s}',  
        textposition='outside',  
        marker_color='orange'  
        )

        fig.update_layout(
        xaxis=dict(
        title='Category',
        tickmode='linear',  
        ),
        yaxis=dict(
        title='Qty'
        ),
        title={
        'x': 0.5  
            }
        )

        # Display the chart
        st.plotly_chart(fig)
        
        top_revenue_by_category = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()

        # Create a bar chart
        fig = px.bar(
        data_frame=top_revenue_by_category,
        x='Category',
        y='Amount',
        text='Amount',  
        title='Revenue by Category',
        )

        # Customize the chart
        fig.update_traces(
        texttemplate='%{text:.2s}',  
        textposition='outside',  
        marker_color='orange'  
        )

        fig.update_layout(
        xaxis=dict(
        title='Category',
        tickmode='linear',  #
        ),
        yaxis=dict(
        title='Revenue'
        ),
        title={
        'x': 0.5  
            }
        )

        st.plotly_chart(fig)

    with tab3:
        
        top_qty_by_size = df.groupby('Size')['Qty'].sum().sort_values(ascending=False).reset_index()

        # Create a bar chart
        fig = px.bar(
        data_frame=top_qty_by_size,
        x='Size',
        y='Qty',
        text='Qty',  
        title='Qty by Size',
        )

        fig.update_traces(
        texttemplate='%{text:.2s}',  # Format revenue (e.g., in millions if large numbers)
        textposition='outside',  # Position text outside the bars
        marker_color='orange'  # Set bar color to orange
        )

        fig.update_layout(
        xaxis=dict(
        title='Size',
        tickmode='linear',  
        ),
        yaxis=dict(
        title='Qty'
        ),
        title={
        'x': 0.5  # Center the chart title
            }
        )

        st.plotly_chart(fig)

        
        top_revenue_by_size = df.groupby('Size')['Amount'].sum().sort_values(ascending=False).reset_index()

        fig = px.bar(
        data_frame=top_revenue_by_size,
        x='Size',
        y='Amount',
        text='Amount',  # Display revenue as text on the bars
        title='Revenue by Size',
        )

        fig.update_traces(
        texttemplate='%{text:.2s}',  
        textposition='outside',  
        marker_color='orange'  
        )

        fig.update_layout(
        xaxis=dict(
        title='Size',
        tickmode='linear',  
        ),
        yaxis=dict(
        title='Revenue'
        ),
        title={
        'x': 0.5  
            }
        )

        st.plotly_chart(fig)
        
    with tab4:
        # Top categories by quantity
        top_qty_by_style = df.groupby('Style')['Qty'].sum().sort_values(ascending=False).head(10).reset_index()

        
        fig = px.bar(
        data_frame=top_qty_by_style,
        x='Style',
        y='Qty',
        text='Qty',  
        title='Top 10 Qty by Style',
        )

        # Customize the chart
        fig.update_traces(
        texttemplate='%{text:.2s}',  
        textposition='outside',  
        marker_color='orange'  
        )

        fig.update_layout(
        xaxis=dict(
        title='Style',
        tickmode='linear',  
        ),
        yaxis=dict(
        title='Qty'
        ),
        title={
        'x': 0.5  
            }
        )

        
        st.plotly_chart(fig)
        
        top_revenue_by_style = df.groupby('Style')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()

        # Create a bar chart
        fig = px.bar(
        data_frame=top_revenue_by_style,
        x='Style',
        y='Amount',
        text='Amount',  
        title='Top 10 Revenue by Style',
        )

        
        fig.update_traces(
        texttemplate='%{text:.2s}',  
        textposition='outside',  
        marker_color='orange'  
        )

        fig.update_layout(
        xaxis=dict(
        title='Style',
        tickmode='linear',  
        ),
        yaxis=dict(
        title='Revenue'
        ),
        title={
        'x': 0.5  
            }
        )

        st.plotly_chart(fig)

def page3():
        top10sales = df.groupby('Order_Day').sum().sort_values('Amount', ascending=False)
        top10sales = top10sales.reset_index().head(10)

        fig = px.bar(
            data_frame=top10sales,
            x='Order_Day',
            y='Amount',
            color='Amount',
            color_continuous_scale='turbo',
            title='Top 10 Days When Sales Were Highest',
            text_auto=True
        )
        
        fig.update_layout(
            xaxis=dict(
                title='Order_Day',
                tickmode='linear',
                tickangle=-45
            ),
            yaxis=dict(
                title='Amount'
            ),
            title=dict(
                x=0.5  
            ),
            showlegend=False
        )

        st.plotly_chart(fig)



        highqty = df.groupby('Order_Day').sum().sort_values('Qty', ascending = False)
        highqty = highqty.reset_index().head(10)
    
        fig = px.bar(
        data_frame=highqty,
        x='Order_Day',
        y='Qty',
        title='Top 10 Days When Highest Quantity Of Items Were Sold',
        color='Qty',
        color_continuous_scale='turbo',
        text='Qty'  # Display data labels
        )
        
        # Enhance the layout of the chart
        fig.update_layout(
            xaxis=dict(
                title='Order_Day',
                tickmode='linear',
                tickangle=-45
            ),
            yaxis=dict(
                title='Sales Quantity'
            ),
            title=dict(
                x=0.5  # Center the title
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=False  # Hide legend
        )
        st.plotly_chart(fig)


        grouped_df = df.groupby(['Order_Year', 'Order_Month', 'Order_Day']).sum().reset_index()

        # Create the Plotly scatter plot
        fig = px.scatter(
            data_frame=grouped_df,
            x='Qty',
            y='Amount',
            color='Order_Year',  # Equivalent to `hue`
            size='Order_Year',  # Equivalent to `size`
            symbol='Order_Year',  # Equivalent to `style`
            title='Sales Analysis by Quantity and Amount',
            color_discrete_sequence=px.colors.qualitative.Set2,
            size_max=40,  # Ensure bubble sizes are within a reasonable range
            labels={'Qty': 'Quantity', 'Amount': 'Amount (USD)', 'Order_Year': 'Year'}
        )
        
        # Enhance layout
        fig.update_layout(
            xaxis_title='Quantity',
            yaxis_title='Amount (USD)',
            legend_title='Order Year',
            title_x=0.5,  # Center the title
            height=600,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig)


        fig = px.scatter(
        data_frame=df,
        x='Category',
        y='Size',
        title='Relation Category & Size',
        labels={'Category': 'Category', 'Size': 'Size'}
        )

def page4():

        top10_state_counts = df['ship-state'].value_counts().head(10).reset_index()
        top10_state_counts.columns = ['State', 'Order Count']
        
        # Create a simple bar chart with data labels
        fig = px.bar(
            top10_state_counts,
            x='State',
            y='Order Count',
            text='Order Count',  # Show data labels
            title='Top 10 States by Order Count',
            labels={'State': 'State', 'Order Count': 'Order Count'}
        )
        
        # Optimize the layout
        fig.update_layout(
            xaxis=dict(title='State', tickangle=90),
            yaxis=dict(title='Order Count'),
            title=dict(x=0.5),  # Center the title
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


        top10_state_qty = (
        df.groupby('ship-state')['Qty']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        )
        top10_state_qty.columns = ['State', 'Total Qty']
        
        # Create a bar chart with data labels
        fig = px.bar(
            top10_state_qty,
            x='State',
            y='Total Qty',
            text='Total Qty',  # Show data labels
            title='Top 10 States by Total Quantity',
            labels={'State': 'State', 'Total Qty': 'Total Quantity'}
        )
        
        # Optimize the layout
        fig.update_layout(
            xaxis=dict(title='State', tickangle=90),
            yaxis=dict(title='Total Quantity'),
            title=dict(x=0.5),  # Center the title
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig)


        top10_state_amount = (
        df.groupby('ship-state')['Amount']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        )
        top10_state_amount.columns = ['State', 'Total Amount']
        
        # Create a bar chart with data labels
        fig = px.bar(
            top10_state_amount,
            x='State',
            y='Total Amount',
            text='Total Amount',  # Show data labels
            title='Top 10 States by Total Amount',
            labels={'State': 'State', 'Total Amount': 'Total Amount'}
        )
        
        # Optimize the layout
        fig.update_layout(
            xaxis=dict(title='State', tickangle=90),
            yaxis=dict(title='Total Amount'),
            title=dict(x=0.5),  # Center the title
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
pgs = {
    'Analysis By Time': page1,
    'Products': page2,
    'Metrics': page3,
    'State': page4
}



pg = st.sidebar.radio('Navigate pages', options=pgs.keys())



pgs[pg]()
