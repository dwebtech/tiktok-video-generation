from typing import Dict, List
from moviepy.editor import VideoClip, VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, AudioClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from faster_whisper import WhisperModel


def create_subtitles_for_video(input_video: VideoClip) -> List[Dict[str, str]]:
    """Create subtitles for a given video."""
    audio: AudioClip = input_video.audio
    audio = audio.to_soundarray()  # Convert audio to a readable format
    model: WhisperModel = WhisperModel("small")
    segments, _ = model.transcribe(audio, language='en')
    subtitles: List[Dict[str, str]] = [{'text': segment.text, 'start': segment.start, 'end': segment.end} for segment in list(segments)]
    return subtitles

def add_subtitles(input_video: VideoClip, subtitles: List[Dict[str, str]]):
    """Add subtitles to a given video."""
    # Load the video clip
    video_width, video_height = input_video.size
    
    # Create TextClips for each subtitle
    subtitle_clips: List[TextClip] = []
    for subtitle in subtitles:
        text_clip = TextClip(subtitle['text'], fontsize=75, color='white', bg_color='black', size=(video_width*.75, None), method='caption')
        text_clip = text_clip.set_position(('center', video_height*(4/5))).set_start(subtitle['start']).set_end(subtitle['end'])
        subtitle_clips.append(text_clip)
    
    # Composite the video with the subtitles
    final_video = CompositeVideoClip([input_video] + subtitle_clips)
    return final_video

def merge_videos(input_videos: List[VideoClip]) -> VideoClip:
    """Merge multiple videos into one applying blurry transition."""
    # Apply a blurry transition between videos
    crossfade_duration = 0.3
    clips: List[VideoClip] = []
    for i, video_path in enumerate(input_videos):
        video_clip = video_path

        first_video = i == 0
        last_video = i == len(input_videos)
        if first_video or last_video:
            clips.append(video_clip)
        else:
            clips.append(video_clip.crossfadein(crossfade_duration))

    final = concatenate_videoclips(clips, 
            padding=-crossfade_duration, 
            method="compose")
    return final

def merge_videos_and_add_subtitles(input_videos: List[VideoClip]) -> VideoClip:
    """Merge multiple videos into one and add subtitles."""
    videos_to_merge: List[VideoClip] = []
    ## DEBUG
    videos_to_merge = input_videos
    merged_video = merge_videos(videos_to_merge)
    return merged_video
    ## TO REMOVE

    for input_video in input_videos:
        subtitles: List[Dict[str, str]] = create_subtitles_for_video(input_video)
        videos_to_merge.append(add_subtitles(input_video, subtitles))
    merged_video = merge_videos(videos_to_merge)
    return merged_video

if __name__ == "__main__":
    # Example usage
    video1 = VideoFileClip("./../video.mp4")
    video2 = VideoFileClip("./../video.mp4")
    video3 = VideoFileClip("./../video.mp4")
    audio = AudioFileClip("./../speech.mp3")
    video1 = video1.set_audio(audio)
    video2 = video2.set_audio(audio)
    video1 = video1.subclip(0, 3)
    video2 = video2.subclip(0, 3)
    video3 = video3.subclip(0, 3)
    merged_video = merge_videos_and_add_subtitles([video1, video2, video3])
    merged_video.write_videofile("./../merged_video.mp4")