# -*- coding: UTF-8 -*-

import os
import re
import sys
import requests

from loguru import logger

PWD = os.getcwd()

headers = {
    "User-Agent" : "Mozilla/5.0 (Shining v0.1) ",
}

def banner():
    COLOR = '\033[32m'
    print(f'''
    {COLOR}
   ▄████████    ▄█    █▄     ▄█  ███▄▄▄▄    ▄█  ███▄▄▄▄      ▄██████▄  
  ███    ███   ███    ███   ███  ███▀▀▀██▄ ███  ███▀▀▀██▄   ███    ███ 
  ███    █▀    ███    ███   ███▌ ███   ███ ███▌ ███   ███   ███    █▀  
  ███         ▄███▄▄▄▄███▄▄ ███▌ ███   ███ ███▌ ███   ███  ▄███        
▀███████████ ▀▀███▀▀▀▀███▀  ███▌ ███   ███ ███▌ ███   ███ ▀▀███ ████▄  
         ███   ███    ███   ███  ███   ███ ███  ███   ███   ███    ███ 
   ▄█    ███   ███    ███   ███  ███   ███ ███  ███   ███   ███    ███ 
 ▄████████▀    ███    █▀    █▀    ▀█   █▀  █▀    ▀█   █▀    ████████▀  
                                                                       
                    Author: xxxeyJ & Search?=Null
''')

def main(chain, target):
    chain = search(chain)
    target = check(target)
    try:
        res = requests.get(f"https://{chain}/address/{target}#code", headers=headers).text
        code_pattern = re.compile(r"<pre class='js-sourcecopyarea editor' id='editor\d+' style='margin-top: 5px;'>(.*?)</pre>", re.S)
        filename_pattern = re.compile(r"File \d+ of \d+ : (.*?)</span>")
        contract_name = re.search(r"Contract Name.*?<span.*?>(.*?)</span>", res, re.S).group(1)
        source_codes = code_pattern.findall(res)
        filenames = filename_pattern.findall(res)
        output_path = os.path.join(PWD, contract_name)
    except Exception as e:
        logger.error(e)

    if not os.path.exists(output_path):
        os.mkdir(output_path)
        print(f"[#] The {contract_name} directory has been created.")
    
    for code, filename in zip(source_codes, filenames):
        with open(os.path.join(output_path, filename), "w") as fp:
            print(f"[+] Download {filename}...")
            fp.write(code)
        
    print(f"[#] {contract_name} smart contract code downloaded successfully.\n")

def search(chain):
    chains = dict(eth = "etherscan.io", bsc = "bscscan.com")
    if chain in chains:
        return(chains.get(chain))
    else:
        print("[-] Currently only supported on the ETH/BSC blockchain.\n")
        sys.exit(0)

def check(target):
    if len(target) == 42:
        return target
    else:
        print("[-] The account address of the EVM starts with 0x and is 20 bytes long.\n")
        sys.exit(0)

if __name__== "__main__":
    banner()
    if len(sys.argv) != 3:
        print("Usage: python3 Shining.py Chain Address.")
        sys.exit(0)
    elif len(sys.argv) == 3:
        chain = str(sys.argv[1])
        target = str(sys.argv[2])
        main(chain, target)