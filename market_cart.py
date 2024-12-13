shopping_cart = []
promotion = 100
promotion_cart = []
minimum = None

#TODO: add appropriate arguments and/or returns
def add_item(name, price, option = None, quantity = 1):
    if minimum != None:                                                             #만약 앞에서 할인이 존재한다면 할인율을 적용하기 위하여 if문 사용
        if price * quantity >= minimum:                                             #할인율을 적용해야한다면
            price = (price * promotion) // 100                                      #가격에 할인율 적용
            shopping_cart.append([name, option, quantity, price, price * quantity])         #쇼핑카트와 할인율 적용된 것을 구별하기 위한 카트에 모두 추가
            promotion_cart.append([name, option, quantity, price, price * quantity])
        else: 
            shopping_cart.append([name, option, quantity, price, price * quantity])       #할인이 적용되는 범위가 아니라면, 할인을 적용하지 않고 쇼핑카트에 추가
    else:
        shopping_cart.append([name, option, quantity, price, price * quantity])           #앞에 할인이 없다면 쇼핑카트에 추가
        
def remove_item(name):
    removed = []
    for item in shopping_cart:                                                  #쇼핑카트 내에 item에 대하여 name이 아이템 list의 첫번째 항에 포함된다면 제거 후 removed 리스트에 추가
        if name in item[0]:                                                     
            removed.append(item)
    for item in removed:                                                        #중복 처리나 넘어가는 것을 방지하기 위해 removed에 item을 먼저 추가한 후 추가된 item들을 제거
        shopping_cart.remove(item)
    return removed

def find_item(name):
    find = [item for item in shopping_cart if name in item[0]]                  #list comprehension을 이용해 name이 이름에 포함되는 것 탐색
    return find


def update_quantity(name, new_quantity = 1):
    for i in range(len(shopping_cart)):
        if name == shopping_cart[i][0]:                                            #쇼핑카트에 존재하는 모든 상품에 대해 상품 명에 name을 포함하는지 조사
            if minimum != None:                                                       
                if shopping_cart[i] in promotion_cart:                             #할인율이 적용된 적이 있을 경우, 할인율을 적용했는지 조사하고 적용했다면 우선 값을 되돌림
                    a = (shopping_cart[i][3] * 100) // promotion
                    if a * new_quantity < minimum:                                  #앞에서 구해진 원래 단가에 새로운 수량을 곱해 그 값이 할인을 적용해야하는 값인지 조사하고 적용
                        promotion_cart.remove(shopping_cart[i])
                        shopping_cart[i][3] = a
                         
                else:
                    shopping_cart[i][2] = new_quantity                                                              #할인율을 적용하지 않았다면, 그 가격에 새로운 수량을 곱한것이 할인을 적용해야 하는 값인지 조사하고 적용
                    if shopping_cart[i][3] * shopping_cart[i][2] >= minimum:
                        shopping_cart[i][3] = (shopping_cart[i][3] * promotion) // 100
                        shopping_cart[i][4] = new_quantity * shopping_cart[i][3]
                        promotion_cart.append(shopping_cart[i])                     #할인을 적용했다면 적용 카트에 추가
            shopping_cart[i][2] = new_quantity
            shopping_cart[i][4] = new_quantity * shopping_cart[i][3]
            return shopping_cart[i]
    
def update_option(name, new_option = None):
    for i in range(len(shopping_cart)):
        if name == shopping_cart[i][0]:
            shopping_cart[i][1] = new_option                                        #name이 물건 list의 이름에 포함된다면 옵션을 새 옵션으로 바꿈
            return shopping_cart[i]

def apply_promotion(minimum_price, amount_percentage):
    global promotion                                                                #프로모션과 미니멈을 앞에 add_item과 update_quantity에 적용하기 위해 광역변수로 설정
    global minimum
    if promotion_cart:
        for i in range(len(shopping_cart)):                                         #전에 할인이 적용된 적이 있는 물체들을 원래 값으로 되돌림
            if shopping_cart[i] in promotion_cart:
                promotion_cart.remove(shopping_cart[i])
                shopping_cart[i][4] = (shopping_cart[i][4] * 100) // promotion
                shopping_cart[i][3] = (shopping_cart[i][3] * 100) // promotion
    for i in range(len(shopping_cart)):                                             #할인이 적용되는 물체들에 할인을 적용
            if shopping_cart[i][4] >= minimum_price:
                shopping_cart[i][4] = (shopping_cart[i][4] * (100 - amount_percentage)) // 100
                shopping_cart[i][3] = (shopping_cart[i][3] * (100 - amount_percentage)) // 100
                promotion_cart.append(shopping_cart[i])
    promotion = 100 - amount_percentage                                             #프로모션 : 할인이 적용되어 가격에 곱해야할 값
    minimum = minimum_price                                                         #미니멈 : 할인을 적용해야하는 최소 값


def get_partial_cart(start, end):
    partial_cart = shopping_cart[start:end]                                         #start에서 end까지의 원소를 partial 카트로 설정하고 이를 리턴함
    return partial_cart 

def calculate_total():
    total = 0                                                                       #total이라는 변수에 쇼핑카트 내 원소의 모든 값을 더함
    for i in range(len(shopping_cart)):
        total = total + shopping_cart[i][4]
    return total

def view_cart():                                                                    #우선 먼저 출력해야할 문자열을 출력하고, shopping_cart내의 원소(list) 내의 원소를 전부 분리
    print('상품명 옵션 수량 단가 가격')                                               #이를 분리하는 이유는 option에 괄호를 씌우기 위함
    for i in range(len(shopping_cart)):                                                 
        a = shopping_cart[i][0]
        b = shopping_cart[i][1]
        c = shopping_cart[i][2]
        d = shopping_cart[i][3]
        e = shopping_cart[i][4]
        if b != None:                                                               #option이 None이 아니라면 option에만 괄호를 씌우고 나머지를 출력                                                              
            print(a," (", b ,") ",c,' ',d,' ',e,sep='')
        else:
            print(a,c,d,e)                                                          #option이 None이라면 option은 출력하지 않고 나머지만 출력
        
    print('합계: ', calculate_total())                                               #가격 합계 출력
    
        


# main() is not mandatory.
# You may modify it if you want to or you may leave it as is.
def main():
    while True:
        print("1. Add item")
        print("2. Remove item")
        print("3. Find item")
        print("4. Update item quantity")
        print("5. Update item option")
        print("6. Apply promotion")
        print("7. Get partial cart")
        print("8. Calculate total")
        print("9. View cart")
        print("0. Exit")
        
        choice = int(input("Select an operation: "))
        
        if choice == 1:
            input_list = input("Enter name, price, option(optional), quantity(optional) separated by comma(,): ").split(",")
            name = input_list[0]
            price = float(input_list[1])
            option = input_list[2].strip() if len(input_list) > 2 else None
            quantity = int(input_list[3].strip()) if len(input_list) > 3 else 1
            add_item(name, price, option, quantity)
            print(shopping_cart)
        elif choice == 2:
            delete_name = input()
            print(remove_item(delete_name))
            remove_item(delete_name)
            print(shopping_cart)
        elif choice == 3:
            # TODO
            pass
        elif choice == 4:
            # TODO
            pass
        elif choice == 5:
            # TODO
            pass
        elif choice == 6:
            # TODO
            pass
        elif choice == 7:
            # TODO
            pass
        elif choice == 8:
            # TODO
            pass
        elif choice == 9:
            # TODO
            pass
        elif choice == 0:
            break
        else:
            print("Invalid choice.")


########################################
# Do not modify! #######################
########################################
if __name__ == "__main__":
    main()
########################################
########################################
# Insertion point for grading ##########
########################################