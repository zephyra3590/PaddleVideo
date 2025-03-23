import os
import sys
import json
sys.path.append('action_detect')
from action import ActionDetection
import argparse

if __name__ == '__main__':
    # Create argument parser
    parser = argparse.ArgumentParser(description='Process video for action detection')
    parser.add_argument('filename', nargs='?', default=None, help='Optional: specific file to process')
    args = parser.parse_args()
    
    dataset_dir = "~/datasets/EuroCup2016"
    
    model_predict = ActionDetection(cfg_file="./configs/configs.yaml")
    model_predict.load_model()
    
    results = []
    
    # If a filename is provided, process only that file
    if args.filename:
        video_name = args.filename
        if not os.path.isabs(video_name):
            video_name = os.path.join(dataset_dir, video_name)
        
        print(f"Processing single file: {video_name}")
        imgs_path = video_name.replace(".mp4", "").replace("mp4", "frames")
        pcm_path = video_name.replace(".mp4", ".pcm").replace("mp4", "pcm")
        bmn_results, action_results = model_predict.infer(imgs_path, pcm_path)
        result = {'video_name': video_name,
                  'bmn_results': bmn_results, 
                  'action_results': action_results}
        
        # Save the result to the same directory as the input file
        result_path = video_name.replace(".mp4", ".json")
        with open(result_path, 'w', encoding='utf-8') as f:
            data = json.dumps(result, indent=4, ensure_ascii=False)
            f.write(data)
        print(f"Results saved to: {result_path}")
        
        # Also add to the overall results
        results.append(result)
    # Otherwise, process all files in the list as before
    else:
        video_url = os.path.join(dataset_dir, 'url_val.list')
        with open(video_url, 'r') as f:
            lines = f.readlines()
        lines = [os.path.join(dataset_dir, k.strip()) for k in lines]
        
        for line in lines:
            video_name = line
            print(video_name)
            imgs_path = video_name.replace(".mp4", "").replace("mp4", "frames")
            pcm_path = video_name.replace(".mp4", ".pcm").replace("mp4", "pcm")
            bmn_results, action_results = model_predict.infer(imgs_path, pcm_path)
            result = {'video_name': line,
                      'bmn_results': bmn_results, 
                      'action_results': action_results}
            results.append(result)
            
            # Save individual result file
            result_path = video_name.replace(".mp4", ".json")
            with open(result_path, 'w', encoding='utf-8') as f:
                data = json.dumps(result, indent=4, ensure_ascii=False)
                f.write(data)
            print(f"Results saved to: {result_path}")
    
    # Still save the overall results.json file
    with open('results.json', 'w', encoding='utf-8') as f:
        data = json.dumps(results, indent=4, ensure_ascii=False)
        f.write(data)