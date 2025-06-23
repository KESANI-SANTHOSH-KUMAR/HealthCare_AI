import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ai import prompt_simple_summary

def display_health_analytics(df=None):
    st.title("🩺 Health Analytics Dashboard")
           
            st.subheader("📊 Raw Data")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Data Summary")
            st.write(df.describe(include='all'))

            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

            if 'Date' in df.columns and len(numeric_cols) > 0:
                st.subheader("📈 Time Series Charts")
                for col in numeric_cols:
                    fig = px.line(df, x='Date', y=col, title=f'{col} Over Time')
                    st.plotly_chart(fig, use_container_width=True)

            if len(numeric_cols) > 0:
                st.subheader("📊 Numeric Distributions")
                for col in numeric_cols:
                    fig = px.histogram(df, x=col, nbins=20, title=f'{col} Distribution')
                    st.plotly_chart(fig, use_container_width=True)

            if len(categorical_cols) > 0:
                st.subheader("🥧 Categorical Distributions")
                for col in categorical_cols:
                    value_counts = df[col].value_counts().reset_index()
                    value_counts.columns = [col, 'Count']

                    if len(value_counts) <= 10:
                        fig = px.pie(value_counts, names=col, values='Count', title=f'{col} Distribution')
                    else:
                        fig = px.bar(value_counts, x=col, y='Count', title=f'{col} Distribution')

                    st.plotly_chart(fig, use_container_width=True)

            st.subheader("🧠 Simple Health Summary")
            if st.button("Summarize Health Data"):
                try:
                    summary = prompt_simple_summary(df)
                    st.success(summary)
                except Exception as e:
                    st.error(f"Could not generate summary: {e}")

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    else:
        st.info("📂 Please upload a CSV or Excel file to begin.")
