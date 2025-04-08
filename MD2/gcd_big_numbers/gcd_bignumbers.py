
num1 = 9742867231360457281220952
num2 = 2825240788613971993199718

# recursive (melhor para números pequenos)
def gcd_recursive(a, b):
    return b if a%b == 0 else gcd_recursive(b, a % b)

gcd_recursive = gcd_recursive(num1, num2)

print(f'GCD recursive: {gcd_recursive}')


# iterative (melhor para numeros maiores - tempo de processamento e gasto de memória)
def gcd_iterative(a, b):
    while (b):
        a, b = b, a%b
    return abs(a)

gcd_iterative = gcd_iterative(num1, num2)


print(f'GCD iterative: {gcd_iterative}')


"""
O python usa o sistema "Arbitrary-precision integers" que gerencia automaticamente a memória necessária para armazenar números muito grandes, usando uma estrutura interna que cresce conforme necessário. Nesse caso não é preciso se preocupar com o tamanho do número, como em outras linguagens. Mas é preciso ficar atento, pois como não tem um limite pré definido, ao usar números muito grandes e estourar a quantidade de memória disponível do seu computador, o computador irá travar.
"""
