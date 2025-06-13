# 基于 3D Gaussian Splatting 的物体重建和新视图合成

## 仓库介绍

本项目为课程神经网络和深度学习作业的代码仓库

* 基本要求：
  - (1) 选取身边的物体拍摄多角度图片/视频，并使用 COLMAP 估计相机参数，随后使用其官方代码库训练 3D Gaussian；
  - (2) 基于训练好的 3D Gaussian 在新的轨迹下渲染环绕物体的视频，并在预留的测试图片上评价定量结果。
  - (3) 比较任务 1 中原版 NeRF、任务 1 NeRF 加速技术，以及 3D Gaussian Splatting 三种方法的合成结果和训练/测试效率，在报告中加入相应分析。

## 文件说明
```bash
- gaussian-splatting
  - convert.py  # 调用colmap生成点云
  - train.py # 使用点云数据进行训练
  - render.py # 按照新相机轨迹渲染新视图图像
  - metrics.py # 在测试数据上计算 PSNR 等指标
  - visualize_tensorboard.py # 启用tensorboard记录训练过程指标
  - data # 数据集
    - input.mp4 # 拍摄的物体视频
    - input # 将视频按帧抽取获得图片数据集
    - sparse # 使用colmap得到的点云数据
    - output0611eval
      - point_cloud # 训练后的模型数据
      - train # 对训练数据的渲染结果
      - test # 对测试数据的渲染结果
```

## 一、 数据准备

### 视频抽帧
* 在命令行中运行：
```bash
ffmpeg -i [input_video_path] -r [fps] [output_frame_path]/frame_%04d.jpg
```
* 其中[input_video_path]为原始视频文件路径，[fps]为设定的抽帧帧率（如 30fps），[output_frame_path]为输出图像保存路径。
### 点云文件生成

* 利用 gaussian_splatting 自带的convert.py脚本，将抽帧后的图像数据转换为点云文件。在命令行执行：
```bash
python convert.py --input_path [output_frame_path] --output_path [point_cloud_output_path]
```
* [output_frame_path]为抽帧图像路径，[point_cloud_output_path]为点云文件输出路径。

## 二、 3D Gaussian Splatting 模型训练

* 配置tensorboard记录训练loss变化
```bash
python visualize_tensorboard.py
```
* 执行如下命令进行模型训练：
```bash
python train.py -s data -m data/output --eval
```
其中，-s data指定输入数据路径（即包含点云等数据的data文件夹），-m data/output指定模型训练结果保存路径，--eval参数开启训练过程中的实时评估。
* 执行如下命令查看tensorboard记录的结果：
```bash
tensorboard --logdir="/data/output"  --host=127.0.0.1 --port=8008
```

## 三、视频渲染与实验结果定量评价

### 1. 新视图合成与视频渲染
* 在命令行中运行：
```bash
python render.py -m data/output
```
进行新视图渲染。该命令中的-m参数指定训练好的模型权重文件路径（即data/output），程序基于该模型和预设的新相机轨迹，生成新视图图像。

* 在命令行中运行：
```bash
ffmpeg -framerate 30 -i "data/output/train/ours_30000/gt/%05d.png" -c:v libx264 output_video_gt.mp4
```
使用视频编辑工具ffmpeg将图像序列合成为环绕物体的视频。

### 2. 实验结果定量评价
* 在命令行中运行：
```bash
python metrics.py -m /data/output
```
计算定量评价指标。该命令依据训练好的模型和预留测试数据，计算出 SSIM、PSNR、LPIPS 等指标
