bash scripts/coop/main.sh caltech101 rn50_ep50 end 16 1 False 3

bash scripts/coop/main.sh cub rn50_ep50 end 16 1 False

bash scripts/coop/zeroshot.sh cub rn50_ep50 

bash scripts/coop/main.sh cub rn50 end 16 2 False

bash scripts/coop/main.sh cub rn50_ep100 end 16 4 False 7

bash scripts/coop/main.sh cub rn50_ep100 middle 16 2 False 6



bash scripts/coop/main.sh caltech101 rn50_ep50 end 16 1 False 4

bash scripts/clip_adapter/main.sh caltech101 rn50_ep50 end 16 1 False 4

bash scripts/coop/zeroshot.sh caltech101 rn50_ep50 


bash scripts/coop/main.sh caltech101 rn50_ep100 end 16 2 False 4

bash scripts/clip_adapter/main.sh caltech101 rn50_ep100 end 16 2 False 3


bash scripts/coop/main.sh caltech101 rn50_ep100 end 16 4 False 4

bash scripts/clip_adapter/main.sh caltech101 rn50_ep100 end 16 4 False 3



bash scripts/coop/main.sh caltech101 rn50 end 16 8 False 4

bash scripts/clip_adapter/main.sh caltech101 rn50 end 16 8 False 3


bash scripts/coop/main.sh caltech101 rn50 end 16 16 False 4

bash scripts/clip_adapter/main.sh caltech101 rn50 end 16 16 False 3