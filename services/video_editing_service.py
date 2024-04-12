from typing import Dict, List
from moviepy.editor import VideoClip, concatenate_videoclips, CompositeVideoClip, TextClip, AudioClip
from moviepy.video.tools.subtitles import SubtitlesClip
from faster_whisper import WhisperModel
from moviepy.video import fx as vfx


def create_subtitles_for_video(input_video: VideoClip) -> List[Dict[str, str]]:
    """Create subtitles for a given video."""
    audio: AudioClip = input_video.audio
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
    blurred_videos = []
    for i, video in enumerate(input_videos):
        if i > 0:
            transition_duration = min(0.3, input_videos[i-1].duration, video.duration)
            # Apply the blurry transition to the current video
            blurred_video = video.fx(vfx.blur, ksize=10).crossfadein(transition_duration)
            blurred_videos.append(blurred_video)
        else:
            blurred_videos.append(video)

    # Concatenate the blurred videos
    blurred_final_video = concatenate_videoclips(blurred_videos)
    return blurred_final_video

def merge_videos_and_add_subtitles(input_videos: List[VideoClip]) -> VideoClip:
    """Merge multiple videos into one and add subtitles."""
    videos_to_merge: List[VideoClip] = []
    for input_video in input_videos:
        subtitles: List[Dict[str, str]] = create_subtitles_for_video(input_video)
        videos_to_merge.append(add_subtitles(input_video, subtitles))
    merged_video = merge_videos(videos_to_merge)
    return merged_video