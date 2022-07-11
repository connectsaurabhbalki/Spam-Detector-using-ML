import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
ps = PorterStemmer()

def transform_text(text):
    # convert text into lowercase
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []

    # taking only alphanumeric characters (removing special characters)
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    # removing stopwords and punctuations
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    # stemming
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title("SMS Spam Detector")

input_sms = st.text_area('Enter the message')

if st.button('Predict'):

    # 1. preprocess
    transform_sms = transform_text(input_sms)

    # 2. vectorize
    vector_input = tfidf.transform([transform_sms])

    # 3. predict
    result = model.predict(vector_input)[0]

    # 4. Display
    if result == 1:
        st.header('Spam')
    else:
        st.header('Not Spam')
