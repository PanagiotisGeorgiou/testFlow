import os
import utils
#from pytube import YouTube
import yt_dlp
from moviepy.editor import AudioFileClip
import whisper


def download_youtube_video(url, output_path):
    ydl_opts = {'format': 'bestaudio', 'outtmpl': output_path}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_audio(video_path, audio_path='extracted_audio.mp3'):
    clip = AudioFileClip(video_path)
    clip.write_audiofile(audio_path)
    clip.close()
    return audio_path

def transcribe_audio_to_text(audio_path, model_size='small'):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result['text']

def save_text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)
    print("Transcription saved to {}".format(filename))

def main():
    url = input("Enter YouTube URL: ")
    video_id = next(iter({utils.extract_video_id(url)}))
    video_path = f"{video_id}_video.mp4"
    audio_path = f"{video_id}_extracted_audio.mp3"
    
    # Step 1: Download the video
    if not os.path.exists(video_path):
        print("Downloading video...")
        download_youtube_video(url, video_path)
    
    # Step 2: Extract audio
    print("Extracting audio...")
    extract_audio(video_path, audio_path)
    
    # Step 3: Transcribe audio to text
    print("Transcribing audio...")
    transcription = transcribe_audio_to_text(audio_path)
    
    # Step 4: Save the text to a file
    save_text_to_file(transcription, f"{video_id}_transcription.txt")

if __name__ == "__main__":
    main()

