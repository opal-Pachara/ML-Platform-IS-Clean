import streamlit as st
from model_utils import load_model, predict_with_model

def show_ml():
    st.markdown("""<h1 style='font-family: Athiti; text-align: center;'>Machine Learning Model</h1>""", unsafe_allow_html=True)
    
    # ระบุพาธเต็มของไฟล์ new_decision_tree_model.pkl
    model_path = r"Model ML (Classical)\new_decision_tree_model.pkl"
    
    # โหลดโมเดลโดยใช้ฟังก์ชันจาก model_utils
    model, expected_features = load_model(model_path)
    if model is None:
        return  # หยุดการทำงานถ้าโหลดโมเดลไม่สำเร็จ

    st.subheader("ทดลองใช้งานโมเดล Machine Learning")
    st.write(f"กรุณาใส่ข้อมูล {expected_features} ค่าเพื่อทำนายผล (คั่นด้วยเครื่องหมาย comma)")
    input_data = st.text_input(f"ข้อมูลนำเข้า (เช่น {','.join(['0']*expected_features)})", "")
    
    if st.button("ทำนายผล"):
        predict_with_model(model, input_data, expected_features)