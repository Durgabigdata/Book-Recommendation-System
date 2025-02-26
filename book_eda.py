import streamlit as st 
import pickle
import pandas as pd
import numpy as np

# Function to recommend similar books based on input book title
def recommend(book):
    if book in collaborative_filtering_pivot.index:
        index = np.where(collaborative_filtering_pivot.index == book)[0][0]
        similar_book_items = sorted(list(enumerate(similarities[index])), key=lambda x: x[1], reverse=True)[1:11]
        data = []

        # Retrieve information of similar books from the dataset
        for i in similar_book_items:
            item = []
            temp_df = books_data[books_data['Book-Title'] == collaborative_filtering_pivot.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
            data.append(item)

        return data

# Main streamlit app
st.set_page_config(page_title='Book Recommendation System', layout='wide', page_icon='📚')

# Custom CSS for colorful layout
st.markdown(
    """
    <style>
    .main-title {
        font-size: 50px;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 24px;
        color: #FF5722;
        text-align: center;
        margin-bottom: 10px;
    }
    .book-card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .book-title {
        font-size: 20px;
        color: #673AB7;
        font-weight: bold;
    }
    .book-author {
        color: #3F51B5;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: #888;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="main-title">📚 Book Recommendation System</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center; font-size: 18px;'>Discover your next favorite book based on your current reads!</p>", unsafe_allow_html=True)

# Load data & models
collaborative_filtering_pivot = pickle.load(open("C:\\Users\\Admin\\Downloads\\pivot.pkl", 'rb'))
books_data = pickle.load(open("C:\\Users\\Admin\\Downloads\\Books.pkl", 'rb'))
similarities = pickle.load(open("C:\\Users\\Admin\\Downloads\\similarities.pkl", 'rb'))

book_list = collaborative_filtering_pivot.index.values

# Sidebar for book selection
st.sidebar.title('Find Your Next Read')
st.sidebar.markdown("<p style='color: #4CAF50;'>Select a book to get recommendations:</p>", unsafe_allow_html=True)
selected_book = st.sidebar.selectbox("Type or select a book from the dropdown", book_list)

if st.sidebar.button('Recommend'):
    st.markdown('<div class="sub-title">Recommended Books</div>', unsafe_allow_html=True)

    # Retrieve and display similar books based on the selected book
    fetch_books = recommend(selected_book)

    if fetch_books:
        cols = st.columns(2)
        for idx, book in enumerate(fetch_books):
            with cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class="book-card">
                        <div class="book-title">{book[0]}</div>
                        <div class="book-author">Author: {book[1]}</div>
                        <div>Year of Publication: {book[2]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.write("No recommendations found. Please select another book.")

# Footer
st.markdown('<div class="footer">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)
