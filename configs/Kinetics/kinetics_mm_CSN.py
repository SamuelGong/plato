# clients settings
clients = dict(
    type="simple",  # Type
    total_clients=5,  # The total number of clients
    per_round=2,  # The number of clients selected in each round
    do_test=True)  # Should the clients compute test accuracy locally?

# server settings
server = dict(address="127.0.0.1", port=8000)

# dataset settings for the multimodal data, frames, flow, and audio
import kinetics_csn_rgb, kinetics_tsn_flow, kinetics_audio_feature

data = dict(
    datasource="Kinetics700",
    data_path="./data/Kinetics",
    download_url=
    "https://storage.googleapis.com/deepmind-media/Datasets/kinetics700_2020.tar.gz",
    num_workers=4,
    failed_save_file="failed_record.txt",
    log_file=None,
    compress=False,
    verbose=False,
    skip=False,
    videos_per_gpu=3,
    workers_per_gpu=4,
    train=[
        kinetics_csn_rgb.rgb_data_train, kinetics_tsn_flow.flow_data_train,
        kinetics_audio_feature.audio_data_train
    ],
    val=[
        kinetics_csn_rgb.rgb_data_val, kinetics_tsn_flow.flow_data_val,
        kinetics_audio_feature.audio_data_val
    ],
    test=[
        kinetics_csn_rgb.rgb_data_test, kinetics_tsn_flow.flow_data_test,
        kinetics_audio_feature.audio_data_test
    ],
    sampler="dis_noniid")

# Train settings

## optimizer
optimizer = dict(type='SGD', lr=0.000125, momentum=0.9,
                 weight_decay=0.0001)  # this lr is used for 8 gpus
optimizer_config = dict(grad_clip=dict(max_norm=40, norm_type=2))
# #learning policy
lr_config = dict(policy='step',
                 step=[32, 48],
                 warmup='linear',
                 warmup_ratio=0.1,
                 warmup_by_epoch=True,
                 warmup_iters=16)
total_epochs = 58
checkpoint_config = dict(interval=2)
evaluation = dict(interval=5,
                  metrics=['top_k_accuracy', 'mean_class_accuracy'])
log_config = dict(
    interval=20,
    hooks=[dict(type='TextLoggerHook'),
           dict(type='TensorboardLoggerHook')])

trainer = dict(type="basic",
               batch_size=24,
               optimizer=optimizer,
               optimizer_config=optimizer_config,
               learning_rate_config=lr_config,
               rounds=total_epochs,
               parallelized=False,
               max_concurrency=clients["per_round"],
               target_accuracy=0.67)
algorithm = dict(
    type="fedavg",  # Aggregation algorithm
    cross_silo=True,  # Cross-silo training
    total_silos=2,  # The total number of silos (edge servers)
    local_rounds=2
)  # The number of local aggregation rounds on edge servers before sending
# aggreagted weights to the central server

# runtime settings
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/ircsn_ig65m_pretrained_bnfrozen_r152_32x2x1_58e_kinetics400_rgb'  # noqa: E501
load_from = None
resume_from = None
workflow = [('train', 1)]
find_unused_parameters = True