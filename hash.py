import random
import binascii
import base64
import textwrap

def strtobin(X):
    if len(X)%40 != 0:
        X += chr(40-(len(X)%40))*(40-(len(X)%40))
    
    X_str = bin(int(binascii.hexlify(X.encode()),16))[2:]
    
    if len(X_str)%240 != 0:
        d = len(X_str)//240
        r = d*240
        X_str = X_str[:r]
    
    X_list = textwrap.wrap(X_str,240)
    return(X_list)


def message_schedule(X_list_i):
    
    def shift(s, n):
        return(s[n:] + s[:n])
    
    W = []
    X_list_divided = textwrap.wrap(X_list_i,30)
    
    W.append(X_list_divided[0])
    W.append(X_list_divided[1])
    W.append(X_list_divided[2])
    W.append(X_list_divided[3])
    W.append(X_list_divided[4])
    W.append(X_list_divided[5])
    W.append(X_list_divided[6])
    W.append(X_list_divided[7])
    
    W.append(shift(W[0],1))
    W.append(shift(W[1],-2))
    W.append(shift(W[2],3))
    W.append(shift(W[3],-4))
    W.append(shift(W[4],4))
    W.append(shift(W[5],-3))
    W.append(shift(W[6],2))
    W.append(shift(W[7],-1))
    
    W.append(shift(W[8],1))
    W.append(shift(W[9],-2))
    W.append(shift(W[10],3))
    W.append(shift(W[11],-4))
    W.append(shift(W[12],4))
    W.append(shift(W[13],-3))
    W.append(shift(W[14],2))
    W.append(shift(W[15],-1))
    
    W.append(shift(W[16],1))
    W.append(shift(W[17],-2))
    W.append(shift(W[18],3))
    W.append(shift(W[19],-4))
    W.append(shift(W[20],4))
    W.append(shift(W[21],-3))
    W.append(shift(W[22],2))
    W.append(shift(W[23],-1))
    
    W.append(shift(W[24],1))
    W.append(shift(W[25],-2))
    W.append(shift(W[26],3))
    W.append(shift(W[27],-4))
    W.append(shift(W[28],4))
    W.append(shift(W[29],-3))
    W.append(shift(W[30],2))
    W.append(shift(W[31],-1))
    
    return(W)


def Round_function(ABCD,Kt,Wj,j):
    A = ABCD[0]
    B = ABCD[1]
    C = ABCD[2]
    D = ABCD[3]
    
    def shift(s, n):
        return(s[n:] + s[:n])
    
    def ADD(p,q,r):
        p = int(str(p),2)
        q = int(str(q),2)
        r = int(str(r),2)
        return(str(bin(p+q+r))[3:])
        
    
    def AND(p,q):
        p = int(str(p),2)
        q = int(str(q),2)
        return(str(bin(p&q))[2:])
    
    def OR(p,q):
        p = int(str(p),2)
        q = int(str(q),2)
        return(str(bin(p|q))[2:])
    
    def XOR(p,q):
        p = int(str(p),2)
        q = int(str(q),2)
        return(str(bin(p^q))[2:])
    
    
    def func(a,b,c,d,Kt,Wt,j):
        if j == 0:
            abc = XOR(XOR(AND(a,b),AND(shift(a,7),c)),AND(b,c))
            
        if j == 1:
            abc = XOR(AND(XOR(b,c),OR(shift(c,-21),a)),XOR(shift(b,-16),a))
            
        if j == 2:
            abc = OR(OR(AND(a,b),AND(b,c)),AND(a,c))
        
        if j == 3:
            abc = AND(AND(AND(a,c),OR(shift(b,12),a)),AND(shift(c,13),shift(a,-10)))
    
        d1 = ADD(d,abc,shift(Kt,-15))
        d2 = ADD(shift(c,5),d1,Wj)
        d3 = ADD(shift(a,-5),d2,shift(Wj,15))
        d4 = ADD(shift(b,-10),d3,Kt)
        
        return(d4)
    
    A = func(A,B,C,D,Kt,Wj,j)
    B = shift(A,13)
    C = shift(B,-9)
    D = shift(C,21)
    
    ABCD = []
    ABCD.append(A)
    ABCD.append(B)
    ABCD.append(C)
    ABCD.append(D)
    
    return(ABCD)


def RHA(X):
    K1 = "011111000010000011011101011010"  #"7C20DD68" -2 bits 
    K2 = "110110001111100110101000101011"  #"D8F9A8AF" -2 bits
    K3 = "100110011111011000011111010111"  #"99F61F5C" -2 bits
    K4 = "101001111010101100000010110010"  #"A7AB02C9" -2 bits
    Base64 = "ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz0123456789+/"
    Round_constant = []
    Round_constant.append(K1)
    Round_constant.append(K2)
    Round_constant.append(K3)
    Round_constant.append(K4)
    
    IV = K3 + K2 + K4 + K1 
    
    X_list = strtobin(X)

    
    for i in range(len(X_list)):
        W_list = message_schedule(X_list[i])
        
        if i == 0:
            ABCD = textwrap.wrap(IV,30)
        
        else:
            ABCD = textwrap.wrap(Xi_1,30)
        
        for j in range(4):
            count = 0
            for k in range(10):
                Kt = Round_constant[j]
                Wj = W_list[count]
                count += 1
                ABCD = Round_function(ABCD,Kt,Wj,j)
                
            for k in range(10):
                Kt = Round_constant[j]
                Wj = W_list[count]
                count += 1
                ABCD = Round_function(ABCD,Kt,Wj,j)
                
            for k in range(10):
                Kt = Round_constant[j]
                Wj = W_list[count]
                count += 1
                ABCD = Round_function(ABCD,Kt,Wj,j)
                
            for k in range(10):
                Kt = Round_constant[j]
                Wj = W_list[count]
                count += 1
                ABCD = Round_function(ABCD,Kt,Wj,j)
        
        Xi_1 = "".join(ABCD)
        
    H1 = textwrap.wrap(Xi_1,6)
    HASH = ""
    
    for i in range(len(H1)):
        HASH += Base64[int(H1[i],2)]
        
    HASH = binascii.hexlify(HASH.encode())
    
    print("Hash:",HASH.decode())
    
Message = input("Enter message to calculate its hash: ")
RHA(str(Message))