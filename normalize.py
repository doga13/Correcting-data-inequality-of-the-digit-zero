#Doğa Yüksel

import cv2
import os

#bir görüntünün kenarlarında belirli bir ölçeğe göre daire çizer.
def draw_circle_at_edges(image_path, x, y, width_scale, height_scale):
    image = cv2.imread(image_path)  # Görüntüyü okur.
    height, width, _ = image.shape  # Görüntünün boyutlarını alır.

    # Üst sol köşe için dairenin merkezini hesapla.
    top_left_center_x = float(width) * x - float(width) * float(width_scale / 2)
    top_left_center_y = float(height) * y - float(height) * float(height_scale / 2)

    # Üst sağ köşe ve alt sağ köşe için dairenin merkezini hesapla.
    top_right_center_x = float(width) * x + float(width) * float(width_scale / 2)
    bottom_right_center_x = top_right_center_x
    bottom_right_center_y = float(height) * y + float(height) * float(height_scale / 2)

    top_left = (int(top_left_center_x), int(top_left_center_y))
    bottom_right = (int(bottom_right_center_x), int(bottom_right_center_y))
    coordinates = (top_left, bottom_right)
    
    return coordinates

#iki dikdörtgen alanı değiştirir.
def swap_digits(image_path, output_path, rect1_top_left, rect1_bottom_right, rect2_top_left, rect2_bottom_right):
    image = cv2.imread(image_path)  # Görüntüyü okur.
    # Birinci dikdörtgen alanı belirle.
    rect1_roi = image[rect1_top_left[1]:rect1_bottom_right[1], rect1_top_left[0]:rect1_bottom_right[0]]
    rect1_height, rect1_width = rect1_roi.shape[:2]
    # Birinci dikdörtgeni ikinci dikdörtgenin üstüne yazar.
    image[rect2_top_left[1]:rect2_top_left[1] + rect1_height, rect2_top_left[0]:rect2_top_left[0] + rect1_width] = rect1_roi
    cv2.imwrite(output_path, image)  # Sonucu dosyaya kaydeder.
    return

#metin dosyalarında geçen rakamları sayar.
def count_digits_in_txt_files(txt_folder):
    int_array = [0,0,0,0,0,0,0,0,0,0]  # Her rakam için bir sayaç dizisi.
    for filename in os.listdir(txt_folder):
        if filename.endswith('.txt') and 'output' not in filename:  # 'output' içermeyen .txt dosyalarını seç.
            with open(os.path.join(txt_folder, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.split()
                    if parts and parts[0].isdigit():  # Eğer satırda bir rakam varsa...
                        int_digit = int(parts[0])
                        int_array[int_digit] += 1  # Sayaç dizisinde rakamın sayısını arttır.
    return int_array

#Dizideki en küçük elemanın indeksini bulur.
def find_min_index(arr):
    if not arr:
        return -1
    min_value = arr[0]
    min_index = 0
    for i in range(1, len(arr)):
        if arr[i] < min_value:
            min_value = arr[i]
            min_index = i
    return min_index

# Bu fonksiyon, rakamların sıklığını eşitler.
def equalize(txt_folder, freq_arr):
    total = sum(freq_arr)
    print(f"Total: {total}")
    target = total / 10  # Her rakamın eşit sıklığa ulaşması için hedef değer.
    if (target < 1):
        target = 1
    minfreq = freq_arr[0]
    output_folder = r'C:\Users\doa\Desktop\new\labels'
    os.makedirs(output_folder, exist_ok=True)
    saveString = ''
    
    for filename in os.listdir(txt_folder):
        if filename.endswith('.txt') and 'output' not in filename:  # 'output' içermeyen .txt dosyalarını seç.
            input_file_path = os.path.join(txt_folder, filename)
            output_file_name = f"{filename.split('.')[0]}.txt"
            output_file_path = os.path.join(output_folder, output_file_name)

            with open(input_file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                minfreq = freq_arr[0] + 1
                minindex = 0
                count = 0
                
                for line in lines:
                    parts = line.split()
                    if parts and parts[0].isdigit() and freq_arr[int(parts[0])] < minfreq and freq_arr[int(parts[0])] <= target:
                        minfreq = freq_arr[int(parts[0])]
                        minindex = int(parts[0])
                        saveString = line
                        
                min_values = sorted(range(len(freq_arr)), key=lambda i: freq_arr[i])[:freq_arr[0]]  # Dizideki en küçük '0' sayısı kadar değerleri seçiyoruz.
                min_index_counter = 0  # Min değerleri sırayla almak için bir sayaç
                
                for line in lines:
                    parts = line.split()
                    count += 1
                    if parts and parts[0].isdigit() and int(parts[0]) == 0 and count > 1:
                        freq_arr[0] -= 1
                        minindex = min_values[min_index_counter]
                        freq_arr[minindex] += 1
                        
                        image_path = r'C:\Users\doa\Desktop\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\total_images' + filename.replace('.txt', '.jpeg')
                        output_path = r'C:\Users\doa\Desktop\new\images' + filename.replace('.txt', '.jpeg')
                        output_path = f"{filename.split('.')[0]}_output.jpeg"


                        #Command kisimlari ayni sayac arasinda degisim yapar.
                        # floatx, floatx2, floatx3, floatx4 = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                        # rect1=draw_circle_at_edges(image_path, floatx, floatx2, floatx3, floatx4)
                        
                        # parts2 = saveString.split()

                        # floatx, floatx2, floatx3, floatx4 = float(parts2[1]), float(parts2[2]), float(parts2[3]), float(parts2[4])
                        # rect2=draw_circle_at_edges(image_path, floatx, floatx2, floatx3, floatx4)

                        # swap_digits(image_path, image_path, rect2[0], rect2[1], rect1[0], rect1[1])
                        
                        # Değişim işlemi
                        line = str(minindex) + line[1:]
                        min_index_counter += 1
                        outfile.write(line)
                      
                    else:
                        outfile.write(line)
                        

# Etiket dosyalarını içeren klasör
txt_folder = r'C:\Users\doa\Desktop\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\total_labels'
freq_arr = count_digits_in_txt_files(txt_folder)  # Rakamların sıklıklarını sayar.
print(freq_arr)
equalize(txt_folder, freq_arr)  # Rakamların sıklığını eşitler.
print(freq_arr)
