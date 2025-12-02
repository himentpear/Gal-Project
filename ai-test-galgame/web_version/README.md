学园法庭：结构主义辩论演示 (Danganronpa-style Debate Engine)本项目是一个基于 HTML/CSS/JS 的单文件视觉小说引擎，复刻了《弹丸论破》系列的“无休止议论”核心玩法。📁 1. 文件结构与资源准备为了让程序正常运行，请确保目录结构如下：/Project_Folder
│
├── index.html                  # 核心程序文件
├── bg_court.png                # 表世界背景（法庭/教室）
├── bg_logic.png                # 里世界背景（觉醒/逻辑深潜，建议黑红配色）
│
├── [立绘文件群]                 # 详见下文“命名规则”
│   ├── xjc-normal-stand-angry.png
│   ├── xjc-openmouth-stand-angry.png
│   └── ...
🎨 2. 素材命名规则 (核心机制)引擎通过拼接字符串自动查找立绘图片。您必须严格遵守以下命名格式：格式： [ID]-[嘴型]-[姿势]-[表情].pngID: 在代码 CHARS 对象中定义的角色 ID (如 xjc, yyc)。嘴型:normal: 闭嘴（静止状态）openmouth: 张嘴（说话时自动切换）姿势: 默认为 stand，可修改代码扩展。表情: 在剧本 SCRIPT 中指定的 emotion 字段。示例：如果脚本中写 char: "xjc", emotion: "angry"，引擎会交替加载：xjc-normal-stand-angry.pngxjc-openmouth-stand-angry.png⚙️ 3. 剧本配置系统 (SCRIPT)程序的核心逻辑位于 <script> 标签内的 const SCRIPT = [...] 数组中。每一项代表一个“场景”或“对话气泡”。字段详解表字段名类型必填说明typeString是UI 模式。"normal": 底部对话框模式。"debate": 漂浮弹幕模式（无对话框）。charString是角色 ID，对应 CHARS 配置。emotionString是表情后缀，用于拼接文件名。textString是对话内容。支持 HTML 标签（如 <br> 换行）。nameString否角色显示名称（仅在 normal 模式下显示）。cameraString否镜头调度。"left": 左倾 5° + 左侧角色特写。"right": 右倾 7° + 右侧角色特写。"center": 镜头归正。shakeBoolean否true: 文本出现时触发屏幕微震动。isWeakPointBoolean否true: 必须配合在 text 中使用 <span class='weak-point' onclick='triggerBreak(event)'>...</span>。标记此句为击破点。modeString否世界观切换。"solver": 进入觉醒/反转模式（背景反向移动）。"normal": 恢复默认。isThoughtBoolean否true: 标记为内心独白。用于逻辑判断（如未点击弱点时的提示）。endBoolean否true: 标记剧本结束。🛠️ 4. 核心机制修改指南如果您需要通过代码修改参数，请关注以下函数或 CSS 类：A. 镜头与构图 (#camera-rig)原理：将背景和角色包裹在 #camera-rig 容器中，对容器进行旋转和缩放，从而避免旋转时露出黑色底边。修改位置：CSS .tilt-left: 修改 rotate(-5deg) 调整左倾角度。CSS .tilt-right: 修改 rotate(7deg) 调整右倾角度。CSS .char-img: 修改 bottom: -50% 调整半身像的截取位置。B. 背景无缝滚动原理：利用 CSS background-repeat: repeat-x 和 background-position 动画。修改位置：@keyframes bgScrollLeft: 修改 to { background-position: -200% 0; } 控制滚动距离。.mode-solver #bg-layer: 修改 animation 的持续时间（如 5s）来控制觉醒后的速度。C. 边缘穿帮修复 (警戒线)原理：#stage 的 background 属性设置了 repeating-linear-gradient。修改颜色：在 CSS #stage 中修改 #ffcc00 (黄) 和 #111 (黑) 可以改变警戒线颜色。📝 5. 快速修改示例场景目标：让角色 "yyc" 在觉醒模式下，镜头右倾，并在屏幕中间显示巨大的红色字“绝望”。代码写法：{
    type: "debate",          // 漂浮大字模式
    mode: "solver",          // 觉醒模式（背景黑红+反向）
    camera: "right",         // 镜头右倾
    char: "yyc",
    emotion: "cool",
    // 使用内联样式自定义字体颜色和大小
    text: "<span style='color: red; font-size: 5rem;'>绝 望</span>",
    shake: true              // 震动强调
}
