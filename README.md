# Bitki Hastalıklarını Tespit Eden Mobil Uygulama

Bu repoda, bitki hastalıklarını tespit etmek amacıyla geliştirilmiş mobil uygulamaya ait kod ve model bulunmaktadır. Uygulama, önceden eğitilmiş **Inception-V3** modelini kullanarak bitkilerdeki hastalıkları sınıflandırmaktadır. Ayrıca, kamera ile çekilen görüntülerin arka planı [remove.bg](https://www.remove.bg) servisi kullanılarak temizlenmekte ve bu işlem, hastalık tespiti öncesinde gerçekleştirilmektedir.

## Proje Genel Bakışı

### Veri Seti
Bitki hastalıklarının tespiti için, [Mendeley Data](https://data.mendeley.com/datasets/g7fpgj57wc/2) sitesinde yer alan veri setini kullandık. Bu veri seti, sağlıklı ve hasta bitkilere ait etiketli görüntüler içermektedir. Eğitim, doğrulama ve test setlerine bölerek modeli eğittik ve değerlendirdik.

### Model Mimarisi
Model, görüntü sınıflandırma görevlerinde başarılı olan **Inception-V3** mimarisi üzerine kurulmuştur. Transfer öğrenme yöntemini uyguladık ve modelimizi bitki hastalıklarını tespit edebilecek şekilde ince ayarladık.

### Ana Özellikler
- **Hastalık Tespiti**: Model, bitkinin bir görüntüsünden hastalık türünü tahmin eder.
- **Arka Plan Temizleme**: Daha iyi doğruluk için, kamera ile çekilen görüntüler `remove.bg` API'si ile işlenip arka plan temizlendikten sonra hastalık tespitine tabi tutulur.
- **Mobil Entegrasyon**: Model, mobil uygulamaya entegre edilmiştir. Kullanıcılar, bitki görüntülerini kameradan çekebilir veya yükleyebilir ve anında hastalık tespit sonuçları alabilir.

## Model Detayları

Model mimarisi şu katmanlardan oluşmaktadır:

- **Inception-V3** taban modeli (ImageNet üzerinde önceden eğitilmiş, son katmanları kaldırılmış).
- **Global Ortalama Havuzlama Katmanı**: Inception-V3 ağının çıkışındaki özelliklerin boyutunu azaltır.
- **Tam Bağlantılı Katmanlar**: 1024 nöronlu iki tam bağlantılı katman ve `ReLU` aktivasyon fonksiyonu.
- **Dropout Katmanları**: Aşırı öğrenmeyi önlemek için her tam bağlantılı katmandan sonra eklenmiştir.
- **Çıkış Katmanı**: Hastalıkları çok sınıflı sınıflandırma amacıyla softmax aktivasyonlu bir katman.

### Eğitim Süreci

Model, Mendeley'den indirilen veri seti ile aşağıdaki konfigürasyonda eğitildi:

- **Optimizasyon**: Adam
- **Kayıp Fonksiyonu**: Kategorik Çapraz Entropi
- **Batch Boyutu**: 12
- **Epoch Sayısı**: 20
- **Callbacks**: 
  - ModelCheckpoint: En iyi doğrulama doğruluğuna göre modeli kaydeder.
  - EarlyStopping: 10 epoch boyunca doğrulama doğruluğunda iyileşme olmazsa eğitimi durdurur.

### Değerlendirme

Model, test veri setinde yüksek doğruluk oranı elde etmiştir ve farklı bitki hastalıklarını tespit etmede oldukça başarılıdır.

## Kurulum ve Kurulum Adımları

1. Bu repoyu klonlayın:
    ```bash
    git clone <repo-link>
    cd <repo-directory>
    ```

2. Gerekli Python paketlerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3. Verileri [Mendeley](https://data.mendeley.com/datasets/g7fpgj57wc/2) üzerinden indirip, `train`, `test` ve `val` dizinlerine yerleştirin.

4. Google Drive'ınızı Colab'e bağlayın (Colab kullanıyorsanız):
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    ```

5. Modeli eğitmek için aşağıdaki scripti çalıştırın:
    ```bash
    python train.py
    ```

6. Eğitilen modeli mobil uygulamaya entegre edin.

## Kullanım

- **Görüntü yakalama veya yükleme**: Kullanıcı, bir bitkinin fotoğrafını çekebilir veya mevcut bir görüntüyü yükleyebilir.
- **Arka Plan Temizleme**: Uygulama, `remove.bg` API'si kullanarak görüntüdeki arka planı temizler.
- **Hastalık Tespiti**: Temizlenmiş görüntü, hastalık tespiti için Inception-V3 modeline gönderilir. Tahmin edilen hastalık sonucu ekranda gösterilir.

## Teşekkürler

- **Veri Seti**: Bitki hastalıklarının sınıflandırılması için yüksek kaliteli veriler sağlayan [Plant Village Dataset](https://data.mendeley.com/datasets/g7fpgj57wc/2) katkıcılarına teşekkür ederiz.
- **remove.bg**: Arka plan temizleme için [remove.bg](https://www.remove.bg) servisini kullandık.
