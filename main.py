import streamlit as st
import pandas as pd

# Define a dictionary to store blog post data (initially empty)
posts = {}

# Create function to display blog post list


def list_posts():
    st.title("Blog Posts")
    posts
    for post_id in posts:
        st.write(f"**ID:** {post_id} | **Title:** {post['title']}")
        if st.button(f"View", key=post_id):
            show_post(post_id)

# Create function to display individual blog post


def show_post(post_id):
    post = posts[post_id]
    st.title(post["title"])
    st.markdown(post["content"])

# Create function to create a new blog post


def create_post():
    with st.form("Create New Post"):
        title = st.text_input("Title:", key="title")
        content = st.text_area("Content:", key="content")
        submit = st.form_submit_button()
        if submit:
            new_id = max(posts.keys(), default=00) + 1
            posts[new_id] = {
                "title": title,
                "content": content,
            }
            st.success("Post created successfully!")

# Create function to update a blog post


def update_post(post_id):
    post = posts[post_id].copy()
    with st.form(f"Update Post {post_id}"):
        st.text_input("Title:", key="title", default=post["title"])
        st.text_area("Content:", key="content", default=post["content"])
        if st.form_submitted():
            posts[post_id] = {
                "title": st.session_state["title"],
                "content": st.session_state["content"],
            }
            st.success("Post updated successfully!")

# Create function to delete a blog post

def delete_post(post_id):
    if st.button(f"Delete post {post_id}?", key=f"delete_{post_id}"):
        del posts[post_id]
        st.success("Post deleted successfully!")


# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["List Posts", "Create Post","Update Post","Delete Post"])

# Display page content based on selection
if page == "List Posts":
    list_posts()
elif page == "Create Post":
    create_post()
# elif page == "Update Post":
#     update_post()
# elif page == "Delete Post":
    
    

# Additional pages for update and delete can be added here


def update_post():
    post_id = st.text_input("Enter Post ID", value="")
    post = posts[post_id].copy()
    with st.form(f"Update Post {post_id}"):
        st.text_input("Title:", key="title", default=post["title"])
        st.text_area("Content:", key="content", default=post["content"])
        if st.form_submitted():
            posts[post_id] = {
                "title": st.session_state["title"],
                "content": st.session_state["content"],
            }
            st.session_state.clear()
            st.success("Post updated successfully!")

