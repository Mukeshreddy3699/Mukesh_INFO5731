# -*- coding: utf-8 -*-
"""INFO5731_Assignment_2_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W-ad4qwFM2a27DSbsCOkaqQ70ReQNIT2

# **INFO5731 Assignment 2**

In this assignment, you will work on gathering text data from an open data source via web scraping or API. Following this, you will need to clean the text data and perform syntactic analysis on the data. Follow the instructions carefully and design well-structured Python programs to address each question.

**Expectations**:
*   Use the provided .*ipynb* document to write your code & respond to the questions. Avoid generating a new file.
*   Write complete answers and run all the cells before submission.
*   Make sure the submission is "clean"; *i.e.*, no unnecessary code cells.
*   Once finished, allow shared rights from top right corner (*see Canvas for details*).

* **Make sure to submit the cleaned data CSV in the comment section - 10 points**

**Total points**: 100

**Deadline**: Tuesday, at 11:59 PM.

**Late Submission will have a penalty of 10% reduction for each day after the deadline.**

**Please check that the link you submitted can be opened and points to the correct assignment.**

# Question 1 (40 points)

Write a python program to collect text data from **either of the following sources** and save the data into a **csv file:**

(1) Collect all the customer reviews of a product (you can choose any porduct) on amazon. [atleast 1000 reviews]

(2) Collect the top 1000 User Reviews of a movie recently in 2023 or 2024 (you can choose any movie) from IMDB. [If one movie doesn't have sufficient reviews, collect reviews of atleast 2 or 3 movies]

(3) Collect all the reviews of the top 1000 most popular software from G2 or Capterra.

(4) Collect the **abstracts** of the top 10000 research papers by using the query "machine learning", "data science", "artifical intelligence", or "information extraction" from Semantic Scholar.

(5) Collect all the information of the 904 narrators in the Densho Digital Repository.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

import requests
from bs4 import BeautifulSoup
import pandas as pd

imdb_base_url = f'https://www.imdb.com/title/tt15239678/reviews?ref_=tt_urv'  #imdb reviews
total_reviews = int(input("number of reviews to scrap: "))
extracted_reviews = []
reviews_per_page = 25
iterations = (total_reviews // reviews_per_page) + 1
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

for current_page in range(1, iterations * reviews_per_page, reviews_per_page):
    page_url = f'{imdb_base_url}&start={current_page}'
    response = requests.get(page_url)
    page_content = BeautifulSoup(response.content, 'html.parser')
    review_blocks = page_content.find_all('div', class_='text show-more__control')
    extracted_reviews.extend([block.text.strip() for block in review_blocks])
    if len(extracted_reviews) >= total_reviews:
        break

extracted_reviews = extracted_reviews[:total_reviews]
dune_reviews = extracted_reviews #Scraping user reviews
print(f"Data scraping successful.")
reviews_df = pd.DataFrame( dune_reviews, columns=['reviews'])
reviews_df
reviews_df.to_csv('dune_reviews.csv', index=False)
print(' File created successfully')

data_url="https://raw.githubusercontent.com/Mukeshreddy3699/Mukesh_INFO5731/refs/heads/main/Dune_reviews.csv"
df = pd.read_table(data_url,names=['text'])
df

"""# Question 2 (30 points)

Write a python program to **clean the text data** you collected in the previous question and save the clean data in a new column in the csv file. The data cleaning steps include: [Code and output is required for each part]

(1) Remove noise, such as special characters and punctuations.

(2) Remove numbers.

(3) Remove stopwords by using the stopwords list.

(4) Lowercase all texts

(5) Stemming.

(6) Lemmatization.
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string
import re

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

#1)Remove Noise function
def remove_noise(text):
    clean_text = re.sub('[^a-zA-Z0-9]', ' ', text)
    return clean_text
df['clean_text'] = df['text'].apply(remove_noise)
print("\nData Frame after removing noise:")   #Displaying the Data Frame after removing noise
df

#2)Remove Numbers
def remove_numbers(text):
    clean_text = re.sub(r'\d+', '', text)
    return clean_text
df['clean_text_remove_numbers'] = df['clean_text'].apply(remove_numbers)
print("\nData Frame after removing numbers:")
df

#3)Remove stopwords by using the stopwords List
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    filter_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filter_words)
df['clean_text_remove_stopwords'] = df['clean_text_remove_numbers'].apply(remove_stopwords)
print("\nData Frame after removing stopwords without lowercase:")
df

# 4)Lowercase all texts
df['clean_text_lowercase'] = df['clean_text_remove_stopwords'].apply(lambda x: x.lower())
print("\nData Frame after converting texts to lowercase:")
df

#5)Stemming
stem = PorterStemmer()
def apply_stemming(text):
    words = nltk.word_tokenize(text)
    stemmed_words = [stem.stem(word) for word in words]
    return ' '.join(stemmed_words)
df['clean_text_stemmed'] = df['clean_text_lowercase'].apply(apply_stemming)
print("\nData Frame after applying stemming:")
df

#6)Lemmatization
lemmatizer = WordNetLemmatizer()
def apply_lemmatization(text):
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)
df['clean_text_lemmatized'] = df['clean_text_stemmed'].apply(apply_lemmatization)
print("\nData Frame after applying lemmatization:")
df

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_data_.csv', index=False)
print("\nCleaned data saved ")

"""# Question 3 (30 points)

Write a python program to **conduct syntax and structure analysis of the clean text** you just saved above. The syntax and structure analysis includes:

(1) **Parts of Speech (POS) Tagging:** Tag Parts of Speech of each word in the text, and calculate the total number of N(oun), V(erb), Adj(ective), Adv(erb), respectively.

(2) **Constituency Parsing and Dependency Parsing:** print out the constituency parsing trees and dependency parsing trees of all the sentences. Using one sentence as an example to explain your understanding about the constituency parsing tree and dependency parsing tree.

(3) **Named Entity Recognition:** Extract all the entities such as person names, organizations, locations, product names, and date from the clean texts, calculate the count of each entity.
"""

# Your code here
import pandas as pd
import nltk
from collections import Counter
# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

df = pd.read_csv('cleaned_data_.csv')

#1)Parts of Speech (POS) Tagging
def pos_tagging(text):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return pos_tags
for index, row in df.iterrows():         #Iterate through each row and print the POS tagging on a new line
    pos_tags = pos_tagging(row['clean_text'])
    print(f"POS tagging for row {index + 1}:\n{pos_tags}\n")
    noun_count = verb_count = adj_count = adv_count = 0
    for _, pos in pos_tags:
        if pos.startswith('N'):
            noun_count += 1
        elif pos.startswith('V'):
            verb_count += 1
        elif pos.startswith('JJ'):
            adj_count += 1
        elif pos.startswith('RB'):
            adv_count += 1
    print(f"Total Nouns: {noun_count}")
    print(f"Total Verbs: {verb_count}")
    print(f"Total Adjectives: {adj_count}")
    print(f"Total Adverbs: {adv_count}")

!pip install benepar
!pip install tensorflow
!pip install tensorflow==2.8.0

import benepar
import spacy.cli
benepar.download('benepar_en3')
spacy.cli.download("en_core_web_sm")

import sys
import spacy
from spacy import displacy
parser = benepar.Parser("benepar_en3")
nlp = spacy.load('en_core_web_sm')
options = {'compact': True, 'font': 'Arial black', 'distance': 100}
for sentence in df['clean_text']:
    try:
        tree = parser.parse(sentence)
        print(tree)
    except:
        print("No Parse Tree")
        continue
for sentence in df['clean_text']:     #Printing parse trees using spacy module
    doc = nlp(sentence)
    displacy.render(doc, style='dep', options=options, jupyter=True)

#3)Named Entity Recognition
import en_core_web_sm
nlp=en_core_web_sm.load()
for x in df['clean_text']:
    doc = nlp(x)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if entities:
        print(entities)

"""#**Comment**
Make sure to submit the cleaned data CSV in the comment section - 10 points
"""

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_data_.csv', index=False)
print("\nCleaned data saved ")

"""# Mandatory Question

Provide your thoughts on the assignment. What did you find challenging, and what aspects did you enjoy? Your opinion on the provided time to complete the assignment.
"""

# Write your response below
'''it takes more time to get a large dataset which is challenging due to more run time.'''