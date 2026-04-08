# Images-Compare-Viewer
上下成对的对比实验可视化工具 / Visualization tool for paired comparison experiments


简介
- 将两组相同编号的可视化图片上下并排显示，支持同步/独立切换。适用于对比不同模型或方法在相同场景下的预测/可视化结果差异。

主要特性
- 上下对比两组图片
- 支持同步和独立切换查看
- 键盘快捷键快速翻页（见下方快捷键表）：
  - A / D : 两组同时 上一 / 下一 张
  - Q / E : 上图 单独 上一 / 下一 张
  - Z / C : 下图 单独 上一 / 下一 张

快速开始
1. 克隆仓库：
   git clone https://github.com/1-Anonymous/Images-Compare-Viewer.git
2. 进入项目目录并创建虚拟环境：
   python -m venv .venv
   source .venv/bin/activate
3. 安装依赖，仅需安装 OpenCV 库：
   pip install opencv-python
4. 运行：
   python Images-compare_viewer.py
   （如果系统中 python 指向 Python2，则使用 python3）

运行示例
- 设置两组对应图片文件名一致的对比实验图片绝对地址目录（如 `/home/XXX/Projects/XXX/vis_0403` 和 `/home/XXX/Projects/XXX/vis_0407`）。
- 启动脚本后按键盘快捷键进行翻页和切换（见快捷键）。

截图与示例数据
- 建议在仓库中加入 `examples/` 或 `docs/` 文件夹保存演示截图或 GIF，示例路径：`examples/screenshot.png`。

依赖
- 使用 pip 安装：
  pip install -r requirements.txt

许可证
本项目采用 MIT 许可证，详见 `LICENSE`。

贡献
欢迎通过 issue 或 PR 反馈问题与改进建议。


