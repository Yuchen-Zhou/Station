from moviepy.editor import VideoFileClip

def convert_avi_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)

    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


input = '/root/autodl-tmp/Station/media/videos/1.avi'
output = '/root/autodl-tmp/Station/media/videos/1.mp4'
convert_avi_to_mp4(input, output)