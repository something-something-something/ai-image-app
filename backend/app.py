from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args
import genImages
app=Flask(__name__)


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
@use_args({"prompt":fields.Str(required=True),"guidance_scale":fields.Float(),"width":fields.Integer(),"height":fields.Integer(),"num_samples":fields.Integer(),"seed":fields.Integer(),"eta":fields.Float(),"num_inference_steps":fields.Integer()})
def genStableDiffusionImages(args):
	print('gen stablediff')
	images=genImages.saveImages(genImages.genStableDiffusion(prompt=args["prompt"], width=args["width"], height=args["height"], guidance_scale=args["guidance_scale"],num_samples=args["num_samples"],seed=args["seed"],num_inference_steps=args["num_inference_steps"]),"stable-diffusion",genImages.imageDirPath())
	
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
			}

		]
	},defaultHeaders