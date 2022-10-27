import streamlit as st
from streamlit_lottie import st_lottie
import random

import plotly.graph_objects as go
from annotated_text import annotated_text
from analysis import *


st.set_page_config(page_title="Review-Inator", page_icon=":tada:")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



with st.container():
    st.title('Review-Inator :star2:')
    left_column, right_column = st.columns(2)
    with left_column:
        st.write(
            """
            :large_blue_diamond: Analyse sentiment of the reviews from multiple shopping or services websites. \n
            :large_blue_diamond: Get detail insights and recommendations ! \n
            :large_blue_diamond: Simply paste the urls of products or services below
            """
        )
    with right_column:
        lottie_reviews = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_akvycwlq.json")
        st_lottie(lottie_reviews, height=240, key="reviews")

url = st.text_input('URL of Product/Service', placeholder= 'Enter URL')

if st.button('Analyse'):
    st.write(url)
    data_load_state = st.text('Loading data...')
    all_reviews = getReviews(url)


    with st.container():
        positive , negative = sentiments(all_reviews)
        st.subheader('Sentiment Analysis')
        fig1 = go.Figure(data=[go.Pie(labels=['Positive','Negative'], values= [positive, negative])])
        fig1.update_traces(marker=dict(colors=['red','green']))
        st.plotly_chart(fig1, use_container_width= True)

    with st.container():
        st.subheader('Emotional Traits')
        emotion , score = emotional_traits(all_reviews)
        fig2 = go.Figure(data=[go.Pie(labels= emotion, values= score, hole=.3)])
        st.plotly_chart(fig2, use_container_width= True)

    with st.container():
        left_column, right_column = st.columns(2)
        words , sentences = words_sentences(all_reviews)
        colors = ["#5603AD","#8367C7","#F02D3A", "#F7C548","#950952","#31E981"]
        with left_column:
            st.subheader('Top words')
            for word in words:
                st.markdown('<p style="background-color:'+colors[random.randint(0, 5)]+
                            '; font-size: 18px;border-radius: 12px;text-align: center">'+word+
                            '</p>',unsafe_allow_html=True)
      

        with right_column:
            st.subheader('Top sentences')
            #sentences = ['This is a purely informational message','I hate the product','love the product']
            counter = 0
            for sentence in sentences:
                if counter%4 == 0:
                    st.info(sentence)
                elif counter%4 == 1:
                    st.warning(sentence)
                elif counter%4== 2:
                    st.success(sentence)
                elif counter%4 == 3:
                    st.error(sentence)
                counter+=1
                
    with st.container():
        st.subheader('Final recommendation')
        if negative > positive:
            st.markdown('<p style="color:"red"; font-size: 18px;">Product/Service not recommended buying</p>', unsafe_allow_html=True)
            lottie_dislike = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_L5FmEqdLn6.json")
            st_lottie(lottie_dislike, key="dislike",height=500)
        else:
            st.markdown('<p style="color:"green"; font-size: 18px;">Product/Service recommended buying</p>',
                        unsafe_allow_html=True)
            lottie_buy = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_axztuerm.json")
            st_lottie(lottie_buy, key="buy",height=500)
    data_load_state.text("Done!")




