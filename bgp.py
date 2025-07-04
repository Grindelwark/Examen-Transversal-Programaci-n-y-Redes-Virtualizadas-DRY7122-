# script sistemas autonomos BGP solo AS de 16 bits
while True:
    entrada = input("Número de AS (o 'salir'): ")
    if entrada.lower() == "salir":
        break
    try:
        asn = int(entrada)
        if 1 <= asn <= 64495:
            print("AS público\n")
        elif 64512 <= asn <= 65534:
            print(" AS privado\n")
        else:
            print("Fuera de rango de 16 bits\n")
    except:
        print(" Entrada inválida\n")



