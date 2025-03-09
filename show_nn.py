import streamlit as st
import torch
from datetime import time

def load_model(model_path):
    try:
        model = torch.load(model_path, map_location=torch.device('cpu'))
        model.eval()
        return model
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {str(e)}")
        return None

def preprocess_input(location, festival, travel_time, day, weather):
    location_map = {"กรุงเทพ": 0, "เชียงใหม่": 1, "ภูเก็ต": 2}
    festival_map = {"ไม่มี": 0, "สงกรานต์": 1, "ลอยกระทง": 2}
    day_map = {"จันทร์": 0, "อังคาร": 1, "พุธ": 2, "พฤหัส": 3, "ศุกร์": 4, "เสาร์": 5, "อาทิตย์": 6}
    weather_map = {"แจ่มใส": 0, "ฝนตก": 1, "หมอก": 2}

    location_val = location_map.get(location, 0)
    festival_val = festival_map.get(festival, 0)
    time_val = travel_time.hour + travel_time.minute / 60
    day_val = day_map.get(day, 0)
    weather_val = weather_map.get(weather, 0)

    input_tensor = torch.tensor([location_val, festival_val, time_val, day_val, weather_val], dtype=torch.float32)
    return input_tensor.unsqueeze(0)

def show_nn():
    st.markdown("<h1 style='font-family: Athiti; text-align: center;'>Traffic Prediction (Neural Network)</h1>", unsafe_allow_html=True)
    
    # โหลดโมเดล
    model_path = "model/best_traffic_prediction_model.pt"  # ปรับพาธให้สัมพันธ์กับโฟลเดอร์
    model = load_model(model_path)
    if model is None:
        return

    # รับ input
    location = st.selectbox("สถานที่จะไป", ["กรุงเทพ", "เชียงใหม่", "ภูเก็ต"])
    festival = st.selectbox("เทศกาล", ["ไม่มี", "สงกรานต์", "ลอยกระทง"])
    travel_time = st.time_input("เวลาที่ต้องการเดินทาง", value=time(12, 0))
    day = st.selectbox("วัน", ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์", "เสาร์", "อาทิตย์"])
    weather = st.selectbox("สภาพอากาศ", ["แจ่มใส", "ฝนตก", "หมอก"])

    if st.button("ทำนายการจราจร"):
        input_tensor = preprocess_input(location, festival, travel_time, day, weather)
        with torch.no_grad():
            prediction = model(input_tensor)
            prediction_value = prediction.item()
        st.success(f"ระดับความหนาแน่น: {prediction_value:.2f} (0 = โล่ง, 100 = แน่นมาก)")
        if prediction_value < 30:
            st.write("จราจรโล่ง เดินทางสะดวก")
        elif prediction_value < 70:
            st.write("จราจรปานกลาง อาจล่าช้า")
        else:
            st.write("จราจรหนาแน่น เผื่อเวลา")