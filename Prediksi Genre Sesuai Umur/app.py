import streamlit as st
import pandas as pd
import joblib
import html
import os

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Prediksi Genre Musik",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
header[data-testid="stHeader"] {
    background: transparent;
}

.stApp {
    background:
        radial-gradient(circle at top left, #121222 0%, transparent 35%),
        radial-gradient(circle at bottom right, #171126 0%, transparent 35%),
        #080910;
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.logo {
    text-align: center;
    font-size: 55px;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #a855f7;
    margin-bottom: 12px;
}

.subtitle {
    text-align: center;
    color: #b8b8c5;
    font-size: 19px;
    margin-bottom: 25px;
}

.badge {
    width: fit-content;
    margin: 0 auto 35px auto;
    padding: 12px 25px;
    border-radius: 30px;
    background: linear-gradient(135deg, #6657f5, #a855f7);
    font-weight: bold;
}

div[data-testid="stNumberInput"] input {
    background-color: #191a24 !important;
    color: white !important;
    border-radius: 15px !important;
    min-height: 55px;
}

div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] label {
    color: white !important;
    font-weight: 500;
}

div[data-testid="stNumberInput"] label p {
    color: white !important;
    font-size: 16px;
}

div.stButton > button {
    width: 100%;
    min-height: 58px;
    border: none;
    border-radius: 16px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(135deg, #6657f5, #a855f7);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    color: white;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.35);
}

.result-card {
    background: linear-gradient(
        135deg,
        rgba(102, 87, 245, 0.18),
        rgba(166, 77, 244, 0.12)
    );
    border: 1px solid #694ff4;
    border-radius: 24px;
    padding: 30px;
    text-align: center;
    margin-top: 30px;
}

.genre-result {
    font-size: 42px;
    font-weight: 800;
    color: #a855f7;
    margin: 12px 0;
}

.section-box {
    background: #101118;
    border: 1px solid #292a35;
    border-radius: 25px;
    padding: 35px;
    margin-top: 35px;
}

.section-title {
    text-align: center;
    font-size: 27px;
    font-weight: bold;
    margin-bottom: 30px;
}

.song-card {
    background: #191a23;
    border: 1px solid #30313c;
    padding: 18px 22px;
    border-radius: 15px;
    margin-bottom: 12px;
    transition: 0.3s;
}

.song-card:hover {
    border-color: #a855f7;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.25);
}

.song-card.playing {
    border-color: #a855f7;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
}

div[data-testid="column"] div.stButton > button {
    min-height: 42px;
    font-size: 14px;
    border-radius: 12px;
}

.now-playing-box {
    background: #101118;
    border: 1px solid #694ff4;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 25px;
}

.now-playing-label {
    color: #a855f7;
    font-weight: bold;
    margin-bottom: 12px;
}

.now-playing-frame {
    border-radius: 14px;
    overflow: hidden;
}

.song-title {
    font-size: 18px;
    font-weight: bold;
    color: white;
}

.artist-name {
    color: #a9a9b5;
    margin-top: 6px;
}

.spotify-text {
    color: #1DB954;
    margin-top: 12px;
    font-weight: bold;
}

.cards-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.info-card {
    background: #191a23;
    border: 1px solid #30313c;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    transition: 0.3s;
}

.info-card:hover {
    transform: translateY(-4px);
    border-color: #a855f7;
    box-shadow: 0 10px 28px rgba(139, 92, 246, 0.25);
}

@keyframes melayang {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.step-icon-wrap {
    width: 68px;
    height: 68px;
    margin: 0 auto 18px auto;
    border-radius: 50%;
    background: linear-gradient(135deg, #6657f5, #a855f7);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.step-icon-emoji {
    font-size: 30px;
    display: inline-block;
    animation: melayang 2.4s ease-in-out infinite;
}

.info-card:nth-child(1) .step-icon-emoji { animation-delay: 0s; }
.info-card:nth-child(2) .step-icon-emoji { animation-delay: 0.3s; }
.info-card:nth-child(3) .step-icon-emoji { animation-delay: 0.6s; }

.step-badge {
    position: absolute;
    top: -6px;
    right: -6px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #080910;
    border: 2px solid #a855f7;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    color: white;
}

.number-circle {
    width: 58px;
    height: 58px;
    margin: 0 auto 20px auto;
    border-radius: 50%;
    background: linear-gradient(135deg, #6657f5, #a855f7);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    font-weight: bold;
}

.card-title {
    font-size: 19px;
    font-weight: bold;
    margin-bottom: 12px;
}

.card-text {
    color: #b9b9c5;
    line-height: 1.7;
}

.features-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.feature-item {
    background: #191a23;
    border: 1px solid #30313c;
    padding: 26px;
    border-radius: 18px;
    transition: 0.3s;
    text-align: center;
}

.feature-item:hover {
    transform: translateY(-4px);
    border-color: #a855f7;
    box-shadow: 0 10px 28px rgba(139, 92, 246, 0.25);
}

.feature-icon {
    width: 56px;
    height: 56px;
    margin: 0 auto 16px auto;
    border-radius: 16px;
    background: linear-gradient(135deg, #6657f5, #a855f7);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
}

.feature-title {
    font-size: 17px;
    font-weight: bold;
    color: white;
    margin-bottom: 8px;
}

.feature-desc {
    color: #b9b9c5;
    font-size: 14px;
    line-height: 1.6;
}

.check {
    display: inline-flex;
    width: 30px;
    height: 30px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: linear-gradient(135deg, #6657f5, #a855f7);
    margin-right: 10px;
    color: white;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: #777785;
    margin-top: 50px;
    padding: 25px;
}

@media (max-width: 768px) {
    .cards-container,
    .features-container {
        grid-template-columns: 1fr;
    }

    .main-title {
        font-size: 35px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================
try:
    model = joblib.load("knn_music_genre_model.pkl")
    scaler = joblib.load("scaler_age.pkl")
    genre_encoder = joblib.load("label_encoder_genre.pkl")

except FileNotFoundError as e:
    st.error(f"File model tidak ditemukan: {e}")
    st.stop()

except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

# =========================================================
# 60 REKOMENDASI LAGU
# 12 GENRE × 5 LAGU
# =========================================================
artis_dikenal = {

    # Bollywood
    "tumhiho": "Arijit Singh",
    "kesariya": "Arijit Singh",
    "kalhonaaho": "Sonu Nigam",
    "channamereya": "Arijit Singh",
    "malang": "Ved Sharma",

    # Classical
    "furelise": "Ludwig van Beethoven",
    "canonind": "Johann Pachelbel",
    "thefourseasonsspring": "Antonio Vivaldi",
    "thefourseasons": "Antonio Vivaldi",
    "moonlightsonata": "Ludwig van Beethoven",
    "swanlake": "Pyotr Ilyich Tchaikovsky",

    # Country
    "takemehomecountryroads": "John Denver",
    "jolene": "Dolly Parton",
    "thegambler": "Kenny Rogers",
    "beforehecheats": "Carrie Underwood",
    "tennesseewhiskey": "Chris Stapleton",

    # Electronic
    "animals": "Martin Garrix",
    "faded": "Alan Walker",
    "leanon": "Major Lazer & DJ Snake",
    "titanium": "David Guetta ft. Sia",
    "wakemeup": "Avicii",

    # Hip-Hop
    "loseyourself": "Eminem",
    "sickomode": "Travis Scott",
    "godsplan": "Drake",
    "humble": "Kendrick Lamar",
    "industrybaby": "Lil Nas X & Jack Harlow",

    # Indie
    "sweaterweather": "The Neighbourhood",
    "505": "Arctic Monkeys",
    "riptide": "Vance Joy",
    "home": "Edward Sharpe & The Magnetic Zeros",
    "pumpedupkicks": "Foster The People",

    # Jazz
    "takefive": "Dave Brubeck",
    "flymetothemoon": "Frank Sinatra",
    "whatawonderfulworld": "Louis Armstrong",
    "autumnleaves": "Bill Evans Trio",
    "myfavoritethings": "John Coltrane",

    # K-Pop
    "dynamite": "BTS",
    "howyoulikethat": "BLACKPINK",
    "lovedive": "IVE",
    "ditto": "NewJeans",
    "godsmenu": "Stray Kids",

    # Latin
    "despacito": "Luis Fonsi ft. Daddy Yankee",
    "bailando": "Enrique Iglesias",
    "migente": "J Balvin & Willy William",
    "takitaki": "DJ Snake",
    "vivirmivida": "Marc Anthony",

    # Pop
    "shapeofyou": "Ed Sheeran",
    "blindinglights": "The Weeknd",
    "levitating": "Dua Lipa",
    "flowers": "Miley Cyrus",
    "asitwas": "Harry Styles",

    # R&B
    "earnedit": "The Weeknd",
    "noguidance": "Chris Brown ft. Drake",
    "leavethedooropen": "Silk Sonic",
    "adorn": "Miguel",
    "webelongtogether": "Mariah Carey",

    # Rock
    "bohemianrhapsody": "Queen",
    "smellsliketeenspirit": "Nirvana",
    "hotelcalifornia": "Eagles",
    "sweetchildomine": "Guns N' Roses",
    "backinblack": "AC/DC",
}

# =========================================================
# LOKASI FOLDER MUSIK LOKAL
# =========================================================
# Dihitung berdasarkan lokasi file app.py ini sendiri, supaya
# tetap benar walau Streamlit dijalankan dari direktori lain.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "music")

EKSTENSI_AUDIO = (".mp3", ".wav", ".m4a", ".ogg")


def normalisasi(teks):
    return "".join(c for c in teks.lower() if c.isalnum())


def cari_folder_genre(genre):
    """
    Mencari nama folder di dalam music/ yang cocok dengan
    genre hasil prediksi (tidak peka huruf besar/kecil).
    Mengembalikan nama folder ASLI di disk, atau None.
    """

    if not os.path.isdir(MUSIC_DIR):
        return None

    for nama_folder in os.listdir(MUSIC_DIR):
        path_folder = os.path.join(MUSIC_DIR, nama_folder)
        if os.path.isdir(path_folder) and nama_folder.lower() == genre.lower():
            return nama_folder

    return None


def ambil_lagu_dari_folder(nama_folder):
    """
    Membaca semua file audio di dalam music/<nama_folder>/
    dan mengembalikan daftar (judul, artis, path_file).

    Judul diambil dari nama file (tanpa ekstensi).
    Artis diisi dari tabel artis_dikenal jika judulnya
    dikenali, kalau tidak dikosongkan.
    """

    folder = os.path.join(MUSIC_DIR, nama_folder)

    if not os.path.isdir(folder):
        return []

    file_list = sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith(EKSTENSI_AUDIO)
    )

    daftar_lagu = []

    for nama_file in file_list[:5]:
        judul = os.path.splitext(nama_file)[0]
        artis = artis_dikenal.get(normalisasi(judul), "")
        path_file = os.path.join(folder, nama_file)
        daftar_lagu.append((judul, artis, path_file))

    return daftar_lagu


# =========================================================
# STATE PEMUTAR MUSIK
# =========================================================
if "now_playing" not in st.session_state:
    st.session_state.now_playing = None

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="logo">🎵</div>
<div class="main-title">Prediksi Genre Musik</div>
<div class="subtitle">
Temukan genre musik yang sesuai dengan usiamu dan nikmati rekomendasi lagu pilihan untuk menemani setiap suasana.
</div>
<div class="badge">
🎧 Prediksi Berdasarkan Usia
</div>
""", unsafe_allow_html=True)

# =========================================================
# INPUT USIA
# =========================================================
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    usia = st.number_input(
        "Masukkan usia pengguna (15-60 tahun)",
        min_value=15,
        max_value=60,
        value=21,
        step=1
    )

    tombol_prediksi = st.button(
        "🎵 Cari Genre",
        use_container_width=True
    )

    if tombol_prediksi:
        st.session_state.sudah_prediksi = True
        st.session_state.usia_terakhir = usia

# =========================================================
# HASIL PREDIKSI
# =========================================================
if "sudah_prediksi" not in st.session_state:
    st.session_state.sudah_prediksi = False

if st.session_state.sudah_prediksi:

    usia = st.session_state.usia_terakhir

    # Membuat data input
    data_baru = pd.DataFrame(
        [[usia]],
        columns=["age"]
    )

    # Standardisasi
    data_scaled = scaler.transform(data_baru)

    # Prediksi KNN
    hasil_prediksi = model.predict(data_scaled)

    # Mengubah angka encoding menjadi nama genre
    genre = genre_encoder.inverse_transform(
        hasil_prediksi
    )[0]

    genre = str(genre).strip()

    # =====================================================
    # HASIL GENRE
    # =====================================================
    st.markdown(f"""
<div class="result-card">
<div style="color:#b8b8c5;">
Hasil Prediksi Genre Musik
</div>

<div class="genre-result">
🎶 {html.escape(genre)}
</div>

<div style="color:#b8b8c5;">
Berdasarkan usia pengguna:
<b>{usia} tahun</b>
</div>
</div>
""", unsafe_allow_html=True)

    # =====================================================
    # CARI FOLDER GENRE
    # =====================================================
    genre_key = cari_folder_genre(genre)

    daftar_lagu = (
        ambil_lagu_dari_folder(genre_key) if genre_key else []
    )

    # =====================================================
    # REKOMENDASI LAGU
    # =====================================================
    st.markdown("""
<div class="section-box">
<div class="section-title">
🎧 5 Rekomendasi Lagu
</div>
""", unsafe_allow_html=True)

    if genre_key and daftar_lagu:

        # Jika ada lagu yang sedang diputar, tampilkan pemutarnya
        # di bagian atas, sebelum daftar lagu.
        now_playing = st.session_state.now_playing

        if now_playing and now_playing["genre"] == genre_key:
            label_artis = (
                f" — {html.escape(now_playing['artis'])}"
                if now_playing["artis"] else ""
            )

            st.markdown(f"""
<div class="now-playing-box">
<div class="now-playing-label">
▶ Sedang Diputar: {html.escape(now_playing['judul'])}{label_artis}
</div>
</div>
""", unsafe_allow_html=True)

            if os.path.isfile(now_playing["path"]):
                try:
                    st.audio(now_playing["path"], autoplay=True)
                except TypeError:
                    # Versi Streamlit lama belum punya parameter autoplay
                    st.audio(now_playing["path"])
                    st.caption(
                        "Klik tombol ▶ pada pemutar di atas untuk "
                        "mulai memutar (autoplay tidak didukung di "
                        "versi Streamlit ini)."
                    )
            else:
                st.warning(
                    "File audio untuk lagu ini tidak ditemukan lagi. "
                    "Mungkin file sudah dipindah atau dihapus."
                )

        for nomor, (judul, artis, path_file) in enumerate(
            daftar_lagu,
            start=1
        ):

            is_playing = (
                now_playing
                and now_playing["genre"] == genre_key
                and now_playing["path"] == path_file
            )

            card_class = "song-card playing" if is_playing else "song-card"

            baris_artis = (
                f"""<div class="artist-name">🎤 {html.escape(artis)}</div>"""
                if artis else ""
            )

            col_info, col_tombol = st.columns([5, 1])

            with col_info:
                st.markdown(f"""
<div class="{card_class}">
<div class="song-title">
{nomor}. 🎵 {html.escape(judul)}
</div>
{baris_artis}
</div>
""", unsafe_allow_html=True)

            with col_tombol:
                label = "⏸ Diputar" if is_playing else "▶ Putar"
                if st.button(
                    label,
                    key=f"play_{genre_key}_{nomor}",
                    use_container_width=True
                ):
                    if is_playing:
                        st.session_state.now_playing = None
                    else:
                        st.session_state.now_playing = {
                            "genre": genre_key,
                            "judul": judul,
                            "artis": artis,
                            "path": path_file
                        }
                    st.rerun()

    elif genre_key and not daftar_lagu:
        st.warning(
            f"Belum ada file mp3 di folder `music/{genre_key}/`. "
            "Tambahkan hingga 5 file audio (.mp3, .wav, .m4a, atau .ogg) "
            "ke folder tersebut."
        )

    else:
        st.warning(
            f"Rekomendasi untuk genre '{genre}' belum tersedia. "
            f"Pastikan ada folder `music/{genre}/` yang berisi file audio."
        )

    # Menutup section rekomendasi
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================================================
# CARA KERJA
# =========================================================
st.markdown("""
<div class="section-box">

<div class="section-title">
Cara Menggunakan Aplikasi
</div>

<div class="cards-container">

<div class="info-card">
<div class="step-icon-wrap">
<span class="step-icon-emoji">🔢</span>
<span class="step-badge">1</span>
</div>
<div class="card-title">Masukkan Usia</div>
<div class="card-text">
Isi kolom usia sesuai dengan usiamu saat ini
menggunakan tombol angka yang tersedia.
</div>
</div>

<div class="info-card">
<div class="step-icon-wrap">
<span class="step-icon-emoji">🎯</span>
<span class="step-badge">2</span>
</div>
<div class="card-title">Klik Cari Genre</div>
<div class="card-text">
Tekan tombol "Cari Genre" dan tunggu sebentar
hingga hasil prediksi muncul di layar.
</div>
</div>

<div class="info-card">
<div class="step-icon-wrap">
<span class="step-icon-emoji">🎧</span>
<span class="step-badge">3</span>
</div>
<div class="card-title">Dengarkan Musik</div>
<div class="card-text">
Pilih salah satu rekomendasi lagu, lalu tekan
tombol "Putar" untuk mendengarkannya langsung.
</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FITUR SISTEM
# =========================================================
st.markdown("""
<div class="section-box">

<div class="section-title">
Fitur Sistem Prediksi Genre Musik
</div>

<div class="features-container">

<div class="feature-item">
<div class="feature-icon">🎯</div>
<div class="feature-title">Prediksi Personal</div>
<div class="feature-desc">
Genre musik diprediksi otomatis sesuai dengan usia yang kamu masukkan.
</div>
</div>

<div class="feature-item">
<div class="feature-icon">⚡</div>
<div class="feature-title">Hasil Instan</div>
<div class="feature-desc">
Cukup satu klik, hasil prediksi dan rekomendasi langsung tampil.
</div>
</div>

<div class="feature-item">
<div class="feature-icon">🎶</div>
<div class="feature-title">5 Lagu Pilihan</div>
<div class="feature-desc">
Setiap genre dilengkapi lima rekomendasi lagu terbaik untukmu.
</div>
</div>

<div class="feature-item">
<div class="feature-icon">▶️</div>
<div class="feature-title">Putar Langsung</div>
<div class="feature-desc">
Dengarkan lagunya langsung di dalam aplikasi, tanpa perlu pindah ke platform lain.
</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
🎧 Temukan Genre Favoritmu, Dengarkan Musik yang Sesuai dengan Gayamu
</div>
""", unsafe_allow_html=True)