#!/bin/sh

# check if ../../models/vqgan_imagenet_f16_16384.ckpt exists, if not curl it
if [ ! -f ../../models/vqgan_imagenet_f16_16384.ckpt ]; then
    curl https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1 -o ../../models/vqgan_imagenet_f16_16384.ckpt
fi

docker-compose -f ../../docker-compose.yml build
