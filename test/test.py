import os

base_dir = r"D:\Source_MB\checkin\venv"
activate_this = os.path.join(base_dir, "Scripts", "activate")

if os.path.exists(activate_this):
    print(f"File activate tồn tại tại: {activate_this}")
else:
    print(f"Không tìm thấy file activate tại: {activate_this}")
