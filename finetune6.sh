DS_SKIP_CUDA_CHECK=1

export CUDA_VISIBLE_DEVICES=0,1,2,3,4
export PATH=/home/limengze/cuda-12.1/bin:$PATH 
export LD_LIBRARY_PATH=/home/limengze/cuda-12.1/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64
export CUDA_HOME=/usr/local/cuda-12.1

export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1

deepspeed finetune_deepseekcoder.py \
    --model_name_or_path /home/limengze/chen_dongheng/DeepSeek-Coder/finetune/finetune_result2_link/pab/checkpoint-40 \
    --data_path 1208_train_pairs_plus_latex_3.json \
    --output_dir finetune_result2_link/pab2 \
    --num_train_epochs 60 \
    --model_max_length 1024 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 10 \
    --save_total_limit 10 \
    --learning_rate 2e-6 \
    --warmup_steps 10 \
    --logging_steps 1 \
    --lr_scheduler_type "cosine" \
    --gradient_checkpointing True \
    --report_to "tensorboard" \
    --deepspeed configs/ds_config_zero3.json \
    --bf16 True