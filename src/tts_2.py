import tts_text as texts
import os
from pydub import AudioSegment
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.editor import VideoFileClip, AudioFileClip
import shutil
from comtypes import client
import tts
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

path = r"C:\Users\Thanh Lu\AppData\Local\Programs\Python\Python311\Lib\site-packages\TTS\.models.json"

model_manager = ModelManager(path)
model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC_ph")
voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])
syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

mypath=r"C:\Users\Thanh Lu\OneDrive\tts\sample.pptx"

def sort_key(file_name):
    # Extract the numeric part of the file name for sorting
    base_name, _ = os.path.splitext(file_name)
    return int(base_name)

def getWav (my_path):
    des_path=os.path.join(os.getcwd(),"To_Wavs")
    if not os.path.exists(des_path):
            os.makedirs(des_path)
    contents = texts.getText(my_path)
    for i,text in enumerate(contents): 
        outputs = syn.tts(text)
        syn.save_wav(outputs, os.path.join(des_path, f"{i+1}.wav"))    

def combineAudio ():
    audio_path=os.path.join(os.getcwd(),"To_Wavs")
    des_path=os.path.join(os.getcwd(),"To_Wavs")
    files = os.listdir(audio_path)
    # Filter for .mp3 files
    wav_files = [file for file in files if file.endswith('.wav')]
    # Sort the files if needed (optional)
    wav_files=sorted(wav_files,key=sort_key)
    # Initialize an empty AudioSegment
    full_audio = AudioSegment.silent(500)
    # Process and concatenate each .mp3 file
    for wav_file in wav_files:
        file_path = os.path.join(audio_path, wav_file)
        audio = AudioSegment.from_wav(file_path)
        # Concatenate the audio file & add delay 1s in between each audio
        full_audio += audio + AudioSegment.silent(500)
        print("Successfully combine an audio" + wav_file)
    # Export the concatenated audio to a new file
    output_path=os.path.join(des_path,"full_audio.wav")
    full_audio.export(output_path, format='wav')
    print("Successfully combine all audio" + des_path+"\\"+"full_audio.wav")

def getDuration():
    des_path=os.path.join(os.getcwd(),"To_Wavs")
    files = os.listdir(des_path)
    # Filter for .mp3 files
    wav_files = [file for file in files if file.endswith('.wav')]
    # Sort the files if needed (optional)
    wav_files=sorted(wav_files,key=sort_key)
    duration=[]
    for wav_file in wav_files:
        file_path = os.path.join(des_path, wav_file)
        audio = AudioSegment.from_wav(file_path)
        duration.append((audio.duration_seconds)+0.5)
    return duration

def getImg (my_path):
    file_path = os.path.abspath(my_path)
    des_path = os.path.join(os.getcwd(),"To_Pngs")
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    powerpoint = client.CreateObject('Powerpoint.Application')
    presentation=powerpoint.Presentations.Open(file_path)
    slides_count = presentation.Slides.Count
    for i in range(1, slides_count + 1):
        slide = presentation.Slides(i)
        slide.Export(os.path.join(des_path, f"{i}.png"), "PNG")
    powerpoint.ActivePresentation.Close()
    powerpoint.Quit()
getImg (mypath)

def getClip():
    folder_path = os.path.join(os.getcwd(),"To_Pngs")
    # Define the durations for each image clip (in seconds)
    des_path=os.path.join(os.getcwd(), "To_Mp4")
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    durations = getDuration()  # Example durations for three images
    # List all files in the folder
    files = os.listdir(folder_path)
    # Filter for image files (assuming .jpg files, you can adjust this as needed)
    image_files = [file for file in files if file.endswith('.png')]
    # Sort the image files if needed (optional)
    image_files=sorted(image_files,key=sort_key)
    # Check if the number of durations matches the number of image files
    if len(durations) != len(image_files):
        raise ValueError("The number of durations must match the number of image files")
    # Create video clips from each image with the specified durations
    clips = []
    for image_file, duration in zip(image_files, durations):
        file_path = os.path.join(folder_path, image_file)
        clip = ImageClip(file_path).set_duration(duration)
        clips.append(clip)
    # Concatenate the clips
    temp_clip = concatenate_videoclips(clips)
    # Define the output video file path
    output_path = os.path.join(des_path,"temp.mp4")
    # Export the final video
    temp_clip.write_videofile(output_path, codec='libx264', fps=1)

def video_wsound():
    video_path = os.path.join(os.getcwd(), "To_Mp4", "temp.mp4")
    audio_path = os.path.join(os.getcwd(), "To_Wavs", "full_audio.wav")
    output_path = os.path.join(os.getcwd(), "presentation_AIvoice.mp4")

    # Load the video file
    video_clip = VideoFileClip(video_path)

    # Load the audio file
    audio_clip = AudioFileClip(audio_path)

    # Set the audio of the video clip to the loaded audio
    final_clip = video_clip.set_audio(audio_clip)

    # Export the final video with the new audio
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    print("Successfully created a video at "+ output_path)

def clearUp():
    try:
        shutil.rmtree(os.path.join(os.getcwd(), "To_Mp4"))
        shutil.rmtree(os.path.join(os.getcwd(), "To_Wavs"))
        shutil.rmtree(os.path.join(os.getcwd(), "To_Pngs"))
        print("Successfully delete all redundant files")
    except:
        pass

def main():
        #make sure remove all unnecessary folder and file before create new video.
        clearUp()
        #create images from pptx
        getImg(mypath) 
        #create mp3 files from speaker note
        getWav(mypath)
        #generate clip (mp4)
        getClip()
        #combine all mp3 files 
        combineAudio()
        #combine the mp3 and mp4 file
        video_wsound()
        #make sure remove all unnecessary folder
        clearUp()
if (__name__=="__main__"):
    main()