from typing import List
from selenium import webdriver
import json


def word_to_byte_array(word_array: List[int]) -> List[int]:
    result = []
    for word in word_array:
        for j in range(3, -1, -1):
            result.append((word >> 8 * j) & 0xff)
    return result


def byte_array_to_string(byte_arr: List[int]) -> str:
    result = ""
    for b in byte_arr:
        result += chr(b)
    return result


def main():
    config = {}
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get("https://www.manhuabei.com/manhua/DrSTONE/556042.html")
    iv_word_array = driver.execute_script('''var _0x353aae = {
            'TOtFq': _0x4936('22', 'CA]!')
        };return CryptoJS[_0x4936('2b', '#!#H')][_0x4936('2c', '7vBr')]['parse'](_0x353aae[_0x4936('2d', 'OO8Z')]);''')
    passphase_word_array = driver.execute_script(
        "return CryptoJS['enc'][_0x4936('2e', '5iKm')][_0x4936('2f', 'cFEf')](_0x4936('30', 'eo!$'));")
    config['iv'] = byte_array_to_string(word_to_byte_array(iv_word_array['words']))
    config['passphase'] = byte_array_to_string(
        word_to_byte_array(passphase_word_array['words']))
    with open('config/manhuabei_decrypt_config.json', 'w') as f:
        json.dump(config, f)
    
    driver.close()


if __name__ == "__main__":
    main()
