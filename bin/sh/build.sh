#!/bin/sh

# check if ../../models/vqgan_imagenet_f16_16384.ckpt exists, if not curl it
if [ ! -f ../../models/vqgan_imagenet_f16_16384.ckpt ]; then
    curl -L "https://heibox.uni-heidelberg.de/f/867b05fc8c4841768640/?dl=1" -o ../../models/vqgan_imagenet_f16_16384.ckpt
fi

docker-compose -f ../../docker-compose.yml build
