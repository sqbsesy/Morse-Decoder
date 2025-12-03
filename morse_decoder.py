
import re
import argparse
import sys

class MorseDecoder:
    def __init__(self):
        # 标准摩斯电码表 (国际标准)
        self.morse_code = {
            # 字母
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z',
            # 数字
            '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
            '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0',
            # 标点符号
            '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!',
            '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&', '---...': ':',
            '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-', '..--.-': '_',
            '.-..-.': '"', '...-..-': '$', '.--.-.': '@',
            # 特殊信号
            '...---...': 'SOS', '-.-': 'K', '.-.-.': 'AR', '-...-': 'BT',
            '.-...': 'AS', '........': 'ERROR'
        }
        
        # 无线电简语和Q代码
        self.radio_shorthands = {
            # 业余无线电简写
            'VY': 'VERY',                   # ...- -.--
            'GUD': 'GOOD',                  # --. ..- -..
            'OM': 'Old Man',
            'YL': 'Young Lady',
            'ES': 'And',
            'DE': 'From',
            'PSE': 'Please',
            'TNX': 'Thanks',
            'HW': 'How',
            'CP': 'Can copy',
            'CUAGN': 'See you again',
            'R': 'Received',
            'CQ': 'Calling any station',
            'CL': 'Closing station',
            'BK': 'Break',
            'VA': 'End of contact',
            'SK': 'Silent key',
            
            # 数字简语
            '73': 'Best regards',           # --··
            '88': 'Love and kisses',        # ---·
            '92': 'Yours sincerely',
            '30': 'No more, end of message',
        }

    def decode_standard(self, morse_str):
        """标准摩斯电码解码（字面值）"""
        # 标准化输入
        morse_str = morse_str.strip()
        morse_str = re.sub(r'[·•]', '.', morse_str)  # 统一点符号
        morse_str = re.sub(r'[\-—]', '-', morse_str)  # 统一划符号
        morse_str = re.sub(r'\s+', ' ', morse_str)   # 合并空格
        
        # 分割单词
        words = re.split(r'\s{2,}|/', morse_str)
        decoded_words = []
        
        for word in words:
            if not word:
                continue
            chars = word.split()
            decoded_chars = []
            
            for char in chars:
                if char in self.morse_code:
                    decoded_chars.append(self.morse_code[char])
                else:
                    decoded_chars.append(f"[{char}?]")
            
            decoded_word = ''.join(decoded_chars)
            decoded_words.append(decoded_word)
        
        return ' '.join(decoded_words)

    def decode_with_context(self, morse_str):
        """上下文感知解码 - 优先考虑无线电含义"""
        standard_decode = self.decode_standard(morse_str)
        upper_decode = standard_decode.upper()
        
        # 检测简写
        detected_shorthands = {}
        context_decode = upper_decode
        
        # 应用简写替换
        for shorthand, meaning in self.radio_shorthands.items():
            if re.search(r'\b' + re.escape(shorthand) + r'\b', context_decode):
                detected_shorthands[shorthand] = meaning
                context_decode = re.sub(r'\b' + re.escape(shorthand) + r'\b', f"[{shorthand}={meaning}]", context_decode)
        
        return {
            'standard': standard_decode,
            'contextual': context_decode,
            'detected_shorthands': detected_shorthands,
        }
    
    def _generate_flag_guesses(self, results):
        """基于解码结果生成可能的flag猜测"""
        guesses = []
        standard = results['standard'].upper()
        contextual = results['contextual']
        
        # 基础处理：移除非字母数字字符
        clean_text = re.sub(r'[^A-Z0-9]', '', standard)
        
        # 生成基本flag
        if clean_text:
            guesses.append(f"flag{{{clean_text.lower()}}}")
        
        # 特别处理VY和GUD
        if "VY" in standard or "GUD" in standard:
            replaced = standard.replace("VY", "VERY").replace("GUD", "GOOD")
            clean_replaced = re.sub(r'[^A-Z0-9]', '', replaced)
            if clean_replaced:
                guesses.append(f"flag{{{clean_replaced.lower()}}}")
        
        # 检测73结尾
        if "73" in contextual:
            base = re.sub(r'73\b.*', '', standard)
            clean_base = re.sub(r'[^A-Z0-9]', '', base)
            if clean_base:
                guesses.append(f"flag{{{clean_base.lower()}_73}}")
        
        # 去重
        return list(dict.fromkeys(guesses))

    def print_results(self, results):
        """打印简化版解码结果"""
        # 1. 标准字面解码
        print(f"标准字面解码:")
        print(f"   {results['standard']}\n")
        
        # 2. 无线电上下文解码
        print(f"无线电上下文解码:")
        print(f"   {results['contextual']}\n")
        
        # 3. 无线电简写
        print(f"无线电简写:")
        if results['detected_shorthands']:
            for shorthand, meaning in results['detected_shorthands'].items():
                print(f"   • {shorthand} = {meaning}")
        else:
            print("   (无检测到的简写)")
        print()
        
        # 4. 推测的flag格式
        flag_guesses = self._generate_flag_guesses(results)
        print(f"推测的flag格式 (尝试这些!):")
        if flag_guesses:
            for guess in flag_guesses:
                print(f"   - {guess}")
        else:
            print("   (无推测的flag格式)")

def main():
    parser = argparse.ArgumentParser(description='摩斯电码智能解码器 - 简化输出版')
    parser.add_argument('input', help='摩斯电码字符串 (例如: "...- -.-- / --. ..- -..")')
    
    args = parser.parse_args()
    decoder = MorseDecoder()
    
    # 执行解码
    results = decoder.decode_with_context(args.input)
    
    # 打印简化结果
    decoder.print_results(results)

if __name__ == "__main__":
    main()
