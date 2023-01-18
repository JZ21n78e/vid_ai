import os
import spacy
from extract_keywords_for_each_sentence import our_keyword_extractor

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from pathlib import Path

from aws_s3 import upload_file as aws_s3_uploadfile
import uuid


def pollyfy(para):
    '''
    takes a paragraph as input and returns list of s3 url of uploaded polly sentences 
    '''
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(para)
    sentences = [sent.text.strip() for sent in doc.sents]
    url_lists=aws_polly_s3(sentences)
    print("DEBUG: S3URL LIST:  ",url_lists)
    return url_lists

def aws_polly_s3(sentences):
    '''
    takes list of sentences and generates audio using amazon polly 
    and returns list of urls for each sentence
    '''
    session = Session(profile_name="jayson",region_name='ap-southeast-2')
    print(session.available_profiles)
    polly = session.client("polly")
    s3_url_list=[]
    s3_url_header ='''https://s3.ap-southeast-2.amazonaws.com/com.21n78e.pollyfiles/'''
    for i,sentence in enumerate(sentences):
        file_name = f"speech_{uuid.uuid1()}.mp3"
        s3_url_list.append(s3_url_header+file_name)
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=sentence, OutputFormat="mp3",
                                                VoiceId="Joanna")
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)

        if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join(gettempdir(), file_name)
                    print(f"DEBUG: Temp dir == {output}")
                    try:
                        # Open a file for writing the output as a binary stream
                            with open(output, "wb") as file:
                                file.write(stream.read())
                            aws_s3_uploadfile(output)
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
                        sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # # Play the audio using the platform's default player
        # if sys.platform == "win32":
        #     os.startfile(output)
        #     print(output)
        # else:
        #     # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        #     opener = "open" if sys.platform == "darwin" else "xdg-open"
        #     subprocess.call([opener, output])
        # pass
    
    return s3_url_list



if __name__ =='__main__':
    op=pollyfy("there is a decline in bitcoin price nowadays. This is due to ongoing war between russia and ukraine. The market is also taking a toll. The dollar is facing inflation. Alleluia praise the Lord.")
    print(op)
