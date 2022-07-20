class BasicConstr_linear:
    def leftCyclicRotation(in_vars, offset):
        out = [None for i in range(0, len(in_vars))]
        for i in range(0, len(in_vars)):
            out[i] = in_vars[(i-offset) % len(in_vars)]

        return out

    def activeSboxConstraints(in_vars, out_vars, r, k):
        """
        Generate the constraints of the k-th S-box at round r.
        Note, we include the r, and k parameters to index the activity marker variable
        k47 + k48 + k49 + k50 - y1 >= 0
        k47 - y1 <= 0
        k48 - y1 <= 0
        k49 - y1 <= 0
        k50 - y1 <= 0
        4 k47 + 4 k48 + 4 k49 + 4 k50 - vInSbox4 - vInSbox5 - vInSbox6 - vInSbox7 >= 0
        4 vInSbox4 + 4 vInSbox5 + 4 vInSbox6 + 4 vInSbox7 - k47 - k48 - k49 - k50 >= 0
        """
        dummy_var = 'S_' + str(r) + '_' + str(k)
        constraints = list([])
        s = ' + '.join(in_vars) + ' - ' + dummy_var + ' >= 0'
        constraints.append(s)
        for v in in_vars:
            constraints.append(v + ' - ' + dummy_var + ' <= 0')

        in_size = len(in_vars)
        out_size = len(out_vars)

        if in_size != out_size:
            for v in out_vars:
                constraints.append(v + ' - ' + dummy_var + ' <= 0')

        if in_size == out_size:
            c = ' + '.join([str(out_size) + ' ' + in_vars[j] for j in range(0, in_size)])
            c = c + ' - '
            c = c + ' - '.join(out_vars) + ' >= 0'
            constraints.append(c)

            c = ' + '.join([str(in_size) + ' ' + out_vars[j] for j in range(0, out_size)])
            c = c + ' - '
            c = c + ' - '.join(in_vars) + ' >= 0'
            constraints.append(c)

        return constraints
    def activeSboxConstraints_add(in_vars, out_vars, r, k):
        """
        Generate the constraints of the k-th S-box at round r.
        Note, we include the r, and k parameters to index the activity marker variable
        k47 + k48 + k49 + k50 - y1 >= 0
        k47 - y1 <= 0
        k48 - y1 <= 0
        k49 - y1 <= 0
        k50 - y1 <= 0
        4 k47 + 4 k48 + 4 k49 + 4 k50 - vInSbox4 - vInSbox5 - vInSbox6 - vInSbox7 >= 0
        4 vInSbox4 + 4 vInSbox5 + 4 vInSbox6 + 4 vInSbox7 - k47 - k48 - k49 - k50 >= 0
        """
        dummy_var = 'AS_' + str(r) + '_' + str(k)
        constraints = list([])
        s = ' + '.join(in_vars) + ' - ' + dummy_var + ' >= 0'
        constraints.append(s)
        for v in in_vars:
            constraints.append(v + ' - ' + dummy_var + ' <= 0')

        in_size = len(in_vars)
        out_size = len(out_vars)

        if in_size != out_size:
            for v in out_vars:
                constraints.append(v + ' - ' + dummy_var + ' <= 0')

        if in_size == out_size:
            c = ' + '.join([str(out_size) + ' ' + in_vars[j] for j in range(0, in_size)])
            c = c + ' - '
            c = c + ' - '.join(out_vars) + ' >= 0'
            constraints.append(c)

            c = ' + '.join([str(in_size) + ' ' + out_vars[j] for j in range(0, out_size)])
            c = c + ' - '
            c = c + ' - '.join(in_vars) + ' >= 0'
            constraints.append(c)

        return constraints

    def getConstraints_Branch(xs, ys, zs,r,j):
        """
        generate the constraints of zs = xs xor ys, where
        zs, ys, and xs are lists of variables
        Example:
            >>> ConstraintGenerator.xorConstraints(['x0','x1','x2'],['y0','y1','y2'],['z0','z1','z2']);
            ['x0 + y0 + z0 <= 2',
             'x0 + y0 + z0 - 2 xor_dummy0_x0_y0_z0 >= 0',
             'xor_dummy0_x0_y0_z0 - x0 >= 0',
             'xor_dummy0_x0_y0_z0 - y0 >= 0',
             'xor_dummy0_x0_y0_z0 - z0 >= 0',
             'x1 + y1 + z1 <= 2',
             'x1 + y1 + z1 - 2 xor_dummy1_x1_y1_z1 >= 0',
             'xor_dummy1_x1_y1_z1 - x1 >= 0',
             'xor_dummy1_x1_y1_z1 - y1 >= 0',
             'xor_dummy1_x1_y1_z1 - z1 >= 0',
             'x2 + y2 + z2 <= 2',
             'x2 + y2 + z2 - 2 xor_dummy2_x2_y2_z2 >= 0',
             'xor_dummy2_x2_y2_z2 - x2 >= 0',
             'xor_dummy2_x2_y2_z2 - y2 >= 0',
             'xor_dummy2_x2_y2_z2 - z2 >= 0']
        """
        dummy_vars ='o_r' +str(r)+'_'+ str(j)

        constraints = list([])

        c = xs + ' + ' + ys + ' + ' + zs + ' <= 2'
        constraints.append(c)

        # 2. The branch number of the XOR operation is 2
        c = xs + ' + ' + ys + ' + ' + zs + ' - 2 ' + dummy_vars + ' >= 0'
        constraints.append(c)
        constraints.append(dummy_vars + ' - ' + xs + ' >= 0')
        constraints.append(dummy_vars + ' - ' + ys + ' >= 0')
        constraints.append(dummy_vars + ' - ' + zs + ' >= 0')

        return constraints

    def xorConstraints(xs, ys, zs):
        '''
         >> BasicConstr_linear.getConstraints_XOR(['a','b','c'])
         >> ['a - b = 0', 'a - c = 0']
        '''

        constraints = list([])

        # 1. There are at most 2 of the x, y, z can be 1, where z = x xor y
        c = xs + ' - ' + ys + ' = 0'
        constraints.append(c)
        c = ys + ' - ' + zs + ' = 0'
        constraints.append(c)
        return constraints

    def getConstraints_AND(Input1, Input2, Output0):
        '''
        >> BasicConstr_linear.getConstraints_AND('a','b','c')
        >> ['c - a >= 0', 'c - b >= 0']
        '''
        Constr = []
        Constr = Constr + [Output0 + ' - ' + Input1 + ' >= 0']
        Constr = Constr + [Output0 + ' - ' + Input2 + ' >= 0']
        return Constr

    def getConstraints_Rot_on_word(Input, Output, len_word, shiftbit):
        '''
        >> BasicConstr_linear.getConstraints_Rot_on_word(['a1','b1','c1','d1','e1','f1'],['a2','b2','c2','d2','e2','f2'], 3, 1)
        >>
        ['b1 - a2 = 0',
         'c1 - b2 = 0',
         'a1 - c2 = 0',
         'e1 - d2 = 0',
         'f1 - e2 = 0',
         'd1 - f2 = 0']
        '''
        n = len(Input)//len_word
        Constr = []
        for j in range(n):
            In0 = Input[len_word*j : len_word*(j + 1)]
            Out0 = Output[len_word*j : len_word*(j + 1)]
            for h in range(len_word):
                Constr = Constr + [In0[(h + shiftbit) % len_word] + ' - ' + Out0[h] + ' = 0']
        return Constr

    def genFromConstraintTemplate(in_vars, out_vars,probit1,probit2, ineq_template):
        """
        Example:
            >>> ConstraintGenerator.genFromConstraintTemplate(['x0', 'x1'], ['y0'], [(-1, 2, 3, 1), (1, -1, 0, -2)] )
            ['-1 x0 + 2 x1 + 3 y0 >= - 1', '1 x0 - 1 x1 + 0 y0 >= 2']
            >>> ConstraintGenerator.genFromConstraintTemplate(['x0', 'x1'], ['y0'], [(-1, 2, 3, 1), (-1, -1, 0, -2)] )
            ['-1 x0 + 2 x1 + 3 y0 >= - 1', '-1 x0 - 1 x1 + 0 y0 >= 2']
        """
        assert ineq_template != list([])
        assert (len(in_vars) + len(out_vars) + 2) == (len(ineq_template[1]) - 1)
        #若最右端为index0则需要reverse
        in_vars.reverse()
        out_vars.reverse()

        vars_list = in_vars + out_vars  + [probit1] + [probit2]
        constraints = list([])
        for T in ineq_template:
            s = str(T[0]) + ' ' + in_vars[0]
            for j in range(1, len(vars_list)):
                if T[j] >= 0:
                    s = s + ' + ' + str(T[j]) + ' ' + vars_list[j]
                elif T[j] < 0:
                    s = s + ' - ' + str(-T[j]) + ' ' + vars_list[j]

            s = s + ' >= '
            if T[-1] <= 0:
                s = s + str(-T[-1])
            elif T[-1] > 0:
                s = s + '- ' + str(T[-1])

            constraints.append(s)

        return constraints

    def equalConstraints_single(x, y):
        c = []
        c = c + [x + ' - ' + y + ' = 0']

        return c

    def equalConstraints(x, y):
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[i] + ' = 0']

        return c

    @staticmethod
    def getVariables_From_Constraints(C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace('+', ' ')
            temp = temp.replace('-', ' ')
            temp = temp.replace('>=', ' ')
            temp = temp.replace('<=', ' ')
            temp = temp.replace('=', ' ')
            temp = temp.split()
            for v in temp:
                if not v.isdecimal():
                    V.add(v)

        return V