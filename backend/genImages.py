from importlib.metadata import metadata
import os
import posixpath
import json
from datetime import date,timezone,datetime
from diffusers import DiffusionPipeline,StableDiffusionPipeline,LMSDiscreteScheduler,StableDiffusionImg2ImgPipeline,DPMSolverMultistepScheduler
from PIL import Image
from torch import autocast
import torch


def genLatentDiffusion(prompt='default prompt',dimmSteps=200,dimmEta=0.0,numIter=1,height=256,width=256,numSamples=4,scale=5.0):

	model=DiffusionPipeline.from_pretrained("CompVis/ldm-text2im-large-256")

	images=model(prompt=[prompt]*numSamples,height=height,width=width, guidance_scale=scale,eta=dimmEta,num_inference_steps=dimmSteps).images
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


def genStableDiffusion(prompt='default prompt', num_inference_steps=50,eta=0.0,seed=100,guidance_scale=7.5,height=512,width=512,num_samples=4,enable_safety_checker=True):

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
	if not enable_safety_checker:
		model.safety_checker=blah
	
	with autocast("cuda"):
		images=model(prompt=[prompt]*num_samples, num_inference_steps= num_inference_steps,eta=eta,guidance_scale=guidance_scale,height=height,width=width,  generator=generatorSeed).images
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


def genStableDiffusion_2_1_768(negative_prompt='',prompt='default prompt', num_inference_steps=50,eta=0.0,seed=100,guidance_scale=7.5,height=768,width=768,num_samples=4,enable_safety_checker=True):

	# kdpm2=EulerAncestralDiscreteScheduler(
	# 	num_train_timesteps=1000,
	# 	beta_start=0.0001,
	# 	beta_end=0.02,
	# 	beta_schedule="linear",
	# 	prediction_type='epsilon'
	# )
	# lms=LMSDiscreteScheduler(
	# 	beta_start=0.000085,
	# 	beta_end=0.012,
	# 	beta_schedule="scaled_linear"
	# )

	model=StableDiffusionPipeline.from_pretrained(
		"models/stable-diffusion-2-1",
	 	local_files_only=True,
		torch_dtype=torch.float16
	)
	model.scheduler = DPMSolverMultistepScheduler.from_config(model.scheduler.config)
	model = model.to("cuda")

	generatorSeed=torch.Generator("cuda").manual_seed(seed)
	
	images = model(prompt=prompt, negative_prompt=negative_prompt, num_images_per_prompt=num_samples, num_inference_steps= num_inference_steps, eta=eta, guidance_scale=guidance_scale, height=height, width=width,   generator=generatorSeed).images

	return {
		'images':images,
		'metadata':{
			'prompt':prompt,
			'negative_prompt':negative_prompt,
			'num_inference_steps':num_inference_steps,
			'eta':eta,
			'height':height,
			'width':width,
			'num_samples':num_samples,
			'guidance_scale':guidance_scale,
			'seed':seed,
			'model':'stable-diffusion2.1:stabilityai/stable-diffusion-2-1',
			'scheduler':{
				'type':'DPMSolverMultistepScheduler',
			}
		}
	}






def genStableDiffusionImgToImg(prompt='default prompt', num_inference_steps=50,eta=0.0,seed=100,guidance_scale=7.5,height=512,width=512,num_samples=4,enable_safety_checker=True,image=Image.new("RGB",(512,512)),strength=0.8):
	img=image.resize((width,height))
	# lms=LMSDiscreteScheduler(
	# 	beta_start=0.000085,
	# 	beta_end=0.012,
	# 	beta_schedule="scaled_linear"
	# )

	model=StableDiffusionImg2ImgPipeline.from_pretrained(
		"models/stable-diffusion-v1-4",
	 	local_files_only=True
		#scheduler=lms
	).to("cuda")

	generatorSeed=torch.Generator("cuda").manual_seed(seed)
	if not enable_safety_checker:
		model.safety_checker=blah
	
	with autocast("cuda"):
		images=model(prompt=[prompt]*num_samples, image=[img]*num_samples, num_inference_steps= num_inference_steps,eta=eta,guidance_scale=guidance_scale,  generator=generatorSeed,strength=strength).images
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
			'strength':strength,
			'model':'stable-diffusion-img2img:CompVis/stable-diffusion-v1-4',
			'scheduler':{
				'type':'default'
			}
		}
	}


def pathToGenerated():
	return posixpath.join('generated','images',date.today().isoformat())

def imageDirTempPath(tempdir):
	return posixpath.join(tempdir,pathToGenerated())

def imageDirTempUrlPath():
	return posixpath.join('tempstatic',pathToGenerated())

def imageDirPath():
	return posixpath.join('static',pathToGenerated())


def saveImages(obj,algoName,baseImageDir,urlPath=None):
	directoryPath=posixpath.join(baseImageDir,algoName)
	os.makedirs(directoryPath,exist_ok=True)
	totalImgInDir=len(os.listdir(directoryPath))

	exifdata=Image.Exif()
	exifdata[37510]=bytes.fromhex('00 00 00 00 00 00 00 00')+json.dumps(obj["metadata"]).encode(encoding='utf-8')

	imgPaths=[]
	imgnum=totalImgInDir+1
	for img in obj["images"]:
		filename=algoName+"-"+str(datetime.now(tz=timezone.utc).timestamp())+"-imageNumber-"+str(imgnum)+".png"
		savepath=directoryPath
		imgsavepath=posixpath.join(savepath,filename)
		img.save(imgsavepath,exif=exifdata)

		if urlPath is None:
			imgPaths.append(imgsavepath)
		else:
			imgPaths.append(posixpath.join(urlPath,algoName,filename))
		imgnum+=1
	return imgPaths


def blah(images,clip_input):
	print('blah')
	has_nsfw_concepts=[]
	return images, has_nsfw_concepts


