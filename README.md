# Website Pengumpulan Dataset Audio

## Pendahuluan
Website Pengumpulan Dataset Audio merupakan aplikasi yang bertujuan untuk melakukan pengumpulan data audio hasil dari proses perekaman suara. Website ini juga mendata target perekaman (speaker) seperti jenis kelamin, kategori umur, suku dan dialek. Selain itu, kalimat yang dibacakan oleh speaker juga dihitung setelah proses perekaman selesai. 

Website ini dibuat di sistem operasi *Ubuntu 18.04* dengan bahasa pemrograman *Python 3.6* menggunakan framework *Django*. Website dapat diakses melalui browser secara lokal melalui alamat `http://localhost:<port>` atau secara jaringan  pribadi melalui `https://<ip_address>:<port>`. Website ini juga dapat di-deploy langsung ke cloud platform Heroku agar dapat diakses secara global (internet).
## Fitur
1. Perekaman Suara

    Website dapat melakukan perekaman suara berdasarkan suatu kalimat. Kalimat tersebut ditampilkan berdasarkan jumlah perekaman tersedikit dan ditampilkan secara acak. Hasil perekaman suara akan disimpan menjadi file audio format .wav dengan nama file berupa:
    
    **(kode kalimat)_(kode nama)_(jenis_kelamin)_(umur)_(suku)_(dialek)_(waktu perekaman).wav**

2. Pengelolaan Data
    Website mendukung pengelolaan data yang ada sebagai administrator seperti data kalimat, jenis kelamin, kategori umur, suku dan dialek. Fitur ini dilengkapi dengan fungsi dasar seperti menambah, melihat, mengubah, dan menghapus data. Selain itu, fitur ini juga dilengkapi dengan fungsi pencarian, filtering dan import export data.

## Instalasi
1. Buat virtual environment untuk Python 3.6 dan aktifkan.
    ```
    $ virtualenv -p python3.6 env
    $ source env/bin/activate
    ```

2. Install semua library yang diperlukan.
    ```
    $ pip install -r requirements.txt
    ```

3. Lakukan migrasi awal untuk django-model.
    ```
    $ python manage.py migrate
    ```

4. Buat superuser sebagai django-admin pertama.
    ```
    $ python manage.py createsuperuser
    ```
5. Jalankan server website dan akses `http://localhost:<port>` secara lokal.
    ```
    $ python manage.py runserver
    ```
6. Opsi lain untuk menjalankan server website melalui jaringan pribadi.
    ```
    $ python manage.py runsslserver <ip_address>:<port>
    ```
