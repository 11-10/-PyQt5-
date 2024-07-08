# -基于PyQt5的图片标注-
使用PyQt5对图片进行标注
修改config.py 文件
img_width = 640  # 图片resize大小-宽
img_height = 640  # 图片resize大小-高
widget_width = 1000  # 窗口大小-宽
widget_height = 800  # 窗口大小-高
original_path = '20240708/data'  # 原始图片文件夹路径
results_path = '20240708/result'  # 标注结果存放文件夹路径
support_type = ['jpg', 'jpeg', 'png']  # 希望支持的图片后缀名（QPixMap支持的图片格式才行）
backup_path = '20240708/backup'  # 备份文件夹路径
result_name_template = '%s-%s-%s-%s.jpg'  # %s表示坐标点 依次为 x0, y0, x1, y1
运行main.py即可。
基于https://gitee.com/wb200327/image_tagger代码修改

可视化：
![image](https://github.com/11-10/Image-annotation-based-on-PyQt/assets/100272245/aa6f0984-38a0-4bdf-b87b-67dcfc7b4575)

