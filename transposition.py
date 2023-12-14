#transposition.py

import random

Key_size = 0
Key_size = int(Key_size)


''' 
function : 문자열 끝의 의미없는 '&' 문자열을 지움
input : 문자열
output : 끝의 '&' 문자열이 지워진 문자열
'''
def Delete_(Input_string):
    idx = len(Input_string) - 1
    while idx >= 0 and Input_string[idx] == '&':
        idx -= 1

    return Input_string[:idx+1]



''' 
function : 0~99 사이의 난수로 키를 만듦
input : None
output : 키 문자열
'''
def Make_key():
    key = ""
    
    # 기존에 나온 난수를 저장할 set
    existing_numbers = set()

    for i in range(0, Key_size):
        while True:
            # 중복된 숫자가 아닌 경우에만 사용
            tmp = random.randint(0, 99)

            # 중복이 아닌 난수가 생성되면 루프 종료
            if tmp not in existing_numbers:
                existing_numbers.add(tmp)
                break
            
        tmp = str(tmp).zfill(2)   
        tmp = int(tmp)
        tmp = chr(tmp)
        key += tmp

    print(key)
    
    return key



''' 
function : 암호화 테이블을 만듦
input : 키 문자열
output : 암호 테이블
'''
def Make_table(key):
    order_list = [0] * Key_size
    ret = [0] * Key_size

    # 주어진 키의 각 문자에 대해 두자리 ASCII 값으로 리스트에 저장
    for i, char in enumerate(key):
        order_list[i] = str(ord(char)).zfill(2)

    # 상대적인 순서로 나열된 리스트 생성
    sorted_order = sorted(order_list)  

    # 키의 각 문자에 대하여 [인덱스 : 문자가 문장에서 나온 순서, 값 : 문자의 상대적 순서] 인 리스트 생성
    for i in range(0, Key_size):
        ret[i] = sorted_order.index(order_list[i])

    return ret



''' 
function : 파일을 읽고 암호화 파일을 생성함
input : 파일경로, 암호화 테이블
output : None
'''
def Encryption(filename, O_list):
    E_code = ""
    buf = dict()

    try:
        with open(filename, 'r') as file:
            text = file.read()

    except FileNotFoundError:
        print("Can't open a file")
        return

    File_size = len(text)
    For_range = int(File_size / Key_size)
    
    if File_size % Key_size != 0:
        For_range+=1
        
    for i in range(0, For_range):
        for j in range(0, Key_size):
            # 파일이 끝났을 경우 암호화를 위하여 끝에 '&' 추가;
            if 12*i+j >= len(text):
                buf[O_list[j]] = '&'

            else:
                buf[O_list[j]] = text[12*i+j]

        # key의 상대적 순서로 암호화 코드 추가
        for k in range(0, Key_size):
            E_code += buf.pop(k)

    with open('Encryped_file.txt', 'w') as file:
        file.write(E_code)

    return



''' 
function : 암호화 파일을 읽고 복호화 파일을 생성함
input : 파일경로, 암호화 테이블
output : None
'''
def Decryption(filename, O_list):
    result = ""
    buf = dict()    

    # Decode를 위한 순서 리스트 재생성
    D_list = [0] * Key_size

    for i in range(0, Key_size):
        D_list[i] = O_list.index(i)

    try:
        with open(filename, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print("Can't open a file")
        return

    File_size = len(text)
    For_range = int(File_size / Key_size)
    
    for i in range(0, For_range):
        for j in range(0, Key_size):
            buf[D_list[j]] = text[12*i+j]

        # D_list로 복호화 문자 추가
        for k in range(0, Key_size):
            result += buf.pop(k)

    D_code = Delete_(result)

    with open('Decryped_file.txt', 'w') as file:
        file.write(D_code)

    return    



#Main 함수
def Main():
    print("Write a file path")
    file_path = input()

    print("Your key is ")
    key = Make_key()
    table = Make_table(key)
    
    Encryption(file_path, table)
    file_path = r"C:\Users\p\Desktop\Encryped_file.txt"
    Decryption(file_path, table)


Main()
