# pip install plotly
# import all the library
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="COdeSource Analytics Page",
    page_icon="📈"
)

st.title(":red[Data] :rainbow[Analytics] :green[Web App]")
st.header("Analysis of Data with me",divider="rainbow")

file = st.file_uploader("Drop a csv or excel file", type=['csv','xlsx'])
if(file !=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
    
    st.dataframe(data)
    st.info("File is successfully uploaded",icon="💡")

    st.subheader(':rainbow[Basic information of the dataset]', divider="rainbow")
    tab1, tab2, tab3, tab4 = st.tabs(['Summery','Top and Bottoms rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in the data set {data.shape[1]}  columns in the data set.')
        st.subheader(":grey[Stastical Summary of the data set. ]")
        st.dataframe(data.describe())
    
    with tab2:
        st.subheader(f':grey[Top 1o rows of the Data set.]')
        toprows = st.slider(f'Number of top rows display on the page',1,data.shape[0], key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(f":grey[Bottom 10 rows of the data set.]")
        bottomrows = st.slider(f'Number of bottom rows display on the page',1,data.shape[0], key='bottomslider')
        st.dataframe(data.tail(bottomrows))
    
    with tab3:
        st.subheader(f":grey[Data types of the columns]")
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(f":grey[Name of the columns of the table]")
        st.dataframe(data.columns)
    
    st.subheader(":rainbow[Column value to count]", divider='rainbow')
    with st.expander("Value Count"):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose column name', options=list(data.columns))
        with col2:
            toprows = st.number_input('Top rows', min_value=1 ,step=1)

        counts = st.button("Counts")
        if(counts == True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader("Visualization", divider='grey')
            fig = px.bar(data_frame=result, x=column, y = 'count', text='count', template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result, x=column, y='count', text='count', template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result , names=column, values='count')
            st.plotly_chart(fig)
        
    st.subheader(":rainbow[Groupby : Simplify your data analysis]", divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups')
    with st.expander('Group By your columns'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby', options = list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options= list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation', options=['sum','max','min','mean'])

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col, operation)
            ).reset_index()
            st.dataframe(result)

            st.subheader(':grey[Data Visualization]', divider='grey')
            graphs = st.selectbox('Choose Your Graphs ', options=['line','bar','scatter','pie','sunbrust'])

            if(graphs=='line'):
                y_axis = st.selectbox("Choose x axis",options=list(result.columns))
                x_axis = st.selectbox("Choose y axis",options=list(result.columns))
                color = st.selectbox("Choose the color",options=[None]+list(result.columns))
                fig = px.line(data_frame=result, x = x_axis, y= y_axis, color=color)
                # fig.show()
                st.plotly_chart(fig)
            elif(graphs=='bar'):
                y_axis = st.selectbox("Choose x axis",options=list(result.columns))
                x_axis = st.selectbox("Choose y axis",options=list(result.columns))
                color = st.selectbox("Choose the color",options=[None]+list(result.columns))
                fig = px.bar(data_frame=result, x = x_axis, y= y_axis, color=color)
                st.plotly_chart(fig)
            elif(graphs=='scatter'):
                y_axis = st.selectbox("Choose x axis",options=list(result.columns))
                x_axis = st.selectbox("Choose y axis",options=list(result.columns))
                color = st.selectbox("Choose the color",options=[None]+list(result.columns))
                size = st.selectbox('Size Column', options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result, x = x_axis, y= y_axis, color=color, size=size)
                st.plotly_chart(fig)
            elif(graphs=='pie'):
                values = st.selectbox('Choose numerical values',options=list(result.columns))
                names = st.selectbox('Choose labels',options=list(result.columns))
                fig = px.pie(data_frame=result, values= values, names= names)
                st.plotly_chart(fig)
            elif(graphs=='sunbrust'):
                path = st.multiselect('Choose categorical columns',options=list(result.columns))
                values = st.selectbox('Choose the numerical value', options=[None]+list(result.columns))
                fig = px.sunburst(data_frame=result, path=path, values=values)
                st.plotly_chart(fig)
            


