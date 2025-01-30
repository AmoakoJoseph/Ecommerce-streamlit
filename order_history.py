import streamlit as st
from database import get_products

# Initialize session state for order history if it doesn't exist
if "order_history" not in st.session_state:
    st.session_state["order_history"] = []


def app():
    # Display order history
    def display_order_history():
        st.header("Order History")

        if not st.session_state["order_history"]:
            st.write("No orders yet.")
            return

        # Iterate through each order in order history
        for order in st.session_state["order_history"]:
            st.subheader(f"**Order Date:** {order['date']}")
            st.write("**Items:**")

            # Iterate through each item in the order
            for item in order["items"]:
                product = item["product"]
                quantity = item["quantity"]
                st.write(f"- {product['name']} x {quantity} = **${product['price'] * quantity}**")

            st.write(f"**Total:** ${order['total']}\n---")

    display_order_history()
