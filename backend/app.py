from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args
import genImages
app=Flask(__name__)


@app.route("/genimage",methods=["OPTIONS"])
def genImagePreflight():
	print('preflight')
	return '',{
		'Access-Control-Allow-Origin':'http://localhost:3000',
		'Access-Control-Allow-Methods':'POST,GET,OPTIONS',
		'Access-Control-Max-Age':2,
		'Access-Control-Allow-Headers':'Content-Type'
	}

@app.route("/genimage",methods=["POST"])
@use_args({"prompt":fields.Str(required=True),"scale":fields.Float(),"width":fields.Integer(),"height":fields.Integer(),"numSamples":fields.Integer()})
def genImage(args):

	images=genImages.saveImages(genImages.genLatentDiffusion(prompt=args["prompt"], width=args["width"], height=args["height"], scale=args["scale"],numSamples=args["numSamples"]),"latent-diffusion",genImages.imageDirPath())
	
	return {
		"prompt":args["prompt"],
		"files":images
	},{
		'Access-Control-Allow-Origin':'http://localhost:3000',
		'Access-Control-Allow-Methods':'POST,GET,OPTIONS'
	}