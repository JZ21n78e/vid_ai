#!/usr/bin/env python
import pyttsx3
import time
import spacy
import pytextrank
import pandas as pd


def our_keyword_extractor(para):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(para)
    sentences = [sent.text.strip() for sent in doc.sents]
    
    ordered_queries=[]
    nlp.add_pipe("textrank")
    for s in sentences:
        doc = nlp(s)
        container_of_keywords=[]

        if len(doc._.phrases)<2:
            if len(doc._.phrases)==1:
                query=doc._.phrases[0].text
                ordered_queries.append(query)

            else:
                query=s
                ordered_queries.append(query)
        else:  
            for phrase in doc._.phrases:
                #print(phrase.text)
                container_of_keywords.append(phrase.text)
                #print(phrase.rank, phrase.count)
                #print(phrase.chunks)
                #print('\n')
                print(len(container_of_keywords))

                if len(container_of_keywords)==2:
                    print(container_of_keywords)
                    query=container_of_keywords[0]+' '+container_of_keywords[1]
                    ordered_queries.append(query)

                    break
                    
    df = pd.DataFrame({'List of sentences': sentences,'Keyword': ordered_queries})

    for i in range(len(df)):
        print(df.iloc[i])
        print("\n")
        response=input("Do you wish to change the keyword?: ")
        if response=='y':
            df.at[i,'Keyword'] = input("New keyword?: ")
            
            
    return list(df['Keyword']),list(df['List of sentences'])

