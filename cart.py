import streamlit as st
from database import get_products
import stripe
from datetime import datetime

stripe.api_key = "your-key-here"

# Ensure session state is initialized for cart and notifications
if "cart" not in st.session_state:
    st.session_state["cart"] = []

if "notifications" not in st.session_state:
    st.session_state["notifications"] = []

if "order_history" not in st.session_state:
    st.session_state["order_history"] = []

# Add product to cart
def add_to_cart(product, quantity):
    if product not in [item["product"] for item in st.session_state["cart"]]:  # Prevent duplicates
        st.success(f"Added {quantity} x {product['name']} to cart!")
        st.session_state["notifications"].append(f"Added {quantity} x {product['name']} to Cart.")
        st.session_state["cart"].append({"product": product, "quantity": quantity})
    else:
        st.warning(f"{product['name']} is already in your cart!")

# Remove product from cart
def remove_from_cart(product):
    st.session_state["cart"] = [item for item in st.session_state["cart"] if item["product"] != product]
    st.success(f"Removed {product['name']} from cart!")
    st.session_state["notifications"].append(f"Removed {product['name']} from Cart.")

# Display cart
def display_cart():
    st.header("Cart")
    if not st.session_state["cart"]:
        st.write("Your cart is empty.")
        return

    total = 0
    for item in st.session_state["cart"]:
        product = item["product"]
        quantity = item["quantity"]
        with st.container():
            st.image(product["image"], width=100)
            st.write(f"**{product['name']}** - ${product['price']} x {quantity}")
            if st.button(f"Remove - {product['name']}", key=f"remove_{product['id']}"):
                remove_from_cart(product)

        total += product["price"] * quantity

    st.write(f"**Total: ${total}**")
    if st.button("Proceed to Payment"):
        process_payment(total)

# Payment processing
def process_payment(total, payment_method="Card"):
    selected_payment = st.radio("Select Payment Method", ["Card", "PayPal", "Google Pay"])
    if selected_payment != "Card":
        st.warning(f"{selected_payment} integration coming soon!")
        return

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
                        "unit_amount": int(total * 100),  # Stripe requires amount in cents
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://example.com/payment-success",
            cancel_url="https://example.com/payment-cancel",
            payment_intent_data={
                "metadata": {
                    "user_email": st.session_state["user_email"],
                }
            },
        )
        st.markdown(f"[Click here to complete your payment]({session.url})")

        # Save order to history
        order = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": st.session_state["cart"],
            "total": total
        }

        # Add order notification
        st.session_state["notifications"].append(f"Order placed on {order['date']} with total: ${total}.")
        st.session_state["order_history"].append(order)
        st.session_state["cart"] = []  # Clear the cart after successful payment
    except stripe.error.StripeError as e:
        st.error(f"Stripe error occurred: {e.user_message}")
    except Exception as e:
        st.error(f"An error occurred during payment processing: {str(e)}")
def app():
    display_cart()