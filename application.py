import shutil
import sys
from pytube import YouTube
from pytube import Search
import warnings
warnings.filterwarnings('ignore')
import glob
import os
import math
import moviepy.editor as mp
import mutagen
from mutagen.mp3 import MP3
from pydub import AudioSegment
import streamlit as st
import yagmail

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    youtubeObject.download()

def send_parts(email,parts):
    yag = yagmail.SMTP('akshatgirdhar02@gmail.com', 'ocyuxqgobnrtelri')
    subject = 'Mashup File'
    contents="Please find the attachment below"

    for i, part in enumerate(parts):
        part_filename = 'Part{}_{}'.format(i+1,'Mashup.mp3')
        yag.send(email, subject,contents,attachments= [part_filename])

def main():
    st.title("Mashup")
    st.markdown("**Output will be sent via email as a set of 6 mp3 files,since size of final file might be large and couldn't be sent in single go.**")
    with st.form(key='form2'):
        singer = st.text_input(
        "Enter name of the singer 👇",
        )
        number= st.number_input(
        "Enter the number of videos 👇",
        min_value=1,
        max_value=30,
        )
        cut= st.number_input(
        "Enter the duration of each video to cut(in seconds) 👇",
        min_value=20,
        max_value=60,
        step=5,
        )
        email = st.text_input(
        "Enter the email 👇",
        )
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col3:
            submit_button=st.form_submit_button(label="Submit")
        with col4:
            pass
        with col5:
            pass
    
    if (singer is not None and number is not None and cut is not None and email is not None):
        number=int(number)
        cut=int(cut)
        s=Search(singer)
        if(len(s.results)!=0):
            found=len(s.results)
            searchResults = {}
            remaining=3*number-found
            while(remaining>0):
                s.get_next_results()
                found=len(s.results)
                remaining=number-found
            for v in s.results:
                searchResults[v.title] = v.watch_url
            links=list(searchResults.values())
            st.write("Links found:",links);
            list1=[]
            final_list=[]
            for("Going inside for")
            for i in range(len(links)):
                st.write("Inside for:")
                yt = YouTube(links[i]) 
                st.write("Title is: ",yt.title)
                try:
                    video_length = yt.length
                    if(video_length<=300):
                        list1.append(links[i])
                except:
                    pass
            st.write("Number of videos required: ",number)
            st.write("Links of videos found: ",list1)
            for i in range(number):
                final_list.append(list1[i])
            for i in final_list:
                print(i)
                try:
                    Download(i)
                except:
                    continue
            st.write("All videos have been downloaded")
            pathdir='.'
            mp4_filenames_list=glob.glob(os.path.join(pathdir,"*mp4"))
            for filename in mp4_filenames_list:
                video=mp.VideoFileClip(filename)
                audio=video.audio
                if(audio is not None):
                    mp3_file_name=filename.replace('.mp4','.mp3')
                    audio.write_audiofile(mp3_file_name)
                    video.close()
            st.write("All videos are converted to audio")
            mp3_filename_list=glob.glob(os.path.join(pathdir,"*mp3"))
            for filename in mp3_filename_list:
                audio = MP3(filename)
                audio_info = audio.info
                length = int(audio_info.length)
                sound = AudioSegment.from_mp3(filename)
                if(cut<length):
                    extract = sound[cut*1000:]
                elif(length>=20):
                    extract=sound[20*1000:]
                elif(length>=10):
                    extract=sound[10*1000:]
                else:
                    extract=sound
                extract.export(filename, format="mp3")
            st.write("All the audio files have been shortened")
            sound1=AudioSegment.from_mp3(mp3_filename_list[0])
            sound2=AudioSegment.from_mp3(mp3_filename_list[1])
            final_sound=sound1.append(sound2,crossfade=150)
            i=0
            noOfFiles=len(mp3_filename_list)
            for filename in mp3_filename_list:
                if(i<2):
                    i+=1
                    continue
                else:
                    i+=1
                    sound1=AudioSegment.from_mp3(filename)
                    final_sound=final_sound.append(sound1,crossfade=150) 
            final_sound.export("Mashup.mp3",format="mp3")
            st.write("Final output is ready")
            filename='Mashup.mp3'
            if submit_button:
                try:
                    divide_file('Mashup.mp3',6)
                    send_parts(email,['Part1_Mashup.mp3', 'Part2_Mashup.mp3', 'Part3_Mashup.mp3', 'Part4_Mashup.mp3', 'Part5_Mashup.mp3', 'Part6_Mashup.mp3'])
                    st.write("Email sent")
                except Exception as e:
                    st.write("Email not sent because %s" %(e))
def divide_file(filename, parts):
    part_size = math.ceil(os.path.getsize(filename) / parts)

    with open(filename, 'rb') as f:
        for i in range(parts):
            part = f.read(part_size)
            part_filename = 'Part{}_{}'.format(i+1,filename)
            with open(part_filename, 'wb') as p:
                p.write(part)

# def deleteVideos():
#     folder = '.\\' 
#     for filename in os.listdir(folder):
#         if filename.endswith(".mp4"):
#             file_path = os.path.join(folder, filename)
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)

# def deleteAudios():
#     folder = '.\\' 
#     for filename in os.listdir(folder):
#         if filename.endswith(".mp3"):
#             file_path = os.path.join(folder, filename)
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)



if __name__=="__main__":
    main()
    # deleteVideos()
    # deleteAudios()
