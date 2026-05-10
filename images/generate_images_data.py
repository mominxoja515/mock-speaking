"""
Bu skriptni lokal kompyuteringizda ishlatib, images_data.py ni to'ldiring.

Ishlatish:
  1. Bu fayl va images/ papkangiz bir joyda bo'lsin
  2. Terminal/CMD da: python generate_images_data.py
  3. Chiqadigan images_data.py ni GitHub-ga push qiling

images/ papkasidagi fayl nomlari:
  img1.jpg, img2.jpg, ... img10.jpg  bo'lishi kerak
  (yoki quyidagi MAPPING ni o'zingizning fayl nomlaringizga moslashtiring)
"""

import base64
import os

IMAGES_FOLDER = "images"   # images/ papkangiz

# Fayl nomlarini img_key larga moslashtiring
MAPPING = {
    "img1":  "img1.jpg",
    "img2":  "img2.jpg",
    "img3":  "img3.jpg",
    "img4":  "img4.jpg",
    "img5":  "img5.jpg",
    "img6":  "img6.jpg",
    "img7":  "img7.jpg",
    "img8":  "img8.jpg",
    "img9":  "img9.jpg",
    "img10": "img10.jpg",
}

def encode_image(path: str) -> str:
    """Rasmni base64 ga o'giradi."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    lines = ["IMAGES = {"]
    found = 0
    missing = []

    for key, filename in MAPPING.items():
        # .jpg bo'lmasa .png ni ham sinab ko'radi
        candidates = [
            os.path.join(IMAGES_FOLDER, filename),
            os.path.join(IMAGES_FOLDER, filename.replace(".jpg", ".png")),
            os.path.join(IMAGES_FOLDER, filename.replace(".jpg", ".jpeg")),
            os.path.join(IMAGES_FOLDER, filename.replace(".jpg", ".webp")),
        ]
        found_file = None
        for c in candidates:
            if os.path.exists(c):
                found_file = c
                break

        if found_file:
            b64 = encode_image(found_file)
            lines.append(f'    "{key}": "{b64}",')
            print(f"✅  {key} → {found_file}  ({len(b64)//1024} KB)")
            found += 1
        else:
            lines.append(f'    "{key}": "",  # ⚠️ fayl topilmadi: {filename}')
            missing.append(filename)
            print(f"⚠️   {key} → topilmadi: {filename}")

    lines.append("}")

    output = "\n".join(lines) + "\n"
    with open("images_data.py", "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\n✅ images_data.py tayyor! ({found}/{len(MAPPING)} rasm)")
    if missing:
        print(f"⚠️  Topilmagan fayllar: {missing}")
        print("   Fayl nomlarini MAPPING da to'g'rilang va qayta ishrating.")

if __name__ == "__main__":
    main()
