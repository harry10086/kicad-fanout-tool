# ![icon](icon.png) KiCad 扇出工具 (Fanout Tool)

<img src="https://img.shields.io/badge/KiCad-v10-brightgreen?style=for-the-badge&logo=KiCad"> <img src="https://img.shields.io/badge/kicad--python-v1.1.0-brightgreen?style=for-the-badge"> <img src="https://img.shields.io/badge/PySide6-Qt-brightgreen?style=for-the-badge">

这是一个基于 Python 的强大插件，旨在为 **KiCad PCB 设计** 中的密集 IC 封装自动执行逃线（扇出）路由。

手动为 QFN、QFP 和 BGA 等密集元件进行布线既乏味又耗时。本工具采用专业级算法（如三段式布线）自动化此过程，瞬间生成干净且无 DRC 错误的走线和过孔。

**支持 KiCAD 9.0.0 和 10.0.0 及以上版本。**

![预览截图](images/gui.png)

## 🚀 核心特性

* **先进的布线算法**：实现稳健的三段式布线（桩 $\rightarrow$ 45° 弯折 $\rightarrow$ 直线），防止走线交叉和 DRC 冲突，尤其适用于四边封装的紧凑角落。
* **多样的对齐模式**：
    * **扇形逃线 (Fan Escape)**：径向分布过孔以节省空间并组织外部连接。
    * **错开扇形/线性 (Staggered Fan/Linear)**：生成多行完美对齐的过孔（内层和外层），最大限度地增加布线通道。
* **全参数控制**：
    * **扇出长度 (Fanout Length)**：自定义从焊盘到过孔的精确间距。
    * **错开间距 (Stagger Gap)**：调整多行过孔之间的距离。
    * **过孔间距 (Via Pitch)**：独立于 IC 焊盘间距设置过孔之间的特定距离。
* **智能封装检测**：自动适配双边 (SOIC, TSSOP) 和四边 (QFP, QFN) 封装，并自动忽略中心散热焊盘 (EP/Thermal pads)。
* **安全且可撤销**：内置撤销系统，可立即恢复生成的走线和过孔，方便安全尝试。

## 🛠️ 安装方法

### 通过 KiCad 插件和内容管理器 (推荐)
将我们的自定义仓库添加到 **插件和内容管理器**，URL 为：
`https://raw.githubusercontent.com/harry10086/kicad-repository/main/repository.json`

![pcm](images/pcm.png)

### 手动安装
- 下载插件源码的 **.zip** 文件。
- 找到您的 KiCad 插件文件夹：
  - **Windows:** `Documents\KiCad\10.0\plugins`
  - **Linux:** `~/.local/share/kicad/10.0/plugins`
  - **macOS:** `~/Documents/KiCad/10.0/plugins`
- 将压缩包解压到 KiCad 插件目录。
- 重启 KiCad / PCB 编辑器。

## 🖥️ 使用方法

1. 打开 **PCB 编辑器**。
2. 选择您想要进行扇出的封装（IC）。
3. 前往 **工具 (Tools)** $\rightarrow$ **外部插件 (External Plugins)** $\rightarrow$ **扇出工具 (Fanout Tool)**（或点击顶部工具栏的图标）。
4. 配置参数：
   - 目标封装 (例如 SOIC/QFN)
   - 对齐方式 (扇形逃线, 错开, 线性)
   - 自定义距离 (扇出长度, 错开间距, 过孔间距)。
5. 点击 **扇出 (Run Fanout)** 生成走线和过孔。
6. (可选) 如果您想调整参数并重新尝试，请使用内置的 **撤销 (Undo)** 按钮。

## 演示视频
[![观看视频](https://img.youtube.com/vi/dmmUoKqVd8w/sddefault.jpg)](https://youtu.be/dmmUoKqVd8w)

## 📦 使用的库
本项目依赖于以下强大的开源库：
 - [kicad-python](https://pypi.org/project/kicad-python/): KiCad API Python 绑定。
 - [PySide6](https://pypi.org/project/PySide6/): Qt for Python 官方模块，用于图形用户界面。

## 📜 许可证与致谢

插件代码采用 MIT 许可证，详见 `LICENSE`。
