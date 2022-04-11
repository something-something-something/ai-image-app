#lightlymodfied from this script into a function https://github.com/CompVis/latent-diffusion/blob/main/scripts/txt2img.py
#  license of the original script:
# MIT License

# Copyright (c) 2022 Machine Vision and Learning Group, LMU Munich

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse, os, sys, glob
import torch
import numpy as np
from omegaconf import OmegaConf
from PIL import Image
import gc
from tqdm import tqdm, trange
from einops import rearrange
#from torchvision.utils import make_grid
import sysconfig

sys.path.append(sysconfig.get_path('data')+'/src/latent-diffusion')
sys.path.append(sysconfig.get_path('data')+'/src/taming-transformers')
from ldm.util import instantiate_from_config
from ldm.models.diffusion.ddim import DDIMSampler


def load_model_from_config(config, ckpt, verbose=False):
	print(f"Loading model from {ckpt}")
	pl_sd = torch.load(ckpt, map_location="cpu")
	sd = pl_sd["state_dict"]
	model = instantiate_from_config(config.model)
	m, u = model.load_state_dict(sd, strict=False)
	if len(m) > 0 and verbose:
		print("missing keys:")
		print(m)
	if len(u) > 0 and verbose:
		print("unexpected keys:")
		print(u)

	model.cuda()
	model.eval()
	return model


def genImages(prompt='default prompt',dimmSteps=200,dimmEta=0.0,numIter=1,height=256,width=256,numSamples=4,scale=5.0):



	config = OmegaConf.load(sysconfig.get_path('data')+'/src/latent-diffusion/'+"configs/latent-diffusion/txt2img-1p4B-eval.yaml")  # TODO: Optionally download from same location as ckpt and chnage this logic
	model = load_model_from_config(config,"modelimg/model.ckpt")  # TODO: check path

	device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
	model = model.to(device)
	sampler = DDIMSampler(model)

	#os.makedirs(opt.outdir, exist_ok=True)
	

	prompt 


	sample_path = os.path.join("static","latentdiff" ,"images")
	os.makedirs(sample_path, exist_ok=True)
	base_count = len(os.listdir(sample_path))
	imagesGenerated=[]
	all_samples=list()
	with torch.no_grad():
		with model.ema_scope():
			uc = None
			if scale != 1.0:
				uc = model.get_learned_conditioning(numSamples * [""])
			for n in trange(numIter, desc="Sampling"):
				c = model.get_learned_conditioning(numSamples * [prompt])
				shape = [4,height//8, width//8]
				samples_ddim, _ = sampler.sample(S=dimmSteps,
												 conditioning=c,
												 batch_size=numSamples,
												 shape=shape,
												 verbose=False,
												 unconditional_guidance_scale=scale,
												 unconditional_conditioning=uc,
												 eta=dimmEta)

				x_samples_ddim = model.decode_first_stage(samples_ddim)
				x_samples_ddim = torch.clamp((x_samples_ddim+1.0)/2.0, min=0.0, max=1.0)

				for x_sample in x_samples_ddim:
					x_sample = 255. * rearrange(x_sample.cpu().numpy(), 'c h w -> h w c')
					imgsavepath=os.path.join(sample_path, f"{base_count:04}.png")
					imagesGenerated.append(imgsavepath)
					Image.fromarray(x_sample.astype(np.uint8)).save(imgsavepath)

					base_count += 1
				all_samples.append(x_samples_ddim)
	del model
	gc.collect()
	torch.cuda.empty_cache()
	return imagesGenerated
	# additionally, save as grid
	#grid = torch.stack(all_samples, 0)
	#grid = rearrange(grid, 'n b c h w -> (n b) c h w')
	#grid = make_grid(grid, nrow=opt.n_samples)

	# to image
	#grid = 255. * rearrange(grid, 'c h w -> h w c').cpu().numpy()

	#snum=1
	#for s in all_samples:
	#	Image.fromarray(s.astype(np.uint8)).save(os.path.join(outpath, f'{prompt.replace(" ", "-")}.png'))
	#	snum+=1
	
	#print(f"Your samples are ready and waiting four you here: \n{outpath} \nEnjoy.")