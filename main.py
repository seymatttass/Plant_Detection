import streamlit as st
import psycopg2
import base64
import numpy as np
import cv2
from helper import classify_plant

# Veritabanından en son eklenen resmi getirme
def get_latest_image_from_db():
    try:
        connection = psycopg2.connect(
            dbname="dbtest",
            user="postgres",
            password="4141",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        query = "SELECT image FROM webcam_images ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        image_data = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return image_data

    except Exception as e:
        print(f"Veritabanından resim çekme hatası: {e}")
        return None

# Base64 formatında arka plan resmini yükleme
def load_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

# Streamlit uygulaması
def main():
    # Arka plan resmi ve CSS stilleri ekle
    bg_image = load_background_image('33.jpg')  # Arka plan resminin dosya adını ve yolunu buraya yazın
    page_bg_img = f'''
    <style>
    body {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    }}
    .stApp {{
        background: transparent;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Plant Health 🍃")

    # Kullanıcıdan resim seçme
    option = st.selectbox("Choose an option", ["Latest image from database", "Upload your own image", "Capture image from your phone"])

    if option == "Latest image from database":
        # Veritabanından en son eklenen resmi çek
        image_data = get_latest_image_from_db()

        if image_data:
            # Base64 verisini bytes'a dönüştür
            img_bytes = base64.b64decode(image_data)

            # Bytes verisini numpy array olarak oku
            nparr = np.frombuffer(img_bytes, np.uint8)

            # OpenCV ile görüntüyü oku
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Bitki sınıflandırma işlemi
            st.header("Sonuç")
            class_name, confidence = classify_plant(image)

            if class_name is not None and confidence is not None:
                st.write(f"Class: {class_name}")
                st.write(f"Confidence: {confidence:.2f}")

                # Sınıflandırılmış resmi göster
                st.image(image, channels="BGR", use_column_width=True)
            else:
                st.write("Sınıflandırma yapılamadı. Görüntüyü ve modeli kontrol edin.")

        else:
            st.write("Veritabanında resim bulunamadı.")

    elif option == "Upload your own image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Dosyayı oku ve işle
            image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # Bitki sınıflandırma işlemi
            st.header("Sonuç")
            class_name, confidence = classify_plant(image)

            if class_name is not None and confidence is not None:
                st.write(f"Class: {class_name}")
                st.write(f"Confidence: {confidence:.2f}")

                # Sınıflandırılmış resmi göster
                st.image(image, channels="BGR", use_column_width=True)
            else:
                st.write("Sınıflandırma yapılamadı. Görüntüyü ve modeli kontrol edin.")

        else:
            st.write("Lütfen bir resim yükleyin.")

    elif option == "Capture image from your phone":
        st.write("Bu seçenek şu anda geliştirme aşamasında. Lütfen daha sonra tekrar deneyin.")

if __name__ == "__main__":
    main()
