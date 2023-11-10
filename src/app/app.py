import gradio as gr
import torch

import diffusers
from diffusers import AutoPipelineForInpainting, UNet2DConditionModel
from share_btn import community_icon_html, loading_icon_html, share_js


device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = AutoPipelineForInpainting.from_pretrained("diffusers/stable-diffusion-xl-1.0-inpainting-0.1", torch_dtype=torch.float16, variant="fp16").to(device)


def read_content(file_path: str) -> str:
    """read the content of target file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def predict(dict, prompt="", negative_prompt="", guidance_scale=7.5, steps=20, strength=1.0, scheduler="EulerDiscreteScheduler"):
    if negative_prompt == "":
        negative_prompt = None
    scheduler_class_name = scheduler.split("-")[0]

    add_kwargs = {}
    if len(scheduler.split("-")) > 1:
        add_kwargs["use_karras"] = True
    if len(scheduler.split("-")) > 2:
        add_kwargs["algorithm_type"] = "sde-dpmsolver++"

    scheduler = getattr(diffusers, scheduler_class_name)
    pipe.scheduler = scheduler.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", subfolder="scheduler", **add_kwargs)

    init_image = dict["image"].convert("RGB").resize((1024, 1024))
    mask = dict["mask"].convert("RGB").resize((1024, 1024))

    output = pipe(prompt=prompt, negative_prompt=negative_prompt, image=init_image, mask_image=mask, guidance_scale=guidance_scale, num_inference_steps=int(steps), strength=strength)

    return output.images[0], gr.update(visible=True)
