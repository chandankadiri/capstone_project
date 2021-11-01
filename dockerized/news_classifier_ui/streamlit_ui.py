import streamlit as st
import requests
import json
import requests
from bs4 import BeautifulSoup

def parse_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    if 'timesofindia.indiatimes.com' in url:
        text_input = soup.find_all("div",class_='_3YYSt clearfix')[0].text
    elif 'ndtv.com' in url:
        text_input = soup.find_all("div",class_='sp-cn ins_storybody')[0].text
    elif 'news18.com' in url:
        text_input = soup.find_all("div",class_='jsx-3531000781')[0].text
    elif 'timesnownews.com' in url:
        text_input = soup.find_all("div",class_='artical-description')[0].text
    else:
        text_input = soup.find_all("div",class_='artical-description')[0].text
    return  text_input

#with open("style.css") as f:
#    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

st.set_page_config(layout="wide")
#st.title('News Articles Classfier')
st.markdown("<h1 style='text-align: center; color: purple;'>News Articles Classifier</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h3 style='text-align: center; color: black;'>Categorize News Articles</h3>", unsafe_allow_html=True)
    with st.form(key='predict_form'):
        text_input = st.text_area(label='Enter some text/URL:')
        submit = st.form_submit_button(label='Categorize')
    
    if submit:
        if text_input.startswith('http'):
            text_input = parse_url(text_input)
        resp =  requests.post('http://train_predict:8889/predict',
                data=json.dumps({'text':str(text_input)}),verify=False)
        print(resp.status_code)
        #st.write(f'<b>{resp.json()["category"]}</b>')
        html_string = f'<h2>Predicted Category: {resp.json()["category"].capitalize()}</h2>'
        st.markdown(html_string, unsafe_allow_html=True)
        st.write(text_input)
with col2:
    st.markdown("<h3 style='text-align: center; color: black;'>Train News Articles</h3>", unsafe_allow_html=True)
    with st.form(key='retrain_form'):
        text_input = st.text_area(label='Enter some text/URL:')
        category = st.text_input(label='Enter Category:')
        submit = st.form_submit_button(label='Retrain')

    if submit:
        if text_input.startswith('http'):
            text_input = parse_url(text_input)
        resp =  requests.post('http://train_predict:8889/retrain',
                data=json.dumps([{'text':str(text_input),'category':category}]),verify=False)
        print(resp.status_code)
        #st.write(f'<b>{resp.json()["category"]}</b>')
        html_string = f'<h2>{resp.json()}</h2>'
        st.markdown(html_string, unsafe_allow_html=True)
        st.write(text_input)
