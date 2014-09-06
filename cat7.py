#! /usr/bin/env python

#in this version the array refers the origin data string

import sys
sys.path.append('./')
import grph
import copy
import time

def match2(array,index0,currentlv,lvsto):
    dict2 = {'A':'U','U':'A','G':'C','C':'G'}
    base0 = array[index0]
    wlii = 1
    waitsto = [[index0,base0]]
    ind0tp = index0
    while True:
        base1 = array[index0+wlii]
        ind1tp = index0 + wlii
        if base1 == dict2.get(base0):
            if len(waitsto) == 1:
                return(index0+wlii,currentlv)
            else: #mvout
                if currentlv not in lvsto:
                    lvsto[currentlv] = {data[ind0tp]:[ind0tp,ind1tp]} #there is no more one pair of brackets for isolating matched base so that the base can quickly switch.
                elif data[ind0tp] not in lvsto[currentlv]:
                    lvsto[currentlv][data[ind0tp]] = [ind0tp,ind1tp]
                else:
                    lvsto[currentlv][data[ind0tp]].append(ind0tp)
                    lvsto[currentlv][data[ind0tp]].append(ind1tp)
                del(waitsto[-1])
                ind0tp = waitsto[-1][0]
                base0 = waitsto[-1][1]
                wlii += 1
                currentlv -= 1
        else: #mvin
            waitsto.append([index0+wlii,base1])
            base0 = base1
            ind0tp = index0 + wlii
            wlii += 1
            currentlv += 1

def match3(array,index0,index1,currentlv,count,sto2_i=[]): #add check point as None
    dict2 = {'A':'U','U':'A','G':'C','C':'G'}
    waitsto = [[index0,array[index0]]]
    if index1 != 0:
        waitsto.append([index1,array[index1]])
        ind0tp = index1
        base0 = array[index1]
    else:
        ind0tp = index0
        base0 = array[index0]
    treelv = currentlv
    ind1tp = ind0tp + 1
    if ind1tp in sto2_i:
        return None
    elif ind1tp == len(array):
        return None
    base1 = array[ind1tp]
    while True:
        if base1 == dict2.get(base0):
            if len(waitsto) == 1:
                return(ind1tp)
            else: #mvout
                del(waitsto[-1])
                ind0tp = waitsto[-1][0]
                base0 = waitsto[-1][1]
                ind1tp = ind1tp + 1
                if ind1tp in sto2_i:
                    return None
                elif ind1tp == len(array):
                    return None
                base1 = array[ind1tp]
                treelv -= 1
        else: #mvin
            waitsto.append([ind1tp,base1])
            ind0tp = ind1tp
            base0 = base1
            ind1tp = ind0tp + 1
            if ind1tp in sto2_i:
                return None
            elif ind1tp == len(array):
                return None
            base1 = array[ind1tp]
            treelv += 1

def count1(lvsto_i_j): #count and sto current lv current base temp string
    ctstotp = [] #the data is like [[(0,1),(2,3),...], [(0,3),(1,2),...], ...]
    ctstotp2 = []
    wli = 0
    for i in range(len(lvsto_i_j)//2):
        lvstotp = copy.copy(lvsto_i_j)
        lvstotp[1], lvstotp[i*2+1] = lvstotp[i*2+1], lvstotp[1]
        lvstotp[i*2+1], lvstotp[i*2] = lvstotp[i*2], lvstotp[i*2+1]
        ctstotp.append(lvstotp)
    #print('ctstotp: ', ctstotp) ##tft
    #abstract the string as 012345, 0 has matched.
    for i in range(len(lvsto_i_j)-2): #like 1234
        print ('i', i) ##tft
        for j in range(len(lvsto_i_j)//2 - 1 - wli//2): #like 1 matches to 24, 3 matches to 4, so the range is 2211.
            #print('j: ', j) ##tft
            #print('ctstotp: ', ctstotp) ##tft
            #print('ctstotp2: ', ctstotp2) ##tft
            for ii in range(len(ctstotp)):
                for jj in ctstotp[ii][::-1]:
                    if lvsto_i_j[i+1] == jj[1] or lvsto_i_j[i+1+j*2+1] == jj[1]:
                        if ctstotp[ii] not in ctstotp2:
                            ctstotp2.append(copy.copy(ctstotp[ii]))
                        break
                    elif lvsto_i_j[i+1] < jj[1] and lvsto_i_j[i+1+j*2+1] > jj[1]:
                        #ctstotp2.append(copy.copy(ctstotp[ii]))
                        break
                    elif lvsto_i_j[i+1] > jj[1] and lvsto_i_j[i+1+j*2+1] > jj[1]:
                        if jj != ctstotp[ii][0]:
                            continue
                        else:
                            #print('ctstotp_ii: ', ctstotp[ii]) ##tft
                            #print('ind0,ind1: ', lvsto_i_j[i+1],lvsto_i_j[i+1+j*2+1]) ##tft
                            ctstotp2.append(copy.copy(ctstotp[ii]))
                            ctstotp2[-1].append((lvsto_i_j[i+1],lvsto_i_j[i+1+j*2+1]))
                            break #not running, just as a mark
                    else: #lvsto_i_j[i+1] < jj[i] and lvsto_i_j[i+1+j*2+1] < jj[1]
                        #print('ctstotp_ii, ii: ', ctstotp[ii], ii) ##tft
                        #print('ind0,ind1: ', lvsto_i_j[i+1],lvsto_i_j[i+1+j*2+1]) ##tft
                        ctstotp2.append(copy.copy(ctstotp[ii]))
                        ctstotp2[-1].append((lvsto_i_j[i+1],lvsto_i_j[i+1+j*2+1]))
                        break
        ctstotp = copy.copy(ctstotp2)
        #print('ctstotp2: ',ctstotp2) ##tft
        ctstotp2 = []
        wli += 1
    #print('lvsto_0_U: ', lvsto[0]['U']) ##tft
    return(ctstotp)

if __name__ == '__main__':
    data = grph.formatindict()
    data = data[0][1] #the string of base
    au = ['A','U'] ; cg = ['C','G']
    sto = [] #sto matchable intern string, the data is like [[index0,index1,currentlv,count], ...]
    count = 0
    currentlv = 0
    index0 = 0
    lvsto = {} #lvsto is to store matched bases in different level, the data is like {0:{'A':[(0,1),...],'U':[...]} ,1:{...},...}
    while True:
        matchtp = match2(data,index0,currentlv,lvsto)
        index1 = matchtp[0]
        currentlv = matchtp[1]
        if currentlv not in lvsto:
            lvsto[currentlv] = {data[index0]:[index0,index1]}
        elif data[index0] not in lvsto[currentlv]:
            lvsto[currentlv][data[index0]] = [index0,index1]
        else:
            lvsto[currentlv][data[index0]].append(index0)
            lvsto[currentlv][data[index0]].append(index1)
        index0 = index1 + 1
        if index0 == len(data):
            break
    #print('lvsto: ',lvsto) ##tft
    xtime = time.time()
    print(count1(lvsto[0]['A'])) ##tft
    print ('timecost: ',time.time() - xtime)
