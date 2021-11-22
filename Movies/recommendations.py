import warnings
warnings.filterwarnings("ignore")

import pandas as pd

import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from fuzzywuzzy import fuzz 
from fuzzywuzzy import process

def bag(string):
    
    StopWords = stopwords.words('english')

    split = word_tokenize(string)
    
    words = [*set(x.lower() for x in split if x.isalpha() or x.isdigit())]
    
    clean_words = " ".join([x for x in words if x not in StopWords])

    return clean_words

def find_title(df,query):
    
    mov = process.extractOne(query, df.title)
    return mov[0]

def recommend(title,indices,cs,df):
    
    index = indices[title]
    
    cosine_sim = list(enumerate(cs[index]))
    
    top_10 = sorted(cosine_sim,key = lambda x : x[1],reverse = True)[1:11]
    
    top_ind = [i[0] for i in top_10]
    
    result = df.title[top_ind]
    
    # for x in result:
        
    #     print(x) 
    return result

def getRec(filePath, query):
    
    df = pd.read_csv(filePath)
    
    indices = pd.Series(df.index, index = df.title)
    
    bags = list(map(bag,df.summary))
    
    vectorizer = TfidfVectorizer ()
    x = vectorizer.fit_transform(bags).toarray()
    
    cs = cosine_similarity(x)
    
    title = find_title(df,query)
    
    return recommend(title,indices,cs,df)

# if __name__ == "__main__":
    
#     filePath = r"C:\Users\Sanket\Desktop\Python\Web FrameWork\assests\Movies_DataSet.csv"
#     Name = input("Enter a Movie Name: ")
#     getRec(filePath, Name)