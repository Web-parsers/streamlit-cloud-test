import streamlit as st
import requests
import subprocess
import json
import os

st.title("🔧 HTTP & System Debug Console")

# ---- HTTP Request Form ----
st.header("HTTP Request Tester")

method = st.selectbox("Method", ["GET", "POST", "OPTIONS"])
url = st.text_input("URL", "https://bot-backend-dev.webparsers.com/demo-bots/create-complete-demo-bot")
headers_text = st.text_area("Headers (JSON)", '{"Content-Type": "application/json"}')
body_text = st.text_area("Body (JSON, only for POST)", '{"test": "ping"}')

if st.button("Send via requests"):
    try:
        headers = json.loads(headers_text) if headers_text.strip() else {}
        data = json.loads(body_text) if body_text.strip() else {}

        if method == "GET":
            r = requests.get(url, headers=headers)
        elif method == "POST":
            r = requests.post(url, headers=headers, json=data)
        elif method == "OPTIONS":
            r = requests.options(url, headers=headers)
        else:
            st.error("Unsupported method")

        st.write("### Status Code:", r.status_code)
        st.write("### Headers:", dict(r.headers))
        st.write("### Body:", r.text[:2000])  # limit output
    except Exception as e:
        st.error(f"Request failed: {e}")

# ---- Curl Execution ----
st.header("cURL Execution")

curl_cmd = st.text_input("Enter cURL command", "curl -I https://bot-backend-dev.webparsers.com/")
if st.button("Run cURL"):
    try:
        result = subprocess.run(
            curl_cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        st.code(result.stdout + result.stderr)
    except Exception as e:
        st.error(f"cURL failed: {e}")

# ---- OS Operations ----
st.header("OS Operations")

os_cmd = st.text_input("Enter OS command", "curl ifconfig.me")
if st.button("Run OS Command"):
    try:
        result = subprocess.run(
            os_cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        st.code(result.stdout + result.stderr)
    except Exception as e:
        st.error(f"OS command failed: {e}")
