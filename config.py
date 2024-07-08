img_width = 640  # 图片resize大小-宽
img_height = 640  # 图片resize大小-高
widget_width = 1000  # 窗口大小-宽
widget_height = 800  # 窗口大小-高
original_path = '20240708/data'  # 原始图片文件夹路径
results_path = '20240708/result'  # 标注结果存放文件夹路径
support_type = ['jpg', 'jpeg', 'png']  # 希望支持的图片后缀名（QPixMap支持的图片格式才行）
backup_path = '20240708/backup'  # 备份文件夹路径
result_name_template = '%s-%s-%s-%s.jpg'  # %s表示坐标点 依次为 x0, y0, x1, y1
# (如x0=10, y0=20, x1=30, y1=40；result_name_template='%s_%s_%s_%s.png'; 则结果的文件名为10_20_30_40.png)