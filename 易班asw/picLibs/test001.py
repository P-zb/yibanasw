import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt

# 读取验证码图片
image = cv2.imread('./login.jpg')

# 将图像转换为灰度图
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 对图像进行二值化处理
_, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

# 对二值化图像进行降噪处理
denoised_image = cv2.medianBlur(binary_image, 5)

# 使用连通组件分析来找出不同的物体
labels = measure.label(denoised_image, connectivity=2)
regions = measure.regionprops(labels)

# 根据区域的属性（如颜色、形状等）进行筛选
filtered_regions = []
for region in regions:
    if region.area > 100:  # 仅保留面积大于100的区域
        filtered_regions.append(region)

# 找到体积最小的物体
min_volume_region = min(filtered_regions, key=lambda region: region.area)

# 标记体积最小的物体并显示
min_row, min_col, max_row, max_col = min_volume_region.bbox
cv2.rectangle(image, (min_col, min_row), (max_col, max_row), (255, 0, 255), 2)

# 显示处理后的图像
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
