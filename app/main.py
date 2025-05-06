import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

st.set_page_config(page_title="Restaurant Order Manager", layout="wide")
st.title("📦 Restaurant Order Management Tool")

uploaded_file = st.file_uploader("Upload Order CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    if st.button("Display File Data"):
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df)

    # Email summary report
    if st.button("Send Email Summary (Datewise)"):
        if 'Order Date' not in df.columns:
            st.error("Column 'Order Date' not found in file.")
        else:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            summary = df.groupby(df['Order Date'].dt.date)['Order Total'].sum().reset_index()

            msg = MIMEMultipart()
            msg['From'] = 'your_email@example.com'
            msg['To'] = 'recipient@example.com'
            msg['Subject'] = 'Datewise Order Summary'

            body = "Please find below the datewise order total:\n\n" + summary.to_string(index=False)
            msg.attach(MIMEText(body, 'plain'))

            # Email sending setup
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('your_email@example.com', 'your_password')  # Use app password
                server.send_message(msg)
                server.quit()
                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")

    # Filters for Download and Delete
    st.subheader("🔍 Filter Data by Date & Restaurant")
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    date_filter = st.date_input("Select Order Date")
    restaurant_filter = st.selectbox("Select Restaurant", df['Restaurant Name'].dropna().unique())

    filtered_df = df[(df['Order Date'].dt.date == date_filter) & (df['Restaurant Name'] == restaurant_filter)]

    if not filtered_df.empty:
        st.dataframe(filtered_df)

        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name='filtered_orders.csv',
            mime='text/csv'
        )

        # Delete button
        if st.button("Delete Filtered Records"):
            df = df.drop(filtered_df.index)
            st.success("Filtered records deleted. They will not be in further downloads.")
    else:
        st.info("No matching records found for selected filters.")
else:
    st.info("Upload a CSV file to get started.")
