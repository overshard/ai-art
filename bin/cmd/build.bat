IF NOT EXIST ../../models/vqgan_imagenet_f16_16384.ckpt (
    curl -L "https://heibox.uni-heidelberg.de/f/867b05fc8c4841768640/?dl=1" -o ../../models/vqgan_imagenet_f16_16384.ckpt
)

docker-compose -f ../../docker-compose.yml build

PAUSE
