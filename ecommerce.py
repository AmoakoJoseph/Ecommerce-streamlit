import streamlit as st
import auth, cart, home, order_history, user_profile, wishlist
import stripe
import os

# Initialize Stripe API securely
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if "wishlist" not in st.session_state:
    st.session_state["wishlist"] = []

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

PAGES = {
    "Home": home,
    "Cart": cart,
    "Wishlist": wishlist,
    "Order History": order_history,
    "User Profile": user_profile,
}


def main():
    if not st.session_state.get("authenticated"):
        auth.app()
    else:
        st.title("Ecommerce")
        st.sidebar.title("Navigation")
        selected_page = st.sidebar.radio("Go to", list(PAGES.keys()) + ["Logout"])

        if selected_page == "Logout":
            st.session_state["authenticated"] = False
            st.rerun()  # Forces UI refresh after logout
        else:
            PAGES[selected_page].app()


if __name__ == "__main__":
    st.set_page_config(
        page_title="E-commerce Platform",
        page_icon="🛒",
        layout="wide",
    )
    main()

