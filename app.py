import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


#reading the data from excel file

df = pd.read_excel(r"C:\Users\bhupi\Sales Dashboard\PythonStreamlit\Data_Adidas.xlsx")
st.set_page_config(layout="wide")

st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

image = Image.open(r"C:\Users\bhupi\Sales Dashboard\PythonStreamlit\adidas-logo.jpg")


col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image, caption='Adidas', width=100)
    
html_title= """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test"> Adidas Sales DashBoard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)
    
    
col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")
    
with col4:
    fig =  px.bar(df, x = "Retailer", y="TotalSales", labels={"TotalSales": "Total Sales {$}"},
                  title = "Total Sales by Retailer", hover_data=["TotalSales"],
                  template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)
    
_, view1, download1, view2, download2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander =st.expander("Retailer wise Sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with download1:
    st.download_button(label="Download Retailer wise Sales", data=data.to_csv().encode("utf-8"), file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by= df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Month_Year", y = "TotalSales", title="Total sales Over Time", template="gridon")
    st.plotly_chart(fig1,use_container_width=True)
    
with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with download2:
    st.download_button(label="Download Monthly Sales", data=data.to_csv().encode("utf-8"),file_name="MonthlySales.csv", mime="text/csv")

st.divider()

result1 = df.groupby(by="State")[["TotalSales","UnitsSold"]].sum().reset_index()

# add the unit sold as a line char on secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name = "Total sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y = result1["UnitsSold"], mode = "lines", name = "Unit Solds", yaxis="y2"))
fig3.update_layout(
    title = "Total sales and Unit Solds by State",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total Sales", showgrid =  True),
    yaxis2=dict(title="Unit Sold", overlaying = "y", side = 'right'),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)
_, col6 = st.columns([0.1,1])

with col6:
    st.plotly_chart(fig3,use_container_width=True)
    
_,view3,download3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("View Data for Sales by Unit Sold")
    expander.write(result1)

with download3:
    st.download_button(label="Download Sales by Unit Sold", data=result1.to_csv().encode("utf=8"),file_name="sales-By-UnitsSold.csv", mime="text/csv")

st.divider()

_, col7 = st.columns([0.1,1])

treemap = df[["Region", "City","TotalSales"]].groupby(by = ["Region", "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >=0:
        return '{:.2f} Million'.format(value / 1_000_000)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path = ["Region","City"], values = "TotalSales",hover_name="TotalSales (Formatted)", hover_data = ["TotalSales (Formatted)"],color = "City", height = 700, width = 600)

fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total sales by Region and City")
    st.plotly_chart(fig4,use_container_width=True)

_, view4, download4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["Region", "City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum()
    expander = st.expander("View Data for Total Sales by Region and City")
    expander.write(result2)
    
with download4:
    st.download_button(label="Download Total Sales by Region and City", data=result2.to_csv().encode("utf-8"), file_name="Sales_by_Region&City", mime= "text/csv")
    

_,view5, download5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("View sales Raw Data")
    expander.write(df)
    
with download5:
   st.download_button(label="Download Total Sales in Raw Data", data=df.to_csv().encode("utf-8"), file_name="Sales_Raw_Data", mime= "text/csv")

st.divider()