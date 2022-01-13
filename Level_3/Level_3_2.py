def solution(l):
    num_size = len(l)
    # Your code here

    for i in range(num_size, ):
        idx = -i-1
        num = l[idx]
        l[idx] = [j for j in range(idx+1, num_size)  if l[j] % num == 0]

    divisor_size_list = [len(divisor) for divisor in l]

    count_lucky_triple = 0
    for i,divisors in enumerate(l):
        for j in divisors:
            count_lucky_triple += divisor_size_list[j]
    return count_lucky_triple

        


if __name__ == '__main__':
    print(solution([1, 1, 1]))
    