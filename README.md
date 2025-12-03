# Morse-Decoder
Morse_Decoder

📡 Morse Decoder - CTF专用简化版

🚀 使用示例 基本用法 bash 直接解码摩斯电码 python morse_decoder.py "...- -.-- / --. ..- -.." 或使用可执行文件 ./morse_decoder.py ".... . .-.. .-.. --- / --·· --··" 实际输出示例

标准字面解码: VY GUD

无线电上下文解码: [VY=VERY] [GUD=GOOD]

无线电简写: • GUD = GOOD • VY = VERY

推测的flag格式 (尝试这些!): flag{vygud} flag{verygood} CTF实战用例 bash 案例1: 包含73 (Best regards) - 常见flag结尾 python morse_decoder.py "--·· --··"

输出:

标准字面解码: EE

无线电上下文解码: [73=Best regards] [73=Best regards]

无线电简写: • 73 = Best regards

推测的flag格式 (尝试这些!): flag{ee} flag{bestregardsbestregards} flag{_73}

bash 案例2: 复杂序列 (SOS + VY + GUD + 73) python morse_decoder.py "... --- ... / ...- -.-- / --. ..- -.. / --·· --··"

输出:

标准字面解码: SOS VY GUD EE

无线电上下文解码: SOS [VY=VERY] [GUD=GOOD] [73=Best regards] [73=Best regards]

无线电简写: • 73 = Best regards • GUD = GOOD • VY = VERY

推测的flag格式 (尝试这些!): flag{sosvygudee} flag{sosverygoodbestregardsbestregards} flag{sosvery_good_73} 📋 输出说明

脚本输出严格遵循以下四部分格式：

    标准字面解码 基础摩斯电码到字母的直接转换 保留原始空格结构 未知字符标记为 [?character?]
    无线电上下文解码 识别无线电简写（VY, GUD, 73等） 格式: [简写=含义] 未识别部分保持原样
    无线电简写 列出所有检测到的简写及其含义 每行格式: • 简写 = 含义 无简写时显示 (无检测到的简写)
    推测的flag格式 基于解码内容智能生成flag建议 优先考虑无线电含义（VY→VERY, GUD→GOOD） 处理常见CTF模式（73结尾、SOS开头等） 无推测时显示 (无推测的flag格式) 🛠️ 技术细节 支持的无线电简写 简写 含义 摩斯码

VY VERY ...- -.-- GUD GOOD --. ..- -.. 73 Best regards --·· 88 Love and kisses ---· SOS Emergency ... --- ... CQ Calling any station -.-. --.- DE From -.. . ES And . ... Flag推测逻辑

    基础转换：移除非字母数字字符，转换为小写
    简写替换：VY→VERY, GUD→GOOD, 73→_73
    模式识别： 73结尾 → flag{content_73} SOS开头 → flag{sos_content} Q代码 → QCODE{content} 🤝 贡献指南

发现新的CTF常用简写？欢迎贡献！

    Fork此仓库
    修改self.radio_shorthands字典添加新简写
    提交Pull Request 📜 许可证

MIT License - 免费用于个人和商业项目

提示：在CTF比赛中，当看到--··时，记住它通常是73（Best regards）而不是EE！ 记住口诀： "VY不是VY，是VERY！ GUD不是GUD，是GOOD！ --··不是EE，是73！"
