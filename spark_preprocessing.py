import pyspark
from pyspark.sql import SparkSession
from mongo_utils import read_from_mongo
import nltk
from nltk.stem import WordNetLemmatizer
import re
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub("[^a-zA-Z]", " ", text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

lemmatizer = WordNetLemmatizer()

def tokenize_and_lemmatize(text):
    # tokenization to ensure that punctuation is caught as its own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []

    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    lem = [lemmatizer.lemmatize(t) for t in filtered_tokens]
    return lem

def data_cleansing(text):
    text = clean_text(text)
    text = remove_stopwords(text)
    lem_words = tokenize_and_lemmatize(text)
    return lem_words

def collect_preprocess_data():
    ss = SparkSession.builder.appName("capstone").getOrCreate()
    pdf = read_from_mongo()
    sdf = ss.createDataFrame(pdf[['category','text']])
    print(sdf.count())
    lem_udf = udf(data_cleansing, ArrayType(StringType()))
    sdf = sdf.withColumn('processed_text',lem_udf(sdf['text']))
    print(sdf.head(2))
    return sdf

if __name__ == '__main__':
    collect_preprocess_data()
