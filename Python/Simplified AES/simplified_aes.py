import numpy as np
ptext=0b1101011100101000
key  =0b0100101011110101
ctext=0b0010010011101100

rcon1=0b10000000
rcon2=0b00110000
w0=w1=w2=w3=w4=w5=None
 
# S-Box
sBox  = [0x9, 0x4, 0xa, 0xb,
         0xd, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3,
         0xc, 0xe, 0xf, 0x7]
 
# Inverse S-Box
sBoxI = [0xa, 0x5, 0x9, 0xb, 
         0x1, 0x7, 0x8, 0xf,
         0x6, 0x0, 0x2, 0x3, 
         0xc, 0x4, 0xd, 0xe]

def split_nibbles(input_stream):
    high=input_stream>>8
    low=input_stream&0x0ff
    nibble1=high>>4
    nibble2=high&0x0f
    nibble3=low>>4
    nibble4=low&0x0f
    return([nibble1,nibble2,nibble3,nibble4])

def column_matrix(lst):
    temp=lst[1]
    lst[1]=lst[2]
    lst[2]=temp
    lst_vector=np.resize(np.array(lst),(2,2))
    return (lst_vector)
    
def switch_rows(lst):
    temp=lst[1,0]
    lst[1,0]=lst[1,1]
    lst[1,1]=temp
    return lst

def mult(p1, p2):
    p = 0
    while p2:
        if p2 & 0b1:
            p ^= p1
        p1 <<= 1
        if p1 & 0b10000:
            p1 ^= 0b11
        p2 >>= 1
    return p & 0b1111


    

def mix_columns(lst):
    return np.resize(np.array([lst[0,0] ^ mult(4, lst[1,0]),
                               lst[0,1] ^ mult(4, lst[1,1]),
                               lst[1,0] ^ mult(4, lst[0,0]),
                               lst[1,1] ^ mult(4, lst[0,1])]),(2,2))
def inv_mix_columns(lst):
    return np.resize(np.array([mult(9, lst[0,0]) ^ mult(2, lst[1,0]),
                               mult(9, lst[0,1]) ^ mult(2, lst[1,1]),
                               mult(9, lst[1,0]) ^ mult(2, lst[0,0]), 
                               mult(9, lst[1,1]) ^ mult(2, lst[0,1])]),(2,2))
def mat_str(lst):
    return ((lst[0,0]<<12)^(lst[1,0]<<8)^(lst[0,1]<<4)^lst[1,1])

def expand_keys(key):
    w0=key>>8
    w1=key&0x0ff
    w2=w0^rcon1^((sBox[w1&0x0f]<<4)^(sBox[w1>>4]))
    w3=w2^w1
    w4=w2^rcon2^((sBox[w3&0x0f]<<4)^(sBox[w3>>4]))
    w5=w3^w4
    return([(w0<<8)^w1,(w2<<8)^w3,(w4<<8)^w5])

    

def encrypt():
    #initializing 
    state_vector=column_matrix(split_nibbles(ptext))
    keys=expand_keys(key)
    k01_matrix=column_matrix(split_nibbles(keys[0]))
    k23_matrix=column_matrix(split_nibbles(keys[1]))
    k45_matrix=column_matrix(split_nibbles(keys[2]))
    #round 0
    state_vector^=k01_matrix
    #round 1
    for i in range(0,2):
        for j in range(0,2):
            state_vector[i,j]=sBox[state_vector[i,j]]       
    state_vector=switch_rows(state_vector)
    state_vector=mix_columns(state_vector)

    state_vector^=k23_matrix


    #round 2

    for i in range(0,2):
        for j in range(0,2):
            state_vector[i,j]=sBox[state_vector[i,j]]

    state_vector=switch_rows(state_vector)

    state_vector^=k45_matrix
    print(state_vector)
    print(bin(mat_str(state_vector)))

def decrypt():
    #initializing 
    state_vector=column_matrix(split_nibbles(ctext))
    keys=expand_keys(key)
    k01_matrix=column_matrix(split_nibbles(keys[0]))
    k23_matrix=column_matrix(split_nibbles(keys[1]))
    k45_matrix=column_matrix(split_nibbles(keys[2]))
    #round 0
    state_vector^=k45_matrix
    #round 1
    state_vector=switch_rows(state_vector)
    for i in range(0,2):
        for j in range(0,2):
            state_vector[i,j]=sBoxI[state_vector[i,j]]       
    state_vector^=k23_matrix


    #round 2
    state_vector=inv_mix_columns(state_vector)
    state_vector=switch_rows(state_vector)

    for i in range(0,2):
        for j in range(0,2):
            state_vector[i,j]=sBoxI[state_vector[i,j]]

    state_vector^=k01_matrix
    print(state_vector)
    print(bin(mat_str(state_vector)))

encrypt()
decrypt()