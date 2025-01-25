import fastapi
from fastapi import FastAPI,APIRouter
import llmpredict
from llmpredict import imagepredictmodel
from pydantic import BaseModel
import cv2
import base64
import numpy as np

router=APIRouter(
    preifix='/video',
    tags=['video']
)
def process_video(video_path):
 
    # Open video file using OpenCV
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Couldn't open video.")
        return []
    
    frame_base64_list = []
    
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        if not ret:
            break  # No more frames to read
        
        # Convert the frame to JPEG format (other formats can be used)
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Convert the buffer to bytes
        frame_bytes = buffer.tobytes()
        
        # Encode the frame to base64
        frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')
        
        # Append the base64 string of the frame to the list
        frame_base64_list.append(frame_base64)
    
    cap.release()  # Close the video file
    return frame_base64_list

class video (BaseModel):
    video_name:str
@router.get('/videosummary')
def video(query:video):
    video_name=query ["video_name"]
    base64Frames=process_video(video_name)
    #print(base64Frames)
    llm=imagepredictmodel()
    response = llm.invoke(
    [
    {"role": "system", "content": "You are generating a video summary. Please provide a summary of the video. Respond in Markdown."},
      {"role": "user", "content": [
    {"type":"text", "text": "These are the frames from the video."},
    *map(lambda x: {"type": "image_url",
                    "image_url":{"url":f'data:image/jpg;base64,{x}',"detail":"low"}},base64Frames)
    ],
    }
    ],
    temperature=0,)
    print(response.content)
    return response.content

