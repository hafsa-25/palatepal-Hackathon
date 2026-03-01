import streamlit as st
from recommender import recommend, like_dish, dislike_dish

if "liked_dishes" not in st.session_state:
    st.session_state.liked_dishes = set()

if "disliked_dishes" not in st.session_state:
    st.session_state.disliked_dishes = set()

if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = ""

# Display feedback message at the top
if st.session_state.feedback_message:
    st.info(st.session_state.feedback_message)
    st.session_state.feedback_message = ""  

st.sidebar.header("🍽️ Your Taste Profile")

cuisine = st.sidebar.selectbox("Select preferred cuisine:", ["Pakistani", "Indian", "Italian", "Turkish"])
spice_level = st.sidebar.slider("Spice Level (1 = mild, 5 = very spicy):", 1, 5, 3)
dietary_type = st.sidebar.selectbox("Dietary Preference:", ["Veg", "Non-Veg"])
avoid_seafood = st.sidebar.checkbox("Avoid Seafood", value=False)
disliked_ingredient = st.sidebar.text_input("Disliked Ingredients (comma-separated):", "")


if st.sidebar.button("Get Recommendations"):
    recommendations = recommend(
        cuisine=cuisine,
        spice_level=spice_level,
        dietary_type=dietary_type,
        top=5,
        avoid_seafood=avoid_seafood,
        disliked_ingredient=disliked_ingredient
    )

    st.subheader("Recommended Dishes 🍲")

    if recommendations.empty:
        st.warning("No dishes found matching your preferences.")
    else:
        for idx, row in recommendations.iterrows():
            dish_name = row["dish_name"]

            st.markdown(
                f"### 🍽️ {dish_name}\n"
                f"**Cuisine:** {row['cuisine']}  \n"
                f"**Spice Level:** {row['spice_level']}  \n"
                f"**Type:** {row['dietary_type']}"
            )

            st.write(row["description"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"👍 Like {dish_name}", key=f"like_{dish_name}_{idx}"):
                    message = like_dish(dish_name)
                    st.session_state.liked_dishes.add(dish_name.lower())
                    st.session_state.feedback_message = message
                    st.experimental_rerun()  

            with col2:
                if st.button(f"👎 Dislike {dish_name}", key=f"dislike_{dish_name}_{idx}"):
                    message = dislike_dish(dish_name)
                    st.session_state.disliked_dishes.add(dish_name.lower())
                    st.session_state.feedback_message = message
                    st.experimental_rerun()  

            st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.subheader("Your Feedback")
st.sidebar.write("Liked Dishes:", ", ".join(st.session_state.liked_dishes) or "None")
st.sidebar.write("Disliked Dishes:", ", ".join(st.session_state.disliked_dishes) or "None")
