import os
import ffmpeg
from tkinter import Tk, filedialog, messagebox

def check_audio_channels(file):
    probe = ffmpeg.probe(file, select_streams='a')
    channels = probe['streams'][0]['channels']
    return channels == 12

def process_audio(file, output_folder):
    output_file = os.path.join(output_folder, os.path.basename(file))
    
    # FFMPEG command to map channels and add metadata
    ffmpeg.input(file).output(output_file, 
        filter_complex="[0:a]pan=12c|c0=c0|c1=c1|c2=c2|c3=c3|c4=c4|c5=c5|c6=c6|c7=c7|c8=c8|c9=c9|c10=c10|c11=c11",
        metadata="s:a:0 channel_layout=7.1.4(side)"
    ).run()

def main():
    root = Tk()
    root.withdraw()

    # Get the input folder
    input_folder = filedialog.askdirectory(title="Select Input Folder containing WAV files")
    if not input_folder:
        return

    # Get the output folder
    output_folder = filedialog.askdirectory(title="Select Output Folder for processed files")
    if not output_folder:
        return

    # Process each file
    for file in os.listdir(input_folder):
        if file.endswith('.wav'):
            full_path = os.path.join(input_folder, file)
            
            # Check if the file is 7.1.4
            if not check_audio_channels(full_path):
                messagebox.showerror("Error", f"The file {file} is not 7.1.4")
                return

            # Process the audio
            process_audio(full_path, output_folder)

    messagebox.showinfo("Success", "All files processed successfully!")

if __name__ == "__main__":
    main()