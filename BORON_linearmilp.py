__author__ = 'lv'

from math import *
from copy import *
from CryptoMIP import *

Sbox_Template=[(0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 1),\
(-2, 0, 1, -2, 0, 1, 1, 0, 2, 4, 0),\
(1, 0, 0, 1, 1, 2, 2, 0, -2, 0, 0),\
(-1, 0, 0, -1, 1, -2, -2, 0, 4, 6, 0),\
(2, 0, 1, 2, 0, -1, -1, 0, 0, 2, 0),\
(-1, 0, -2, 1, -1, 1, -1, 0, 4, 5, 0),\
(1, 0, -1, -2, -1, -1, 1, 0, 4, 5, 0),\
(0, 0, -2, -1, 3, -3, 1, -2, 8, 5, 0),\
(-5, -1, -4, 2, -3, -4, 3, 0, 15, 10, 0),\
(-1, -9, 2, -5, -4, -3, 4, -6, 27, 19, 0),\
(1, -7, -2, -5, -8, 3, -3, -4, 28, 19, 0),\
(3, 0, 8, 3, 6, -1, -1, 4, -7, -5, 0),\
(11, 12, 2, 4, 3, 5, 10, 6, -7, -20, 0),\
(-3, 0, 4, -2, 3, 2, 1, -3, 3, 4, 0),\
(-1, 2, -7, -1, 4, 6, -3, 2, 12, 5, 0),\
(-3, 2, 4, 4, -5, -1, -1, 1, 10, 4, 0),\
(3, -1, -3, -4, -4, 2, -5, 0, 15, 10, 0)]

class BORON_linearmilp():
    def __init__(self):
        self.Keysize=128
        self.Blocksize=64

    def genVars_SBox_In(self,r):
        return ['SBIn_r'+str(r)+'_'+str(i) for i in range(self.Blocksize)]
    def genVars_SBox_Out(self,r):
        return ['SBOut_r'+str(r)+'_'+str(i) for i in range(self.Blocksize)]
    def genVars_Branch0_another(self,r):
        return ['B0another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Branch0_down(self,r):
        return ['B0down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Xor1_down(self,r):
        return ['X1down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Branch1_another(self,r):
        return ['B1another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Xor2_down(self,r):
        return ['X2down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Branch2_another(self,r):
        return ['B2another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Branch3_another(self,r):
        return ['B3another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_Branch3_down(self,r):
        return ['B3down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]

    #def genVars_ActiveSBox_In(self,r):
    #    return ['S'+str(r)+'_'+str(i) for i in range(0,32)]
    #密钥恢复阶段
    #前向决定关系
    def genVars_RK(self,r):
        return ['roundkey_'+str(r)+'_'+str(i) for i in range(self.Blocksize)]
    def genVars_cutting_guessed_subkey(self, r):
        return ['CSK_'+str(r)+'_'+str(i) for i in range(self.Blocksize)]
    def genVars_KeyM_AK_In(self,r):
        return ['KMAKIn_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyM_SBox_In(self,r):
        return ['KMSBIn_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyM_SBox_Out(self,r):
        return ['KMSBOut_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyM_Branch0_another(self,r):
        return ['KMB0another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Branch0_down(self,r):
        return ['KMB0down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Xor1_down(self,r):
        return ['KMX1down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Branch1_another(self,r):
        return ['KMB1another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Xor2_down(self,r):
        return ['KMX2down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Branch2_another(self,r):
        return ['KMB2another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Branch3_another(self,r):
        return ['KMB3another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyM_Branch3_down(self,r):
        return ['KMB3down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]


    #后向决定关系
    def genVars_KeyW_AK_In(self,r):
        return ['KWAKIn_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyW_AK_Out(self,r):
        return ['KWAKOut_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyW_SBox_In(self,r):
        return ['KWSBIn_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyW_SBox_Out(self,r):
        return ['KWSBOut_'+str(j)+'_r'+str(r) for j in range(self.Blocksize)]
    def genVars_KeyW_Branch0_another(self,r):
        return ['KWB0another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Branch0_down(self,r):
        return ['KWB0down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Xor1_down(self,r):
        return ['KWX1down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Branch1_another(self,r):
        return ['KWB1another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Xor2_down(self,r):
        return ['KWX2down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Branch2_another(self,r):
        return ['KWB2another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Branch3_another(self,r):
        return ['KWB3another_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_Branch3_down(self,r):
        return ['KWB3down_r'+str(r)+'_'+str(i) for i in range(self.Blocksize//4)]
    def genVars_KeyW_BO(self,r):
        return ['KWBO_r'+str(r)+'_'+str(i) for i in range(self.Blocksize)]


    #约束输入掩码不全为0
    def genConstraints_InputNonzero(self):
        temp=self.genVars_SBox_In(1)
        temp = ' + '.join(temp)
        temp = temp +" >= 1"
        return temp

    def genConstraints_nibbleshift(self,vars_in):
        vars_out=[0]*self.Blocksize
        for i in range(4):
            vars_out[i+12]=vars_in[i+4]
        for i in range(4):
            vars_out[i+8]=vars_in[i]
        for i in range(4):
            vars_out[i+4]=vars_in[i+12]
        for i in range(4):
            vars_out[i]=vars_in[i+8]
        for i in range(4):
            vars_out[i+28]=vars_in[i+20]
        for i in range(4):
            vars_out[i+24]=vars_in[i+16]
        for i in range(4):
            vars_out[i+20]=vars_in[i+28]
        for i in range(4):
            vars_out[i+16]=vars_in[i+24]
        for i in range(4):
            vars_out[i+44]=vars_in[i+36]
        for i in range(4):
            vars_out[i+40]=vars_in[i+32]
        for i in range(4):
            vars_out[i+36]=vars_in[i+44]
        for i in range(4):
            vars_out[i+32]=vars_in[i+40]
        for i in range(4):
            vars_out[i+60]=vars_in[i+52]
        for i in range(4):
            vars_out[i+56]=vars_in[i+48]
        for i in range(4):
            vars_out[i+52]=vars_in[i+60]
        for i in range(4):
            vars_out[i+48]=vars_in[i+56]
        return vars_out

    def genConstraints_bitrotation(self,vars_in):
        vars_out=[0]*self.Blocksize
        for i in range(16):
            vars_out[i]=vars_in[(i-1)%16]
        for i in range(16):
            vars_out[i+16]=vars_in[(i-4)%16+16]
        for i in range(16):
            vars_out[i+32]=vars_in[(i-7)%16+32]
        for i in range(16):
            vars_out[i+48]=vars_in[(i-9)%16+48]
        return vars_out


    #输出的值为相关性的指数*-1
    def genObjectiveFun_to_Round(self,r):
        assert (r>=1)
        C=list([])
        C1=list([])
        for i in range(1, r+1):
            for j in range(0, self.Blocksize//4):
                C.append('p0_' + str(i) + '_' + str(j))
        C=' + '.join(C)
        for i in range(1, r+1):
            for j in range(0, self.Blocksize//4):
                C1.append('p1_' + str(i) + '_' + str(j))
        C1=' + 2 '.join(C1)
        C=C+' + 2 '+C1
        return C


    def genConstraints_R(self,r):
        assert (r>=1)
        C=list([])
        SBIn=self.genVars_SBox_In(r)
        SBOut=self.genVars_SBox_Out(r)
        B0a=self.genVars_Branch0_another(r)
        B0d=self.genVars_Branch0_down(r)
        X1d=self.genVars_Xor1_down(r)
        B1a=self.genVars_Branch1_another(r)
        X2d=self.genVars_Xor2_down(r)
        B2a=self.genVars_Branch2_another(r)
        B3a=self.genVars_Branch3_another(r)
        B3d=self.genVars_Branch3_down(r)
        SBIn1=self.genVars_SBox_In(r+1)
        #self.KeyUpdate()
        for j in range(0, self.Blocksize//4):
            p0 = 'p0_' + str(r) + '_' + str(j)
            p1 = 'p1_' + str(r) + '_' + str(j)
            #C += BasicConstr_linear.activeSboxConstraints(RIn[4 * j + 0:4 * j + 4],MC[4 * j + 0:4 * j + 4], r, j)
            C += BasicConstr_linear.genFromConstraintTemplate(SBIn[4*j + 0 : 4*j + 4] , SBOut[4*j + 0 : 4*j + 4],p1,p0,Sbox_Template)
        NibbleshiftOut=self.genConstraints_nibbleshift(SBOut)
        BitrotationOut=self.genConstraints_bitrotation(NibbleshiftOut)
        for i in range(0,16):
            C+=BasicConstr_linear.getConstraints_Branch(BitrotationOut[i],B0a[i],B0d[i],r,i)
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(B0d[i],B1a[i],SBIn1[i])
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(BitrotationOut[i+16],B3a[i],X1d[i])
        for i in range(0,16):
            C+=BasicConstr_linear.getConstraints_Branch(X1d[i],B1a[i],SBIn1[i+16],r,i+16)
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(BitrotationOut[i+32],B0a[i],X2d[i])
        for i in range(0,16):
            C+=BasicConstr_linear.getConstraints_Branch(X2d[i],B2a[i],SBIn1[i+32],r,i+32)
        for i in range(0,16):
            C+=BasicConstr_linear.getConstraints_Branch(BitrotationOut[i+48],B3a[i],B3d[i],r,i+48)
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(B3d[i],B2a[i],SBIn1[i+48])

        return C

    #生成密钥恢复的目标函数

    def genObjective_Key(self,En_Round,Dis_Round,De_Round):
        RK=[]
        for i in range(1,En_Round+1):
            RK+=self.genVars_RK(i)
        for i in range(Dis_Round+En_Round+1,Dis_Round+En_Round+De_Round+1):
            RK+=self.genVars_RK(i)
        #CK=self.genVars_cutting_guessed_subkey(1)+self.genVars_cutting_guessed_subkey(2)
        '''CK=self.genVars_cutting_guessed_subkey(1)'''
        #Objective=' + '.join(RK)+' - '+' - '.join(CK)
        Objective=' + '.join(RK)
        return Objective

    #前r0轮：向前决定关系
    def genConstraints_Key_M(self,r):
        assert (r>=1)
        C=list([])
        SBIn=self.genVars_KeyM_SBox_In(r)
        SBOut=self.genVars_KeyM_SBox_Out(r)
        B0a=self.genVars_KeyM_Branch0_another(r)
        B0d=self.genVars_KeyM_Branch0_down(r)
        X1d=self.genVars_KeyM_Xor1_down(r)
        B1a=self.genVars_KeyM_Branch1_another(r)
        X2d=self.genVars_KeyM_Xor2_down(r)
        B2a=self.genVars_KeyM_Branch2_another(r)
        B3a=self.genVars_KeyM_Branch3_another(r)
        B3d=self.genVars_KeyM_Branch3_down(r)
        AKIn=self.genVars_KeyM_AK_In(r)
        AKIn1=self.genVars_KeyM_AK_In(r+1)
        RK=self.genVars_RK(r)
        NibbleshiftOut=self.genConstraints_nibbleshift(SBOut)
        BitrotationOut=self.genConstraints_bitrotation(NibbleshiftOut)
        for i in range(0,16):
            C+=[B0a[i]+' + '+B0d[i]+' - '+BitrotationOut[i]+' >= 0']
            C+=[BitrotationOut[i]+' - '+B0a[i]+' >= 0']
            C+=[BitrotationOut[i]+' - '+B0d[i]+' >= 0']
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(B0d[i],B1a[i],AKIn1[i])
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(BitrotationOut[i+16],B3a[i],X1d[i])
        for i in range(0,16):
            C+=[B1a[i]+' + '+AKIn1[i+16]+' - '+X1d[i]+' >= 0']
            C+=[X1d[i]+' - '+B1a[i]+' >= 0']
            C+=[X1d[i]+' - '+AKIn1[i+16]+' >= 0']
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(BitrotationOut[i+32],B0a[i],X2d[i])
        for i in range(0,16):
            C+=[B2a[i]+' + '+AKIn1[i+32]+' - '+X2d[i]+' >= 0']
            C+=[X2d[i]+' - '+B2a[i]+' >= 0']
            C+=[X2d[i]+' - '+AKIn1[i+32]+' >= 0']
        for i in range(0,16):
            C+=[B3a[i]+' + '+B3d[i]+' - '+BitrotationOut[i+48]+' >= 0']
            C+=[BitrotationOut[i+48]+' - '+B3a[i]+' >= 0']
            C+=[BitrotationOut[i+48]+' - '+B3d[i]+' >= 0']
        for i in range(0,16):
            C+=BasicConstr_linear.xorConstraints(B3d[i],B2a[i],AKIn1[i+48])
        for j in range(0, self.Blocksize//4):
            C+=[SBIn[4*j+0]+' - '+SBIn[4*j+1]+' = 0']
            C+=[SBIn[4*j+0]+' - '+SBIn[4*j+2]+' = 0']
            C+=[SBIn[4*j+0]+' - '+SBIn[4*j+3]+' = 0']
            C+=[SBIn[4*j+0]+' - '+SBOut[4*j+0]+' >= 0']
            C+=[SBIn[4*j+0]+' - '+SBOut[4*j+1]+' >= 0']
            C+=[SBIn[4*j+0]+' - '+SBOut[4*j+2]+' >= 0']
            C+=[SBIn[4*j+0]+' - '+SBOut[4*j+3]+' >= 0']
            C+=[SBOut[4*j+0]+' + '+SBOut[4*j+1]+' + '+SBOut[4*j+2]+' + '+SBOut[4*j+3]+' - '+SBIn[4*j+0]+' >= 0']

        for i in range(0,self.Blocksize):
            C+=BasicConstr_linear.xorConstraints(AKIn[i],RK[i],SBIn[i])
        return C

    #后r2轮：向下确定关系
    def genConstraints_Key_W(self,r):
        assert (r>=1)
        C=list([])
        SBIn=self.genVars_KeyW_SBox_In(r)
        SBOut=self.genVars_KeyW_SBox_Out(r)
        B0a=self.genVars_KeyW_Branch0_another(r)
        B0d=self.genVars_KeyW_Branch0_down(r)
        X1d=self.genVars_KeyW_Xor1_down(r)
        B1a=self.genVars_KeyW_Branch1_another(r)
        X2d=self.genVars_KeyW_Xor2_down(r)
        B2a=self.genVars_KeyW_Branch2_another(r)
        B3a=self.genVars_KeyW_Branch3_another(r)
        B3d=self.genVars_KeyW_Branch3_down(r)
        #AKOut=self.genVars_KeyW_AK_Out(r)
        AKIn=self.genVars_KeyW_AK_In(r)
        SBIn1=self.genVars_KeyW_SBox_In(r+1)
        BO=self.genVars_KeyW_BO(r)
        RK=self.genVars_RK(r)
        NibbleshiftOut=self.genConstraints_nibbleshift(SBOut)
        BitrotationOut=self.genConstraints_bitrotation(NibbleshiftOut)
        for i in range(0,64):
            C+=[BO[i]+' - '+BitrotationOut[i]+' = 0']
        for i in range(0,16):
            '''C+=[B0a[i]+' + '+AKOut[i]+' - '+B0d[i]+' >= 0']
            C+=[B0d[i]+' - '+B0a[i]+' >= 0']
            C+=[B0d[i]+' - '+AKOut[i]+' >= 0']'''
            C+=[B0a[i]+' + '+BitrotationOut[i]+' - '+B0d[i]+' >= 0']
            C+=[B0d[i]+' - '+B0a[i]+' >= 0']
            C+=[B0d[i]+' - '+BitrotationOut[i]+' >= 0']
        for i in range(0,16):
            #C+=BasicConstr_linear.xorConstraints(B0d[i],B1a[i],SBIn1[i])
            C+=BasicConstr_linear.xorConstraints(B0d[i],B1a[i],AKIn[i])
        for i in range(0,16):
            #C+=BasicConstr_linear.xorConstraints(AKOut[i+16],B3a[i],X1d[i])
            C+=BasicConstr_linear.xorConstraints(BitrotationOut[i+16],B3a[i],X1d[i])
        for i in range(0,16):
            '''C+=[X1d[i]+' + '+B1a[i]+' - '+SBIn1[i+16]+' >= 0']
            C+=[SBIn1[i+16]+' - '+B1a[i]+' >= 0']
            C+=[SBIn1[i+16]+' - '+X1d[i]+' >= 0']'''
            C+=[X1d[i]+' + '+B1a[i]+' - '+AKIn[i+16]+' >= 0']
            C+=[AKIn[i+16]+' - '+B1a[i]+' >= 0']
            C+=[AKIn[i+16]+' - '+X1d[i]+' >= 0']
        for i in range(0,16):
            #C+=BasicConstr_linear.xorConstraints(AKOut[i+32],B0a[i],X2d[i])
            C+=BasicConstr_linear.xorConstraints(BitrotationOut[i+32],B0a[i],X2d[i])
        for i in range(0,16):
            '''C+=[X2d[i]+' + '+B2a[i]+' - '+SBIn1[i+32]+' >= 0']
            C+=[SBIn1[i+32]+' - '+B2a[i]+' >= 0']
            C+=[SBIn1[i+32]+' - '+X2d[i]+' >= 0']'''
            C+=[X2d[i]+' + '+B2a[i]+' - '+AKIn[i+32]+' >= 0']
            C+=[AKIn[i+32]+' - '+B2a[i]+' >= 0']
            C+=[AKIn[i+32]+' - '+X2d[i]+' >= 0']
        for i in range(0,16):
            '''C+=[B3a[i]+' + '+AKOut[i+48]+' - '+B3d[i]+' >= 0']
            C+=[B3d[i]+' - '+B3a[i]+' >= 0']
            C+=[B3d[i]+' - '+AKOut[i+48]+' >= 0']'''
            C+=[B3a[i]+' + '+BitrotationOut[i+48]+' - '+B3d[i]+' >= 0']
            C+=[B3d[i]+' - '+B3a[i]+' >= 0']
            C+=[B3d[i]+' - '+BitrotationOut[i+48]+' >= 0']
        for i in range(0,16):
            #C+=BasicConstr_linear.xorConstraints(B3d[i],B2a[i],SBIn1[i+48])
            C+=BasicConstr_linear.xorConstraints(B3d[i],B2a[i],AKIn[i+48])
        for j in range(0, self.Blocksize//4):
            C+=[SBOut[4*j+0]+' - '+SBOut[4*j+1]+' = 0']
            C+=[SBOut[4*j+0]+' - '+SBOut[4*j+2]+' = 0']
            C+=[SBOut[4*j+0]+' - '+SBOut[4*j+3]+' = 0']
            C+=[SBOut[4*j+0]+' - '+SBIn[4*j+0]+' >= 0']
            C+=[SBOut[4*j+0]+' - '+SBIn[4*j+1]+' >= 0']
            C+=[SBOut[4*j+0]+' - '+SBIn[4*j+2]+' >= 0']
            C+=[SBOut[4*j+0]+' - '+SBIn[4*j+3]+' >= 0']
            C+=[SBIn[4*j+0]+' + '+SBIn[4*j+1]+' + '+SBIn[4*j+2]+' + '+SBIn[4*j+3]+' - '+SBOut[4*j+0]+' >= 0']

        for i in range(0,self.Blocksize):
            #C+=BasicConstr_linear.xorConstraints(BitrotationOut[i],RK[i],AKOut[i])
            C+=BasicConstr_linear.xorConstraints(AKIn[i],RK[i],SBIn1[i])

        return C

    def genConstraints_cutting_guessed_subkey(self):
        C=[]
        CK1 = self.genVars_cutting_guessed_subkey(1)
        CK2 = self.genVars_cutting_guessed_subkey(2)
        K1=self.genVars_RK(1)
        K2=self.genVars_RK(2)
        K3=self.genVars_RK(3)
        #K12=self.genVars_RK(12)
        #K13=self.genVars_RK(13)
        for i in range(0,51):
            C+=[K1[i]+' + '+K2[i+13]+' - 2 '+CK1[i]+' >= 0']
            C+=[K1[i]+' + '+K2[i+13]+' - '+CK1[i]+' <= 1']
            C+=[K2[i]+' + '+K3[i+13]+' - 2 '+CK2[i]+' >= 0']
            C+=[K2[i]+' + '+K3[i+13]+' - '+CK2[i]+' <= 1']


        for i in range(51,64):
            C+=[CK1[i]+' = 0']
            C+=[CK2[i]+' = 0']
        return C

    def genConstraints_Key_additional(self,Dis_Round,En_Round,De_Round):
        C=[]
        SB0=self.genVars_SBox_In(1)
        SBR=self.genVars_SBox_In(Dis_Round+1)


        AKE=self.genVars_KeyM_AK_In(En_Round+1)
        SBD=self.genVars_KeyW_SBox_In(Dis_Round+En_Round+1)
        p0=[]
        p1=[]
        for i in range(1,Dis_Round+1):
            for j in range(0, self.Blocksize//4):
                p0.append('p0_' + str(i) + '_' + str(j))
                p1.append('p1_' + str(i) + '_' + str(j))
        p0=' + 2 '.join(p0)
        p1=' + 4 '.join(p1)
        p='2 '+p0+' + 4 '+p1
        p=p+' <= 66'
        C+=[p]

        for j in range(self.Blocksize):
            C += [SB0[j]+' - '+ AKE[j] + ' = 0']

        for j in range(self.Blocksize):
            C += [SBD[j]+' - '+ SBR[j] + ' = 0']

        #C += [self.genObjective_Key(En_Round,Dis_Round,De_Round) + ' <= '+ str(self.Keysize-1)]
        C += [self.genObjective_Key(En_Round,Dis_Round,De_Round) + ' >= 1']


        return C

    def genModel(self,f,r):
        V=set([])
        C=list([])
        '''SBIn1=self.genVars_SBox_In(1)
        SBOut1=self.genVars_SBox_Out(1)
        SBOut2=self.genVars_SBox_Out(2)
        SBOut4=self.genVars_SBox_Out(4)
        SBOut9=self.genVars_SBox_Out(9)
        SBOut10=self.genVars_SBox_Out(10)'''
        '''for i in range(0,64):
            if i!=8 and i!=11 and i!=24 and i!=26 and i!=27 and i!=32 and i!=34 and i!=35 and i!=52 and i!=55:
                C+=[SBIn1[i]+' = 0']
        C+=[SBIn1[8]+' = 1']
        C+=[SBIn1[11]+' = 1']
        C+=[SBIn1[24]+' = 1']
        C+=[SBIn1[26]+' = 1']
        C+=[SBIn1[27]+' = 1']
        C+=[SBIn1[32]+' = 1']
        C+=[SBIn1[34]+' = 1']
        C+=[SBIn1[35]+' = 1']
        C+=[SBIn1[52]+' = 1']
        C+=[SBIn1[55]+' = 1']'''
        '''for i in range(0,64):
            if i!=9 and i!=27 and i!=35 and i!=54:
                C+=[SBOut1[i]+' = 0']
        C+=[SBOut1[9]+' = 1']
        C+=[SBOut1[27]+' = 1']
        C+=[SBOut1[35]+' = 1']
        C+=[SBOut1[54]+' = 1']
        for i in range(0,64):
            if i!=20 and i!=22 and i!=33 and i!=35:
                C+=[SBOut2[i]+' = 0']
        C+=[SBOut2[20]+' = 1']
        C+=[SBOut2[22]+' = 1']
        C+=[SBOut2[33]+' = 1']
        C+=[SBOut2[35]+' = 1']
        for i in range(0,64):
            if i!=8 and i!=24 and i!=34 and i!=51:
                C+=[SBOut4[i]+' = 0']
        C+=[SBOut4[8]+' = 1']
        C+=[SBOut4[24]+' = 1']
        C+=[SBOut4[34]+' = 1']
        C+=[SBOut4[51]+' = 1']
        for i in range(0,64):
            if i!=16 and i!=18:
                C+=[SBOut9[i]+' = 0']
        C+=[SBOut9[16]+' = 1']
        C+=[SBOut9[18]+' = 1']'''
        '''for i in range(0,64):
            if i!=28 and i!=29 and i!=30 and i!=44 and i!=45 and i!=46 and i!=60 and i!=61 and i!=62:
                C+=[SBOut10[i]+' = 0']
        C+=[SBOut10[28]+' = 1']
        C+=[SBOut10[29]+' = 1']
        C+=[SBOut10[30]+' = 1']
        C+=[SBOut10[44]+' = 1']
        C+=[SBOut10[45]+' = 1']
        C+=[SBOut10[46]+' = 1']
        C+=[SBOut10[60]+' = 1']
        C+=[SBOut10[61]+' = 1']
        C+=[SBOut10[62]+' = 1']'''
        SBIn=self.genVars_SBox_In(1)
        '''SBOut=self.genVars_SBox_Out(1)
        SBIn7=self.genVars_SBox_In(7)
        SBIn8=self.genVars_SBox_In(8)
        SBIn9=self.genVars_SBox_In(9)'''
        SBIn10=self.genVars_SBox_In(10)
        SBI=SBIn+SBIn10
        SBI=' + '.join(SBI)
        C+=[SBI+" <= 13"]

        '''for i in range(0,64):
            if i!=16 and i!=18 and i!=19 and i!=32 and i!=33 and i!=34 and i!=35:
                C+=[SBIn[i]+' = 0']
        C+=[SBIn[16]+' = 1']
        C+=[SBIn[18]+' = 1']
        C+=[SBIn[19]+' = 1']
        C+=[SBIn[32]+' = 1']
        C+=[SBIn[33]+' = 1']
        C+=[SBIn[34]+' = 1']
        C+=[SBIn[35]+' = 1']
        for i in range(0,64):
            if i!=19 and i!=32:
                C+=[SBOut[i]+' = 0']
        C+=[SBOut[19]+' = 1']
        C+=[SBOut[32]+' = 1']
        for i in range(0,64):
            if i!=16 and i!=62 and i!=61:
                C+=[SBIn7[i]+' = 0']
        C+=[SBIn7[16]+' = 1']
        C+=[SBIn7[62]+' = 1']
        C+=[SBIn7[61]+' = 1']
        for i in range(0,64):
            if i!=30 and i!=31:
                C+=[SBIn8[i]+' = 0']
        C+=[SBIn8[30]+' = 1']
        C+=[SBIn8[31]+' = 1']
        for i in range(0,64):
            if i!=24 and i!=25 and i!=26 and i!=40 and i!=41 and i!=42 and i!=56 and i!=57 and i!=58:
                C+=[SBIn9[i]+' = 0']
        C+=[SBIn9[24]+' = 1']
        C+=[SBIn9[25]+' = 1']
        C+=[SBIn9[26]+' = 1']
        C+=[SBIn9[40]+' = 1']
        C+=[SBIn9[41]+' = 1']
        C+=[SBIn9[42]+' = 1']
        C+=[SBIn9[56]+' = 1']
        C+=[SBIn9[57]+' = 1']
        C+=[SBIn9[58]+' = 1']
        for i in range(0,64):
            if i!=7 and i!=22 and i!=38 and i!=41 and i!=54 and i!=55 and i!=57:
                C+=[SBIn10[i]+' = 0']
        C+=[SBIn10[7]+' = 1']
        C+=[SBIn10[22]+' = 1']
        C+=[SBIn10[38]+' = 1']
        C+=[SBIn10[41]+' = 1']
        C+=[SBIn10[54]+' = 1']
        C+=[SBIn10[55]+' = 1']
        C+=[SBIn10[57]+' = 1']'''
        C+=[self.genConstraints_InputNonzero()]
        '''p0=[]
        p1=[]
        for i in range(1,Dis_Round+1):
            for j in range(0, self.Blocksize//4):
                p0.append('p0_' + str(i) + '_' + str(j))
                p1.append('p1_' + str(i) + '_' + str(j))
        p0=' + 2 '.join(p0)
        p1=' + 4 '.join(p1)
        p='2 '+p0+' + 4 '+p1
        p=p+' = 66'
        C+=[p]'''
        for i in range(1,r+1):
            C+=self.genConstraints_R(i)
        V = BasicConstr_linear.getVariables_From_Constraints(C)
        print('Minimize')
        f.write('Minimize')
        f.write('\n')
        print(self.genObjectiveFun_to_Round(r))
        f.write(self.genObjectiveFun_to_Round(r))
        f.write('\n')
        f.write('\n')
        print('\n')
        print('Subject To')
        f.write('Subject to')
        f.write('\n')
        #print(add_constraint_1)
        #f.write(add_constraint_1)
        #f.write('\n')
        for c in C:
            print(c)
            f.write(c)
            f.write('\n')
        print('\n')
        print('Binary')
        f.write('Binary')
        f.write('\n')
        for v in V:
            print(v)
            f.write(v)
            f.write('\n')
        return C

    def genModel_keyrecovery(self,fw,Dis_Round,En_Round,De_Round):
        V=set([])
        C=list([])
        SBIn1=self.genVars_SBox_In(1)
        SBIn11=self.genVars_SBox_In(11)
        #SBIn1=' + '.join(SBIn1)
        #SBIn1+=' <= 10'
        #SBIn11=' + '.join(SBIn11)
        #SBIn11+=' <= 22'

        '''SBIn1=self.genVars_SBox_In(1)
        SBOut1=self.genVars_SBox_Out(1)
        SBOut2=self.genVars_SBox_Out(2)
        SBOut4=self.genVars_SBox_Out(4)
        SBOut9=self.genVars_SBox_Out(9)
        SBOut10=self.genVars_SBox_Out(10)
        for i in range(0,64):
            if i!=8 and i!=11 and i!=24 and i!=26 and i!=27 and i!=32 and i!=34 and i!=35 and i!=52 and i!=55:
                C+=[SBIn1[i]+' = 0']
        C+=[SBIn1[8]+' = 1']
        C+=[SBIn1[11]+' = 1']
        C+=[SBIn1[24]+' = 1']
        C+=[SBIn1[26]+' = 1']
        C+=[SBIn1[27]+' = 1']
        C+=[SBIn1[32]+' = 1']
        C+=[SBIn1[34]+' = 1']
        C+=[SBIn1[35]+' = 1']
        C+=[SBIn1[52]+' = 1']
        C+=[SBIn1[55]+' = 1']
        for i in range(0,64):
            if i!=9 and i!=27 and i!=35 and i!=54:
                C+=[SBOut1[i]+' = 0']
        C+=[SBOut1[9]+' = 1']
        C+=[SBOut1[27]+' = 1']
        C+=[SBOut1[35]+' = 1']
        C+=[SBOut1[54]+' = 1']
        for i in range(0,64):
            if i!=20 and i!=22 and i!=33 and i!=35:
                C+=[SBOut2[i]+' = 0']
        C+=[SBOut2[20]+' = 1']
        C+=[SBOut2[22]+' = 1']
        C+=[SBOut2[33]+' = 1']
        C+=[SBOut2[35]+' = 1']
        for i in range(0,64):
            if i!=8 and i!=24 and i!=34 and i!=51:
                C+=[SBOut4[i]+' = 0']
        C+=[SBOut4[8]+' = 1']
        C+=[SBOut4[24]+' = 1']
        C+=[SBOut4[34]+' = 1']
        C+=[SBOut4[51]+' = 1']
        for i in range(0,64):
            if i!=16 and i!=18:
                C+=[SBOut9[i]+' = 0']
        C+=[SBOut9[16]+' = 1']
        C+=[SBOut9[18]+' = 1']
        for i in range(0,64):
            if i!=28 and i!=29 and i!=30 and i!=44 and i!=45 and i!=46 and i!=60 and i!=61 and i!=62:
                C+=[SBOut10[i]+' = 0']
        C+=[SBOut10[28]+' = 1']
        C+=[SBOut10[29]+' = 1']
        C+=[SBOut10[30]+' = 1']
        C+=[SBOut10[44]+' = 1']
        C+=[SBOut10[45]+' = 1']
        C+=[SBOut10[46]+' = 1']
        C+=[SBOut10[60]+' = 1']
        C+=[SBOut10[61]+' = 1']
        C+=[SBOut10[62]+' = 1']'''
        SBIn=self.genVars_SBox_In(1)
        SBOut=self.genVars_SBox_Out(1)
        SBIn7=self.genVars_SBox_In(7)
        SBIn8=self.genVars_SBox_In(8)
        SBOut8=self.genVars_SBox_Out(8)
        SBIn9=self.genVars_SBox_In(9)
        SBOut9=self.genVars_SBox_Out(9)
        SBIn10=self.genVars_KeyW_SBox_In(9)
        for i in range(0,64):
            if i!=16 and i!=18 and i!=19 and i!=32 and i!=33 and i!=34 and i!=35:
                C+=[SBIn[i]+' = 0']
        C+=[SBIn[16]+' = 1']
        C+=[SBIn[18]+' = 1']
        C+=[SBIn[19]+' = 1']
        C+=[SBIn[32]+' = 1']
        C+=[SBIn[33]+' = 1']
        C+=[SBIn[34]+' = 1']
        C+=[SBIn[35]+' = 1']
        for i in range(0,64):
            if i!=19 and i!=32:
                C+=[SBOut[i]+' = 0']
        C+=[SBOut[19]+' = 1']
        C+=[SBOut[32]+' = 1']
        for i in range(0,64):
            if i!=16 and i!=62 and i!=61:
                C+=[SBIn7[i]+' = 0']
        C+=[SBIn7[16]+' = 1']
        C+=[SBIn7[62]+' = 1']
        C+=[SBIn7[61]+' = 1']
        for i in range(0,64):
            if i!=30 and i!=31:
                C+=[SBIn8[i]+' = 0']
        C+=[SBIn8[30]+' = 1']
        C+=[SBIn8[31]+' = 1']
        for i in range(0,64):
            if i!=28 and i!=29 and i!=30:
                C+=[SBOut8[i]+' = 0']
        C+=[SBOut8[28]+' = 1']
        C+=[SBOut8[29]+' = 1']
        C+=[SBOut8[30]+' = 1']
        for i in range(0,64):
            if i!=24 and i!=25 and i!=26 and i!=40 and i!=41 and i!=42 and i!=56 and i!=57 and i!=58:
                C+=[SBIn9[i]+' = 0']
        C+=[SBIn9[24]+' = 1']
        C+=[SBIn9[25]+' = 1']
        C+=[SBIn9[26]+' = 1']
        C+=[SBIn9[40]+' = 1']
        C+=[SBIn9[41]+' = 1']
        C+=[SBIn9[42]+' = 1']
        C+=[SBIn9[56]+' = 1']
        C+=[SBIn9[57]+' = 1']
        C+=[SBIn9[58]+' = 1']
        for i in range(0,64):
            if i!=26 and i!=27 and i!=40 and i!=56:
                C+=[SBOut9[i]+' = 0']
        C+=[SBOut9[26]+' = 1']
        C+=[SBOut9[27]+' = 1']
        C+=[SBOut9[40]+' = 1']
        C+=[SBOut9[56]+' = 1']
        for i in range(0,64):
            if i!=7 and i!=22 and i!=38 and i!=41 and i!=54 and i!=55 and i!=57:
                C+=[SBIn10[i]+' = 0']
        C+=[SBIn10[7]+' = 1']
        C+=[SBIn10[22]+' = 1']
        C+=[SBIn10[38]+' = 1']
        C+=[SBIn10[41]+' = 1']
        C+=[SBIn10[54]+' = 1']
        C+=[SBIn10[55]+' = 1']
        C+=[SBIn10[57]+' = 1']

        #C+=self.genConstraints_cutting_guessed_subkey()
        C+=[self.genConstraints_InputNonzero()]
        C+=self.genConstraints_Key_additional(Dis_Round,En_Round,De_Round)

        for i in range(1,En_Round+1):
            C+=self.genConstraints_Key_M(i)
        for i in range(1,Dis_Round+1):
            C+=self.genConstraints_R(i)
        for i in range(1,De_Round+1):
            C+=self.genConstraints_Key_W(Dis_Round+En_Round+i)


        V=BasicConstr_linear.getVariables_From_Constraints(C)

        fw.write('Minimize'+'\n')
        #print(self.genObjectiveFun_to_Round(Dis_Round))
        #f.write(self.genObjectiveFun_to_Round(Dis_Round))
        fw.write(self.genObjective_Key(En_Round,Dis_Round,De_Round)+'\n')
        fw.write('\n')
        fw.write('Subject To'+'\n')

        for c in C:
            fw.write(c+'\n')

        fw.write('\n')
        fw.write('Binary'+'\n')
        for v in V:
            fw.write(v+'\n')
        fw.close()

if __name__ == '__main__':
    Dis_Round=9
    En_Round=1
    De_Round=1
    a=BORON_linearmilp()
    #f = open('C:\\Users\\lv\\Desktop\\' + 'round' + str(Dis_Round) + '.lp', 'w')
    f = open('C:\\Users\\lv\\Desktop\\' + 'round' + str(Dis_Round+En_Round+De_Round) + '.lp', 'w')
    #a.genModel(f,Dis_Round)
    a.genModel_keyrecovery(f,Dis_Round,En_Round,De_Round)