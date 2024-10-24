import subprocess
def embeded_cc():
        video_folder = r"C:\Users\tuant\OneDrive\Documents\GitHub\PresentoAI2\media\b9a8a38cd9334e649a29ee3ea81becc2\sample\temp"
        output_folder=r"C:\Users\tuant\OneDrive\Documents\GitHub\PresentoAI2\media\b9a8a38cd9334e649a29ee3ea81becc2\sample\output"
        video_path = r"C:\Users\tuant\OneDrive\Documents\GitHub\PresentoAI2\media\b9a8a38cd9334e649a29ee3ea81becc2\sample\temp\b9a8a38cd9334e649a29ee3ea81becc2.mp4"
        subtitle_path=r"C:\Users\tuant\OneDrive\Documents\GitHub\PresentoAI2\media\b9a8a38cd9334e649a29ee3ea81becc2\sample\output\sub-presetation.en.srt"
        output_path=r"C:\Users\tuant\OneDrive\Documents\GitHub\PresentoAI2\media\b9a8a38cd9334e649a29ee3ea81becc2\sample\output\b9a8a38cd9334e649a29ee3ea81becc2.mp4"
        try:
        # Construct the ffmpeg command to embed the soft subtitle
            command = [
                'ffmpeg',
                '-i', video_path,  # Input video
                '-i', subtitle_path,  # Input subtitle
                '-c', 'copy',  # Copy video and audio without re-encoding
                '-c:s', 'mov_text',  # Codec for subtitles (mov_text for MP4 container)
                output_path
            ]
            # Execute the command using subprocess
            subprocess.run(command, check=True)
            print(f"Subtitle embedded successfully! Output saved to: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print("Failed to embed subtitle into video.")

embeded_cc()