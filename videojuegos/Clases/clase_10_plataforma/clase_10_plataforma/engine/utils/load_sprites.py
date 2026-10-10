import json

def load_piskel_animation(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    frames = []
    for frame_name, frame_data in data['frames'].items():
        rect = frame_data['frame']
        frames.append((rect['x'], rect['y'], rect['w'], rect['h']))
    return frames, data['meta']['image']