from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import os
import time
import math
from faster_whisper import WhisperModel

def create_subtitles(input_video):
    # create a video object and extract the audio
    video_clip = VideoFileClip(input_video)
    extracted_audio = f"audio-output.wav"
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(extracted_audio)
    # create a whisper model to use AI to detect the words being said
    model = WhisperModel("small")
    segments, info = model.transcribe(extracted_audio, language='en')
    segments = list(segments)
    subtitles = []
    # place the subtitles 
    for segment in segments:
        subtitles.append({'text': segment.text, 'start': segment.start, 'end': segment.end})
    return subtitles

def add_subtitles(input_video, subtitles):
    # Load the video clip
    video_clip = VideoFileClip(input_video)
    video_width, video_height = video_clip.size
    
    # Create TextClips for each subtitle
    subtitle_clips = []
    for subtitle in subtitles:
        text_clip = TextClip(subtitle['text'], fontsize=75, color='white', bg_color='black', size=(video_width*.75, None), method='caption')
        text_clip = text_clip.set_position(('center', video_height*(4/5))).set_start(subtitle['start']).set_end(subtitle['end'])
        subtitle_clips.append(text_clip)
    
    # Composite the video with the subtitles
    final_video = CompositeVideoClip([video_clip] + subtitle_clips)
    # Write the final video to a file
    final_video.write_videofile('output_video_with_subtitles.mp4')

def run(input_video):
    # Open the video and audio
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("speech.mp3")
    
    # Concatenate the video clip with the audio clip
    final_input_clip = video_clip.set_audio(audio_clip)
    
    # Export the final video with audio
    final_input_clip.write_videofile("output3.mp4")
    input_video = "output3.mp4"
    subtitles = create_subtitles(input_video)
    output_video = add_subtitles(input_video, subtitles)
