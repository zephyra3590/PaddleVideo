"""
get frames and pcm from video
"""
import os
import sys
from concurrent import futures
import argparse

def extract_frames(video_name, out_folder, fps=5):
    if os.path.exists(out_folder):
        os.system('rm -rf ' + out_folder + '/*')
        os.system('rm -rf ' + out_folder)
    os.makedirs(out_folder)
    cmd = 'ffmpeg -v 0 -i %s -r %d -q 0 %s/%s.jpg' % (video_name, fps,
                                                     out_folder, '%08d')
    os.system(cmd)

def extract_pcm(video_name, file_name_pcm):
    cmd = 'ffmpeg -y -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s -v 0' % (
        video_name, file_name_pcm)
    os.system(cmd)

def process(line, dataset, dst_frames, dst_pcm):
    print(line)
    mp4_name = os.path.join(dataset, line)
    basename = os.path.basename(line).split('.')[0]
    folder_frame = os.path.join(dst_frames, basename)
    filename_pcm = os.path.join(dst_pcm, basename + '.pcm')
    # extract
    extract_frames(mp4_name, folder_frame)
    extract_pcm(mp4_name, filename_pcm)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract frames and PCM from video files')
    parser.add_argument('filename', nargs='?', help='Optional: specific file to process')
    args = parser.parse_args()
    
    # Use the correct path with expanduser to handle the tilde
    dataset = os.path.expanduser("~/datasets/EuroCup2016")
    dst_frames = os.path.join(dataset, 'frames')
    dst_pcm = os.path.join(dataset, 'pcm')
    
    if not os.path.exists(dst_frames):
        os.mkdir(dst_frames)
    if not os.path.exists(dst_pcm):
        os.mkdir(dst_pcm)
    
    # If a filename is provided, process only that file
    if args.filename:
        file_path = os.path.join(dataset, args.filename)
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            sys.exit(1)
        process(args.filename, dataset, dst_frames, dst_pcm)
    # Otherwise, process all files in the list as before
    else:
        url_list = os.path.join(dataset, 'url.list')
        with open(url_list, 'r') as f:
            lines = f.readlines()
        lines = [k.strip() for k in lines]
        # multi thread
        with futures.ProcessPoolExecutor(max_workers=10) as executer:
            fs = [executer.submit(process, line, dataset, dst_frames, dst_pcm) for line in lines]
        #for line in lines:
        #    process(line, dataset, dst_frames, dst_pcm)
    
    print("done")