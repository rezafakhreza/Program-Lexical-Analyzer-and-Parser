from email.mime import base
from click import option

import requests
import streamlit as tb
from streamlit_lottie import st_lottie

from inspect import stack
import string
from parso import parse

def lexicalAn(sentence):
    input_string = sentence.lower()+'#'

    #intialization
    alphabet_list = list(string.ascii_lowercase)
    state_list = ['q0','q1','q2','q3','q4','q5','q6','q7','q8','q9',
                'q10','q11','q12','q13','q14','q15','q16','q17','q18',
                'q19','q20','q21','q22','q23','q24','q25','q26','q27',
                'q28','q29','q30','q31','q32','q33','q34','q35','q36',
                'q37','q38','q39','q40']

    transition_table = {}

    for state in state_list:
        for alphabet in alphabet_list:
            transition_table[(state,alphabet)] = 'error'
        transition_table[(state, '#')] = 'error'
        transition_table[(state, ' ')] = 'error'

    #spaces berfore input string 
    transition_table['q0',' '] = 'q0'

    #transition final state
    transition_table[('q4', '#')] = 'accept'
    transition_table[('q40', '#')] = 'accept'

    #update the transition table for the following token: ulin
    transition_table[('q0', 'u')] = 'q1'
    transition_table[('q1', 'l')] = 'q2'
    transition_table[('q2', 'i')] = 'q3'
    transition_table[('q3', 'n')] = 'q4'

    #update the transition table for the following token: ngajak
    transition_table[('q0', 'n')] = 'q9'
    transition_table[('q9', 'g')] = 'q5'
    transition_table[('q5', 'a')] = 'q6'
    transition_table[('q6', 'j')] = 'q7'
    transition_table[('q7', 'a')] = 'q8'
    transition_table[('q8', 'k')] = 'q4'

    #update the transition table for the following token: nambut
    transition_table[('q0', 'n')] = 'q9'
    transition_table[('q9', 'a')] = 'q10'
    transition_table[('q10', 'm')] = 'q11'
    transition_table[('q11', 'b')] = 'q12'
    transition_table[('q12', 'u')] = 'q13'
    transition_table[('q13', 't')] = 'q4'

    #update the transition table for the following token: nolak
    transition_table[('q0', 'n')] = 'q9'
    transition_table[('q9', 'o')] = 'q14'
    transition_table[('q14', 'l')] = 'q15'
    transition_table[('q15', 'a')] = 'q8'
    transition_table[('q8', 'k')] = 'q4'

    #update the transition table for the following token: tuang
    transition_table[('q0', 't')] = 'q17'
    transition_table[('q17', 'u')] = 'q18'
    transition_table[('q18', 'a')] = 'q19'
    transition_table[('q19', 'n')] = 'q20'
    transition_table[('q20', 'g')] = 'q4'

    #update the transition table for the following token: motor
    transition_table[('q0', 'm')] = 'q21'
    transition_table[('q21', 'o')] = 'q22'
    transition_table[('q22', 't')] = 'q23'
    transition_table[('q23', 'o')] = 'q24'
    transition_table[('q24', 'r')] = 'q4'

    #update the transition table for the following token: mi
    transition_table[('q0', 'm')] = 'q21'
    transition_table[('q21', 'i')] = 'q4'

    #update the transition table for the following token: konci
    transition_table[('q0', 'k')] = 'q25'
    transition_table[('q25', 'o')] = 'q26'
    transition_table[('q26', 'n')] = 'q27'
    transition_table[('q27', 'c')] = 'q28'
    transition_table[('q28', 'i')] = 'q4'

    #update the transition table for the following token: acis
    transition_table[('q0', 'a')] = 'q29'
    transition_table[('q29', 'c')] = 'q30'
    transition_table[('q30', 'i')] = 'q31'
    transition_table[('q31', 's')] = 'q4'

    #update the transition table for the following token: babaturan
    transition_table[('q0', 'b')] = 'q32'
    transition_table[('q32', 'a')] = 'q33'
    transition_table[('q33', 'b')] = 'q34'
    transition_table[('q34', 'a')] = 'q35'
    transition_table[('q35', 't')] = 'q36'
    transition_table[('q36', 'u')] = 'q37'
    transition_table[('q37', 'r')] = 'q38'
    transition_table[('q38', 'a')] = 'q39'
    transition_table[('q39', 'n')] = 'q4'

    #transition space
    transition_table[('q4', ' ')] = 'q40'
    transition_table[('q40', ' ')] = 'q40'

    #transition for new token 
    transition_table[('q40', 'u')] = 'q1'
    transition_table[('q40', 'n')] = 'q9'
    transition_table[('q40', 't')] = 'q17'
    transition_table[('q40', 'm')] = 'q21'
    transition_table[('q40', 'k')] = 'q25'
    transition_table[('q40', 'a')] = 'q29'
    transition_table[('q40', 'b')] = 'q32'

    #lexical analysis
    idx_char = 0
    state = 'q0'
    current_token = ''
    print(input_string)
    while state != 'accept':
        current_char = input_string[idx_char]
        current_token += current_char
        state = transition_table[(state, current_char)]
        if state == 'q4':
            #print('current token: ',current_token, ', valid')
            current_token = ''
        if state == 'error':
            #print('error')
            break
        idx_char += 1

    #conclusion
    if state == 'accept':
        accept = True
        return accept
    else:
        accept = False
        return accept

def parser(kalimat):
    non_terminal = ['S', 'V', 'N']
    terminal = ['ulin', 'nambut', 'tuang', 'nolak', 'ngajak', 'motor', 'acis', 'mi', 'konci', 'babaturan' ]

    tokens = kalimat.lower().split()
    tokens.append('EOS')

    #Definisi Parse Tabel
    parse_table = {}

    #EOS
    parse_table[('S','EOS')] = ['error']
    parse_table[('V','EOS')] = ['error']
    parse_table[('N','EOS')] = ['error']

    #S
    parse_table[('S', 'babaturan')] = ['N', 'V', 'N']
    parse_table[('S', 'motor')] = ['N', 'V', 'N']
    parse_table[('S', 'acis')] = ['N', 'V', 'N']
    parse_table[('S', 'mi')] = ['N', 'V', 'N']
    parse_table[('S', 'konci')] = ['N', 'V', 'N']
    parse_table[('S', 'ulin')] = ['error']
    parse_table[('S', 'nambut')] = ['error']
    parse_table[('S', 'tuang')] = ['error']
    parse_table[('S', 'nolak')] = ['error']
    parse_table[('S', 'ngajak')] = ['error']

    #N
    parse_table[('N', 'babaturan')] = ['babaturan']
    parse_table[('N', 'motor')] = ['motor']
    parse_table[('N', 'acis')] = ['acis']
    parse_table[('N', 'mi')] = ['mi']
    parse_table[('N', 'konci')] = ['konci']
    parse_table[('N', 'ulin')] = ['error']
    parse_table[('N', 'nambut')] = ['error']
    parse_table[('N', 'tuang')] = ['error']
    parse_table[('N', 'nolak')] = ['error']
    parse_table[('N', 'ngajak')] = ['error']

    #V
    parse_table[('V', 'babaturan')] = ['error']
    parse_table[('V', 'motor')] = ['error']
    parse_table[('V', 'acis')] = ['error']
    parse_table[('V', 'mi')] = ['error']
    parse_table[('V', 'konci')] = ['error']
    parse_table[('V', 'ulin')] = ['ulin']
    parse_table[('V', 'nambut')] = ['nambut']
    parse_table[('V', 'tuang')] = ['tuang']
    parse_table[('V', 'nolak')] = ['nolak']
    parse_table[('V', 'ngajak')] = ['ngajak']

    #inisiasi stack
    stack = []
    stack.append('#')
    stack.append('S')

    #Main Program

    #input reading initializatio 
    Index_token = 0
    symbol = tokens[Index_token]



    try :
        while (len(stack) > 0):
            top = stack[len(stack)-1]
            #print("top = ", top)
            #print("symbol = ", symbol)
    
            if top in terminal:
                #print("Top merupakan simbol terminal")
                
                if top == symbol:
                    stack.pop()
                    Index_token +=1
                    symbol = tokens[Index_token]
                    if symbol == "EOS":
                        #print("isi stack:", stack)
                        stack.pop()
                else:
                    print("error")
                    break
            elif top in non_terminal:
                #print("Top adalah simbol non-terminal")
                if parse_table[(top, symbol)][0] != "error":
                    stack.pop()
                    symbols_to_be_pushed = parse_table[(top, symbol)]
                    for i in range(len(symbols_to_be_pushed)-1, -1, -1):
                        stack.append(symbols_to_be_pushed[i])
                else:
                    #print("error")
                    break
            else:
                #print("error")
                break
            #print("Isi stack = ", stack)
            #print()

        if (symbol == 'EOS') and (len(stack) == 0):
            tb.write("Validasi Kata Dalam Kalimat : '", kalimat, "' terdapat atau sesuai dalam list kata :heavy_check_mark:")
            tb.write("Kalimat : '", kalimat, "' diterima oleh grammar :heavy_check_mark:")
        else:
            tb.write("Validasi Kata Dalam Kalimat : '", kalimat, "' terdapat atau sesuai dalam list kata :heavy_check_mark:")
            tb.write("Kalimat : '", kalimat, "' tidak sesuai grammar :x:")

    except:
        print("Kata Dalam Kalimat Tidak Terdapat Dalam List Kata :(")


tb.set_page_config(page_title="Tugas Besar TBA", page_icon=":computer:", layout="wide")

def load_lottieurl(url):
    i = requests.get(url)
    if i.status_code != 200:
        return None
    else:
        return i.json()

animasi = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_hgp6wzzw.json")
halo = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_3vbOcw.json")
animasithanks = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_totrpclr.json")
programer = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_1LhsaB.json")

with tb.container():
    left, right = tb.columns(2)

    with left:
        tb.title("Program TUBES TBA :snowman:")
        tb.title("Lexical Analyzer & Parser (BAHASA SUNDA)")
        tb.write("---")
        tb.subheader("Subject :sunny:")
        tb.write("Babaturan")
        tb.write("---")
        tb.subheader("Verb :umbrella:")
        tb.write ("Ulin, Nambut, Tuang, Nolak, Ngajak")
        tb.write("---")
        tb.subheader("Object :snowflake:")
        tb.write("Motor, Acis, Mi, Konci")
    
    tb.write("---")    
    with right:
        st_lottie(animasi, height=700, key="coding")

with tb.container():

    left, right = tb.columns(2)

    with left :
        st_lottie(halo, height=350, key="hello")

    with right :
        tb.subheader("SILAHKAN MASUKKIN INPUTAN KALIMAT SESUAI LIST KATA DIATAS YAA :purple_heart: ")
        tb.write("ATURAN KATA UNTUK KALIMATNYA : SUBJECK/OBJECT, VERB, SUBJECT/OBJECT")

        title = tb.text_input(" ")

        if title != "":
            accept = lexicalAn(title)

            if accept == True:
                parser(title)
            else:
                tb.write("KATA DALAM KALIMAT TIDAK TERDAPAT PADA LIST KATA :confused: ")

    tb.write("---")

with tb.container():

    left, mid, right = tb.columns(3)
    
    with mid :
        tb.header("This Website Made By")
    tb.write("---")

with tb.container():

    kolom1, kolom2 = tb.columns(2)

    with kolom1:
        tb.subheader("Famardi Putra Muhammad R. (1301204391) ")
        tb.write("as PROGRAMMER :innocent: ")

        tb.subheader("Rafli Muhamad Fakhreza (1301204006)  ")
        tb.write("as WEB DESIGNER :yum: ")
       

        tb.subheader("Muhammad Daffa’ Ibrahim (1301204051) ")
        tb.write("as PROGRAMMER :sunglasses: ")

    with kolom2 :
        st_lottie(programer, height=300, key="programmer")
    tb.write("---")

    st_lottie(animasithanks, height=600, key="thank you")

    tb.write("---")
    tb.write("---")



