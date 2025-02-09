import pandas as pd
from glob import glob

def load_subtitles_dataset(dataset_path):
    # Get all .ass files in the dataset path
    subtitles_paths = glob(dataset_path + '/*.ass')

    scripts = []
    episode_num = []

    for path in subtitles_paths:
        try:
            # Read lines from the current file
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines = lines[27:]  # Skip the first 27 lines (metadata/headers)

                # Process each line: split by comma, rejoin from index 9 onward
                lines = [",".join(line.strip().split(',')[9:]) for line in lines]

            # Replace newline markers and join lines into a single script
            lines = [line.replace('\\N', ' ') for line in lines]
            script = " ".join(lines)
            scripts.append(script)

            # Extract episode number from the filename
            episode = int(path.split('-')[-1].split('.')[0].strip())
            episode_num.append(episode)
        except Exception as e:
            print(f"Error processing file {path}: {e}")
            continue

    # Create a DataFrame from the collected data
    df = pd.DataFrame.from_dict({"episode": episode_num, "script": scripts})
    return df