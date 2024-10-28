#Doğa Yüksel

import os
import cv2
import random

# Koordinatları normalize edilmiş formattan orijinal boyuta döndürür
def denormalize(coord, dim):
    return int(coord * dim)

# Veri kümesindeki rakam resimlerini yükler ve bir sözlükte saklar
def load_digit_images(dataset_folder):
    digit_images = {}
    for class_folder in os.listdir(dataset_folder):
        class_path = os.path.join(dataset_folder, class_folder)
        if os.path.isdir(class_path):
            digit_images[class_folder] = []
            for digit_image in os.listdir(class_path):
                digit_image_path = os.path.join(class_path, digit_image)
                image = cv2.imread(digit_image_path)
                digit_images[class_folder].append(image)
    return digit_images

# Etiket dosyasındaki bilgileri okuyup bir sözlükte saklar
def get_labels(label_path):
    labels = {}
    with open(label_path, 'r') as f:
        for idx, line in enumerate(f):
            parts = line.strip().split()
            class_id = parts[0]
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            labels[idx] = (class_id, x_center, y_center, width, height)
    return labels

# Belirtilen yükseklik ve genişliğe en yakın görüntüyü bulur
def find_closest_image(digit_images, new_class_id, target_height, target_width):
    closest_image = None
    closest_diff = float('inf')
    for height_class_folder in digit_images:
        if height_class_folder.startswith(f'class_{new_class_id}_height_'):
            _, _, _, height_str = height_class_folder.split('_')
            height = int(height_str)
            height_diff = abs(height - target_height)
            if height_diff <= closest_diff:
                for digit_image in digit_images[height_class_folder]:
                    img_h, img_w, _ = digit_image.shape
                    width_diff = abs(img_w - target_width)
                    total_diff = height_diff + width_diff
                    if total_diff < closest_diff:
                        closest_diff = total_diff
                        closest_image = digit_image
    return closest_image

# Belirtilen görüntüyü işler ve çıktıyı kaydeder
def process_image(image_path, orig_labels, new_labels, output_path, digit_images):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image: {image_path}")
        return

    H, W, _ = image.shape

    # Her bir etiket için işlemler
    for idx in new_labels:
        orig_class_id = orig_labels[idx][0]
        new_class_id = new_labels[idx][0]
        if orig_class_id != new_class_id:
            x_center = new_labels[idx][1]
            y_center = new_labels[idx][2]
            width = new_labels[idx][3]
            height = new_labels[idx][4]

            # Koordinatları denormalize et
            x_center = denormalize(x_center, W)
            y_center = denormalize(y_center, H)
            width = denormalize(width, W)
            height = denormalize(height, H)

            x1 = max(0, x_center - width // 2)
            y1 = max(0, y_center - height // 2)
            x2 = min(W, x_center + width // 2)
            y2 = min(H, y_center + height // 2)

            # En yakın yüksekliğe ve genişliğe sahip görseli seç
            digit_image = find_closest_image(digit_images, new_class_id, height, width)
            if digit_image is not None:

                #Width uymayan digitler için kırpma işlemi
                img_h, img_w, _ = digit_image.shape
                crop_img = digit_image[:min(img_h, y2-y1), :min(img_w, x2-x1)]

                # Ortaya yerleştirme için hesaplamalar
                y_offset = y1 + (y2 - y1 - crop_img.shape[0]) // 2
                x_offset = x1 + (x2 - x1 - crop_img.shape[1]) // 2

                # Yeni görüntüyü orijinal görüntü üzerine yerleştir
                image[y_offset:y_offset+crop_img.shape[0], x_offset:x_offset+crop_img.shape[1]] = crop_img
            else:
                print(f"No suitable image found for class {new_class_id} with height {height} and width {width}")

    # İşlenmiş görüntüyü kaydet
    cv2.imwrite(output_path, image)
    print(f'{output_path} kaydedildi.')

# Klasör yolları
image_folder = r'C:\Users\doa\Desktop\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\total_images'
orig_label_folder = r'C:\Users\doa\Desktop\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\total_labels'
new_label_folder = r'C:\Users\doa\Desktop\new\labels'
output_folder = r'C:\Users\doa\Desktop\new\images'
dataset_folder = r'C:\Users\doa\Desktop\WithoudRedCrop'

# Çıktı klasörünü oluştur
os.makedirs(output_folder, exist_ok=True)

# Rakam resimlerini yükle
digit_images = load_digit_images(dataset_folder)

# Her bir görüntü için işlem yap
for image_name in os.listdir(image_folder):
    if image_name.endswith('.jpeg'):
        image_path = os.path.join(image_folder, image_name)
        orig_label_path = os.path.join(orig_label_folder, image_name.replace('.jpeg', '.txt'))
        new_label_path = os.path.join(new_label_folder, image_name.replace('.jpeg', '.txt'))
        output_path = os.path.join(output_folder, image_name)

        # Etiket dosyaları varsa işlemi gerçekleştir
        if os.path.exists(orig_label_path) and os.path.exists(new_label_path):
            orig_labels = get_labels(orig_label_path)
            new_labels = get_labels(new_label_path)
            process_image(image_path, orig_labels, new_labels, output_path, digit_images)

print("İşlem tamamlandı!")
