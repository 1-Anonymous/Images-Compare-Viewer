import cv2
import os
import glob
import numpy as np
# 屏蔽 Qt 的相关警告输出
os.environ.setdefault("QT_LOGGING_RULES", "*=false")


def get_image_list(dir_path):
    # 获取目录下所有的图片，假设格式为 .png 或 .jpg
    exts = ['*.png', '*.jpg', '*.jpeg']
    images = []
    for ext in exts:
        images.extend(glob.glob(os.path.join(dir_path, ext)))
    # 按照文件名排序，确保两组图片的顺序和编号对应
    images.sort()
    return images


def main():
    # 替换为你实际的目录路径
    DIR1 = "/home/XXX/XXX/vis_XXX/XXX1"  # 上面的图片目录 (baseline)
    DIR2 = "/home/XXX/XXX/vis_XXX/XXX2"   # 下面的图片目录 (new)

    # 获取倒数第二个文件夹名称中最后一个下划线之后的内容
    def get_folder_suffix(dir_path):
        p = os.path.normpath(dir_path)
        parent = os.path.basename(os.path.dirname(p))  # 倒数第二级文件夹名
        if '_' in parent:
            return parent.rsplit('_', 1)[-1]
        return ''

    # 用于在各自图片顶部居中显示并自动缩放的文本绘制函数
    def draw_top_center_text(img, text, top_offset=20, padding=20, color=(0, 0, 255)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 初始更大的字体
        scale = 3
        thickness = 5
        (w, h), baseline = cv2.getTextSize(text, font, scale, thickness)
        # 如果文本宽度超出最大宽度，逐步减小字体
        # while w > max_width and scale > 0.05:
        #     scale -= 0.05
        #     (w, h), baseline = cv2.getTextSize(text, font, scale, thickness)
        # 计算左下角坐标，使文本水平居中并靠近顶部
        x = max(padding, (img.shape[1] - w) // 2) + w//3
        y = int(top_offset + h)
        # 绘制半透明背景矩形以提高可读性
        # rect_x1 = max(0, x - 10)
        # rect_y1 = max(0, top_offset - 6)
        # rect_x2 = min(img.shape[1], x + w + 10)
        # rect_y2 = min(img.shape[0], int(top_offset + h + 6))
        # overlay = img.copy()
        # cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
        # alpha = 0.35
        # cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        cv2.putText(img, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)

    img_paths1 = get_image_list(DIR1)
    img_paths2 = get_image_list(DIR2)

    suffix1 = get_folder_suffix(DIR1)
    suffix2 = get_folder_suffix(DIR2)

    if not img_paths1 or not img_paths2:
        print("未找到图片，请检查目录路径")
        return

    idx1 = 0
    idx2 = 0
    total1 = len(img_paths1)
    total2 = len(img_paths2)

    window_name = "Image Comparison Viewer"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        # 读取当前索引的图片
        img1 = cv2.imread(img_paths1[idx1])
        img2 = cv2.imread(img_paths2[idx2])

        # 如果图片尺寸不完全一致，可以将其 resize 到相同的宽度
        # 这里假设图片本来的尺寸是一致的
        if img1 is not None and img2 is not None:
            # 确保宽度一致以便上下拼接
            if img1.shape[1] != img2.shape[1]:
                width = min(img1.shape[1], img2.shape[1])
                img1 = cv2.resize(img1, (width, int(img1.shape[0] * width / img1.shape[1])))
                img2 = cv2.resize(img2, (width, int(img2.shape[0] * width / img2.shape[1])))

            # 上下拼接图像
            concat_img = np.vstack((img1, img2))
            
            # 在图像上添加文本显示当前的文件名进度，方便对比
            text1 = f"DIR1 [{idx1+1}/{total1}]:{(' ' + suffix1) if suffix1 else ''} {os.path.basename(img_paths1[idx1])}"
            text2 = f"DIR2 [{idx2+1}/{total2}]:{(' ' + suffix2) if suffix2 else ''} {os.path.basename(img_paths2[idx2])}"

            # 在各自图片的顶部居中显示文本（上方/下方分别有独立的上边距）
            top_offset_top = 20
            top_offset_bottom = img1.shape[0] + 20
            draw_top_center_text(concat_img, text1, top_offset=top_offset_top)
            draw_top_center_text(concat_img, text2, top_offset=top_offset_bottom)

            cv2.imshow(window_name, concat_img)
        else:
            print(f"警告：无法读取图像 {img_paths1[idx1]} 或 {img_paths2[idx2]}")

        # 等待按键，0表示无限等待
        key = cv2.waitKey(0) & 0xFF

        # 检测窗口是否被关闭（点击右上角关闭按钮）
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

        # Esc 键退出
        if key == 27:
            break

        # A 键：两组图片同时上一张
        elif key == ord('a') or key == ord('A'):
            idx1 = max(0, idx1 - 1)
            idx2 = max(0, idx2 - 1)

        # D 键：两组图片同时下一张
        elif key == ord('d') or key == ord('D'):
            idx1 = min(total1 - 1, idx1 + 1)
            idx2 = min(total2 - 1, idx2 + 1)

        # Q 键：上方 DIR1 切换上一张
        elif key == ord('q') or key == ord('Q'):
            idx1 = max(0, idx1 - 1)

        # E 键：上方 DIR1 切换下一张
        elif key == ord('e') or key == ord('E'):
            idx1 = min(total1 - 1, idx1 + 1)

        # Z 键：下方 DIR2 切换上一张
        elif key == ord('z') or key == ord('Z'):
            idx2 = max(0, idx2 - 1)

        # C 键：下方 DIR2 切换下一张
        elif key == ord('c') or key == ord('C'):
            idx2 = min(total2 - 1, idx2 + 1)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
