# 🐢 Duvardan Kaçan Kaplumbağa

## Proje Hakkında

Bu proje, ROS 2 Humble ve Python kullanılarak geliştirilmiş otonom bir kaplumbağa hareket kontrol uygulamasıdır.

Projenin amacı, Turtlesim simülasyon ortamında hareket eden bir kaplumbağanın konumunu sürekli takip ederek duvarlara yaklaştığında yön değiştirmesini sağlamaktır.

Uygulama, ROS 2'nin publisher/subscriber haberleşme yapısını ve parametre yönetimini kullanmaktadır.

## 1. Ödev Gereksinimleri

Proje kapsamında aşağıdaki işlemler gerçekleştirilmiştir:

- `turtle_duvar_py` isimli Python paketi oluşturulmuştur.
- `/turtle1/pose` konusuna abone olunarak kaplumbağanın X ve Y koordinatları okunmuştur.
- `/turtle1/cmd_vel` konusuna hız komutları gönderilmiştir.
- Kaplumbağanın otonom şekilde ileri hareket etmesi sağlanmıştır.
- X veya Y koordinatı 1.0'ın altına ya da 10.0'ın üzerine çıktığında duvar algılanmıştır.
- Duvar algılandığında kaplumbağanın yön değiştirmesi sağlanmıştır.
- `get_logger().info()` kullanılarak terminale duvar uyarıları yazdırılmıştır.

### Bonus: ROS 2 Parametreleri

Hareket hızı ve duvar sınırları ROS 2 parametreleri üzerinden değiştirilebilir.

| Parametre | Açıklama |
|---|---|
| `hiz` | Kaplumbağanın ileri hareket hızı |
| `alt_sinir` | Duvar algılama alt sınırı |
| `ust_sinir` | Duvar algılama üst sınırı |

## 2. Kullanılan Teknolojiler

- Ubuntu
- ROS 2 Humble
- Python 3
- Turtlesim
- `rclpy`
- `geometry_msgs`
- `turtlesim.msg.Pose`

## 3. Çalışma Mantığı

Program başlatıldığında kaplumbağa ileri doğru hareket etmeye başlar.

ROS 2 üzerinden kaplumbağanın konumu sürekli okunur.

Kaplumbağa duvarlara yaklaştığında mevcut konumu kontrol edilir ve yön değiştirme işlemi gerçekleştirilir.

Yön değiştirme tamamlandığında kaplumbağa yeniden ileri hareket eder.

Bu süreç program durdurulana kadar devam eder.

### Duvar Algılama Koşulu

```python
if x < 1.0 or x > 10.0 or y < 1.0 or y > 10.0:
```

Duvar algılandığında terminalde aşağıdakine benzer bir mesaj görüntülenir:

```text
[INFO] Duvara yaklasildi! x=10.05, y=5.54
```

## 4. Kurulum

ROS 2 Humble kurulu Ubuntu ortamında bir çalışma alanı oluşturulur.

```bash
mkdir -p ~/robotik_ws/src
cd ~/robotik_ws/src
```

Proje bu çalışma alanının `src` klasörüne yerleştirilir.

Ardından paket derlenir:

```bash
cd ~/robotik_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select turtle_duvar_py --symlink-install
source install/setup.bash
```

## 5. Çalıştırma

İlk terminalde Turtlesim başlatılır:

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

İkinci terminalde proje çalıştırılır:

```bash
source /opt/ros/humble/setup.bash
source ~/robotik_ws/install/setup.bash
ros2 run turtle_duvar_py duvar_kac
```

### Parametrelerle Çalıştırma

Hız ve sınır değerleri aşağıdaki gibi değiştirilebilir:

```bash
ros2 run turtle_duvar_py duvar_kac --ros-args -p hiz:=2.0 -p alt_sinir:=2.0 -p ust_sinir:=9.0
```

### Parametreleri Kontrol Etme

```bash
ros2 param list /duvar_kac
```

```bash
ros2 param get /duvar_kac hiz
ros2 param get /duvar_kac alt_sinir
ros2 param get /duvar_kac ust_sinir
```

## 6. Test Sonuçları

Uygulama Turtlesim üzerinde test edilmiştir.

Testler sırasında:

- Kaplumbağanın ileri hareket ettiği,
- Duvarlara yaklaştığında yön değiştirdiği,
- Duvar algılama mesajlarının terminalde görüntülendiği,
- ROS 2 parametrelerinin başarıyla okunduğu

gözlemlenmiştir.

## 7. Ekran Görüntüleri

Projenin çalışmasına ait ekran görüntüleri `images/` klasöründe paylaşılacaktır.

## 8. Proje Dosyaları

```text
turtle_duvar_py/
├── turtle_duvar_py/
│   ├── __init__.py
│   └── duvar_kac.py
├── resource/
├── test/
├── package.xml
├── setup.py
├── setup.cfg
├── README.md
└── images/
```

`build/`, `install/` ve `log/` klasörleri derleme çıktıları olduğu için teslim paketine dahil edilmez.
