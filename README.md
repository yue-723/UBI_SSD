# UBI_SSD
## train args
```
  python train.py --datasets /root/ubi/UBI_SSD/Data/train/  --validation_dataset /root/ubi/UBI_SSD/Data/val/  --net mb2-ssd-lite --pretrained_ssd models/mb2-ssd-lite-net.pth --scheduler cosine --lr 0.01 --t_max 100 --batch_size 36 --num_epochs 200
```
