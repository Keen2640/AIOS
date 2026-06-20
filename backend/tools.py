from datetime import datetime

# -------------------------
# Calculator
# -------------------------
def calculator(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculator error: {e}"

# -------------------------
# Reverse Text
# -------------------------
def reverse_text(text):
    return text[::-1]

# -------------------------
# Current Time
# -------------------------
def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -------------------------
# Read File
# -------------------------
def file_reader(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Read error: {e}"

# -------------------------
# Write File
# -------------------------
def file_writer(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"Saved to {path}"
    except Exception as e:
        return f"Write error: {e}"