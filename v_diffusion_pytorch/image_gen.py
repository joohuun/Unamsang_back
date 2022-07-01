from .diffusion import get_model, sampling, utils
from .CLIP import clip
import gc
import math
import sys
import torch
from torchvision import utils as tv_utils
from tqdm.notebook import tqdm
import random
from PIL import ImageFile, Image
import numpy as np
import os
from datetime import datetime

sys.path.append('/v-diffusion-pytorch')

# device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
'''
Gpu 사용 시에는 'cpu' 부분을 'cuda'로
    .cpu() 는 .cuda()로 변경
model 부분만 half()가 추가되어서 주석으로 남겨놓음
'''

model = get_model('cc12m_1_cfg')()
_, side_y, side_x = model.shape
model.load_state_dict(torch.load('cc12m_1_cfg.pth', map_location='cpu'))

# model = model.half().cuda().eval().requires_grad_(False)
model = model.cpu().eval().requires_grad_(False)

clip_model = clip.load(model.clip_model, jit=False, device='cpu')[0]


##################################################

height = 256
width = 256
side_x = width
side_y = height
steps = 1
n_images = 4
weight = 3  # 3이 디폴트
eta = 0
display_every = 5
save_progress_video = True
save_name = 0.00000000

##################################################################


def run(username, prompt):
    target_embed = clip_model.encode_text(clip.tokenize(prompt)).float().cpu()
    now = datetime.now().strftime('%Y%m%d%H%M%S')

    def cfg_model_fn(x, t):
        """The CFG wrapper function."""
        n = x.shape[0]
        x_in = x.repeat([2, 1, 1, 1])
        t_in = t.repeat([2])
        clip_embed_repeat = target_embed.repeat([n, 1])
        clip_embed_in = torch.cat(
            [torch.zeros_like(clip_embed_repeat), clip_embed_repeat])
        v_uncond, v_cond = model(x_in, t_in, clip_embed_in).chunk(2, dim=0)
        v = v_uncond + (v_cond - v_uncond) * weight
        return v

    def display_callback(info):
        global save_name
        save_name += 0.00000001
        nrow = math.ceil(info['pred'].shape[0]**0.5)
        grid = tv_utils.make_grid(info['pred'], nrow, padding=0)
        utils.to_pil_image(grid).save(
            f"./media/images/steps/%.8f.png" % save_name)

        if info['i'] % display_every == 0:
            nrow = math.ceil(info['pred'].shape[0]**0.5)
            grid = tv_utils.make_grid(info['pred'], nrow, padding=0)
            tqdm.write(f'Step {info["i"]} of {steps}:')

            tqdm.write(f'')

    print("Prompt is: " + prompt)

    seed = random.randint(0, 2**32)
    print("Seed is: " + str(seed))
    gc.collect()
    torch.cuda.empty_cache()
    torch.manual_seed(seed)
    x = torch.randn([n_images, 3, side_y, side_x], device='cpu')
    t = torch.linspace(1, 0, steps + 1, device='cpu')[:-1]
    step_list = utils.get_spliced_ddpm_cosine_schedule(t)
    outs = sampling.sample(cfg_model_fn, x, step_list,
                           eta, {}, callback=display_callback)
    tqdm.write('Done!')

    for i, out in enumerate(outs):
        filename = f'media/images/{username}_{now}_{i}.png'
        utils.to_pil_image(out).save(filename)

    frames = []
    files = []
    init_frame = 0
    last_frame = steps

    directory = 'media/images/steps'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        files.append(f)
    for i in range(init_frame, last_frame):
        frames.append(Image.open(files[i]))
    frames[-1].save(f"media/images/{username}_{now}_finalgrid.png")

    # steps에 저장된 이미지들은 바로 삭제
    for filename in os.listdir(directory):
        os.remove(f'{directory}/{filename}')

    return f"{username}_{now}"
