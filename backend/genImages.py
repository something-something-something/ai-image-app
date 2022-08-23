from importlib.metadata import metadata
import os
import posixpath
import json
from datetime import date,timezone,datetime
from diffusers import DiffusionPipeline,StableDiffusionPipeline,LMSDiscreteScheduler
from PIL import Image
from torch import autocast
import torch

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
			'scale':scale,
			'model':'latent-diffusion:CompVis/ldm-text2im-large-256'
		}
	}


def genStableDiffusion(prompt='default prompt', num_inference_steps=50,eta=0.0,seed=100,guidance_scale=7.5,height=512,width=512,num_samples=4):

	lms=LMSDiscreteScheduler(
		beta_start=0.000085,
		beta_end=0.012,
		beta_schedule="scaled_linear"
	)

	model=StableDiffusionPipeline.from_pretrained(
		"models/stable-diffusion-v1-4",
	 	local_files_only=True,
		scheduler=lms
	).to("cuda")

	generatorSeed=torch.Generator("cuda").manual_seed(seed)
	
	with autocast("cuda"):
		images=model(prompt=[prompt]*num_samples, num_inference_steps= num_inference_steps,eta=eta,guidance_scale=guidance_scale,height=height,width=width,  generator=generatorSeed)["sample"]
	print(images)
	return {
		'images':images,
		'metadata':{
			'prompt':prompt,
			'num_inference_steps':num_inference_steps,
			'eta':eta,
			'height':height,
			'width':width,
			'num_samples':num_samples,
			'guidance_scale':guidance_scale,
			'seed':seed,
			'model':'stable-diffusion:CompVis/stable-diffusion-v1-4',
			'scheduler':{
				'type':'LMSDiscreteScheduler',
				'beta_start':0.000085,
				'beta_end':0.012,
				'beta_schedule':"scaled_linear"
			}
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




