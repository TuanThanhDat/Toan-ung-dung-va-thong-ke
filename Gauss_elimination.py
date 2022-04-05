
# @input là 1 dòng của ma trân HPT
# @output là 
#     - Nếu tìm thấy vị trí đầu dòng có giá trị khác 0 thì trả về vị trí đó
#     - Nếu không tìm thấy thì trả về -1
def find_first_left(line):
    for index in range(0,len(line)-1): # len(line)-1 do đang xét ma trận mở rộng, phần tử cuối cùng là hệ số tự do không tính
        if line[index] != 0:
            return index
    return -1


# Hoán vị dòng
def line_permutation(A,index_row1,index_row2):
    A[index_row1],A[index_row2] = A[index_row2],A[index_row1]


# @input là Ma trận mở rộng của Hệ phương trình
# @output là Ma trận bậc thang mà giá trị đầu dòng đã rút gọn về 1 
def Gauss_elimination(A):
    # Vị trí đang xét đầu tiên
    current_row = 0
    current_col = 0
    
    while current_row < len(A) and current_col < len(A[0]):
        # Kết thúc khi đã xét xong giá trị đầu dòng tại cột cuối cùng
        if current_col == len(A[0]):
            break

        # Tại dòng và cột đang xét không có giá trị khác 0
        # Ta phải tìm dòng khác (nếu có) tại cột đó có giá trị khác 0 để hoán vị
        if A[current_row][current_col] == 0:
            # vị trí dòng kế tiếp để xem xét
            other_row = current_row + 1

            # Tìm dòng thỏa có giá trị khác 0 tại cột đang xét
            while other_row < len(A):
                if A[other_row][current_col] != 0:
                    # Hoán vị dòng rồi thoát tìm (dòng thay thế)
                    line_permutation(A,current_row,other_row)
                    break
                other_row = other_row + 1

            # Nếu không tìm thấy dòng phù hợp tức là tại cột đang xét không có giá trị đầu dòng
            # Xét cột tiếp theo và tiếp tục vòng lặp
            if other_row >= len(A):
                current_col = current_col + 1
                continue

        # Đưa giá trị đầu dòng về 1
        head_value = A[current_row][current_col]
        for index in range(current_col,len(A[0])):
            A[current_row][index] = A[current_row][index] / head_value

        # Rút gọn cột
        for other_row in range(current_row+1,len(A)):
            head_value = A[other_row][current_col]
            for other_col in range(current_col,len(A[0])):
                if head_value != 0:
                    A[other_row][other_col] = A[other_row][other_col] - head_value * A[current_row][other_col]

        # Xét dòng với cột tiếp theo
        current_row = current_row + 1
        current_col = current_col + 1


# @input là ma trận bậc thang
# @output là cặp giá trị
#    - Giá trị đầu tiên cho biết HPT vô nghiệm(0), nghiệm duy nhất(1) hoặc vô số nghiệm(2)
#    - Giá trị thứ hai là danh sách các ma trận nghiệm
#        + Ma trận đầu tiên là ma trận số thực (không có ẩn tự do)
#        + Những ma trận sau(nếu có) là ma trận của các ẩn tự do
def back_substitution(A):
    # Vị trí hệ số tự do
    he_so = len(A[0]) - 1

    # Xóa các dòng 0
    for i in range(len(A)-1,-1,-1):
        temp = find_first_left(A[i])
        if temp != -1 or A[i][-1] != 0:
            break
        A.pop()

    # = 0 nếu vô nghiệm
    # = 1 nếu có nghiệm duy nhất
    # = 2 nếu có vô số nghiệm
    so_nghiem = 1  # mặc định

    # dùng để khởi tạo số cột từng nghiem trong bo_nghiem
    so_an = len(A[0])-1

    # dùng để tạo số ma trận nghiem cho bo_nghiem
    so_an_tu_do = so_an - len(A)

    # đánh dấu vị trí ma trận nghiệm thêm 1 vào nghiem trong bo_nghiem của ẩn tự do
    cur_an_tu_do = 0

    # Kiểm tra số ẩn tự do
    if so_an_tu_do > 0:
        so_nghiem = 2

    # nếu không có giá trị thì nghiệm trong bộ nghiêm = 0
    bo_nghiem = []

    # Khởi tạo bộ nghiệm
    nghiem = []
    for i in range(0,so_an_tu_do+1): # chỉ giải nghiệm nhiều nhất 1 ẩn tự do
        for j in range(0,so_an):
            nghiem.append(0)
        bo_nghiem.append(nghiem)
        nghiem = []

    # Tính nghiệm/bộ nghiệm
    left_first = 0         # vị trí có giá trị khác 0 đầu dòng
    curr_index = so_an - 1 # vị trí mong đợi là đầu dòng
    for i in range(len(A)-1, -1, -1):
        line = A[i]                        # dòng thứ i của ma trận thang A
        left_first = find_first_left(line) # vị trí giá trị khác 0 đầu tiên tại dòng đang xét

        # Xét trường hợp HPT vô nghiệm
        if left_first == -1 and line[-1] != 0:
            so_nghiem = 0
            break
        
        # Nếu vị trí đang xét (curr_index) không phải giá trị đầu dòng (left_first)
        # Thì tức là tại vị trí đang xét là ẩn tự do
        # Gán 1 tại vị trí ma trận tự do của nó
        # rồi lùi curr_index kiểm tra tiếp
        if left_first != curr_index:
            cur_an_tu_do += 1
            while True:
                # Thêm 1 vào vị trí phần ma trận nghiệm ẩn tự do tại cur_an_tu_do
                bo_nghiem[cur_an_tu_do][curr_index] = 1 

                # Xét tiếp cột tiếp theo tại dòng đó
                curr_index = curr_index - 1

                # Dừng vòng lặp nếu vị trí mong đợi đã trùng với vị trí đầu dòng
                if left_first == curr_index:
                    break

                # nếu còn ẩn tự do thì sẽ thêm 1 vào ma trận nghiệm ẩn tự do tiếp theo
                cur_an_tu_do = cur_an_tu_do + 1
        
        # Thay ngược giá trị
        bo_nghiem[0][left_first] = line[-1]      # Cộng hệ số tự do
        for j in range(0, so_an_tu_do+1):        # xét từng ma trận nghiệm trong bo_nghiem
            for h in range(left_first+1, so_an): # xét từng vị trí tại ma trận nghiệm đó
                bo_nghiem[j][left_first] -= line[h] * bo_nghiem[j][h]

        # Lùi vị trí đầu dòng mong đợi
        curr_index -= 1

    return so_nghiem,bo_nghiem
        

# Chưa có chức năng nhập ma trận từ màn hình console
# Chỉ có thể thay đổi giá trí ma trận trực tiếp từ source code
def main():
    print('\n')

    A = [[4,-2,-4,2,1],[6,-3,0,-5,3],[8,-4,28,-44,11],[-8,4,-4,12,-5]]

    print("Ma tran mo rong A   =", A)
    Gauss_elimination(A)
    print("Ma tran bac thang A =", A)

    so_nghiem,bo_nghiem = back_substitution(A)
    
    if so_nghiem == 0:
        print("HPT Vo nghiem")
    elif so_nghiem == 1:
        print("HPT co nghiem duy nhat")
        print(bo_nghiem)
    else:
        print("HPT co vo so nghiem")
        print(bo_nghiem)
    
    print('\n')
    

if __name__ == "__main__":
    main()



