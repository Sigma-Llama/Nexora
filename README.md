# Nexora - Aplikacija za Sporočilno

To je aplikacija za pošiljanje sporočil v realnem času. Namen aplikacije je ravnovesje med privatnostjo in funkcijonalnostjo.

## 👥 Avtorja

* **Luka Podbreznik**
* **Sinan Šale**

---

## 📖 O Projektu

Nexora je projekt, razvit v programskem jeziku Python, ki je arhitekturno ločen na dva glavna segmenta:
* **Strežnik (Server):** Hrbtenica aplikacije, ki skrbi za vso poslovno logiko, upravljanje s podatkovno bazo, avtentikacijo uporabnikov in pošiljanje sporočil.
* **Odjemalec (Client/App):** Namizni grafični vmesnik (GUI), ki služi kot točka za interakcijo uporabnika s strežnikom.

Cilj projekta je ustvariti robustno in razširljivo platformo za klepet.

---

## ✨ Ključne Funkcionalnosti

* **Avtentikacija Uporabnikov:** Registracija in prijava uporabnikov.
* **Upravljanje s Klepeti:** Ustvarjanje, brisanje in upravljanje sob.
* **Pošiljanje Sporočil:** Pošiljanje sporočil v realnem času z uporabo WebSocketov.
* **Podatkovna Baza:** Shranjevanje uporabnikov, sporočil in podatkov o klepetih v MySQL bazi.
* **Ponastavitev Gesla:** Funkcionalnost ponastavitve pozabljenega gesla preko e-pošte (Gmail).
* **Upravljanje Pravic:** Sistem za določanje vlog in pravic uporabnikov (v razvoju).
* **Docker Integracija:** Celoten strežniški del je zapakiran v Docker vsebnike za enostavno postavitev in skalabilnost.
* **Napredna enkripcija:** Čeprav je še vedno v delu, bo aplikaciaja imela odlično End-To-End enkripcijo sporočil. 

---

## 🛠️ Tehnološki Sklop

* **Backend:** Python
* **Frontend (GUI):** Python z knjižnico Custom Tkinter
* **Podatkovna Baza:** MySQL
* **Komunikacija:** WebSockets
* **Strežniška tehnologija:** Docker & Docker Compose

---

## 📁 Struktura Projekta

<code>Nexora/
│
├── client/
│   ├── app/
│   │   ├── app_gui.py
│   │   ├── domain_gui.py
│   │   ├── login_sigin_gui.py
│   │   ├── main.py
│   │   └── websocket.py
│   └── release/
|       └── v1
│
├── server/
│   ├── mysql/
│   │   ├── db.sql
│   │   └── Dockerfile
│   │
│   ├── python/
│   │   ├── db_def.py
│   │   ├── gmail_call.py
│   │   ├── main.py
│   │   ├── websocket.py
│   │   └── Dockerfile
|   |
│   ├── release/
|   |   └── v1
|   └── docker-compose.yml
|
├── LICENSE
└── README.md</code>

---

## Kako Začeti?

Za zagon projekta boste potrebovali nameščen **Docker**, **Docker Compose** in **Python 3** (za zagon odjemalca).

### 1. Zagon Strežnika (Server)

Strežnik je v celoti zasnovan za delo v Docker okolju, tako je najlažje za vzpostavitev strižnika in predstavlja najmanj težav.

1.  **Klonirajte repozitorij:**
    ```sh
    git clone https://github.com/Sigma-Llama/Nexora.git
    cd Nexora
    ```

2.  **Zaženite Docker Compose:**
    Ta ukaz bo zgradil in zagnal Docker konteiner, ki vsebuje Python aplikacijo in MySQL podatkovno bazo.
    Za zagon konteinerja moremo prvo locirati datoteko `docker-compose.yml`, z naslednjimi komandami.
    ```sh
    cd server
    docker-compose up -d
    ```

Strežnik bo že deloval vendar brez grafičnega vmesnika. Strežnik bo tako že pošiljal in sprejemau podatke preko prejdoločenega porta (definiran v `docker-compose.yml`).

### 2. Zagon Odjemalca (Client/App)

Odjemalec se zažene lokalno in se poveže na strežnik.

1.  **Pojdite v mapo odjemalca:**
    ```sh
    cd client/app/release
    ```

2.  **Zaženite glavno aplikacijo:**

    Tukaj samo zaženite aplikacijo.
    
    ```sh
    Nexar.exe
    ```

Aplikacija bi se morala odpreti in vam omogočiti prijavo ali registracijo.

---

## OpenSource

Ta projekt je popolnoma open source. Z tem lahko dokažemo največjo vrnost podatkov.