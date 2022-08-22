import os
import posixpath
import json
from datetime import date,timezone,datetime
from diffusers import DiffusionPipeline
from PIL import Image


def genLatentDiffusion(prompt='default prompt',dimmSteps=200,dimmEta=0.0,numIter=1,height=256,width=256,numSamples=4,scale=5.0):

	model=DiffusionPipeline.from_pretrained("CompVis/ldm-text2im-large-256")

	images=model(prompt=[prompt]*numSamples,height=height,width=width, guidance_scale=scale,eta=dimmEta,num_inference_steps=dimmSteps)["sample"]
	
	return {
		"images":images,
		"metadata":{
			'prompt':prompt,
			'dimmSteps':dimmSteps,
			'dimmEta':dimmEta,
			'numIter':numIter,
			'height':height,
			'width':width,
			'numSamples':numSamples,
			'scale':scale
		}
	}



def imageDirPath():
	return posixpath.join('static','generated','images',date.today().isoformat())


def saveImages(obj,algoName,baseImageDir):
	directoryPath=posixpath.join(baseImageDir,algoName)
	os.makedirs(directoryPath,exist_ok=True)
	totalImgInDir=len(os.listdir(directoryPath))

	exifdata=Image.Exif()
	exifdata[37510]=bytes.fromhex('00 00 00 00 00 00 00 00')+json.dumps(obj["metadata"]).encode(encoding='utf-8')

	imgPaths=[]
	imgnum=totalImgInDir+1
	for img in obj["images"]:
		imgpath=posixpath.join(directoryPath,algoName+"-"+str(datetime.now(tz=timezone.utc).timestamp())+"-imageNumber-"+str(imgnum)+".png")
		img.save(imgpath,exif=exifdata)
		imgPaths.append(imgpath)
		imgnum+=1
	return imgPaths




