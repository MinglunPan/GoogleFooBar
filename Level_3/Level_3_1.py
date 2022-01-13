from fractions import Fraction as frac
def getGCD(a,b):
    """Calculate the Greatest Common Divisor for
    two numbers.
    """
    if b == 0: return a
    return getGCD(b, a % b)
def getMultiGCD(num_list):
    """Calculate the Greate Common Divisor for 
    a list of numbers
    """
    curr_gcd = num_list[0]
    for i in range(1, len(num_list)):
        curr_gcd = getGCD(curr_gcd, num_list[i])
    return curr_gcd
def getLCM(a,b):
    """Calculate the Least Common Multiplier for
    two numbers.
    """
    return a * b / getGCD(a,b)
def getMultiLCM(num_list):
    """Calculate the Least Common Multiplier for
    a list of numbers.
    """
    init_num = 1
    for num in num_list:
        init_num = getLCM(num, init_num)
    return init_num
    
def solveEquations(A, b):
    """Solve the linear equations AX=B
    """
    row_size = len(A)
    col_size = (len(A[0]) + 1) if row_size > 0 else 0
    A_b =  [A[idx] + [b[idx]] for idx in range(row_size)]
    # Use pivot columns to reduce the equations
    for col_idx in range(col_size):
        for row_idx in range(col_idx+1, row_size):
            
            r = [-(row_val * frac(A_b[row_idx][col_idx],A_b[col_idx][col_idx])) for row_val in A_b[col_idx]]
            A_b[row_idx] = [sum(pair) for pair in zip(A_b[row_idx], r)]
    # Solve ax = b
    ans = []
    A_b = A_b[::-1]
    for row_idx in range(row_size):
        row_b = sum([(ans[-prior_row_idx-1]*A_b[row_idx][-prior_row_idx-2]) for prior_row_idx in range(row_idx)])
        ans.insert(0,frac((A_b[row_idx][-1]-row_b), A_b[row_idx][-row_idx-2]))
    return ans
    
def transpose(A):
    """Return the transpose of matrix A
    """
    row_size = len(A)
    col_size = len(A[0]) if row_size > 0 else 0
    return [[A[row_idx][col_idx] for row_idx in range(row_size)] for col_idx in range(col_size)]
    
def solution(m):
    row_size = len(m)
    m_row_sum = [sum(r) for r in m]
    
    for i in range(row_size):
        if m_row_sum[i] == m[i][i]:
            m_row_sum[i] = m[i][i] = 0

    col_size = len(m[0])
    
    # Construct the coefficients for Linear equation systems
    m = [
        [frac(m[i][j],m_row_sum[i]) if m_row_sum[i] != 0 else 0 for j in range(col_size)] 
        for i in range(row_size)]
    
    for i in range(len(m)):
        m[i][i] -= 1
    b = m[0]
    m[0] = [0] * col_size
    m[0][0] = 1
    
    result = solveEquations(transpose(m),b)
    # Format the result and simplify the fractions.
    result = [-val for i,val in enumerate(result) if m_row_sum[i] == 0]
    lcm = getMultiLCM([x.denominator for x in result])
    result = [x*lcm for x in result]
    result = [x.numerator for x in result]
    gcd = getMultiGCD(result)
    result = [x / gcd for x in result]
    result += [sum(result)]
    return result
