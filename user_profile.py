import streamlit as st
from database import get_products, get_db, User


def app():
    # Notification system
    def display_notifications():
        if st.session_state["notifications"]:
            st.header("Notifications")
            for notification in st.session_state["notifications"]:
                st.write(f"- {notification}")
            if st.button("Clear Notifications"):
                st.session_state["notifications"] = []

    # User profile
    def display_user_profile():
        email = st.session_state["user_email"]
        user = get_db().query(User).filter(User.email == email).one_or_none()

        if user:
            st.header("User Profile")
            st.write(f"**Name:** {user.name}")
            st.write(f"**Email:** {user.email}")
            st.write(f"**Phone:** {user.phone if user.phone else 'NA'}")

            if user.address:
                st.write(f"**Address:** {user.address}")
            else:
                if st.button("Add Address"):
                    address = st.text_area("Enter your address")
                    if st.button("Save Address"):
                        user.address = address
                        get_db().commit()  # Save to database
                        st.success("Address added successfully")

            if st.button("Edit Profile"):
                edit_name = st.text_input("Edit Name", user.name)
                edit_phone = st.text_input("Edit Phone", user.phone)
                if st.button("Save Changes"):
                    user.name = edit_name
                    user.phone = edit_phone
                    get_db().commit()  # Save changes to database
                    st.success("Profile updated successfully")
        else:
            st.warning("User profile not found.")

    display_notifications()
    display_user_profile()
