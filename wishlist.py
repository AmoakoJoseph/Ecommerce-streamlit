import streamlit as st
from database import get_products
from cart import add_to_cart

# Initialize session state variables
if "wishlist" not in st.session_state:
    st.session_state["wishlist"] = []

if "notifications" not in st.session_state:
    st.session_state["notifications"] = []


# Add product to wishlist
def add_to_wishlist(product):
    if product not in st.session_state["wishlist"]:
        st.session_state["wishlist"].append(product)  # Add to session state
        st.success(f"Added {product['name']} to wishlist!")
        st.session_state["notifications"].append(f"Added {product['name']} to Wishlist.")
    else:
        st.info(f"{product['name']} is already in your wishlist.")
        st.session_state["notifications"].append(f"{product['name']} is already in your Wishlist.")


# Display wishlist
def display_wishlist():
    st.header("Wishlist")

    if not st.session_state["wishlist"]:
        st.write("Your wishlist is empty.")
        st.session_state["notifications"].append("Attempted to view Wishlist, but it is empty.")
        return

    for product in st.session_state["wishlist"]:
        with st.container():
            st.image(product["image"], width=100)
            st.write(f"**{product['name']}** - ${product['price']}")

            if st.button(f"Add to Cart - {product['name']}", key=f"add_wishlist_{product['id']}"):
                add_to_cart(product, 1)
                st.session_state["notifications"].append(f"{product['name']} added from Wishlist to Cart.")

# Example usage (Call this in your main app file)
# display_wishlist()
def app():
    display_wishlist()