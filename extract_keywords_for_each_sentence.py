#!/usr/bin/env python
# import pyttsx3
# import time
import spacy
import pytextrank
import pandas as pd


def our_keyword_extractor(para):
    '''
    for given para , uses nlp to find keywords and returns two list containing keywords and  sentences

    '''

    nlp = spacy.load("en_core_web_lg")
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
        # response=input("Do you wish to change the keyword?: ")
        # if response=='y':
        #     df.at[i,'Keyword'] = input("New keyword?: ")
            
            
    return list(df['Keyword']),list(df['List of sentences'])

if __name__ == "__main__":
    para='there is a decline in bitcoin price nowadays. This is due to ongoing war between russia and ukraine. The market is also taking a toll. The dollar is facing inflation. Alleluia praise the Lord.'
    var,sentences = our_keyword_extractor(para)
    print(var)
    print(sentences)

    # para='there is a decline in bitcoin price nowadays. This is due to ongoing war between russia and ukraine. The market is also taking a toll. The dollar is facing inflation. Alleluia praise the Lord.'
    # para = "They decided to settle the argument with a race. They agreed on a route and started off the race. The rabbit shot ahead and ran briskly for some time. Then seeing that he was far ahead of the tortoise, he thought he'd sit under a tree for some time and relax before continuing the race. He sat under the tree and soon fell asleep."
    # para = "The last goal doesn’t matter. The last victory, already forgotten. Yesterday is gone. Lost, in the record books. But today is up for grabs. Unpredictable. Unwritten. Undecided. “Now” is ours. Do something and be remembered. Or do nothing and be forgotten. No one owns today. Take it"
 