import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Setup Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # File dari Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Streamlit UI
st.title("🌅 Sunset Talk - Kirim Cerita Kamu")

name = st.text_input("Nama (Opsional)", "")
story = st.text_area("Tulis ceritamu di sini...")

if st.button("Kirim Cerita"):
    if story.strip():
        doc_ref = db.collection("stories").add({
            "name": name if name else "Anonim",
            "story": story,
            "timestamp": datetime.datetime.now()
        })
        st.success("Cerita kamu telah dikirim! Terima kasih! 🌅")
    else:
        st.error("Cerita tidak boleh kosong!")

# Menampilkan cerita yang sudah dikirim
st.subheader("📖 Cerita dari Audiens")
stories = db.collection("stories").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()

for s in stories:
    data = s.to_dict()
    st.write(f"**{data['name']}**: {data['story']}")
    st.markdown("---")
