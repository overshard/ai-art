"""
Checks to make sure all our files and folders exist in /data. We need in the
data folder:

- /data/models/
- /data/models/vqgan_imagenet_f16_16384.json
- /data/models/vqgan_imagenet_f16_16384.ckpt
- /data/outputs/
- /data/outputs/steps/
- /data/config.json
"""
import requests
import os

vqgan_imagenet_f16_16384_ckpt_url = "https://heibox.uni-heidelberg.de/f/867b05fc8c4841768640/?dl=1"

vqgan_imagenet_f16_16384_json = """{
  "params": {
    "embed_dim": 256,
    "n_embed": 16384,
    "ddconfig": {
      "double_z": false,
      "z_channels": 256,
      "resolution": 256,
      "in_channels": 3,
      "out_ch": 3,
      "ch": 128,
      "ch_mult": [1, 1, 2, 2, 4],
      "num_res_blocks": 2,
      "attn_resolutions": [16],
      "dropout": 0.0
    },
    "lossconfig": {
      "params": {
        "disc_conditional": false,
        "disc_in_channels": 3,
        "disc_start": 0,
        "disc_weight": 0.75,
        "disc_num_layers": 2,
        "codebook_weight": 1.0
      }
    }
  }
}
"""

config_json = """{
    "prompts": ["space", "fractal"],
    "init_image": "",
    "size": [256, 256],
    "max_iterations": 250,
    "save_freq": 50
}
"""


def check_files_and_folders():
    print("Checking that you have all the files and folders required...")

    # check that models folder exists, if not create it
    if not os.path.exists("/data/models"):
        print("Creating models folder...")
        os.makedirs("/data/models")

    # check that outputs folder exists, if not create it
    if not os.path.exists("/data/outputs"):
        os.makedirs("/data/outputs")
        os.makedirs("/data/outputs/steps")

    # check that config.json exists, if not create it
    if not os.path.exists("/data/config.json"):
        print("Creating config.json...")
        with open("/data/config.json", "w") as f:
            f.write(config_json)

    # check that vqgan_imagenet_f16_16384.json exists, if not create it
    if not os.path.exists("/data/models/vqgan_imagenet_f16_16384.json"):
        print("Creating vqgan_imagenet_f16_16384.json...")
        with open("/data/models/vqgan_imagenet_f16_16384.json", "w") as f:
            f.write(vqgan_imagenet_f16_16384_json)
            f.close()

    # check that vqgan_imagenet_f16_16384.ckpt exists, if not download and
    # write in chunks since it's a large file
    if not os.path.exists("/data/models/vqgan_imagenet_f16_16384.ckpt"):
        print("Downloading vqgan_imagenet_f16_16384.ckpt...")
        with open("/data/models/vqgan_imagenet_f16_16384.ckpt", "wb") as f:
            r = requests.get(vqgan_imagenet_f16_16384_ckpt_url)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()
