import streamlit as st
import pandas as pd
import hashlib
import math
import stripe

# Initialize Stripe API
stripe.api_key = "your_stripe_secret_key"

# Add custom CSS for background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://via.placeholder.com/1920x1080');
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sample product data
products = [
    {"id": 1, "name": "Product A", "description": "Description of Product A", "price": 10.0, "image": "https://via.placeholder.com/150", "category": "Category 1"},
    {"id": 2, "name": "Product B", "description": "Description of Product B", "price": 20.0, "image": "https://via.placeholder.com/150", "category": "Category 2"},
    {"id": 3, "name": "Product C", "description": "Description of Product C", "price": 30.0, "image": "https://via.placeholder.com/150", "category": "Category 1"},
    {"id": 4, "name": "Product D", "description": "Description of Product D", "price": 40.0, "image": "https://via.placeholder.com/150", "category": "Category 2"},
    {"id": 5, "name": "Product E", "description": "Description of Product E", "price": 50.0, "image": "https://via.placeholder.com/150", "category": "Category 3"},
]

# User credentials (stored here for simplicity)
if "users" not in st.session_state:
    st.session_state["users"] = {"user@example.com": hashlib.sha256("password".encode()).hexdigest()}

# Initialize session state
if "cart" not in st.session_state:
    st.session_state["cart"] = []
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""

# Authentication and Registration
def register(email, password):
    if email in st.session_state["users"]:
        st.error("User already exists")
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        st.session_state["users"][email] = hashed_password
        st.success("Registration successful! Please log in.")

def login(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if email in st.session_state["users"] and st.session_state["users"][email] == hashed_password:
        st.session_state["authenticated"] = True
        st.session_state["user_email"] = email
        st.success("Logged in successfully!")
    else:
        st.error("Invalid credentials")

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.success("Logged out successfully!")

# Add product to cart
def add_to_cart(product):
    st.session_state["cart"].append(product)
    st.success(f"Added {product['name']} to cart!")

# Remove product from cart
def remove_from_cart(product):
    st.session_state["cart"].remove(product)
    st.success(f"Removed {product['name']} from cart!")

# Payment processing
def process_payment(total):
    try:
        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Cart Items",
                        },
                        "unit_amount": int(total * 100),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        st.markdown(f"[Click here to complete your payment]({session.url})")
    except Exception as e:
        st.error(f"Error processing payment: {e}")

# Display product catalog in grid
def display_products():
    st.header("Products")
    categories = ["All"] + sorted(set([product["category"] for product in products]))
    selected_category = st.selectbox("Filter by Category", categories)

    filtered_products = products if selected_category == "All" else [p for p in products if p["category"] == selected_category]

    search_query = st.text_input("Search Products")
    if search_query:
        filtered_products = [p for p in filtered_products if search_query.lower() in p["name"].lower()]

    # Display products in grid
    cols_per_row = 3
    num_rows = math.ceil(len(filtered_products) / cols_per_row)

    for i in range(num_rows):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i * cols_per_row + j
            if idx < len(filtered_products):
                product = filtered_products[idx]
                with cols[j]:
                    st.image(product["image"], use_column_width=True)
                    st.write(f"**{product['name']}**")
                    st.write(product["description"])
                    st.write(f"Price: ${product['price']}")
                    if st.button(f"Add to Cart - {product['name']}", key=f"add_{product['id']}"):
                        add_to_cart(product)

# Display cart
def display_cart():
    st.header("Cart")
    if not st.session_state["cart"]:
        st.write("Your cart is empty.")
        return

    total = 0
    for product in st.session_state["cart"]:
        with st.container():
            st.image(product["image"], width=100)
            st.write(f"**{product['name']}** - ${product['price']}")
            if st.button(f"Remove - {product['name']}", key=f"remove_{product['id']}"):
                remove_from_cart(product)
        total += product["price"]

    st.write(f"**Total: ${total}**")
    if st.button("Proceed to Payment"):
        process_payment(total)

# Login and Registration page
def login_or_register_page():
    st.header("Login or Register")
    option = st.radio("Select an option", ["Login", "Register"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            login(email, password)
    elif option == "Register":
        if st.button("Register"):
            register(email, password)

# Main navigation
def main():
    st.title("E-commerce Website")

    if not st.session_state["authenticated"]:
        login_or_register_page()
        return

    menu = ["Home", "Cart", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        display_products()
    elif choice == "Cart":
        display_cart()
    elif choice == "Logout":
        logout()

if __name__ == "__main__":
    main()
