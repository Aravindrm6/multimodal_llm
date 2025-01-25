import fastapi
from fastapi import FastAPI,APIRouter
import llmpredict
from llmpredict import imagepredictmodel
from pydantic import BaseModel

router=APIRouter(
    preifix='/image',
    tags=['image']
)

class image (BaseModel):
    image:str
@router.get('/imagesummary')
def summarize_with_openai_image (input: image):
    input-input.model_dump(mode='json')
    img_base64=input['image']
    #img_base64 = convert_image_to_base64(image_path)
    llm = imagepredictmodel()
    
    prompt=f"Summarize the content of this image in 50 words:"
    response = llm.invoke([
    {"role": "system", "content": "You are a helpful Assistant."}, 
    {"role": "user", "content": f"""Please summarize the following image. The image is provided below:
    ![Image] (data:image/jpeg;base64, {img_base64})
    {prompt}"""}],
    temperature=0)

    print(response.content)
    return response.content