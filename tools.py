from moviepy.editor import VideoFileClip

def convert_avi_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

convert_avi_to_mp4('back/static/video/track.avi', 'back/static/video/track.mp4')