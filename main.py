import streamlit as st
import json

# Define a function to load and save posts from JSON file


def load_posts():
    try:
        with open("posts.json", "r") as f:
            posts = json.load(f)
    except FileNotFoundError:
        posts = []
    return posts


def save_posts(posts):
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=4)
        st.success("Post Saved")


# Initialize posts list
posts = load_posts()

# Define functions for CRUD operations


def create_post():
    title = st.text_input("Enter post title:")
    content = st.text_area("Write your post:")
    submit = st.button("Create Post")
    if submit and title and content:
        new_post = {"title": title, "content": content}
        posts.append(new_post)
        save_posts(posts)
        st.success("Post created successfully!")
    elif submit and (not title or not content):
        st.warning("Please fill out both title and content.")


# Display header and sidebar
st.title("My Awesome Blog")
menu = st.sidebar.selectbox("Choose an option:", ["Home", "Create", "Update", "Delete"])
# Show posts on home page
if menu == "Home":
    if not posts:
        st.write("No posts available.")
    else:
        for index, post in enumerate(posts):
            st.header(f"{index + 1}. {post['title']}")
            st.markdown(post["content"])

# Create new post form
elif menu == "Create":
    create_post()

# Update post page
elif menu == "Update":
    st.header("Update Post")
    post_index = st.selectbox("Select post to update:",
                              options=list(range(len(posts))), index=0)

    if posts:
        post = posts[post_index]
        updated_title = st.text_input("Edit post title:", value=post["title"])
        updated_content = st.text_area(
            "Edit post content:", value=post["content"])
        submit = st.button("Update Post")

        if submit and updated_title.strip() and updated_content.strip():
            posts[post_index]["title"] = updated_title
            posts[post_index]["content"] = updated_content
            save_posts(posts)
            st.success("Post updated successfully!")

# Delete post page
elif menu == "Delete":
    st.header("Delete Post")
    post_index = st.selectbox("Select post to delete:",
                              options=list(range(len(posts))), index=0)

    if posts:
        st.write(f"Are you sure you want to delete the post: {
                 posts[post_index]['title']}?")
        confirmation = st.button("Delete Post")

        if confirmation:
            del posts[post_index]
            save_posts(posts)
            st.success("Post deleted successfully!")
