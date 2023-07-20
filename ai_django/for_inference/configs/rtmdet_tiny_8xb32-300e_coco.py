_base_ = [
    "../_base_/default_runtime.py",
    "../_base_/schedules/schedule_1x.py",
    "../_base_/datasets/coco_detection.py",
    "../rtmdet/rtmdet_tta.py",
]

# checkpoint = "https://download.openmmlab.com/mmdetection/v3.0/rtmdet/cspnext_rsb_pretrain/cspnext-tiny_imagenet_600e.pth"  # noqa
checkpoint = "/content/drive/Othercomputers/내 Mac/Active/kdt_hackerton/mmdetection/work_dirs/rtmdet_tiny_8xb32-300e_coco/epoch_7.pth"

# dataset settings
dataset_type = "CocoDataset"
data_root = "data/coco/"
backend_args = None
classes = (
    "no symptoms",
    "corneal ulcer",
    "corneal flap",
    "conjunctivitis",
    "non-ulcerative keratitis",
    "blepharitis",
)

model = dict(
    type="RTMDet",
    data_preprocessor=dict(
        type="DetDataPreprocessor",
        mean=[103.53, 116.28, 123.675],
        std=[57.375, 57.12, 58.395],
        bgr_to_rgb=False,
        batch_augments=None,
    ),
    backbone=dict(
        type="CSPNeXt",
        arch="P5",
        expand_ratio=0.5,
        deepen_factor=0.167,
        widen_factor=0.375,
        channel_attention=True,
        norm_cfg=dict(type="SyncBN"),
        act_cfg=dict(type="SiLU", inplace=True),
        init_cfg=dict(type="Pretrained", prefix="backbone.", checkpoint=checkpoint),
    ),
    neck=dict(
        type="CSPNeXtPAFPN",
        in_channels=[96, 192, 384],
        out_channels=96,
        num_csp_blocks=1,
        expand_ratio=0.5,
        norm_cfg=dict(type="SyncBN"),
        act_cfg=dict(type="SiLU", inplace=True),
    ),
    bbox_head=dict(
        type="RTMDetSepBNHead",
        num_classes=6,
        in_channels=96,
        stacked_convs=2,
        feat_channels=96,
        anchor_generator=dict(type="MlvlPointGenerator", offset=0, strides=[8, 16, 32]),
        bbox_coder=dict(type="DistancePointBBoxCoder"),
        loss_cls=dict(
            type="QualityFocalLoss", use_sigmoid=True, beta=2.0, loss_weight=2.0
        ),
        loss_bbox=dict(type="GIoULoss", loss_weight=1.0),
        with_objectness=False,
        exp_on_reg=False,
        share_conv=True,
        pred_kernel_size=1,
        norm_cfg=dict(type="SyncBN"),
        act_cfg=dict(type="SiLU", inplace=True),
    ),
    train_cfg=dict(
        assigner=dict(type="DynamicSoftLabelAssigner", topk=13),
        allowed_border=-1,
        pos_weight=-1,
        debug=False,
    ),
    test_cfg=dict(
        nms_pre=30000,
        min_bbox_size=0,
        score_thr=0.001,
        nms=dict(type="nms", iou_threshold=0.50),
        max_per_img=300,
    ),
)

train_pipeline = [
    dict(type="LoadImageFromFile", backend_args={{_base_.backend_args}}),
    dict(type="LoadAnnotations", with_bbox=True),
    # dict(
    #     type="CachedMosaic",
    #     img_scale=(640, 640),
    #     pad_val=114.0,
    #     max_cached_images=20,
    #     random_pop=False,
    # ),
    dict(type="Resize", scale=(640, 640), keep_ratio=True),
    # dict(
    #     type="RandomResize", scale=(640, 640), ratio_range=(0.5, 2.0), keep_ratio=True
    # ),
    # dict(type="RandomCrop", crop_size=(640, 640)),
    # dict(type="YOLOXHSVRandomAug"),
    dict(type="RandomFlip", prob=0.01),
    dict(type="Pad", size=(640, 640), pad_val=dict(img=(114, 114, 114))),
    # dict(
    #     type="CachedMixUp",
    #     img_scale=(640, 640),
    #     ratio_range=(1.0, 1.0),
    #     max_cached_images=10,
    #     pad_val=(114, 114, 114),
    #     prob=0.5,
    # ),
    dict(type="PackDetInputs"),
]

train_pipeline_stage2 = [
    dict(type="LoadImageFromFile", backend_args={{_base_.backend_args}}),
    dict(type="LoadAnnotations", with_bbox=True),
    dict(
        type="RandomResize", scale=(640, 640), ratio_range=(0.5, 2.0), keep_ratio=True
    ),
    dict(type="RandomCrop", crop_size=(640, 640)),
    dict(type="YOLOXHSVRandomAug"),
    dict(type="RandomFlip", prob=0.01),
    dict(type="Pad", size=(640, 640), pad_val=dict(img=(114, 114, 114))),
    dict(type="PackDetInputs"),
]

test_pipeline = [
    dict(type="LoadImageFromFile", backend_args={{_base_.backend_args}}),
    dict(type="Resize", scale=(640, 640), keep_ratio=True),
    dict(type="Pad", size=(640, 640), pad_val=dict(img=(114, 114, 114))),
    dict(
        type="PackDetInputs",
        meta_keys=("img_id", "img_path", "ori_shape", "img_shape", "scale_factor"),
    ),
]


train_dataloader = dict(
    batch_size=32,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type="DefaultSampler", shuffle=True),
    batch_sampler=dict(type="AspectRatioBatchSampler"),
    dataset=dict(
        type=dataset_type,
        metainfo=dict(classes=classes),
        data_root=data_root,
        ann_file="annotations/train_coco.json",
        data_prefix=dict(img="train/"),
        filter_cfg=dict(filter_empty_gt=True, min_size=32),
        pipeline=train_pipeline,
        backend_args=backend_args,
    ),
)

val_dataloader = dict(
    batch_size=8,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type="DefaultSampler", shuffle=False),
    dataset=dict(
        type=dataset_type,
        metainfo=dict(classes=classes),
        data_root=data_root,
        ann_file="annotations/val_coco.json",
        data_prefix=dict(img="val/"),
        test_mode=True,
        pipeline=test_pipeline,
        backend_args=backend_args,
    ),
)

test_dataloader = val_dataloader

max_epochs = 30  # 300
stage2_num_epochs = 10
base_lr = 0.003
interval = 1

train_cfg = dict(
    max_epochs=max_epochs,
    val_interval=interval,
    dynamic_intervals=[(max_epochs - stage2_num_epochs, 1)],
)

val_evaluator = dict(proposal_nums=(100, 1, 10))
test_evaluator = val_evaluator

# optimizer
optim_wrapper = dict(
    _delete_=True,
    type="OptimWrapper",
    optimizer=dict(type="AdamW", lr=base_lr, weight_decay=0.05),
    paramwise_cfg=dict(norm_decay_mult=0, bias_decay_mult=0, bypass_duplicate=True),
)

# learning rate
param_scheduler = [
    dict(type="LinearLR", start_factor=1.0e-5, by_epoch=False, begin=0, end=1000),
    dict(
        # use cosine lr from 150 to 300 epoch
        type="CosineAnnealingLR",
        eta_min=base_lr * 0.05,
        begin=max_epochs // 2,
        end=max_epochs,
        T_max=max_epochs // 2,
        by_epoch=True,
        convert_to_iter_based=True,
    ),
]

# hooks
default_hooks = dict(
    checkpoint=dict(
        interval=interval, max_keep_ckpts=3  # only keep latest 3 checkpoints
    )
)

custom_hooks = [
    dict(
        type="EMAHook",
        ema_type="ExpMomentumEMA",
        momentum=0.0002,
        update_buffers=True,
        priority=49,
    ),
    dict(
        type="PipelineSwitchHook",
        switch_epoch=28,
        switch_pipeline=train_pipeline_stage2,
    ),
]
vis_backends = [
    dict(type="LocalVisBackend"),
    dict(
        type="WandbVisBackend",
        init_kwargs=dict(project="withpet"),
    ),
]
visualizer = dict(
    type="DetLocalVisualizer", vis_backends=vis_backends, name="visualizer"
)
