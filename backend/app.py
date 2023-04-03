import tempfile
from flask import Flask,Blueprint
from webargs import fields
from webargs.flaskparser import use_args
import genImages
from PIL import Image
import urllib.request

app=Flask(__name__)

tempDirForGenerated=tempfile.mkdtemp(prefix='ai-image-app')

print('tempdir= '+tempDirForGenerated)

tempDirBlueprint=Blueprint('tempfiles',__name__,static_folder=tempDirForGenerated,static_url_path='/tempstatic' )
app.register_blueprint(tempDirBlueprint)


# TODO Figure out where to set these globally
optionsPrefilghtResponseHeaders={
	'Access-Control-Allow-Origin':'http://localhost:3000',
	'Access-Control-Allow-Methods':'POST,GET,OPTIONS',
	'Access-Control-Max-Age':2,
	'Access-Control-Allow-Headers':'Content-Type'
}

defaultHeaders={
		'Access-Control-Allow-Origin':'http://localhost:3000',
		'Access-Control-Allow-Methods':'POST,GET,OPTIONS'
}

@app.route("/latentDiffusion/genimage",methods=["OPTIONS"])
def genLatentDiffusionImagesPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders

@app.route("/latentDiffusion/genimage",methods=["POST"])
@use_args({"prompt":fields.Str(required=True),"scale":fields.Float(),"width":fields.Integer(),"height":fields.Integer(),"numSamples":fields.Integer()})
def genLatentDiffusionImages(args):

	images=genImages.saveImages(genImages.genLatentDiffusion(prompt=args["prompt"], width=args["width"], height=args["height"], scale=args["scale"],numSamples=args["numSamples"]),"latent-diffusion",genImages.imageDirPath())
	
	return {
		"prompt":args["prompt"],
		"files":images
	},defaultHeaders

@app.route("/latentDiffusion/getFormFields",methods=["OPTIONS"])
def getLatentDiffusionFormDataPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders


@app.route("/latentDiffusion/getFormFields",methods=["POST"])
def getLatentDiffusionFormData():
	
	return {
		"formFieldsData":[
			{
				"name":'prompt',
				"displayName":"Prompt",
				"defaultValue":"a painting of an ai",
				"type":"textbox"

			},
			{
				"name":'width',
				"displayName":"Width",
				"defaultValue":"256"
			},
			{
				"name":'height',
				"displayName":"height",
				"defaultValue":"256"
			},
			{
				"name":'scale',
				"displayName":"scale",
				"defaultValue":"8"
			},
			{
				"name":'numSamples',
				"displayName":"Number of pictures",
				"defaultValue":"6"
			}
		]
	},defaultHeaders




@app.route("/stableDiffusion/genimage",methods=["OPTIONS"])
def genStableDiffusionImagesPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders

@app.route("/stableDiffusion/genimage",methods=["POST"])
@use_args({"prompt":fields.Str(required=True),"guidance_scale":fields.Float(),"width":fields.Integer(),"height":fields.Integer(),"num_samples":fields.Integer(),"seed":fields.Integer(),"eta":fields.Float(),"num_inference_steps":fields.Integer(),"enable_safety_checker":fields.Boolean(truthy=['on'],falsy=['off']),"use_temp_dir":fields.Boolean(truthy=['on'],falsy=['off'])})
def genStableDiffusionImages(args):
	print('gen stablediff')

	
	dirToWriteImage=genImages.imageDirPath()
	urlPathForImages=None

	if args["use_temp_dir"]:
		dirToWriteImage=genImages.imageDirTempPath(tempDirForGenerated)
		urlPathForImages=genImages.imageDirTempUrlPath()

	images=genImages.saveImages(genImages.genStableDiffusion(prompt=args["prompt"], width=args["width"], height=args["height"], guidance_scale=args["guidance_scale"],num_samples=args["num_samples"],seed=args["seed"],num_inference_steps=args["num_inference_steps"],enable_safety_checker=args["enable_safety_checker"]),"stable-diffusion",dirToWriteImage,urlPath=urlPathForImages)
	
	return {
		"prompt":args["prompt"],
		"files":images
	},defaultHeaders

@app.route("/stableDiffusion/getFormFields",methods=["OPTIONS"])
def getStableDiffusionFormDataPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders


@app.route("/stableDiffusion/getFormFields",methods=["POST"])
def getStableDiffusionFormData():
	
	return {
		"formFieldsData":[
			{
				"name":'prompt',
				"displayName":"Prompt",
				"defaultValue":"a painting of an ai",
				"type":"textbox"

			},
			{
				"name":'width',
				"displayName":"Width",
				"defaultValue":"512"
			},
			{
				"name":'height',
				"displayName":"height",
				"defaultValue":"512"
			},
			{
				"name":'guidance_scale',
				"displayName":"guidance_scale",
				"defaultValue":"7.5"
			},
			{
				"name":'num_samples',
				"displayName":"Number of pictures",
				"defaultValue":"6"
			},
			{
				"name":'num_inference_steps',
				"displayName":"Number Inference Steps",
				"defaultValue":"50"
			},
			{
				"name":'eta',
				"displayName":"eta",
				"defaultValue":"0.0"
			},
			{
				"name":'seed',
				"displayName":"seed",
				"defaultValue":"100"
			},
			{
				"name":'enable_safety_checker',
				"displayName":"saftey checker",
				"defaultValue":"on",
				"type":"radio",
				'possibleValues':[
					{
						'value':'on',
						'displayName':'Enable Saftey Checker'
					},
					{
						'value':'off',
						'displayName':'Disable Saftey Checker'
					}
					
				]
			},
			{
				"name":'use_temp_dir',
				"displayName":"use temp dir",
				"defaultValue":"off",
				"type":"radio",
				'possibleValues':[
					{
						'value':'on',
						'displayName':'save to temp dir '+tempDirForGenerated
					},
					{
						'value':'off',
						'displayName':'Save to backend/static'
					}
					
				]
			}

		]
	},defaultHeaders

@app.route("/stableDiffusion2-1-768/genimage",methods=["OPTIONS"])
def genStableDiffusion_2_1_768_ImagesPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders

@app.route("/stableDiffusion2-1-768/genimage",methods=["POST"])
@use_args({"prompt":fields.Str(required=True),"negative_prompt":fields.Str(required=True),"guidance_scale":fields.Float(),"width":fields.Integer(),"height":fields.Integer(),"num_samples":fields.Integer(),"seed":fields.Integer(),"eta":fields.Float(),"num_inference_steps":fields.Integer(),"use_temp_dir":fields.Boolean(truthy=['on'],falsy=['off'])})
def genStableDiffusion_2_1_768_Images(args):
	print('gen stablediff')

	
	dirToWriteImage=genImages.imageDirPath()
	urlPathForImages=None

	if args["use_temp_dir"]:
		dirToWriteImage=genImages.imageDirTempPath(tempDirForGenerated)
		urlPathForImages=genImages.imageDirTempUrlPath()

	images=genImages.saveImages(genImages.genStableDiffusion_2_1_768(prompt=args["prompt"], negative_prompt=args["negative_prompt"], width=args["width"], height=args["height"], guidance_scale=args["guidance_scale"],num_samples=args["num_samples"],seed=args["seed"],num_inference_steps=args["num_inference_steps"]),"stable-diffusion2-1-768",dirToWriteImage,urlPath=urlPathForImages)
	
	return {
		"prompt":args["prompt"],
		"files":images
	},defaultHeaders


@app.route("/stableDiffusion2-1-768/getFormFields",methods=["OPTIONS"])
def getStableDiffusion_2_1_768_FormDataPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders

@app.route("/stableDiffusion2-1-768/getFormFields",methods=["POST"])
def getStableDiffusion_2_1_768_FormData():
	
	return {
		"formFieldsData":[
			{
				"name":'prompt',
				"displayName":"Prompt",
				"defaultValue":"a painting of an ai",
				"type":"textbox"

			},
			{
				"name":'negative_prompt',
				"displayName":"Negative Prompt",
				"defaultValue":"low quality, lowres, disfigured, deformed, blurred, blurry, bad art",
				"type":"textbox"

			},
			{
				"name":'width',
				"displayName":"Width",
				"defaultValue":"768"
			},
			{
				"name":'height',
				"displayName":"height",
				"defaultValue":"768"
			},
			{
				"name":'guidance_scale',
				"displayName":"guidance_scale",
				"defaultValue":"7.5"
			},
			{
				"name":'num_samples',
				"displayName":"Number of pictures",
				"defaultValue":"6"
			},
			{
				"name":'num_inference_steps',
				"displayName":"Number Inference Steps",
				"defaultValue":"50"
			},
			{
				"name":'eta',
				"displayName":"eta",
				"defaultValue":"0.0"
			},
			{
				"name":'seed',
				"displayName":"seed",
				"defaultValue":"100"
			},
			{
				"name":'use_temp_dir',
				"displayName":"use temp dir",
				"defaultValue":"off",
				"type":"radio",
				'possibleValues':[
					{
						'value':'on',
						'displayName':'save to temp dir '+tempDirForGenerated
					},
					{
						'value':'off',
						'displayName':'Save to backend/static'
					}
					
				]
			}

		]
	},defaultHeaders





@app.route("/controlnetScribbleToStableDiffusion1-5/getFormFields",methods=["OPTIONS"])
def getControlnetScribbleToStableDiffusion_1_5FormDataPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders


@app.route("/controlnetScribbleToStableDiffusion1-5/getFormFields",methods=["POST"])
def getControlnetScribbleToStableDiffusion_1_5FormData():
	
	return {
		"formFieldsData":[
			{
				"name":'prompt',
				"displayName":"Prompt",
				"defaultValue":"a painting of an ai",
				"type":"textbox"
			},
			{
				"name":'image',
				"displayName":"Image",
				"defaultValue":{
					'imgUrl':'',
					'width':512,
					'height':512
				},
				"type":"imagewidthheight"
			},
			{
				"name":'guidance_scale',
				"displayName":"guidance_scale",
				"defaultValue":"7.5"
			},
			{
				"name":'num_samples',
				"displayName":"Number of pictures",
				"defaultValue":"6"
			},
			{
				"name":'num_inference_steps',
				"displayName":"Number Inference Steps",
				"defaultValue":"50"
			},
			{
				"name":'eta',
				"displayName":"eta",
				"defaultValue":"0.0"
			},
			{
				"name":'seed',
				"displayName":"seed",
				"defaultValue":"100"
			},
			{
				"name":'enable_safety_checker',
				"displayName":"saftey checker",
				"defaultValue":"on",
				"type":"radio",
				'possibleValues':[
					{
						'value':'on',
						'displayName':'Enable Saftey Checker'
					},
					{
						'value':'off',
						'displayName':'Disable Saftey Checker'
					}
					
				]
			},
			{
				"name":'use_temp_dir',
				"displayName":"use temp dir",
				"defaultValue":"off",
				"type":"radio",
				'possibleValues':[
					{
						'value':'on',
						'displayName':'save to temp dir '+tempDirForGenerated
					},
					{
						'value':'off',
						'displayName':'Save to backend/static'
					}
					
				]
			}
		]
	},defaultHeaders






@app.route("/controlnetScribbleToStableDiffusion1-5/genimage",methods=["OPTIONS"])
def genControlnetScribbleToStableDiffusion_1_5_ImagesPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders

@app.route("/controlnetScribbleToStableDiffusion1-5/genimage",methods=["POST"])
@use_args({
	"prompt":fields.Str(required=True),
	"guidance_scale":fields.Float(),
	"num_samples":fields.Integer(),
	"seed":fields.Integer(),
	"eta":fields.Float(),
	"num_inference_steps":fields.Integer(),
	"image":fields.Nested({
		"height":fields.Integer(),
		"width":fields.Integer(),
		"imgUrl":fields.Str(required=True)
		}),
	"use_temp_dir":fields.Boolean(truthy=['on'],falsy=['off']),
	"enable_safety_checker":fields.Boolean(truthy=['on'],falsy=['off'])
})
def genControlnetScribbleToStableDiffusion_1_5_Images(args):

	
	img=Image.open(urllib.request.urlopen(args["image"]["imgUrl"])).convert("RGB")


	dirToWriteImage=genImages.imageDirPath()
	urlPathForImages=None

	if args["use_temp_dir"]:
		dirToWriteImage=genImages.imageDirTempPath(tempDirForGenerated)
		urlPathForImages=genImages.imageDirTempUrlPath()

	images=genImages.saveImages(genImages.genControlnetScribbleToStableDiffusion_1_5(prompt=args["prompt"], width=args["image"]["width"], height=args["image"]["height"], guidance_scale=args["guidance_scale"],num_samples=args["num_samples"],seed=args["seed"],num_inference_steps=args["num_inference_steps"],image=img,enable_safety_checker=args["enable_safety_checker"]),"controlnet-scribles-stable-diffusion-1-5",dirToWriteImage,urlPath=urlPathForImages)

	return {
		"prompt":args["prompt"],
		"files":images
	},defaultHeaders



	
	img=Image.open(urllib.request.urlopen(args["image"]["imgUrl"])).convert("RGB")


	dirToWriteImage=genImages.imageDirPath()
	urlPathForImages=None
	
	if args["use_temp_dir"]:
		dirToWriteImage=genImages.imageDirTempPath(tempDirForGenerated)
		urlPathForImages=genImages.imageDirTempUrlPath()

	images=genImages.saveImages(genImages.genControlnetScribbleToStableDiffusion_2_1_512(prompt=args["prompt"], width=args["image"]["width"], height=args["image"]["height"], guidance_scale=args["guidance_scale"],num_samples=args["num_samples"],seed=args["seed"],num_inference_steps=args["num_inference_steps"],image=img,enable_safety_checker=args["enable_safety_checker"]),"controlnet-scribles-stable-diffusion-2-1-512",dirToWriteImage,urlPath=urlPathForImages)

	return {
		"prompt":args["prompt"],
		"files":images
	},defaultHeaders


@app.route("/stableDiffusionImgToImg/getFormFields",methods=["OPTIONS"])
def getStableDiffusionImgToImgFormDataPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders


@app.route("/stableDiffusionImgToImg/getFormFields",methods=["POST"])
def getStableDiffusionImgToImgFormData():
	
	return {
		"formFieldsData":[
			{
				"name":'prompt',
				"displayName":"Prompt",
				"defaultValue":"a painting of an ai",
				"type":"textbox"
			},
			{
				"name":'image',
				"displayName":"Image",
				"defaultValue":{
					'imgUrl':'',
					'width':512,
					'height':512
				},
				"type":"imagewidthheight"
			},
			{
				"name":'strength',
				"displayName":"Strength",
				"defaultValue":"0.8"
			},

			{
				"name":'guidance_scale',
				"displayName":"guidance_scale",
				"defaultValue":"7.5"
			},
			{
				"name":'num_samples',
				"displayName":"Number of pictures",
				"defaultValue":"6"
			},
			{
				"name":'num_inference_steps',
				"displayName":"Number Inference Steps",
				"defaultValue":"50"
			},
			{
				"name":'eta',
				"displayName":"eta",
				"defaultValue":"0.0"
			},
			{
				"name":'seed',
				"displayName":"seed",
				"defaultValue":"100"
			},
			{
				"name":'enable_safety_checker',
				"displayName":"saftey checker",
				"defaultValue":"on",
				"type":"radio",
				'possibleValues':[
					{
						'value':'on',
						'displayName':'Enable Saftey Checker'
					},
					{
						'value':'off',
						'displayName':'Disable Saftey Checker'
					}
					
				]
			}
			

		]
	},defaultHeaders






@app.route("/stableDiffusionImgToImg/genimage",methods=["OPTIONS"])
def genStableDiffusionImgToImgImagesPreflight():
	print('preflight')
	return '',optionsPrefilghtResponseHeaders

@app.route("/stableDiffusionImgToImg/genimage",methods=["POST"])
@use_args({"prompt":fields.Str(required=True),"guidance_scale":fields.Float(),"num_samples":fields.Integer(),"seed":fields.Integer(),"eta":fields.Float(),"num_inference_steps":fields.Integer(),"enable_safety_checker":fields.Boolean(truthy=['on'],falsy=['off']),"image":fields.Nested(
{"height":fields.Integer(),"width":fields.Integer(),"imgUrl":fields.Str(required=True)}), "strength":fields.Float() })
def genStableDiffusionImgToImgImages(args):

	print('gen stablediff img2img')

	img=Image.open(urllib.request.urlopen(args["image"]["imgUrl"])).convert("RGB")

	images=genImages.saveImages(genImages.genStableDiffusionImgToImg(prompt=args["prompt"], width=args["image"]["width"], height=args["image"]["height"], guidance_scale=args["guidance_scale"],num_samples=args["num_samples"],seed=args["seed"],num_inference_steps=args["num_inference_steps"],enable_safety_checker=args["enable_safety_checker"],image=img,strength=args["strength"]),"stable-diffusion-img2img",genImages.imageDirPath())

	return {
		"prompt":args["prompt"],
		"files":images
	},defaultHeaders
