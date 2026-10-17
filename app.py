import random
import requests
import gradio as gr

# Açık kaynaklı Türkçe Sözlük veri tabanı URL'si
SOZLUK_DATA_URL = "https://raw.githubusercontent.com/fatih/turkce-sozluk/master/sozluk.json"

SOZLUK_VERISI = {}
KELIME_LISTESI = []

# Kelimelerin türeyiş yolları ve varsa kültürel/tarihsel hikayeleri için zenginleştirilmiş veri tabanı
HIKAYE_VERISI = {
    "pusula": {
        "tureyis": "İtalyanca 'bussola' (küçük kutu) sözcüğünden gelir. Latince 'buxus' (şimşir ağacı) köküne dayanır; çünkü ilk pusula kutuları şimşir ağacından yapılırdı.",
        "hikaye": "Denizcilik tarihini değiştiren bu araç, ilk zamanlar karanlıkta parlayan sihirli bir kutu gibi görüldüğü için gemiciler arasında mistik bir saygıyla korunurdu."
    },
    "yakamoz": {
        "tureyis": "Rumca 'diakamós' (deniz ışıltısı) kelimesinden dilimize geçmiştir.",
        "hikaye": "Sadece ay ışığı olmadığında, denizdeki tek hücreli canlıların (Noctiluca scintillans) hareketiyle oluşan bu parıltı, eski balıkçılar tarafından 'denizin canlı uykusu' olarak adlandırılırdı."
    },
    "feraset": {
        "tureyis": "Arapça 'frs' kökünden türeyen 'farāsat' (sezme, anlama yetisi) kelimesinden gelir. Aynı kökten gelen 'faras' (at) kelimesiyle de bağlantılıdır.",
        "hikaye": "Eski göçebe kültürlerde iyi bir binicinin atın ruh halini ve gideceği yolu gözlerinden sezebilmesi ustalığından esinlenerek, zihnin en yüksek sezgi seviyesine 'feraset' denilmiştir."
    },
    "hemdem": {
        "tureyis": "Farsça 'hem-' (birlikte, eş) ve 'dem' (nefes, an) kelimelerinin birleşmesiyle türetilmiştir.",
        "hikaye": "Klasik edebiyatta sadece yan yana olan değil, aynı havayı soluyan, sustuklarında bile birbirini anlayan en yakın dostları ve can yoldaşlarını tanımlamak için tasarlanmış derin bir kelimedir."
    }
}

def sozluk_yukle():
    global SOZLUK_VERISI, KELIME_LISTESI
    try:
        print("Türkçe sözlük veri tabanı yükleniyor...")
        response = requests.get(SOZLUK_DATA_URL, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                madde = item.get("madde", "").strip()
                anlam = item.get("anlam", "").strip()
                koken = item.get("lisan", "").strip() or "Türkçe / Belirtilmemiş"
                if madde and anlam:
                    SOZLUK_VERISI[madde.lower()] = {
                        "anlam": anlam,
                        "koken": koken
                    }
            KELIME_LISTESI = list(SOZLUK_VERISI.keys())
            print(f"Başarıyla {len(KELIME_LISTESI)} kelime belleğe yüklendi!")
    except Exception as e:
        print("Sözlük yüklenirken hata oluştu, yedek veriler aktif.", e)

    if not KELIME_LISTESI:
        # Ana sözlük çekilemezse varsayılanları kullan
        SOZLUK_VERISI = {
            "pusula": {"anlam": "Açık denizlerde yön bulmaya yarayan, mıknatıslı iğnesi olan araç.", "koken": "İtalyanca"},
            "yakamoz": {"anlam": "Denizde mikroskobik canlıların çıkardığı biyolojik ışıltı.", "koken": "Rumca"},
            "feraset": {"anlam": "Çabuk kavrama, sezgi yeteneği.", "koken": "Arapça"},
            "hemdem": {"anlam": "Birlikte nefes alan, can dost, yakın arkadaş.", "koken": "Farsça"}
        }
        KELIME_LISTESI = list(SOZLUK_VERISI.keys())

sozluk_yukle()

def dinamik_kart_uret(istenen_tur):
    # Hikaye verisi olan kelimelere öncelik tanıyalım
    mevcut_ozel_kelimeler = [k for k in KELIME_LISTESI if k in HIKAYE_VERISI]
    
    if mevcut_ozel_kelimeler and random.random() < 0.7:  # %70 ihtimalle hikayesi olanları seç
        baslik = random.choice(mevcut_ozel_kelimeler)
    else:
        baslik = random.choice(KELIME_LISTESI)
        
    veri = SOZLUK_VERISI[baslik]
    anlam = veri["anlam"]
    koken = veri["koken"]
    
    # Hikaye ve türeyiş bilgilerini çek veya varsayılan oluştur
    hikaye_detay = HIKAYE_VERISI.get(
        baslik, 
        {
            "tureyis": f"{koken} kökenli bu sözcük zamanla Türkçeleşerek günümüzdeki formunu kazanmıştır.",
            "hikaye": "Bu kelime günlük dilde sıklıkla kullanılmakta olup köklü bir geçmişe sahiptir."
        }
    )

    # Modern Gelişmiş Kart Tasarımı
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #12121e 0%, #1c1c2e 100%);
        border-radius: 20px;
        padding: 28px;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        max-width: 520px;
        margin: auto;
        border: 1px solid #33334d;
    ">
        <!-- Başlık -->
        <div style="font-size: 11px; font-weight: 800; letter-spacing: 2px; color: #ff79c6; margin-bottom: 6px; text-transform: uppercase;">
            🔮 ETİMOLOJİ & KELİME HİKAYESİ
        </div>

        <h2 style="font-size: 34px; margin: 0 0 10px 0; color: #f8f8f2; text-transform: capitalize; font-weight: 700;">
            {baslik}
        </h2>

        <!-- Köken -->
        <div style="
            font-size: 13px; 
            color: #8be9fd; 
            margin-bottom: 18px; 
            background: rgba(139, 233, 253, 0.12); 
            padding: 6px 14px; 
            border-radius: 30px; 
            display: inline-block;
            font-weight: 600;
        ">
            🌍 Köken: {koken}
        </div>

        <!-- Bölüm 1: Anlam -->
        <div style="margin-bottom: 18px;">
            <div style="font-size: 12px; font-weight: 700; color: #f1fa8c; margin-bottom: 4px; text-transform: uppercase;">📖 Kelime Anlamı</div>
            <div style="font-size: 15px; line-height: 1.5; color: #e0e0e0; background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; border-left: 3px solid #f1fa8c;">
                {anlam}
            </div>
        </div>

        <!-- Bölüm 2: Nasıl Türedi -->
        <div style="margin-bottom: 18px;">
            <div style="font-size: 12px; font-weight: 700; color: #50fa7b; margin-bottom: 4px; text-transform: uppercase;">🌱 Nasıl Türedi? (Morfoloji)</div>
            <div style="font-size: 14px; line-height: 1.5; color: #e0e0e0; background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; border-left: 3px solid #50fa7b;">
                {hikaye_detay['tureyis']}
            </div>
        </div>

        <!-- Bölüm 3: Kültürel Hikayesi -->
        <div>
            <div style="font-size: 12px; font-weight: 700; color: #ffb86c; margin-bottom: 4px; text-transform: uppercase;">✨ Kelimenin Hikayesi</div>
            <div style="font-size: 14px; line-height: 1.5; color: #e0e0e0; background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; border-left: 3px solid #ffb86c; font-style: italic;">
                "{hikaye_detay['hikaye']}"
            </div>
        </div>
    </div>
    """
    return card_html

# Gradio Arayüzü Oluşturma
with gr.Blocks(title="Kelime Atlası - Etimoloji ve Hikayeler") as demo:
    gr.Markdown(
        """
        # 📚 Kelime Atlası: Anlam, Etimoloji ve Hikayeler
        Kelimelerin sadece anlamlarını değil; köklerini, nasıl türediklerini ve barındırdıkları gizli hikayeleri öğrenin.
        """
    )

    with gr.Row():
        btn_kelime = gr.Button("✨ Rastgele Hikayeli Kelime Keşfet", variant="primary")

    output_card = gr.HTML(value=dinamik_kart_uret("kelime"))

    btn_kelime.click(fn=lambda: dinamik_kart_uret("kelime"), outputs=output_card)

demo.launch(share=True)
