IF NOT EXIST ../../models/vqgan_imagenet_f16_16384.ckpt (
    curl https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1 -o ../../models/vqgan_imagenet_f16_16384.ckpt
)

docker-compose -f ../../docker-compose.yml build

PAUSE
