#Doğa Yüksel

import os
import cv2

def denormalize(coord, dim):
    return int(coord * dim)

def process_image(image_path, label_path, output_folder):
    # Görüntüyü yükleyin
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image: {image_path}")
        return

    H, W, _ = image.shape

    # Etiket dosyasını okuyun
    with open(label_path, 'r') as f:
        lines = f.readlines()

    # Her etiketi işleyin ve kesilmiş görüntüleri kaydedin
    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) != 5:
            print(f"Skipping line {idx} in {label_path} due to incorrect format")
            continue

        try:
            class_id = parts[0]
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
        except ValueError as e:
            print(f"Skipping line {idx} in {label_path} due to value error: {e}")
            continue

        # Normalize edilmiş koordinatları orijinal boyutlara çevirin
        x_center = denormalize(x_center, W)
        y_center = denormalize(y_center, H)
        width = denormalize(width, W)
        height = denormalize(height, H)

        # Kesme koordinatlarını hesaplayın
        x1 = max(0, x_center - width // 2)
        y1 = max(0, y_center - height // 2)
        x2 = min(W, x_center + width // 2)
        y2 = min(H, y_center + height // 2)

        # Kesme işlemini gerçekleştirin
        digit_image = image[y1:y2, x1:x2]

        # Yükseklik değerine göre klasör oluşturun
        height_folder = os.path.join(output_folder, f'class_{class_id}_height_{height}')
        os.makedirs(height_folder, exist_ok=True)

        # Görüntüyü kaydedin
        output_path = os.path.join(height_folder, f'{os.path.basename(image_path).replace(".jpeg", "")}digit{idx}.jpeg')
        cv2.imwrite(output_path, digit_image)
        print(f'{output_path} kaydedildi.')

# Görüntü ve etiket klasörleri
image_folder = r"C:\Users\doa\Desktop\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\total_images"
label_folder = r"C:\Users\doa\Desktop\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\EVET_Dataset_wo_red_digits\total_labels"
output_folder = r"C:\Users\doa\Desktop\WithoudRedCrop"
os.makedirs(output_folder, exist_ok=True)

# Tüm görüntü dosyalarını işleyin
for image_name in os.listdir(image_folder):
    if image_name.endswith('.jpeg'):
        image_path = os.path.join(image_folder, image_name)
        label_path = os.path.join(label_folder, image_name.replace('.jpeg', '.txt'))

        if os.path.exists(label_path):
            process_image(image_path, label_path, output_folder)

print("İşlem tamamlandı!")