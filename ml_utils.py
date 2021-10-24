import pyspark
from pyspark.sql import SparkSession
from mongo_utils import read_from_mongo,write_to_mongo
import nltk
from nltk.stem import WordNetLemmatizer
import re
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

svc_mdl = None
tfidf_vec = None
id_to_category = None

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

def vectorize_text():
    count_vec = CountVectorizer(stop_words='english', max_features=10000)
    tfidf_vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), tokenizer=tokenize_and_lemmatize, max_features=10000, use_idf=True)
    features = tfidf_vec.fit_transform(news_df.clean_text).toarray()
    labels = news_df.category_id

def train_model():
    global svc_mdl
    global tfidf_vec
    global id_to_category
    pdf = read_from_mongo()
    pdf['category_id'] = pdf['category'].factorize()[0]
    pdf['clean_text'] = pdf['text'].apply(clean_text)
    # count_vec = CountVectorizer(stop_words='english', max_features=10000)
    tfidf_vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), tokenizer=tokenize_and_lemmatize, max_features=10000, use_idf=True)
    labels = pdf.category
    category_id_df = pdf[['category', 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', 'category']].values)
    X = pdf.loc[:,'clean_text']
    y = pdf.loc[:,'category_id']
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(X, y, pdf.index, test_size=0.2, random_state=55)
    xtrain_tfidf = tfidf_vec.fit_transform(X_train)
    xtest_tfidf = tfidf_vec.transform(X_test)
    # xtrain_cv = count_vec.fit_transform(X_train)
    # xtest_cv = count_vec.transform(X_test)
    svc_mdl = LinearSVC()
    svc_mdl.fit(xtrain_tfidf, y_train)
    y_pred = svc_mdl.predict(xtest_tfidf)
    accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
    # Get precision, recall, f1 scores
    precision, recall, f1score, support = score(y_test, y_pred, average='micro')
    print(f'accuracy-{accuracy}\nprecision-{precision}\nrecall-{recall}\nf1score-{f1score}')
    # return svc_mdl

def predict_category(text):
    #import pdb;pdb.set_trace()
    #tfidf_vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), tokenizer=tokenize_and_lemmatize, max_features=10000, use_idf=True)
    text = clean_text(text)
    vec_text = tfidf_vec.transform([text])
    pred_cat = svc_mdl.predict(vec_text)
    print(pred_cat)
    return id_to_category[pred_cat[0]]

def retrain_model(data):
    write_to_mongo(data)
    pdf = read_from_mongo()
    pdf['category_id'] = pdf['category'].factorize()[0]
    pdf['clean_text'] = pdf['text'].apply(clean_text)
    category_id_df = pdf[['category', 'category_id']].drop_duplicates().sort_values('category_id')
    X = pdf.loc[:,'clean_text']
    y = pdf.loc[:,'category_id']
    X_tfidf = tfidf_vec.fit_transform(X)
    svc_mdl.fit(X_tfidf, y)
    return svc_mdl

def spark_collect_preprocess_data():
    ss = SparkSession.builder.appName("capstone").getOrCreate()
    pdf = read_from_mongo()
    sdf = ss.createDataFrame(pdf[['category','text']])
    print(sdf.count())
    lem_udf = udf(data_cleansing, ArrayType(StringType()))
    sdf = sdf.withColumn('processed_text',lem_udf(sdf['text']))
    print(sdf.head(2))
    return sdf

if __name__ == '__main__':
    #collect_preprocess_data()
    train_model()
    predict_category('''There is an abundance of Marathi film news platforms to choose from, it can be difficult to know where to find authentic news. Well, if you are looking for your daily dose of entertainment and exclusive news, gossips, latest clicks by stars this is your one-stop solution to follow all the updates and the latest happenings in Marathi cinema. We will embark on our first-ever Marathi Cinema News platform and we’re always at the forefront to provide the right information at the right time.  Not only that but this section even provides you with details like cast information, box-office collections, related videos and pictures of all the latest Marathi films.''')
