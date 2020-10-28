# Twitter Sentiment App
# By: George Thoraninh

import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.express as px

st.title('Sentiment Analysis of Tweets: US Airlines')
st.sidebar.title('Sentiment Analysis of Tweets: US Airlines')

st.markdown('Streamlit dashboard app to analyze the sentiment of Tweets')
st.sidebar.markdown('Streamlit dashboard app to analyze the sentiment of Tweets')

DATA_URL = ('/Users/gthorani/streamlit_apps/Tweets_2.csv')

@st.cache(persist=True)
def load_data():
    df = pd.read_csv(DATA_URL)
    df['tweet_created'] = pd.to_datetime(df['tweet_created'])
    return df

data = load_data()

st.sidebar.subheader('Show random tweet')
random_tweet = st.sidebar.radio('Sentiment', ('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Chart Type', ['Bar Chart', 'Pie Chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index,
                                'Tweets': sentiment_count.values})

# st.write(sentiment_count[sentiment_count['Sentiment'] == 'negative'])

if not st.sidebar.checkbox('Hide', True):
    st.markdown('### # of Tweets by Sentiment')
    if select == 'Bar Chart':
        fig = px.bar(sentiment_count,
                    x = 'Sentiment',
                    y = 'Tweets',
                    color = 'Sentiment',
                    color_discrete_sequence =['#DD6E42', '#E8DAB2', '#30A1F2'],
                    height = 500)
        st.plotly_chart(fig)            
    else:
        fig = px.pie(sentiment_count, 
                    values = 'Tweets',
                    names = 'Sentiment',
                    color = 'Sentiment',
                    color_discrete_sequence =['#DD6E42', '#E8DAB2', '#30A1F2'])
        st.plotly_chart(fig)            

st.sidebar.subheader('When and where are users tweeting from?')
hour = st.sidebar.slider('Hour of Day', 0, 23)
# hour = st.sidebar.number_input('Hour of Day', min_value = 1, max_value = 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Close', True, key = '1'):
    st.markdown('### Tweet location based on time of day')
    st.markdown('%i tweets between %i:00 and %i:00' % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    # if st.sidebar.checkbox('Show raw data', False):
    #     st.write(modified_data)

st.sidebar.subheader('Breakdown airline tweets by sentiment')
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key = 0)

if len(choice) > 0:
    choice_data = data[data['airline'].isin(choice)]
    fig_choice = px.histogram(choice_data, 
                            x = 'airline',y = 'airline_sentiment',
                            histfunc = 'count',
                            color = 'airline_sentiment',
                            color_discrete_sequence =['#DD6E42', '#E8DAB2', '#30A1F2'],
                            color_discrete_map = {'negative': '#DD6E42', 'neutral': '#E8DAB2', 'positive': '#30A1F2'},
                            facet_col = 'airline_sentiment',
                            labels = {'airline_sentiment': 'tweets'}, 
                            height = 600,
                            width = 800)
    st.plotly_chart(fig_choice)