import re

def clean_text(text: str) -> str:
    text = text.replace("₹", "Rs ")
    text = text.replace("O", "0").replace("S ", "5 ")
    text = re.sub(r"[^\w\s.,:/-]", " ", text)   # remove junk
    text = re.sub(r"\s+", " ", text)            # normalize spaces
    return text.strip()

def extract_merchant(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # Take first "reasonable" line (not too short / garbled)
    for line in lines[:10]:
        if len(line) > 5 and not re.search(r"\d", line):
            return line
    return None

def extract_date(text: str) -> str:
    match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    return match.group(1) if match else None

def extract_time(text: str) -> str:
    match = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?)", text)
    return match.group(1) if match else None

def extract_items(text: str):
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Pattern 1: item qty price
        m1 = re.match(r"(.+?)\s+(\d+)\s+(\d+(?:\.\d{1,2})?)$", line)
        # Pattern 2: item Rs price
        m2 = re.match(r"(.+?)\s+Rs\s?(\d+(?:\.\d{1,2})?)$", line)
        # Pattern 3: item with just a price at end
        m3 = re.match(r"(.+?)\s+(\d+(?:\.\d{1,2})?)$", line)

        if m1:
            desc, qty, price = m1.groups()
            items.append({
                "description": desc.strip(),
                "quantity": int(qty),
                "unit_price": float(price),
                "total": float(price)
            })
        elif m2:
            desc, price = m2.groups()
            items.append({
                "description": desc.strip(),
                "quantity": 1,
                "unit_price": float(price),
                "total": float(price)
            })
        elif m3:
            desc, price = m3.groups()
            items.append({
                "description": desc.strip(),
                "quantity": 1,
                "unit_price": float(price),
                "total": float(price)
            })

    return items

def parse_receipt(text: str) -> dict:
    text = clean_text(text)
    return {
        "merchant_name": extract_merchant(text),
        "date": extract_date(text),
        "time": extract_time(text),
        "items": extract_items(text)
    }
