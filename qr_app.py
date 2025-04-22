import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="Tạo mã QR", page_icon="📱")
st.title("📱 TẠO MÃ QR CODE CÓ LOGO")

qr_type = st.radio("🔹 Chọn loại mã QR:", ["URL", "Wi-Fi"])

logo_file = st.file_uploader("📎 Tải lên logo (tùy chọn)", type=["png", "jpg", "jpeg"])
qr_size = st.slider("🖼️ Kích thước QR (px)", min_value=200, max_value=800, value=400)

def generate_qr(content, logo_file=None):
    # Tạo mã QR với mức sửa lỗi cao để chèn logo
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_img = qr_img.resize((qr_size, qr_size))

    # Nếu có logo
    if logo_file is not None:
        logo = Image.open(logo_file)
        # Resize logo
        logo_size = int(qr_size * 0.2)
        logo = logo.resize((logo_size, logo_size))

        # Tính vị trí dán logo
        pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    return qr_img


if qr_type == "URL":
    url = st.text_input("🌐 Nhập URL:")
    if st.button("🚀 Tạo mã QR"):
        if url:
            img = generate_qr(url, logo_file)
            st.image(img, caption="✅ Mã QR của bạn")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("⬇️ Tải mã QR", data=buf.getvalue(), file_name="qr_url.png", mime="image/png")
        else:
            st.warning("❗ Vui lòng nhập URL!")

elif qr_type == "Wi-Fi":
    ssid = st.text_input("📶 Tên mạng Wi-Fi (SSID):")
    password = st.text_input("🔑 Mật khẩu Wi-Fi:", type="password")
    encryption = st.selectbox("🔒 Loại mã hóa:", ["WPA", "WEP", "nopass"])

    if st.button("🚀 Tạo mã QR"):
        if ssid:
            wifi_content = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
            img = generate_qr(wifi_content, logo_file)
            st.image(img, caption="✅ Mã QR Wi-Fi")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("⬇️ Tải mã QR", data=buf.getvalue(), file_name="qr_wifi.png", mime="image/png")
        else:
            st.warning("❗ Vui lòng nhập tên mạng Wi-Fi!")