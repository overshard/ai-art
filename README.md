# ai-art

Art generation using VQGAN + CLIP using docker containers. A simplified,
updated, and expanded upon version of
[Kevin Costa's work](https://github.com/kcosta42/VQGAN-CLIP-Docker).


## Samples

For samples check out the [AI Assisted](https://isaacbythewood.com/art) section
on the art page on my website.


## Using ai-art

This works best if you have an NVIDIA GPU however there is a fallback CPU mode
included. I've found the CPU mode to take significantly longer than even the
most basic of GPUs though.

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for
your OS.

Download the latest release of this repository from GitHub and put it anywhere
you want.

Run the `bin/sh/build.sh` or `bin/cmd/build.cmd` script based on your respective
platform (the first for Linux and MacOS, the second for Windows).

And you're good to go! You'll get a painting of a potato in your outputs folder
if it works. You can change settings and the prompt in `configs/config.json`.


## Other datasets

Download the latest ImageNet dataset from [ImageNet](http://image-net.org/) or
using the below links. Everything is configured by default for
`vqgan_imagenet_f16_16384.ckpt` so if you click the below download, save the
file as `vqgan_imagenet_f16_16384.ckpt` and put it in the `models` folder you
can start immediately by running a generate script in the `bin` folder.

<table>
  <thead>
    <tr>
      <th>Dataset</th>
      <th>Link</th>
      <th>Config</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ImageNet (f=16), 16384</td>
      <td><a href="https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1">vqgan_imagenet_f16_16384.ckpt</a></td>
      <td>configs/models/vqgan_imagenet_f16_16384.json</td>
    </tr>
    <tr>
      <td>ImageNet (f=16), 1024</td>
      <td><a href="https://heibox.uni-heidelberg.de/d/8088892a516d4e3baf92/files/?p=%2Fckpts%2Flast.ckpt&dl=1">vqgan_imagenet_f16_1024.ckpt</a></td>
      <td>configs/models/vqgan_imagenet_f16_1024.json</td>
    </tr>
  </tbody>
</table>


## Image sizes

The larger the image the more VRAM your graphics card needs:

- 6 GB of VRAM is required to generate 256x256 images.
- 12 GB of VRAM is required to generate 512x512 images.
- 24 GB of VRAM is required to generate 1024x1024 images.

If you don't know how much VRAM your graphics card has you probably have 6 GB
or less so stick with smaller images.

That being said you can do non-square images if you want as long as you don't
go above the number of pixels your GPU's VRAM supports, for example you could
do ultrawide images with 6 GB of ram at "384x128" or do tall images at "128x384"
and so on. You do not have to use numbers with a power of 2, "300x100" is also
perfectly valid.

Don't worry about small image sizes, you can scale them up later using a variety
of tools. I generate all mine at 256x256 and resize them later.


## Usage

You can edit the config file in `configs/config.json` to change any of the
below settings.

I include some helper scripts in `bin` to make it so you can double click on
a script (or run it with `./bin/sh/<script>`) and it will run it just to
simplify things as much as possible.


### Config options

| Argument               | Type           | Descriptions                                                                   |
|------------------------|----------------|--------------------------------------------------------------------------------|
| `prompts`              | List[str]      | Text prompts                                                                   |
| `image_prompts`        | List[FilePath] | Image prompts / target image path                                              |
| `max_iterations`       | int            | Number of iterations                                                           |
| `save_freq`            | int            | Save image iterations                                                          |
| `size`                 | [int, int]     | Image size (width height)                                                      |
| `pixelart`             | [int, int]     | Pixelart image size (width height) (Optional, remove option to disable)        |
| `init_image`           | FilePath       | Initial image                                                                  |
| `init_noise`           | str            | Initial noise image ["gradient","pixels","fractal"]                            |
| `init_weight`          | float          | Initial weight                                                                 |
| `mse_decay_rate`       | int            | Slowly decrease the MSE Loss each specified iterations until it reach about 0  |
| `output_dir`           | FilePath       | Path to output directory                                                       |
| `models_dir`           | FilePath       | Path to models cache directory                                                 |
| `clip_model`           | FilePath       | CLIP model path or name                                                        |
| `vqgan_checkpoint`     | FilePath       | VQGAN checkpoint path                                                          |
| `vqgan_config`         | FilePath       | VQGAN config path                                                              |
| `noise_prompt_seeds`   | List[int]      | Noise prompt seeds                                                             |
| `noise_prompt_weights` | List[float]    | Noise prompt weights                                                           |
| `step_size`            | float          | Learning rate                                                                  |
| `cutn`                 | int            | Number of cuts                                                                 |
| `cut_pow`              | float          | Cut power                                                                      |
| `seed`                 | int            | Seed (-1 for random seed)                                                      |
| `optimizer`            | str            | Optimiser ["Adam","AdamW","Adagrad","Adamax","DiffGrad","AdamP","RAdam"]       |
| `nwarm_restarts`       | int            | Number of time the learning rate is reseted (-1 to disable LR decay)           |
| `augments`             | List[str]      | Enabled augments ["Ji","Sh","Gn","Pe","Ro","Af","Et","Ts","Cr","Er","Re","Hf"] |


## Output

All output is stored in the `outputs` folder, you can see the steps here as well
as final images.


## Training

These are instructions to train a new VQGAN model.

We have a training model that is ready to go in `configs/models/vqgan_custom.json`.
You may want to edit them to meet your need. Check the Model Configuration
section to understand each field.

By default, the models are saved in the `models/checkpoints` folder.


### Dataset

Put your image in a folder inside the data directory (`data` by default).

The dataset must be structured as follow:

```sh
./data/
├── class_x/
│   ├── xxx.png
│   ├── xxy.jpg
│   └── ...
│       └── xxz.ppm
└── class_y/
    ├── 123.bmp
    ├── nsdf3.tif
    └── ...
    └── asd932_.webp
```


### Model Configuration

| Argument             | Type     | Descriptions                                     |
|----------------------|----------|--------------------------------------------------|
| `base_learning_rate` | float    | Initial Learning rate                            |
| `batch_size`         | int      | Batch size (Adjust based on your GPU capability) |
| `epochs`             | int      | Maximum number of epoch                          |
| `output_dir`         | FilePath | Path to directory where to save training images  |
| `models_dir`         | FilePath | Path to directory where to save the model        |
| `data_dir`           | FilePath | Path to data directory                           |
| `seed`               | int      | Seed (-1 for random seed)                        |
| `resume_checkpoint`  | FilePath | Path to pretrained model                         |


### Infos

- Let the Generator train without the Discriminator for a few epochs
  (~3-5 epochs for ImageNet), then enable the Discriminator. The variable
  `lossconfig.params.disc_start` correspond to the number of global step
  (ie. batch iterations) before enabling the Discriminator.
- Once enabled, the Discriminator loss will stagnate around ~1.0,
  __this is a normal behaviour__. The loss will decrease in later epochs.
  (It can take a _very_ long time).
- If you've enabled the Discriminator too soon, the Generator will take a lot
  more time to train.
- Basically there is no rules for the number of epochs. If your dataset is large
  enough, there is no risk of overfitting. So the more you train, the better.
