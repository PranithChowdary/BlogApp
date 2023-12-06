import streamlit as st
import json
import pickle
import pandas as pd 
import numpy as np

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

def load_models():
    '''
    Replace '..path/' by the path of the saved models.
    '''
    
    # Load the vectoriser.
    file = open('/workspace/BlogApp/vectoriser-ngram-(1,2).pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()
    # Load the LR Model.
    file = open('/workspace/BlogApp/Sentiment-BNB.pickle', 'rb')
    LRmodel = pickle.load(file)
    file.close()
    
    return vectoriser, LRmodel

def predict(vectoriser, model, text):
    # Predict the sentiment
    textdata = vectoriser.transform(text)
    sentiment = model.predict(textdata)
    
    # Make a list of text with sentiment.
    data = []
    for text, pred in zip(text, sentiment):
        data.append((text,pred))
        
    # Convert the list into a Pandas DataFrame.
    df = pd.DataFrame(data, columns = ['text','sentiment'])
    df = df.replace([0,1], ["Negative","Positive"])
    return df
    
    
# Display header and sidebar
st.title("My Blog Site")
st.sidebar.title("Team Members")
st.sidebar.write("• Vishnu Reddy Balam – A20553257")
st.sidebar.write("• Harsha Vardhan Reddy Basireddy - A20547234")
st.sidebar.write("• LeenaRadhaAarupya Bhima – A20552405(Voice of the team)")
menu = st.sidebar.selectbox("Choose an option:", ["Home", "Create", "Update", "Delete", "Analyze"])
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
        st.write(f"Are you sure you want to delete the post: {posts[post_index]['title']}?")
        confirmation = st.button("Delete Post")

        if confirmation:
            del posts[post_index]
            save_posts(posts)
            st.success("Post deleted successfully!")

elif menu == 'Analyze':
    vectoriser, LRmodel = load_models()
    post_index = st.selectbox("Select post to analyze:",
                              options=list(range(len(posts))), index=0)
    if post_index:
        post = posts[post_index]
        st.write(post)
        df = predict(vectoriser, LRmodel, post)
        st.write(df.head())
