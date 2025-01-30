import streamlit as st
import math
from database import get_products
from cart import add_to_cart, remove_from_cart, display_cart, process_payment
from wishlist import add_to_wishlist


def app():
    # Display product catalog in grid
    import math
    import streamlit as st
    from database import get_products, get_db  # Import get_db

    def display_products():
        # Open a database session
        with get_db() as db:
            products = get_products(db)  # Pass the session to get_products

        # Get unique categories
        categories = ["All"] + sorted(set(product.category for product in products))

        col1, col2 = st.columns([1, 2])
        with col1:
            selected_category = st.selectbox("Filter by Category", categories)
        with col2:
            search_query = st.text_input("Search Products")

        # Filtering products
        filtered_products = products if selected_category == "All" else [p for p in products if
                                                                         p.category == selected_category]
        if search_query:
            filtered_products = [p for p in filtered_products if search_query.lower() in p.name.lower()]

        # Grid display
        cols_per_row = 3  # Fixed layout for better design
        num_rows = math.ceil(len(filtered_products) / cols_per_row)

        for i in range(num_rows):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i * cols_per_row + j
                if idx < len(filtered_products):
                    product = filtered_products[idx]
                    with cols[j]:
                        st.image(product.image, use_container_width=True)
                        st.write(f"**{product.name}**")
                        st.write(product.description)
                        st.write(f"Price: ${product.price}")

                        quantity = st.slider(f"Quantity ({product.name})", min_value=1, max_value=10, value=1,
                                             key=f"qty_{product.id}")

                        if st.button(f"Add to Cart - {product.name}", key=f"add_{product.id}"):
                            add_to_cart(product, quantity)

                        if st.button(f"Add to Wishlist - {product.name}", key=f"wishlist_{product.id}"):
                            add_to_wishlist(product)

    def logout():
        st.session_state["authenticated"] = False
        st.session_state["user_email"] = ""
        st.success("Logged out successfully!")

    # Display products on page load
    display_products()
