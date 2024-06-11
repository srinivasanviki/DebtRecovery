import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Customer Debt Collection Analysis", layout="wide")

# def nav_link(text_or_image, page_name,image_width=100):
#     # Check if the input is a path to a local image
#    # Check if the input is a path to a local image
#     if text_or_image.endswith(('.jpg', '.jpeg', '.png', '.gif')):
#         # If it's an image path, display the image as a button
#         col = st.columns([0.5])
#         st.image(text_or_image, width=image_width)
#         st.session_state.page = page_name

#     else:
#         # If it's text, create a button with the text and make it clickable
#         if st.button(text_or_image):
#             st.session_state.page = page_name
#             # Use st.rerun to refresh the page and apply the navigation
#             st.rerun()

# Define the left column content based on the selected view
def display_left_column_content(page):
    if page == "customer_view":
        # Left Column for Customer Information and Metrics
        with left_column:
            st.title("Customer Information")
            st.text("Name: Adrian")
            st.text("PHNO: 82865958")
            st.text("Age: 25-35")
            st.markdown("**Risk Score:** 2 (CHR) 🔻")
            st.markdown("**Debt to Income:** 40% 🔻")
            st.text("Prior Use:")
            st.progress(0.5)

            # Sentiment Analysis
            st.markdown("## Sentiment Analysis")
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive", "40%", "")
            col2.metric("Neutral", "50%", "")
            col3.metric("Negative", "10%", "")

    elif page == "agent_view":
        # Left Column for Agent Profile and Metrics
        with left_column:
            # st.title("WALNUT")
            st.image("logo/logo.png", width=100)
            st.markdown("**Agent name:** Oliver Gun")
            st.markdown("**Employee ID:** 123A")

            # Metrics
            st.markdown("## Metrics")
            col1, col2 = st.columns(2)
            col1.metric("Compliance Score", "4.0", "-0.1 MoM")
            col2.metric("DRR", "36%", "+2% MoM")

            col3, col4 = st.columns(2)
            col3.metric("Satisfaction Score", "3.5", "+0.2 MoM")
            col4.metric("Call Abandonment Rate", "1.5%", "+3% MoM")

            # Sentiment Analysis
            st.markdown("## Sentiment Analysis")
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive", "40%", "-2%")
            col2.metric("Neutral", "50%", "+1%")
            col3.metric("Negative", "10%", "+1%")

    else:
        # Left Column for Overall View
        with left_column:
            # st.image("./logo/logo.png", width=100)
            st.text("Overall View")

# Initialize session state for the page
if "page" not in st.session_state:
    st.session_state.page = "overall_view"

# Navigation Links
# st.markdown("### VoxGage")
st.image("logo/VoxGage_Logo_Text.png", width=100)

# Update session state based on the navigation link clicked
def nav_link(text, page_name):
    if st.button(text):
        st.session_state.page = page_name

nav1, nav2, nav3, nav4 = st.columns(4)
with nav1:
    st.image("logo/logo.png", width=100)
    # Display the HTML with Streamlit
    # nav_link("logo/logo.png", "overall_view")
with nav2:
    nav_link("Overall View", "overall_view")
with nav3:
    nav_link("Agent View", "agent_view")
with nav4:
    nav_link("Customer View", "customer_view")

st.markdown("---")

# Define the layout
left_column, main_column = st.columns([1, 3])

# Display left column content based on the selected view
display_left_column_content(st.session_state.page)

# Main View: Content Based on Navigation
with main_column:
    if st.session_state.page == "overall_view":
        st.write("Overall View content goes here.")
        # Empty main view for Overall View

    elif st.session_state.page == "agent_view":
        # Plotting Call Data
        st.markdown("## Call Data")
        call_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Category 1": [50, 45, 40, 35, 30, 25],
            "Category 2": [30, 25, 20, 15, 10, 5],
            "Category 3": [20, 15, 10, 5, 2, 1],
            "Duration 1": [20, 18, 16, 14, 12, 10],
            "Duration 2": [15, 13, 11, 9, 7, 5],
            "Duration 3": [12, 10, 8, 6, 4, 2],
        }
        df = pd.DataFrame(call_data)

        fig, ax1 = plt.subplots(figsize=(6, 3))

        ax2 = ax1.twinx()
        ax1.plot(df["Month"], df["Category 1"], 'g-')
        ax1.plot(df["Month"], df["Category 2"], 'b-')
        ax1.plot(df["Month"], df["Category 3"], 'r-')

        ax2.bar(df["Month"], df["Duration 1"], alpha=0.3, color='green', width=0.4, align='center')
        ax2.bar(df["Month"], df["Duration 2"], alpha=0.3, color='blue', width=0.4, align='center')
        ax2.bar(df["Month"], df["Duration 3"], alpha=0.3, color='red', width=0.4, align='center')

        ax1.set_xlabel('Month')
        ax1.set_ylabel('Num of Calls', color='black')
        ax2.set_ylabel('Duration (mins)', color='black')

        st.pyplot(fig)

        # Latest Call Records
        st.markdown("## Latest Call Records")
        call_records = {
            "Call ID": ["C-1A", "C-2B", "C-3C"],
            "CUSTID": ["CAT1", "CAT2", "CAT1"],
            "Call Category": ["20m5s", "15m10s", "12m25s"],
            "Call Duration": ["4", "4.5", "3"],
            "Compliance Score All": [0.4, 0.7, 0.5],
            "Positive Negative Ratio": ["Resolved", "Forward", "Open"],
            "Status": [5, 7, 4],
            "Customer Sentiment": ["Resolved", "Forward", "Open"]
        }

        df_records = pd.DataFrame(call_records)
        st.dataframe(df_records)

    elif st.session_state.page == "customer_view":
        # Displaying Main View Content for Customer View
        st.title("Customer Debt Collection Analysis")

        # Dummy Data for Visualizations
        call_topics_data = {
            'labels': ['Account & Balance Enquiry', 'Interest Rate Enquiry', 'Fraud Alert'],
            'sizes': [45, 25, 30],
            'colors': ['red', 'green', 'blue']
        }

        days = np.arange(1, 51)
        payment_prob = np.exp(-0.1 * (days - 10)) * 80
        call_frequency = [3, 5, 7, 4, 2]
        call_data = {
            'CALLID': [1, 2, 3],
            'DUR': ['5 Min', '10 Min', '20 Min'],
            'Senti': [5, 7, 1],
            'P/S%': [0.4, 0.7, 0.5]
        }
        call_df = pd.DataFrame(call_data)

        # Layout: Pie Chart, Payment Probability Graph, and Call Topics Frequency
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # Pie Chart for Call Topics
        with col1:
            fig1, ax1 = plt.subplots()
            ax1.pie(call_topics_data['sizes'], labels=call_topics_data['labels'], colors=call_topics_data['colors'],
                    autopct='%1.1f%%', shadow=True, startangle=140)
            ax1.axis('equal')
            st.pyplot(fig1)

        # Payment Probability Graph
        with col2:
            fig2, ax2 = plt.subplots()
            ax2.plot(days, payment_prob)
            ax2.axvline(x=10, color='green', linestyle='--')
            ax2.text(10, 85, "80%", color='green', fontsize=12)
            ax2.set_title('Payment Probability')
            ax2.set_xlabel('Days Since Arrival for Collection')
            ax2.set_ylabel('Payment Prob')
            st.pyplot(fig2)

        # Call Topics Frequency
        with col3:
            calls = [1, 2, 3, 4, 5]
            fig3, ax3 = plt.subplots()
            ax3.bar(calls, call_frequency)
            ax3.set_title('Call Topics Frequency')
            ax3.set_xlabel('Calls')
            ax3.set_ylabel('Frequency')
            st.pyplot(fig3)

        # Bottom Row - Call Data Table
        with col4:
            st.text("21st May")
            st.table(call_df)
