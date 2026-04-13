#creando funcion, a partir de declararla con def




def check_number():
    value = int(input("Enter a number: "))
    
    if value > 10:
        print("Greater than 10")
    else:
        print("10 or less")
        return value


