"""Swoozh icon definitions, 24x24 grid.

Style (from SwoozhIcons): 1.5 px centre stroke, butt caps, miter joins, sharp
corners. Closed shapes are inset 0.75 so the outer edge sits on the keyline.

Element kinds:
  "o"   line, stroked in both variants
  "s"   shape, stroked in Outline, solid in Filled (open paths fill as if closed)
  "cut" detail, stroked in Outline, knocked out of the solid in Filled
  "k"   knockout only in Filled (separation gaps), invisible in Outline
  "d"   dot, solid in Outline, knocked out in Filled
  "f"   solid in both variants
"""
import math


def n(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def circ(cx, cy, r):
    return f"M{n(cx - r)} {n(cy)}a{n(r)} {n(r)} 0 1 0 {n(2 * r)} 0a{n(r)} {n(r)} 0 1 0 {n(-2 * r)} 0Z"


def poly(pts):
    return "M" + "L".join(f"{n(x)} {n(y)}" for x, y in pts) + "Z"


def star(cx, cy, ro, ri, k, rot=-90):
    pts = []
    for i in range(2 * k):
        a = math.radians(rot + i * 180 / k)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts)


def arc(cx, cy, r, a0, a1):
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f"M{n(x0)} {n(y0)}A{n(r)} {n(r)} 0 {large} {sweep} {n(x1)} {n(y1)}"


BAG = "M4.75 7.75H19.25V21.25H4.75Z"
BAG_HANDLE_LONG = "M8.75 10.5V6.25a3.25 3.25 0 0 1 6.5 0V10.5"
BAG_HANDLE = "M8.75 7.75V6.25a3.25 3.25 0 0 1 6.5 0V7.75"
CART_LINE = "M1.75 3.75H4.6L7.1 15.25H18.25"
CART_BASKET = "M5.6 7.25H21.25L19.4 13.75H7Z"
CART_WHEELS = [("s", circ(8.75, 19.25, 1.5)), ("s", circ(16.75, 19.25, 1.5))]
BOX_LID = "M2.75 3.75H21.25V7.75H2.75Z"
BOX_BODY = "M3.75 7.75H20.25V20.25H3.75Z"

CATEGORIES = {
    "🛍️ Shopping & commerce": {
        "shopping-bag": ([("s", BAG), ("o", BAG_HANDLE_LONG)], "bag, shop, buy, purchase"),
        "shopping-bag-plus": ([("s", BAG), ("o", BAG_HANDLE), ("cut", "M12 11.75V17.25M9.25 14.5H14.75")], "bag, add, buy"),
        "shopping-bag-check": ([("s", BAG), ("o", BAG_HANDLE), ("cut", "M9.25 14.5L11.25 16.5L14.75 13")], "bag, done, bought, order"),
        "shopping-cart": ([("o", CART_LINE), ("s", CART_BASKET)] + CART_WHEELS, "cart, trolley, buy"),
        "shopping-cart-plus": ([("o", CART_LINE), ("s", CART_BASKET), ("cut", "M13.5 8.75V12.25M11.75 10.5H15.25")] + CART_WHEELS, "cart, add, buy"),
        "basket": ([("s", "M2.75 9.75H21.25L19.25 20.25H4.75Z"), ("o", "M7.25 9.75L10.25 3.75M16.75 9.75L13.75 3.75"),
                    ("cut", "M8.75 13.25V16.75M12 13.25V16.75M15.25 13.25V16.75")], "basket, groceries, shop"),
        "store": ([("s", "M4.25 2.75H19.75L21.25 8.75H2.75Z"), ("s", "M4.75 8.75H19.25V21.25H4.75Z"),
                   ("cut", "M9.25 2.75L8.5 8.75M14.75 2.75L15.5 8.75M9.75 21.25V15.25H14.25V21.25")], "store, shop, boutique, retail"),
        "gift": ([("s", "M2.75 7.75H21.25V11.75H2.75Z"), ("s", "M4.25 11.75H19.75V21.25H4.25Z"),
                  ("cut", "M12 7.75V21.25M2.75 11.75H21.25"),
                  ("o", "M12 7.75C10.5 4 7.25 2.5 6.75 4.75C6.25 7 9.5 7.75 12 7.75C14.5 7.75 17.75 7 17.25 4.75C16.75 2.5 13.5 4 12 7.75")],
                 "gift, present, reward"),
        "receipt": ([("s", "M4.75 2.75H19.25V21.25L16.83 19.75L14.42 21.25L12 19.75L9.58 21.25L7.17 19.75L4.75 21.25Z"),
                     ("cut", "M8.25 7.25H15.75M8.25 11H15.75M8.25 14.75H12.75")], "receipt, bill, invoice, order"),
        "barcode": ([("o", "M2.75 7.75V3.75H6.75M17.25 3.75H21.25V7.75M21.25 16.25V20.25H17.25M6.75 20.25H2.75V16.25"),
                     ("o", "M7.25 7.5V16.5M10.25 7.5V16.5M12.5 7.5V16.5M15.25 7.5V16.5M17.25 7.5V16.5")], "barcode, scan, product"),
        "badge-percent": ([("s", star(12, 12, 9, 7.25, 8, -90 + 11.25)), ("cut", "M9 15L15 9"),
                           ("cut", circ(9.5, 9.5, 0.75)), ("cut", circ(14.5, 14.5, 0.75))], "sale, discount, offer, percent"),
        "coupon": ([("s", "M2.75 5.75H21.25V9.5A2.5 2.5 0 0 0 21.25 14.5V18.25H2.75V14.5A2.5 2.5 0 0 0 2.75 9.5Z"),
                    ("cut", "M15 5.75V7.75M15 11V13M15 16.25V18.25")], "coupon, voucher, ticket, promo"),
        "heart": ([("s", "M12 19.5L4.74 12.26A4.25 4.25 0 1 1 12 9.25A4.25 4.25 0 1 1 19.26 12.26Z")], "wishlist, favourite, like, love"),
        "star": ([("s", star(12, 12.75, 8.25, 4.1, 5))], "rating, review, favourite"),
    },
    "💳 Paymen & shipping": {
        "credit-card": ([("s", "M2.75 4.75H21.25V19.25H2.75Z"), ("cut", "M2.75 9.25H21.25M6 15.25H10")], "card, payment, pay"),
        "wallet": ([("s", "M19.25 11.25V6.75H2.75V20.25H19.25V15.75"), ("s", "M14.25 11.25H21.25V15.75H14.25Z"),
                    ("o", "M4.25 6.75L15.25 3.25L16.5 6.75"), ("d", circ(17.25, 13.5, 1))], "wallet, payment, balance"),
        "banknote": ([("s", "M2.75 6.75H21.25V17.25H2.75Z"), ("cut", circ(12, 12, 2.25)),
                      ("d", circ(6.25, 12, 1)), ("d", circ(17.75, 12, 1))], "cash, money, bill"),
        "coins": ([("s", "M15.68 8.32A6.5 6.5 0 1 1 8.32 15.68A6.5 6.5 0 0 0 15.68 8.32Z"), ("s", circ(9.25, 9.25, 6.5)),
                   ("k", circ(9.25, 9.25, 8))], "coins, money, cash, points"),
        "contactless": ([("o", arc(4.5, 12, 4.25, -40, 40)), ("o", arc(4.5, 12, 8.5, -40, 40)), ("o", arc(4.5, 12, 12.75, -40, 40))],
                        "contactless, tap, nfc, payment"),
        "truck": ([("s", "M5.31 16.75H2.75V5.75H14.25V9.25H18.25L21.25 12.75V16.75H19.19M15.31 16.75H9.19"),
                   ("cut", "M14.25 9.25V16.75M16.25 9.25V12.75H21.25"),
                   ("s", circ(7.25, 17.25, 2)), ("s", circ(17.25, 17.25, 2)),
                   ("k", circ(7.25, 17.25, 3.5)), ("k", circ(17.25, 17.25, 3.5))], "shipping, delivery, truck"),
        "package": ([("s", "M12 2.5L20.75 7V17L12 21.5L3.25 17V7Z"), ("cut", "M3.25 7L12 11.5L20.75 7M12 11.5V21.5M7.63 4.75L16.38 9.25")],
                    "package, parcel, box, order"),
        "box": ([("s", BOX_LID), ("s", BOX_BODY), ("cut", "M2.75 7.75H21.25M9.75 11.25H14.25")], "box, archive, storage"),
        "box-check": ([("s", BOX_LID), ("s", BOX_BODY), ("cut", "M2.75 7.75H21.25M9.25 13.75L11.25 15.75L14.75 12.25")], "delivered, order, box"),
        "box-return": ([("s", BOX_LID), ("s", BOX_BODY), ("cut", "M2.75 7.75H21.25M15 17V13.25H9.5M11.5 11.25L9.5 13.25L11.5 15.25")],
                       "return, refund, box"),
    },
    "👗 Fashion & apparel": {
        "hanger": ([("o", "M10 6.25a2 2 0 1 1 2 2V9.5"), ("s", "M12 9.5L2.75 15.5V17.75H21.25V15.5Z")], "hanger, wardrobe, clothes"),
        "t-shirt": ([("s", "M8.25 3.75L2.75 6.5L4.5 11L6.75 10.25V20.25H17.25V10.25L19.5 11L21.25 6.5L15.75 3.75C15.25 5.25 13.9 6.25 12 6.25C10.1 6.25 8.75 5.25 8.25 3.75Z")],
                    "t-shirt, top, tee, clothes"),
        "jacket": ([("s", "M8.25 3.75L4 5.75L2.75 20.25H6.25L6.75 12V21.25H17.25V12L17.75 20.25H21.25L20 5.75L15.75 3.75L12 7.25Z"),
                    ("cut", "M12 7.25V21.25")], "jacket, coat, outerwear"),
        "dress": ([("s", "M9.25 2.75V6.25L7.5 10L9.5 11.5L5 21.25H19L14.5 11.5L16.5 10L14.75 6.25V2.75H13.25V5.25C12.5 6 11.5 6 10.75 5.25V2.75Z"),
                   ("cut", "M9.5 11.5H14.5")], "dress, women, clothes"),
        "skirt": ([("s", "M7.25 3.75H16.75V6.25L20.25 20.25H3.75L7.25 6.25Z"), ("cut", "M7.25 6.25H16.75M10.25 6.25L9 20.25M13.75 6.25L15 20.25")],
                  "skirt, women, clothes"),
        "pants": ([("s", "M5.25 2.75H18.75L20.25 21.25H14.25L12 9.25L9.75 21.25H3.75Z"), ("cut", "M5.01 5.75H18.99")], "pants, trousers, jeans"),
        "shorts": ([("s", "M4.25 3.75H19.75L21.25 17.25H14L12 10.25L10 17.25H2.75Z"), ("cut", "M3.92 6.75H20.08")], "shorts, summer, clothes"),
        "sock": ([("s", "M8.25 2.75H15.25V13.25L10.75 19.75C9.75 21.25 7.5 21.6 6 20.6C4.5 19.6 4.25 17.5 5.25 16L8.25 11.75Z"),
                  ("cut", "M8.25 6.25H15.25")], "sock, socks, hosiery"),
        "cap": ([("s", "M4.75 14.75C4.75 9.25 7.75 5.75 12 5.75C16.25 5.75 19.25 9.25 19.25 14.75Z"),
                 ("s", "M2.75 14.75H21.25C21.25 17 17 18.25 12 18.25C7 18.25 2.75 17 2.75 14.75Z"),
                 ("cut", "M12 5.75V14.75"), ("f", circ(12, 3.75, 1.25))], "cap, hat, headwear"),
        "sunglasses": ([("s", "M2.75 9.75H10.25V12.5C10.25 14.5 8.75 16.25 6.5 16.25C4.25 16.25 2.75 14.5 2.75 12.5Z"),
                        ("s", "M13.75 9.75H21.25V12.5C21.25 14.5 19.75 16.25 17.5 16.25C15.25 16.25 13.75 14.5 13.75 12.5Z"),
                        ("o", "M10.25 10.75C11.25 10 12.75 10 13.75 10.75M2.75 9.75L4.25 7.25M21.25 9.75L19.75 7.25")],
                       "sunglasses, glasses, eyewear, accessories"),
        "watch": ([("s", circ(12, 12, 5.25)), ("s", "M8.72 7.9L9.25 2.75H14.75L15.28 7.9"), ("s", "M8.72 16.1L9.25 21.25H14.75L15.28 16.1"),
                   ("cut", "M12 9.5V12L13.75 13")], "watch, time, accessories"),
        "handbag": ([("s", "M3.25 9.25H20.75L19.25 20.25H4.75Z"), ("o", "M8 9.25V7a4 4 0 0 1 8 0V9.25"), ("cut", "M10.25 12.75H13.75")],
                    "handbag, purse, bag, accessories"),
        "sneaker": ([("s", "M2.75 7.75H8.25L10.75 10.75L13.5 11.75L19 13.25C20.4 13.65 21.25 14.75 21.25 16.25V18.25H2.75Z"),
                     ("cut", "M2.75 15.25H21.25M9.75 9.75L8.25 11.25M11.75 11.5L10.25 13")], "sneaker, shoe, trainers, footwear"),
        "high-heel": ([("s", "M3.25 6.25C5.5 6.25 7 7.5 8.5 9.75L11 13.25C12 14.75 13.75 15.75 16 16.25L19.5 17C20.6 17.25 21.25 18 21.25 19.25H10.75C9.5 19.25 8.5 18.5 7.75 17.5L6.75 15.75L5.75 21.25H4.25V12.75C3.5 11.25 3.25 9 3.25 6.25Z")],
                      "high heel, shoe, pump, footwear"),
        "diamond": ([("s", "M7.25 3.75H16.75L21.25 9.25L12 20.75L2.75 9.25Z"),
                     ("cut", "M2.75 9.25H21.25M9.5 3.75L8 9.25L12 20.75L16 9.25L14.5 3.75")], "diamond, jewelry, gem, premium"),
    },
}


def gear(cx, cy, ro, ri, k, top=10, base=17):
    pts = []
    for i in range(k):
        a = i * 360 / k
        for r, d in ((ri, -base), (ro, -top), (ro, top), (ri, base)):
            t = math.radians(a + d)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return poly(pts)


PIN = "M12 21.75C12 21.75 4.75 15 4.75 10A7.25 7.25 0 0 1 19.25 10C19.25 15 12 21.75 12 21.75Z"
EYE = "M2.25 12C4.5 7.75 8 5.25 12 5.25C16 5.25 19.5 7.75 21.75 12C19.5 16.25 16 18.75 12 18.75C8 18.75 4.5 16.25 2.25 12Z"
BELL = "M4.25 17.75L5.75 15.25V10.25A6.25 6.25 0 0 1 18.25 10.25V15.25L19.75 17.75Z"
BELL_EXTRA = [("o", "M9.75 20.75H14.25"), ("o", "M12 2.75V4")]
U_HEAD, U_BODY = circ(12, 7.75, 4), "M4.25 21.25C4.25 16.5 7.75 13.75 12 13.75C16.25 13.75 19.75 16.5 19.75 21.25Z"
US_HEAD, US_BODY = circ(9.5, 7.75, 4), "M2.75 21.25C2.75 16.5 6 13.75 9.5 13.75C13 13.75 16.25 16.5 16.25 21.25Z"

CATEGORIES.update({
    "🧭 Navigation & places": {
        "home": ([("s", "M3.75 9.5L12 3L20.25 9.5V21.25H3.75Z"), ("cut", "M9.75 21.25V15.25H14.25V21.25")], "home, house, start"),
        "map-pin": ([("s", PIN), ("cut", circ(12, 10, 2.5))], "location, pin, place, address"),
        "map-pin-check": ([("s", PIN), ("cut", "M9.25 10L11.25 12L14.75 8.5")], "location, confirmed, address"),
        "map": ([("s", "M2.75 5.5L8.75 3.25L15.25 5.5L21.25 3.25V18.5L15.25 20.75L8.75 18.5L2.75 20.75Z"),
                 ("cut", "M8.75 3.25V18.5M15.25 5.5V20.75")], "map, directions, store locator"),
        "compass": ([("s", circ(12, 12, 9.25)), ("cut", "M15.75 8.25L13.25 13.25L8.25 15.75L10.75 10.75Z")], "compass, explore, discover"),
        "globe": ([("s", circ(12, 12, 9.25)), ("cut", "M2.75 12H21.25"),
                   ("cut", "M12 2.75C9.5 5.25 8.25 8.5 8.25 12C8.25 15.5 9.5 18.75 12 21.25M12 2.75C14.5 5.25 15.75 8.5 15.75 12C15.75 15.5 14.5 18.75 12 21.25")],
                  "globe, world, language, international"),
        "locate": ([("s", circ(12, 12, 6.25)), ("o", "M12 2.75V5.75M12 18.25V21.25M2.75 12H5.75M18.25 12H21.25"), ("d", circ(12, 12, 1.5))],
                   "locate, gps, current location"),
        "route": ([("o", "M5.5 15.75V9.25A3.25 3.25 0 0 1 12 9.25V14.75A3.25 3.25 0 0 0 18.5 14.75V8.25"),
                   ("s", circ(5.5, 18, 2.25)), ("s", circ(18.5, 6, 2.25))], "route, path, tracking, delivery"),
        "signpost": ([("o", "M12 2.75V5.25M12 10.25V11.75M12 16.75V21.25"), ("s", "M4.75 5.25H17.75L20.25 7.75L17.75 10.25H4.75Z"),
                      ("s", "M19.25 11.75H6.25L3.75 14.25L6.25 16.75H19.25Z")], "signpost, directions, way"),
        "building": ([("s", "M4.75 2.75H15.25V21.25H4.75Z"), ("s", "M15.25 8.75H19.25V21.25H15.25Z"),
                      ("cut", "M15.25 8.75V21.25M7.75 6.75H9.25M10.75 6.75H12.25M7.75 10.25H9.25M10.75 10.25H12.25M7.75 13.75H9.25M10.75 13.75H12.25M8.5 21.25V17.25H11.5V21.25")],
                     "building, office, company, mall"),
    },
    "👤 People": {
        "user": ([("s", U_HEAD), ("s", U_BODY)], "user, profile, account, person"),
        "user-plus": ([("s", US_HEAD), ("s", US_BODY), ("o", "M19 8.5V14.5M16 11.5H22")], "add user, invite"),
        "user-minus": ([("s", US_HEAD), ("s", US_BODY), ("o", "M16 11.5H22")], "remove user"),
        "user-check": ([("s", US_HEAD), ("s", US_BODY), ("o", "M16 11.5L18 13.5L21.75 9.75")], "verified user, follow"),
        "users": ([("s", circ(9, 8, 3.75)), ("s", "M2.75 21.25C2.75 17 5.5 14.25 9 14.25C12.5 14.25 15.25 17 15.25 21.25Z"),
                   ("o", "M15 4.5A3.75 3.75 0 0 1 15 11.5M17.25 14.5C19.75 15.25 21.25 17.75 21.25 21.25")], "users, group, team, friends"),
        "user-circle": ([("s", circ(12, 12, 9.25)), ("cut", circ(12, 9.75, 3)),
                         ("cut", "M6.25 18.75C7.5 16.5 9.5 15.25 12 15.25C14.5 15.25 16.5 16.5 17.75 18.75")], "profile, avatar, account"),
        "id-card": ([("s", "M2.75 4.75H21.25V19.25H2.75Z"), ("cut", circ(8.25, 10.25, 2)),
                     ("cut", "M5.25 16C5.75 14.5 6.75 13.75 8.25 13.75C9.75 13.75 10.75 14.5 11.25 16M13.75 9.75H18.25M13.75 13.25H18.25")],
                    "id, contact, membership, card"),
    },
    "🔑 Accounts & access": {
        "key": ([("s", circ(7.5, 16.5, 4.75)), ("o", "M10.86 13.14L20.25 3.75M17 7L19.5 9.5M14.25 9.75L16.25 11.75"), ("d", circ(7.5, 16.5, 1.25))],
                "key, password, access"),
        "eye": ([("s", EYE), ("cut", circ(12, 12, 2.75))], "show, view, visible, preview"),
        "eye-off": ([("s", EYE), ("cut", circ(12, 12, 2.75)), ("o", "M3.75 3.75L20.25 20.25"), ("k", "M4.81 2.69L21.31 19.19")],
                    "hide, hidden, invisible"),
        "password": ([("s", "M2.75 6.75H21.25V17.25H2.75Z"), ("d", circ(7, 12, 1.25)), ("d", circ(12, 12, 1.25)), ("d", circ(17, 12, 1.25))],
                     "password, pin, code"),
        "scan-face": ([("o", "M2.75 7.75V2.75H7.75M16.25 2.75H21.25V7.75M21.25 16.25V21.25H16.25M7.75 21.25H2.75V16.25"),
                       ("o", "M9 9.25V10.75M15 9.25V10.75M8.75 14.75C10.5 16.5 13.5 16.5 15.25 14.75")], "face id, scan, biometric"),
        "qr-code": ([("s", "M3.75 3.75H9.75V9.75H3.75Z"), ("s", "M14.25 3.75H20.25V9.75H14.25Z"), ("s", "M3.75 14.25H9.75V20.25H3.75Z"),
                     ("f", "M13.5 13.5H16.5V16.5H13.5Z"), ("f", "M17.5 17.5H20.5V20.5H17.5Z"), ("f", "M17.5 13.5H20.5V15.5H17.5Z"), ("f", "M13.5 17.5H15.5V20.5H13.5Z")],
                    "qr, scan, code"),
        "settings": ([("s", gear(12, 12, 9.25, 7, 8)), ("cut", circ(12, 12, 2.75))], "settings, gear, preferences"),
    },
    "🔔 Notifications": {
        "bell": ([("s", BELL)] + BELL_EXTRA, "notification, alert, bell"),
        "bell-dot": ([("s", BELL)] + BELL_EXTRA + [("f", circ(19.5, 4.25, 2))], "new notification, unread"),
        "bell-ring": ([("s", BELL)] + BELL_EXTRA + [("o", "M2.75 8.25C3.25 6 4.25 4.25 5.75 3M21.25 8.25C20.75 6 19.75 4.25 18.25 3")],
                      "ringing, alarm, notification"),
        "bell-off": ([("s", BELL)] + BELL_EXTRA + [("o", "M3.25 3.25L20.75 20.75"), ("k", "M4.31 2.19L21.81 19.69")], "mute, notifications off"),
        "bell-plus": ([("s", BELL)] + BELL_EXTRA + [("cut", "M12 8V13.5M9.25 10.75H14.75")], "subscribe, add alert"),
        "inbox": ([("s", "M2.75 13.25L5.75 4.75H18.25L21.25 13.25V19.25H2.75Z"), ("cut", "M2.75 13.25H8.25L9.75 15.75H14.25L15.75 13.25H21.25")],
                  "inbox, messages, tray"),
        "megaphone": ([("s", "M3.75 9.25H8.75L19.25 3.75V20.25L8.75 14.75H3.75Z"), ("o", "M6.25 14.75L7.75 20.25M21.25 10.25V13.75"), ("cut", "M8.75 9.25V14.75")],
                      "announcement, promo, news, campaign"),
    },
})


# ---------------------------------------------------------------- batch 3
def aperture(cx=12, cy=12, R=9.25, ri=4.25):
    """Six blade lines: each starts at an inner hexagon vertex and runs along
    the hexagon edge direction until it meets the outer circle."""
    out = []
    for i in range(6):
        a, b = math.radians(60 * i - 90), math.radians(60 * (i + 1) - 90)
        vx, vy = cx + ri * math.cos(a), cy + ri * math.sin(a)
        dx, dy = math.cos(b) - math.cos(a), math.sin(b) - math.sin(a)
        L = math.hypot(dx, dy); dx, dy = dx / L, dy / L
        px, py = vx - cx, vy - cy
        bq = px * dx + py * dy
        t = -bq + math.sqrt(bq * bq - (px * px + py * py - R * R))
        out.append(f"M{n(vx)} {n(vy)}L{n(vx + t * dx)} {n(vy + t * dy)}")
    return "".join(out)


def octagon(cx, cy, flat):
    R = flat / math.cos(math.radians(22.5))
    return poly([(cx + R * math.cos(math.radians(22.5 + 45 * i)), cy + R * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)])


def mirror(d):
    """Mirror an absolute M/L/H/V/Z path horizontally around x=12."""
    out, cmd = [], None
    for tok in re.findall(r"[MLHVZ]|-?[\d.]+", d):
        if tok in "MLHVZ":
            cmd = tok; out.append(tok); idx = 0; continue
        v = float(tok)
        if cmd in "ML":
            out.append(n(24 - v) if idx % 2 == 0 else n(v)); idx += 1
        elif cmd == "H":
            out.append(n(24 - v))
        else:
            out.append(n(v))
        out.append(" ")
    return re.sub(r" (?=[MLHVZ])", "", "".join(out)).strip()


import re

BUBBLE = "M7.63 19.58A8.75 8.75 0 1 0 4.42 16.38L2.75 21.25Z"
PHONE = "M3.75 3.75H8.5L10.25 8.25L8.25 10C9.5 12.25 11.75 14.5 14 15.75L15.75 13.75L20.25 15.5V20.25C11 20.25 3.75 13 3.75 3.75Z"
HP_ARC = "M3.75 15V12a8.25 8.25 0 0 1 16.5 0V15"
ENVELOPE = "M2.75 4.75H21.25V19.25H2.75Z"
CAL = [("s", "M2.75 4.75H21.25V21.25H2.75Z"), ("cut", "M2.75 9.75H21.25"), ("o", "M7.75 2.75V6.75M16.25 2.75V6.75")]
SHIELD = "M12 2.75L20.25 5.75V11.75C20.25 16.25 16.75 19.5 12 21.25C7.25 19.5 3.75 16.25 3.75 11.75V5.75Z"
SPEAKER = "M2.75 8.75H6.75L12.25 4.25V19.75L6.75 15.25H2.75Z"
MIC = [("s", "M9 6.5a3 3 0 0 1 6 0V11.25a3 3 0 0 1 -6 0Z"),
       ("o", "M5.5 11.25a6.5 6.5 0 0 0 13 0M12 17.75V21.25M8.75 21.25H15.25")]
SLASH = [("o", "M3.25 3.25L20.75 20.75"), ("k", "M4.31 2.19L21.81 19.69")]
FF = ["M3.25 6.25L10.25 12L3.25 17.75Z", "M12.75 6.25L19.75 12L12.75 17.75Z"]

CATEGORIES.update({
    "💬 Communication": {
        "message-circle": ([("s", BUBBLE)], "chat, message, comment, support"),
        "message-dots": ([("s", BUBBLE), ("d", circ(8, 12, 1)), ("d", circ(12, 12, 1)), ("d", circ(16, 12, 1))],
                         "typing, chat, message, live chat"),
        "message-plus": ([("s", BUBBLE), ("cut", "M12 8.25V15.75M8.25 12H15.75")], "new message, start chat"),
        "phone": ([("s", PHONE)], "phone, call, contact"),
        "phone-call": ([("s", PHONE), ("o", "M14.25 3.5A6.25 6.25 0 0 1 20.5 9.75M14.25 7A2.75 2.75 0 0 1 17 9.75")],
                       "calling, call, support"),
        "phone-off": ([("s", PHONE), ("o", "M20.75 3.25L3.25 20.75"), ("k", "M21.81 4.31L4.31 21.81")], "hang up, call off"),
        "headset": ([("o", HP_ARC), ("s", "M3.75 12.75H7.75V18.25H3.75Z"), ("s", "M16.25 12.75H20.25V18.25H16.25Z"),
                     ("o", "M18.25 18.25V21.25H12.25")], "support, customer service, help"),
    },
    "✉️ Mail": {
        "mail": ([("s", ENVELOPE), ("cut", "M2.75 4.75L12 12.5L21.25 4.75")], "mail, email, envelope, newsletter"),
        "mail-open": ([("s", "M2.75 9.25L12 3.25L21.25 9.25V20.25H2.75Z"), ("cut", "M2.75 9.25L12 15L21.25 9.25")],
                      "read, opened, email"),
        "mail-unread": ([("s", "M14.25 4.75H2.75V19.25H21.25V9.75"), ("cut", "M2.75 4.75L12 12.25L15.5 9.41"),
                         ("f", circ(19.5, 4.5, 2.5))], "unread, new email"),
        "at-sign": ([("o", circ(12, 12, 3.5)),
                     ("o", "M15.5 8.75V13.25A2.875 2.875 0 0 0 21.25 13.25V12A9.25 9.25 0 1 0 16.63 20.01")],
                    "email, mention, at"),
        "mailbox": ([("s", "M7 4.25H21.25V15.75H2.75V8.5A4.25 4.25 0 0 1 7 4.25Z"),
                     ("cut", "M11.25 15.75V8.5A4.25 4.25 0 0 0 7 4.25M14.75 11.25V7.75H17.75"), ("o", "M16 15.75V21.25")],
                    "mailbox, post, letters"),
    },
    "🕒 Time & calendar": {
        "clock": ([("s", circ(12, 12, 9.25)), ("cut", "M12 6.75V12L15.5 14")], "time, clock, hours"),
        "alarm-clock": ([("s", circ(12, 13, 7.75)), ("cut", "M12 9.25V13L14.5 14.5"),
                         ("o", "M2.75 6.25L6.25 3.25M21.25 6.25L17.75 3.25M6.52 18.48L4.75 21.25M17.48 18.48L19.25 21.25")],
                        "alarm, reminder, wake"),
        "timer": ([("s", circ(12, 13.25, 8)), ("cut", "M12 9.25V13.25"), ("o", "M9.25 2.75H14.75M12 2.75V5.25M19.5 6L21 4.5")],
                  "timer, stopwatch, countdown, flash sale"),
        "history": ([("o", "M3.25 12A8.75 8.75 0 1 0 6.1 5.5L3.25 8.25"), ("o", "M3.25 3.25V8.25H8.25"), ("o", "M12 7.75V12L15 13.75")],
                    "history, recent, past orders"),
        "calendar": (CAL, "calendar, date, schedule"),
        "calendar-check": (CAL + [("cut", "M9 15.25L11 17.25L15 13.25")], "booked, confirmed date"),
        "calendar-plus": (CAL + [("cut", "M12 12.5V18.5M9 15.5H15")], "add event, book"),
        "calendar-x": (CAL + [("cut", "M9.75 13.25L14.25 17.75M14.25 13.25L9.75 17.75")], "cancel, unavailable date"),
        "calendar-days": (CAL + [("d", circ(x, y, 1)) for y in (13.75, 17.5) for x in (7.5, 12, 16.5)][:5],
                          "calendar, days, month, events"),
    },
    "🛡️ Security": {
        "shield": ([("s", SHIELD)], "shield, protection, security"),
        "shield-check": ([("s", SHIELD), ("cut", "M8.75 12L11 14.25L15.25 10")], "secure, protected, verified"),
        "shield-alert": ([("s", SHIELD), ("cut", "M12 7.75V12.25"), ("d", circ(12, 15.5, 1))], "warning, risk, alert"),
        "shield-off": ([("s", SHIELD)] + SLASH, "unprotected, insecure"),
        "shield-lock": ([("s", SHIELD), ("cut", circ(12, 10.25, 2)), ("cut", "M12 12.25V15.75")], "secure checkout, privacy"),
        "badge-check": ([("s", star(12, 12, 9, 7.25, 8, -90 + 11.25)), ("cut", "M8.75 12L11 14.25L15.25 10")],
                        "verified, authentic, approved"),
        "octagon-alert": ([("s", octagon(12, 12, 9.25)), ("cut", "M12 7.25V12.75"), ("d", circ(12, 16, 1))], "error, stop, danger"),
        "vault": ([("s", "M2.75 3.25H21.25V19.25H2.75Z"), ("cut", circ(11, 11.25, 3.75)), ("cut", "M18 8.75V13.75"),
                   ("o", "M6.25 19.25V21.25M17.75 19.25V21.25")], "vault, safe, savings"),
    },
    "🎬 Multimedia": {
        "skip-forward": ([("s", "M4.75 4.75L15.25 12L4.75 19.25Z"), ("o", "M19.25 4.75V19.25")], "next, skip"),
        "skip-back": ([("s", "M19.25 4.75L8.75 12L19.25 19.25Z"), ("o", "M4.75 4.75V19.25")], "previous, back"),
        "fast-forward": ([("s", FF[0]), ("s", FF[1])], "fast forward, forward"),
        "rewind": ([("s", mirror(FF[0])), ("s", mirror(FF[1]))], "rewind, backward"),
        "volume-low": ([("s", SPEAKER), ("o", arc(12.25, 12, 4.25, -45, 45))], "volume, sound, audio"),
        "volume-high": ([("s", SPEAKER), ("o", arc(12.25, 12, 4.25, -45, 45)), ("o", arc(12.25, 12, 8.25, -45, 45))],
                        "volume, loud, sound"),
        "volume-x": ([("s", SPEAKER), ("o", "M15.75 9.25L21.25 14.75M21.25 9.25L15.75 14.75")], "mute, silent, no sound"),
        "music": ([("s", circ(6.25, 18.25, 3)), ("s", circ(18.25, 16.25, 3)), ("o", "M9.25 18.25V5.75L21.25 3.75V16.25")],
                  "music, audio, song"),
        "headphones": ([("o", "M3.75 17.25V12a8.25 8.25 0 0 1 16.5 0V17.25"), ("s", "M3.75 13.75H7.75V20.25H3.75Z"),
                        ("s", "M16.25 13.75H20.25V20.25H16.25Z")], "headphones, audio, listen"),
        "mic": (MIC, "microphone, voice, record"),
        "mic-off": (MIC + SLASH, "mute, microphone off"),
        "video": ([("s", "M2.75 5.75H15.25V18.25H2.75Z"), ("s", "M15.25 10L21.25 6.25V17.75L15.25 14Z")], "video, camera, live"),
        "film": ([("s", "M3.75 2.75H20.25V21.25H3.75Z"),
                  ("cut", "M7.75 2.75V21.25M16.25 2.75V21.25M3.75 7.25H7.75M3.75 12H7.75M3.75 16.75H7.75M16.25 7.25H20.25M16.25 12H20.25M16.25 16.75H20.25")],
                 "film, movie, video"),
        "tv": ([("s", "M2.75 7.25H21.25V19.25H2.75Z"), ("o", "M7.75 2.75L12 7.25L16.25 2.75")], "tv, screen, watch"),
        "repeat": ([("o", "M3.75 11.25V7.25H19.25M16.25 4.25L19.25 7.25L16.25 10.25M20.25 12.75V16.75H4.75M7.75 13.75L4.75 16.75L7.75 19.75")],
                   "repeat, loop"),
        "playlist": ([("o", "M2.75 5.75H16.25M2.75 10.25H16.25M2.75 14.75H10.25"), ("s", "M14.25 13.25L20.25 16.75L14.25 20.25Z")],
                     "playlist, queue"),
    },
    "📷 Photography": {
        "camera": ([("s", "M2.75 6.75H7.25L9 3.75H15L16.75 6.75H21.25V19.25H2.75Z"), ("cut", circ(12, 12.75, 3.5))],
                   "camera, photo, upload"),
        "image": ([("s", "M2.75 3.75H21.25V20.25H2.75Z"), ("cut", circ(15.75, 8, 1.75)),
                   ("cut", "M2.75 16.75L8.25 11.25L17.25 20.25M13.25 16.25L16.25 13.25L21.25 18.25")], "image, photo, picture"),
        "images": ([("o", "M6.25 2.75H21.25V17.75"), ("s", "M2.75 6.25H17.75V21.25H2.75Z"), ("cut", "M2.75 17.25L7.25 12.75L15.75 21.25")],
                   "gallery, photos, lookbook"),
        "aperture": ([("s", circ(12, 12, 9.25)), ("cut", aperture())], "aperture, lens, photography"),
        "focus": ([("o", "M2.75 7.75V2.75H7.75M16.25 2.75H21.25V7.75M21.25 16.25V21.25H16.25M7.75 21.25H2.75V16.25"), ("s", circ(12, 12, 3.75))],
                  "focus, scan, visual search"),
        "flash": ([("s", poly([(13.25, 2.75), (4.75, 13.75), (11.25, 13.75), (10.75, 21.25), (19.25, 10.25), (12.75, 10.25)]))],
                  "flash, lightning, fast, zap"),
        "crop": ([("o", "M6.25 2.75V17.75H21.25M2.75 6.25H17.75V21.25")], "crop, edit, resize"),
    },
    "🌐 Social": {
        "hash": ([("o", "M4.75 9.25H20.25M3.75 14.75H19.25M10.25 3.75L8.25 20.25M15.75 3.75L13.75 20.25")], "hashtag, tag, topic"),
        "link": ([("o", "M9.75 8.25H6.5a3.75 3.75 0 0 0 0 7.5H9.75M14.25 8.25H17.5a3.75 3.75 0 0 1 0 7.5H14.25M8.5 12H15.5")],
                 "link, url, share link"),
        "rss": ([("o", "M4.75 11.25A8 8 0 0 1 12.75 19.25M4.75 4.75A14.5 14.5 0 0 1 19.25 19.25"), ("f", circ(5.5, 18.5, 1.75))],
                "feed, rss, blog"),
        "flame": ([("s", "M12 21.25C8 21.25 5.25 18.5 5.25 14.75C5.25 10.5 9 8.75 9.5 3.25C13 5.25 14.25 8.25 14 10.75C15.25 10 16 8.75 16.25 7.5C17.75 9 18.75 11.75 18.75 14.75C18.75 18.5 16 21.25 12 21.25Z")],
                  "trending, hot, popular"),
        "trending-up": ([("o", "M2.75 17.25L9.25 10.75L13.25 14.75L21.25 6.75M15.25 6.75H21.25V12.75")], "trending, growth, popular"),
        "broadcast": ([("f", circ(12, 12, 2)), ("o", arc(12, 12, 5.5, -45, 45)), ("o", arc(12, 12, 5.5, 135, 225)),
                       ("o", arc(12, 12, 9.25, -45, 45)), ("o", arc(12, 12, 9.25, 135, 225))], "live, broadcast, stream"),
        "crown": ([("s", poly([(3.25, 7.25), (7.75, 12), (12, 4.75), (16.25, 12), (20.75, 7.25), (19.25, 19.25), (4.75, 19.25)])),
                   ("cut", "M4.31 15.75H19.69")], "vip, premium, influencer, crown"),
    },
})


# ---------------------------------------------------------------- batch 4
FILE = "M5.25 2.75H14.25L18.75 7.25V21.25H5.25Z"
FOLD = ("cut", "M14.25 2.75V7.25H18.75")
FOLDER = "M2.75 4.25H9.75L11.75 6.75H21.25V19.75H2.75Z"
CLOUD = "M7.5 19.25A4.25 4.25 0 0 1 6.9 10.8A5.5 5.5 0 1 1 17.1 10.8A4.25 4.25 0 0 1 16.5 19.25Z"
AXES = ("o", "M2.75 2.75V21.25H21.25")

CATEGORIES.update({
    "📱 Devices": {
        "smartphone": ([("s", "M6.75 2.75H17.25V21.25H6.75Z"), ("cut", "M10.75 18H13.25")], "phone, mobile, app"),
        "tablet": ([("s", "M4.25 2.75H19.75V21.25H4.25Z"), ("cut", "M10.75 18H13.25")], "tablet, ipad"),
        "laptop": ([("s", "M4.75 5.25H19.25V16.25H4.75Z"), ("s", "M2.75 16.25H21.25V19.25H2.75Z"), ("cut", "M4.75 16.25H19.25")],
                   "laptop, computer, notebook"),
        "monitor": ([("s", "M2.75 3.75H21.25V16.75H2.75Z"), ("o", "M12 16.75V20.25M7.75 20.25H16.25")], "monitor, desktop, screen"),
        "smartwatch": ([("s", "M6.75 7.25H17.25V16.75H6.75Z"), ("s", "M9 7.25L9.5 2.75H14.5L15 7.25"), ("s", "M9 16.75L9.5 21.25H14.5L15 16.75"),
                        ("cut", "M6.75 7.25H17.25M6.75 16.75H17.25"), ("o", "M19.25 10.5V13.5")], "smartwatch, wearable"),
        "keyboard": ([("s", "M2.75 5.75H21.25V18.25H2.75Z"), ("cut", "M8.25 14.75H15.75")] + [("d", circ(x, 9.75, 1)) for x in (6.5, 10.17, 13.83, 17.5)],
                     "keyboard, typing"),
        "mouse": ([("s", "M12 2.75C15.5 2.75 18.25 5 18.25 9V15C18.25 19 15.5 21.25 12 21.25C8.5 21.25 5.75 19 5.75 15V9C5.75 5 8.5 2.75 12 2.75Z"),
                   ("cut", "M12 6.75V10.25")], "mouse, computer"),
        "printer": ([("s", "M6.75 17.25H2.75V8.75H21.25V17.25H17.25"), ("s", "M6.75 2.75H17.25V8.75H6.75Z"),
                     ("o", "M6.75 14.25H17.25V21.25H6.75Z"), ("k", "M5.25 12.75H18.75")], "printer, print, label"),
        "battery": ([("s", "M2.75 7.25H18.75V16.75H2.75Z"), ("o", "M21.25 10V14"), ("cut", "M6.25 10V14M10 10V14")], "battery, power, charge"),
        "wifi": ([("o", arc(12, 19, 4.5, -135, -45)), ("o", arc(12, 19, 9, -135, -45)), ("o", arc(12, 19, 13, -135, -45)), ("f", circ(12, 19, 1.75))],
                 "wifi, internet, connection"),
        "bluetooth": ([("o", "M6.25 7.25L17.25 16.75L12 21.25V2.75L17.25 7.25L6.25 16.75")], "bluetooth, wireless"),
    },
    "📄 File icons": {
        "file": ([("s", FILE), FOLD], "file, document, page"),
        "file-text": ([("s", FILE), FOLD, ("cut", "M8.75 11.75H15.25M8.75 14.75H15.25M8.75 17.75H12.75")], "document, text, terms"),
        "file-plus": ([("s", FILE), FOLD, ("cut", "M12 11.25V17.75M8.75 14.5H15.25")], "new file, add document"),
        "file-check": ([("s", FILE), FOLD, ("cut", "M8.75 14.5L11 16.75L15.25 12.5")], "approved document"),
        "file-download": ([("s", FILE), FOLD, ("cut", "M12 10.75V17.25M9.25 14.5L12 17.25L14.75 14.5")], "download, pdf, invoice"),
        "folder": ([("s", FOLDER)], "folder, directory, collection"),
        "folder-open": ([("s", "M2.75 19.75V4.25H9.75L11.75 6.75H19.25V10.25"), ("s", "M6.25 10.25H21.25L18.25 19.75H2.75Z"),
                         ("cut", "M2.75 19.75L6.25 10.25H19.25")], "open folder, browse"),
        "folder-plus": ([("s", FOLDER), ("cut", "M12 9.75V16.75M8.5 13.25H15.5")], "new folder, add collection"),
        "clipboard-list": ([("s", "M4.75 4.25H19.25V21.25H4.75Z"), ("s", "M8.75 2.75H15.25V6.25H8.75Z"),
                            ("cut", "M8.25 10.75H15.75M8.25 14H15.75M8.25 17.25H12.75")], "list, order, checklist"),
        "save": ([("s", "M2.75 2.75H17.25L21.25 6.75V21.25H2.75Z"), ("cut", "M7.25 21.25V13.75H16.75V21.25M7.25 2.75V7.75H14.75V2.75")], "save, disk"),
        "cloud": ([("s", CLOUD)], "cloud, storage, online"),
        "cloud-upload": ([("s", CLOUD), ("cut", "M12 16.25V10.75M9.5 13.25L12 10.75L14.5 13.25")], "upload, backup, sync"),
    },
    "💰 Finance": {
        "dollar-circle": ([("s", circ(12, 12, 9.25)), ("cut", "M15 8.75H10.5A1.75 1.75 0 0 0 10.5 12.25H13.5A1.75 1.75 0 0 1 13.5 15.75H9M12 6.25V17.75")],
                          "dollar, price, money"),
        "euro-circle": ([("s", circ(12, 12, 9.25)), ("cut", "M15.5 8.5A4.75 4.75 0 1 0 15.5 15.5M6.75 10.75H12.5M6.75 13.25H12.5")], "euro, price, money"),
        "landmark": ([("s", poly([(2.75, 9.25), (12, 3), (21.25, 9.25)])), ("o", "M6 9.25V17.25M10 9.25V17.25M14 9.25V17.25M18 9.25V17.25"),
                      ("o", "M4.25 17.25H19.75M2.75 20.75H21.25")], "bank, institution"),
        "calculator": ([("s", "M4.75 2.75H19.25V21.25H4.75Z"), ("cut", "M8.25 6.25H15.75V9.25H8.25Z")]
                       + [("d", circ(x, y, 1)) for y in (13, 17) for x in (8.5, 12, 15.5)], "calculator, math, total"),
        "trending-down": ([("o", "M2.75 6.75L9.25 13.25L13.25 9.25L21.25 17.25M15.25 17.25H21.25V11.25")], "decline, price drop"),
        "piggy-bank": ([("s", "M4.25 11.5C4.25 8 7.5 5.75 11.75 5.75H16L19 3.75V8.25C20 9 20.75 10.25 21.25 11.25V14.75H19.25C18.75 15.75 18 16.5 17.25 17.25V20.25H13.75V18.75H9.75V20.25H6.25V17C5 15.75 4.25 13.75 4.25 11.5Z"),
                        ("cut", "M9.25 9.25H13.75"), ("d", circ(16.5, 11, 1)), ("o", "M4.25 11.5L2.75 10.25")], "savings, piggy bank, rewards"),
    },
    "📊 Charts": {
        "bar-chart": ([("s", "M3.75 12.75H7.75V20.25H3.75Z"), ("s", "M10 7.75H14V20.25H10Z"), ("s", "M16.25 3.75H20.25V20.25H16.25Z")], "chart, bars, stats"),
        "bar-chart-horizontal": ([("s", "M3.75 3.75H11.25V7.75H3.75Z"), ("s", "M3.75 10H16.25V14H3.75Z"), ("s", "M3.75 16.25H20.25V20.25H3.75Z")], "chart, bars, ranking"),
        "line-chart": ([AXES, ("o", "M6.75 15.75L11 10.75L14.25 13.75L20.25 6.25")], "chart, line, trend"),
        "area-chart": ([AXES, ("s", "M6.25 17.75V13.25L10.75 8.75L14.25 11.75L19.25 6.25V17.75Z")], "chart, area, analytics"),
        "pie-chart": ([("s", "M11 4.75A8.25 8.25 0 1 0 19.25 13H11Z"), ("s", "M14 2.75A7.25 7.25 0 0 1 21.25 10H14Z")], "chart, pie, share"),
        "donut-chart": ([("s", circ(12, 12, 9.25)), ("cut", circ(12, 12, 3.5)), ("cut", "M12 2.75V8.5M15.03 13.75L20.01 16.63")], "chart, donut, breakdown"),
        "gauge": ([("o", arc(12, 14.5, 9.25, -200, 20)), ("o", "M12 14.5L16.25 9.75"), ("f", circ(12, 14.5, 1.75))], "gauge, speed, performance"),
        "activity": ([("o", "M2.75 12H7.25L10 4.75L14 19.25L16.75 12H21.25")], "activity, pulse, health"),
    },
    "🏠 Home": {
        "sofa": ([("s", "M5.25 5.25H18.75V11.25H5.25Z"), ("s", "M2.75 10.25H6.25V14.25H17.75V10.25H21.25V18.75H2.75Z"),
                  ("cut", "M6.25 14.25H17.75"), ("o", "M5.25 18.75V20.75M18.75 18.75V20.75")], "sofa, couch, living room"),
        "bed": ([("o", "M2.75 5.25V20.25M21.25 17.25V20.25"), ("s", "M2.75 11.75H21.25V17.25H2.75Z"), ("s", "M5.75 7.75H11.25V11.75H5.75Z")], "bed, bedroom, sleep"),
        "lamp": ([("s", "M8 3.25H16L18.75 11.75H5.25Z"), ("o", "M12 11.75V20.75M8.25 20.75H15.75")], "lamp, light, lighting"),
        "chair": ([("s", "M6.75 2.75H17.25V12.25H6.75Z"), ("s", "M5.25 12.25H18.75V15.25H5.25Z"), ("cut", "M6.75 12.25H17.25"), ("o", "M6.75 15.25V21.25M17.25 15.25V21.25")], "chair, seat, furniture"),
        "lightbulb": ([("s", "M9 17.25V15.5C6.75 14 5.75 12 5.75 9.5A6.25 6.25 0 0 1 18.25 9.5C18.25 12 17.25 14 15 15.5V17.25Z"), ("o", "M9.75 20.5H14.25")], "idea, light, tip"),
        "bath": ([("s", "M2.75 11.75H21.25V15.25C21.25 18 19.25 19.75 16.75 19.75H7.25C4.75 19.75 2.75 18 2.75 15.25Z"),
                  ("o", "M5.25 11.75V5.25A2.25 2.25 0 0 1 9.75 5.25M6.75 19.75V21.25M17.25 19.75V21.25")], "bath, bathroom, tub"),
        "washing-machine": ([("s", "M3.75 2.75H20.25V21.25H3.75Z"), ("cut", circ(12, 13.5, 4.5)), ("cut", "M3.75 6.75H20.25")], "washer, laundry, appliance"),
        "fridge": ([("s", "M5.75 2.75H18.25V21.25H5.75Z"), ("cut", "M5.75 9.25H18.25M8.75 5.25V7.25M8.75 11.75V15.25")], "fridge, kitchen, appliance"),
        "plant": ([("s", "M7.25 14.25H16.75L15.75 21.25H8.25Z"), ("o", "M12 14.25V8.25"), ("s", "M12 8.25C12 5 9.75 3 5.75 3C5.75 6.5 8 8.25 12 8.25Z"),
                   ("s", "M12 10.25C12 7.75 14.25 5.25 18.25 5.25C18.25 8.5 16 10.25 12 10.25Z")], "plant, decor, nature"),
    },
    "🍽️ Food & beverage": {
        "coffee": ([("s", "M4.25 8.25H17.25V14.75C17.25 18.25 15 20.25 12 20.25H9.5C6.5 20.25 4.25 18.25 4.25 14.75Z"),
                    ("o", "M17.25 10.25H18.5A2.75 2.75 0 0 1 18.5 15.75H17M8.25 3V5.75M13.25 3V5.75")], "coffee, cafe, drink"),
        "wine": ([("s", "M6.75 2.75H17.25V9.25A5.25 5.25 0 0 1 6.75 9.25Z"), ("o", "M12 14.5V21.25M8 21.25H16")], "wine, glass, drink"),
        "beer": ([("s", "M5.25 7.25H15.75V21.25H5.25Z"), ("s", "M5.25 3.25H15.75V7.25H5.25Z"), ("o", "M15.75 10.25H20.25V17.25H15.75"),
                  ("cut", "M5.25 7.25H15.75M8.75 11V17.5M12.25 11V17.5")], "beer, pint, drink"),
        "utensils": ([("o", "M8 2.75V21.25"), ("o", "M4.25 2.75V8.25C4.25 10.25 6 11.75 8 11.75C10 11.75 11.75 10.25 11.75 8.25V2.75"),
                      ("s", "M19.25 2.75C16.75 3.75 15.25 7.25 15.25 12.75H19.25Z"), ("o", "M19.25 12.75V21.25")], "restaurant, food, dining"),
        "pizza": ([("s", "M12 21.25L2.75 6.75C8 3.25 16 3.25 21.25 6.75Z"), ("cut", "M4.75 9.75C9 7.25 15 7.25 19.25 9.75"),
                   ("d", circ(10, 12, 1.25)), ("d", circ(14.25, 13, 1)), ("d", circ(12, 16.5, 1))], "pizza, food, slice"),
        "apple": ([("s", "M12 7.25C9.5 5.5 4.75 6 4.25 11.25C3.9 15.25 6.5 21.25 9 21.25C10.25 21.25 10.75 20.5 12 20.5C13.25 20.5 13.75 21.25 15 21.25C17.5 21.25 20.1 15.25 19.75 11.25C19.25 6 14.5 5.5 12 7.25Z"),
                   ("o", "M12 7.25C12 5 13.25 3.25 15.5 2.75")], "fruit, apple, healthy"),
        "ice-cream": ([("s", "M6.75 8.25A5.25 5.25 0 0 1 17.25 8.25Z"), ("s", "M6.75 8.25H17.25L12 20Z"), ("cut", "M6.75 8.25H17.25")], "ice cream, dessert, sweet"),
        "cake": ([("s", "M3.75 11.75H20.25V20.75H3.75Z"), ("cut", "M3.75 15.25C6 17 9.25 17 12 15.25C14.75 17 18 17 20.25 15.25"),
                  ("o", "M8.25 11.75V7.75M12 11.75V7.75M15.75 11.75V7.75"), ("f", circ(8.25, 5.5, 1)), ("f", circ(12, 5.5, 1)), ("f", circ(15.75, 5.5, 1))],
                 "cake, birthday, celebrate"),
        "cookie": ([("s", circ(12, 12, 9.25)), ("d", circ(9, 9, 1)), ("d", circ(15, 9.5, 1)), ("d", circ(8.5, 15, 1)), ("d", circ(14.5, 15.5, 1)), ("d", circ(12, 12, 0.75))],
                   "cookie, snack, consent"),
    },
    "🚗 Transportation": {
        "car": ([("s", "M2.75 11.75L5.25 5.25H18.75L21.25 11.75V18.25H2.75Z"), ("cut", "M2.75 11.75H21.25"), ("d", circ(6.5, 15, 1.25)), ("d", circ(17.5, 15, 1.25)),
                 ("o", "M5.25 18.25V20.75M18.75 18.25V20.75")], "car, vehicle, drive"),
        "bus": ([("s", "M4.25 2.75H19.75V18.75H4.25Z"), ("cut", "M4.25 11.25H19.75M12 2.75V11.25"), ("d", circ(8, 15, 1)), ("d", circ(16, 15, 1)),
                 ("o", "M7.25 18.75V21.25M16.75 18.75V21.25")], "bus, public transport"),
        "train": ([("s", "M5.25 2.75H18.75V17.25H5.25Z"), ("cut", "M5.25 10.25H18.75M12 2.75V10.25"), ("d", circ(8.75, 13.75, 1)), ("d", circ(15.25, 13.75, 1)),
                   ("o", "M8.75 17.25L6.25 21.25M15.25 17.25L17.75 21.25")], "train, rail, metro"),
        "plane": ([("s", "M12 2.75C13 2.75 13.5 4 13.5 5.5V9.5L21.25 14.25V16.5L13.5 14V18L15.75 19.75V21.25L12 20.25L8.25 21.25V19.75L10.5 18V14L2.75 16.5V14.25L10.5 9.5V5.5C10.5 4 11 2.75 12 2.75Z")],
                  "plane, flight, express shipping"),
        "ship": ([("s", "M2.75 13.75H21.25L18.75 20.75H5.25Z"), ("s", "M6.75 7.75H17.25V13.75H6.75Z"), ("cut", "M6.75 13.75H17.25"), ("o", "M12 2.75V7.75")], "ship, freight, sea"),
        "bicycle": ([("o", circ(6, 16.25, 3.25)), ("o", circ(18, 16.25, 3.25)),
                     ("o", "M6 16.25L9.25 8.75H15.25L18 16.25M9.25 8.75L12 16.25H6M7.75 6.25H10.75M9.25 6.25V8.75M13.25 5.75H16L15.25 8.75")], "bike, bicycle, cycling"),
        "fuel": ([("s", "M4.75 2.75H14.25V21.25H4.75Z"), ("cut", "M7.75 6.25H11.25V10.25H7.75Z"), ("o", "M2.75 21.25H16.25"),
                  ("o", "M14.25 13.25H16.25C17.25 13.25 17.75 13.75 17.75 14.75V17C17.75 18.1 20.25 18.1 20.25 17V8.25L17.25 5.25")], "fuel, gas, station"),
        "parking": ([("s", "M2.75 2.75H21.25V21.25H2.75Z"), ("cut", "M9.25 18V6.25H13.25A3.5 3.5 0 0 1 13.25 13.25H9.25")], "parking, p"),
        "traffic-light": ([("s", "M7.75 2.75H16.25V21.25H7.75Z"), ("d", circ(12, 6.75, 1.5)), ("d", circ(12, 12, 1.5)), ("d", circ(12, 17.25, 1.5))], "traffic, signal, light"),
    },
})


# ---------------------------------------------------------------- batch 5
def ring(cx, cy, r):
    """Circle as an open path: in Filled only its stroke is knocked out, the disc stays solid."""
    return circ(cx, cy, r).rstrip("Z")


def regular(cx, cy, R, k, rot=-90):
    return poly([(cx + R * math.cos(math.radians(rot + 360 * i / k)), cy + R * math.sin(math.radians(rot + 360 * i / k))) for i in range(k)])


def snowflake(cx=12, cy=12, R=9.25):
    out = []
    for a in range(0, 360, 60):
        t = math.radians(a - 90)
        p = lambda r, off: (cx + r * math.cos(t) - off * math.sin(t), cy + r * math.sin(t) + off * math.cos(t))
        x0, y0 = p(0, 0); x1, y1 = p(R, 0)
        out.append(f"M{n(x0)} {n(y0)}L{n(x1)} {n(y1)}")
        (ax, ay), (mx, my), (bx, by) = p(R - 2.75, 2.5 * 1.0), p(R - 5.25, 0), p(R - 2.75, -2.5)
        out.append(f"M{n(ax)} {n(ay)}L{n(mx)} {n(my)}L{n(bx)} {n(by)}")
    return "".join(out)


def recycle(cx=12, cy=13.5, R=10):
    v = [(cx + R * math.cos(math.radians(-90 + 120 * i)), cy + R * math.sin(math.radians(-90 + 120 * i))) for i in range(3)]
    out = []
    for i in range(3):
        (ax, ay), (bx, by) = v[i], v[(i + 1) % 3]
        L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L; wx, wy = -uy, ux
        px, py = ax + (bx - ax) * .16, ay + (by - ay) * .16
        qx, qy = ax + (bx - ax) * .8, ay + (by - ay) * .8
        h1 = (qx - ux * 3 + wx * 3, qy - uy * 3 + wy * 3); h2 = (qx - ux * 3 - wx * 3, qy - uy * 3 - wy * 3)
        out.append(f"M{n(px)} {n(py)}L{n(qx)} {n(qy)}M{n(h1[0])} {n(h1[1])}L{n(qx)} {n(qy)}L{n(h2[0])} {n(h2[1])}")
    return "".join(out)


CLOUD_S = "M6.5 15.25A3.5 3.5 0 0 1 6 8.3A6.25 6.25 0 0 1 18 8.3A3.5 3.5 0 0 1 17.5 15.25Z"
TUB = "M2.75 6.25L5 19.75H19L21.25 6.25C19.25 6.25 18.75 8.5 16.6 8.5C14.6 8.5 14 6.25 12 6.25C10 6.25 9.4 8.5 7.4 8.5C5.25 8.5 4.75 6.25 2.75 6.25Z"
ZERO = "M12.75 10.75H16.25V16.75H12.75V10.75"
BLEACH = "M12 3.25L21.25 19.75H2.75Z"
DRYER = "M2.75 2.75H21.25V21.25H2.75Z"
IRON = "M2.75 18.75C2.75 13.75 6 10.75 10.25 10.75H18.75L21.25 18.75Z"
IRON_H = "M10.75 6.75H17.75L18.75 10.75"
DONOT = ("cut", "M4 4L20 20M20 4L4 20")

CATEGORIES.update({
    "🌦️ Weather": {
        "sun": ([("s", circ(12, 12, 4.25)),
                 ("o", "M12 2.75V5.25M12 18.75V21.25M2.75 12H5.25M18.75 12H21.25M5.46 5.46L7.23 7.23M16.77 16.77L18.54 18.54M18.54 5.46L16.77 7.23M7.23 16.77L5.46 18.54")],
                "sun, day, light mode, summer"),
        "moon": ([("s", "M20.25 14.25A8.75 8.75 0 1 1 9.75 3.75A8 8 0 0 0 20.25 14.25Z")], "moon, night, dark mode"),
        "cloud-sun": ([("o", "M8.25 2.75V4.75M2.75 8.25H4.75M4.36 4.36L5.77 5.77M12.14 4.36L10.73 5.77"), ("o", arc(8.25, 8.25, 3.5, 150, 350)),
                       ("s", "M8.25 20.25A3 3 0 0 1 8 14.25A5 5 0 0 1 17.75 12.9A3.7 3.7 0 0 1 17.5 20.25Z")], "partly cloudy, weather"),
        "cloud-rain": ([("s", CLOUD_S), ("o", "M8 17.75L7 21.25M12.5 17.75L11.5 21.25M17 17.75L16 21.25")], "rain, weather, rainwear"),
        "cloud-snow": ([("s", CLOUD_S), ("f", circ(8, 19.25, 1)), ("f", circ(12, 20.25, 1)), ("f", circ(16, 19.25, 1))], "snow, winter, weather"),
        "cloud-lightning": ([("s", CLOUD_S), ("o", "M12.75 16.75L10.5 19H13.5L11.25 21.25")], "storm, thunder, weather"),
        "wind": ([("o", "M2.75 8.75H14.25A3 3 0 1 0 11.25 5.75M2.75 12.75H18A3.25 3.25 0 1 1 14.75 16M2.75 16.75H10.25")], "wind, breeze, weather"),
        "snowflake": ([("o", snowflake())], "snowflake, winter, cold"),
        "umbrella": ([("s", "M2.75 13.25A9.25 9.25 0 0 1 21.25 13.25Z"), ("o", "M12 13.25V18.75A2.25 2.25 0 0 1 7.5 18.75")], "umbrella, rain, protection"),
        "thermometer": ([("s", "M9.25 12.75V5.5A2.75 2.75 0 0 1 14.75 5.5V12.75A4.5 4.5 0 1 1 9.25 12.75Z"), ("cut", "M12 8.5V14.25"), ("d", circ(12, 16.5, 1.75))],
                        "temperature, heat, weather"),
        "sunrise": ([("o", "M2.75 19.25H21.25M12 3.25V6.5M4.5 8.75L6.5 10.75M19.5 8.75L17.5 10.75M2.75 15.75H4.25M19.75 15.75H21.25"),
                     ("s", "M6.75 15.75A5.25 5.25 0 0 1 17.25 15.75Z")], "sunrise, morning, dawn"),
    },
    "🧺 Laundry care": {
        "wash-30": ([("s", TUB), ("cut", "M6.75 10.75H10.25V16.75H6.75M7.75 13.75H10.25"), ("cut", ZERO)], "wash, 30 degrees, cold, care label"),
        "wash-40": ([("s", TUB), ("cut", "M7 10.75V14H10.25M10.25 10.75V16.75"), ("cut", ZERO)], "wash, 40 degrees, care label"),
        "wash-60": ([("s", TUB), ("cut", "M10.25 10.75H7V16.75H10.25V14H7"), ("cut", ZERO)], "wash, 60 degrees, care label"),
        "hand-wash": ([("s", TUB), ("cut", "M8.25 16.25V13.25M10.75 16.25V11.25M13.25 16.25V11.25M15.75 16.25V13.25")], "hand wash, delicate, care label"),
        "do-not-wash": ([("s", TUB), DONOT], "do not wash, dry clean only, care label"),
        "bleach": ([("s", BLEACH)], "bleach, care label"),
        "do-not-bleach": ([("s", BLEACH), ("cut", "M7.5 8L16.5 19.75M16.5 8L7.5 19.75")], "do not bleach, care label"),
        "tumble-dry": ([("s", DRYER), ("cut", ring(12, 12, 6.25))], "tumble dry, dryer, care label"),
        "tumble-dry-low": ([("s", DRYER), ("cut", ring(12, 12, 6.25)), ("d", circ(12, 12, 1.5))], "tumble dry low, delicate, care label"),
        "do-not-tumble-dry": ([("s", DRYER), ("cut", ring(12, 12, 6.25)), ("cut", "M2.75 2.75L21.25 21.25M21.25 2.75L2.75 21.25")], "do not tumble dry, care label"),
        "iron": ([("s", IRON), ("o", IRON_H)], "iron, ironing, care label"),
        "iron-low": ([("s", IRON), ("o", IRON_H), ("d", circ(12.5, 15, 1.25))], "iron low, cool iron, care label"),
        "iron-high": ([("s", IRON), ("o", IRON_H), ("d", circ(8.5, 15, 1.25)), ("d", circ(12.5, 15, 1.25)), ("d", circ(16.5, 15, 1.25))], "iron high, hot iron, care label"),
        "do-not-iron": ([("s", IRON), ("o", IRON_H), ("cut", "M7.5 10.75L15.75 18.75M15.75 10.75L7.5 18.75")], "do not iron, care label"),
        "dry-clean": ([("s", circ(12, 12, 9.25)), ("cut", "M9.25 17V7H13.25A3 3 0 0 1 13.25 13H9.25")], "dry clean, professional, care label"),
        "do-not-dry-clean": ([("s", circ(12, 12, 9.25)), ("cut", "M5.5 5.5L18.5 18.5M18.5 5.5L5.5 18.5")], "do not dry clean, care label"),
    },
    "🌱 Sustainability": {
        "leaf": ([("s", "M5.25 18.75C3 10.75 9.25 3.75 20.75 3.25C20.25 14.75 13.25 21 5.25 18.75Z"), ("o", "M2.75 21.25L5.25 18.75"), ("cut", "M5.25 18.75L13.75 10.25")],
                 "leaf, eco, natural, organic"),
        "sprout": ([("o", "M12 21.25V11.25M6.75 21.25H17.25"), ("s", "M12 11.25C12 7.25 9 4.75 3.75 4.75C3.75 9 6.75 11.25 12 11.25Z"),
                    ("s", "M12 14.25C12 11 14.75 8.25 20.25 8.25C20.25 12 17.5 14.25 12 14.25Z")], "sprout, grow, plant, eco"),
        "tree": ([("s", poly([(12, 2.75), (18.25, 10.25), (15.75, 10.25), (19.75, 16.25), (4.25, 16.25), (8.25, 10.25), (5.75, 10.25)])), ("o", "M12 16.25V21.25")],
                 "tree, nature, forest, carbon offset"),
        "recycle": ([("o", recycle())], "recycle, reuse, circular, second hand"),
        "solar-panel": ([("s", "M5.25 4.25H18.75L21.25 16.25H2.75Z"), ("cut", "M12 4.25V16.25M4 10.25H20M8.75 4.25L7.35 16.25M15.25 4.25L16.65 16.25"),
                         ("o", "M12 16.25V20.75M7.75 20.75H16.25")], "solar, energy, renewable"),
        "wind-turbine": ([("o", "M12 10.75V21.25M9.25 21.25H14.75M12 9V2.75M12 9L17.4 12.1M12 9L6.6 12.1"), ("f", circ(12, 9, 1.75))], "wind power, energy, renewable"),
        "plug": ([("s", "M6.75 8.25H17.25V12.5A5.25 5.25 0 0 1 6.75 12.5Z"), ("o", "M9 2.75V8.25M15 2.75V8.25M12 17.75V21.25")], "plug, electric, power"),
        "tote-bag": ([("s", "M4.75 8.25H19.25L20.25 21.25H3.75Z"), ("o", "M8.75 8.25V6a3.25 3.25 0 0 1 6.5 0V8.25")], "tote, reusable bag, eco"),
    },
    "🔧 Tools": {
        "wrench": ([("s", "M20.75 6.25L16.75 10.25L13.75 7.25L17.75 3.25C14 2 9.75 5 10.75 9.75L3.25 17.25L6.75 20.75L14.25 13.25C19 14.25 22 10 20.75 6.25Z")], "wrench, tool, repair, settings"),
        "hammer": ([("s", "M9.25 3.25H18.25L21.25 6.25V9.25H9.25Z"), ("s", "M11.75 9.25H15.75V21.25H11.75Z"), ("cut", "M11.75 9.25H15.75")], "hammer, tool, build"),
        "screwdriver": ([("s", "M9.25 2.75H14.75V11.25H9.25Z"), ("o", "M12 11.25V18"), ("s", "M10.75 17.75H13.25L12.75 21.25H11.25Z")], "screwdriver, tool, repair"),
        "scissors": ([("s", circ(6.25, 6.25, 3.5)), ("s", circ(6.25, 17.75, 3.5)), ("o", "M9.25 8L21.25 18.25M9.25 16L21.25 5.75")], "scissors, cut, tailoring"),
        "tape-measure": ([("s", circ(10, 11, 7.25)), ("cut", circ(10, 11, 2.5)), ("o", "M10 18.25H21.25V14.75")], "tape measure, size guide, tailoring"),
        "sewing-needle": ([("o", "M3.25 20.75L16.5 7.5M16.5 7.5L17.5 3.75L21 3L20.25 6.5Z"), ("o", "M16 8C10 4 5 5 4.5 9C4 13 10 14 12 17")], "needle, sewing, repair, tailoring"),
        "toolbox": ([("s", "M2.75 8.75H21.25V20.25H2.75Z"), ("o", "M8.25 8.75V4.75H15.75V8.75"), ("cut", "M2.75 13.25H10.25M13.75 13.25H21.25"), ("cut", "M10.25 11.75H13.75V14.75H10.25Z")],
                    "toolbox, kit, repair"),
        "flashlight": ([("s", "M8.25 2.75H15.75V7.25L14.25 10V21.25H9.75V10L8.25 7.25Z"), ("cut", "M8.25 7.25H15.75M12 13.25V15.75")], "flashlight, torch, light"),
        "ladder": ([("o", "M7.75 2.75V21.25M16.25 2.75V21.25M7.75 7.25H16.25M7.75 12H16.25M7.75 16.75H16.25")], "ladder, climb, steps"),
    },
    "🎨 Design": {
        "pen-tool": ([("s", "M12 2.75L17.75 14.25L14.75 19.75H9.25L6.25 14.25Z"), ("cut", "M12 2.75V11.25"), ("cut", circ(12, 13, 1.75)), ("o", "M8.25 21.25H15.75")], "pen tool, vector, design"),
        "brush": ([("s", "M2.75 21.25C3.5 17.5 5 15 8 15C10 15 11.25 16.25 11.25 18C11.25 20.25 8 21.25 2.75 21.25Z"), ("s", "M8.5 13.75L18.75 3.25H21.25L21 5.5L10.75 16Z")], "brush, paint, draw"),
        "palette": ([("s", "M12 2.75C6.75 2.75 2.75 6.75 2.75 12C2.75 17.25 6.75 21.25 11.75 21.25C13.75 21.25 14 19.75 13.25 18.75C12.25 17.5 13 16 14.75 16H17C19.5 16 21.25 14.25 21.25 11.5C21.25 6.5 17 2.75 12 2.75Z"),
                     ("d", circ(8, 10, 1.25)), ("d", circ(12, 7, 1.25)), ("d", circ(16.25, 9.75, 1.25)), ("d", circ(7.75, 14.75, 1.25))], "palette, colour, theme"),
        "pipette": ([("s", "M13.25 7L17 10.75L8 19.75H4.25V16Z"), ("s", "M15 5.25L17.25 3C18.25 2 19.75 2.25 20.75 3.25C21.75 4.25 22 5.75 21 6.75L18.75 9Z")], "pipette, eyedropper, colour picker"),
        "layers": ([("s", "M12 2.75L21.25 7.75L12 12.75L2.75 7.75Z"), ("o", "M2.75 12L12 17L21.25 12M2.75 16.25L12 21.25L21.25 16.25")], "layers, stack"),
        "grid": ([("s", "M3.75 3.75H10.25V10.25H3.75Z"), ("s", "M13.75 3.75H20.25V10.25H13.75Z"), ("s", "M3.75 13.75H10.25V20.25H3.75Z"), ("s", "M13.75 13.75H20.25V20.25H13.75Z")], "grid, gallery, view"),
        "layout": ([("s", "M2.75 2.75H21.25V21.25H2.75Z"), ("cut", "M2.75 8.75H21.25M9.25 8.75V21.25")], "layout, dashboard, template"),
        "type": ([("o", "M4.75 7.25V3.75H19.25V7.25M12 3.75V20.25M8.75 20.25H15.25")], "type, text, font"),
        "component": ([("s", poly([(12, 3), (15, 6), (12, 9), (9, 6)])), ("s", poly([(18, 9), (21, 12), (18, 15), (15, 12)])),
                       ("s", poly([(12, 15), (15, 18), (12, 21), (9, 18)])), ("s", poly([(6, 9), (9, 12), (6, 15), (3, 12)]))], "component, design system"),
        "frame": ([("o", "M2.75 7.75H21.25M2.75 16.25H21.25M7.75 2.75V21.25M16.25 2.75V21.25")], "frame, artboard, crop marks"),
        "sparkles": ([("s", star(10.75, 13, 8.25, 2.5, 4)), ("f", star(18.75, 5.25, 3.25, 1, 4))], "sparkles, ai, magic, new"),
        "wand": ([("o", "M3.25 20.75L14.25 9.75"), ("f", star(17.5, 6.5, 3.75, 1.25, 4)), ("f", star(19.75, 13.5, 1.75, .6, 4)), ("f", star(10, 4.5, 1.75, .6, 4))], "wand, magic, auto"),
    },
    "🔷 Shapes": {
        "rectangle": ([("s", "M2.75 5.75H21.25V18.25H2.75Z")], "rectangle, shape"),
        "pill": ([("s", "M8 6.75H16A5.25 5.25 0 0 1 16 17.25H8A5.25 5.25 0 0 1 8 6.75Z")], "pill, capsule, shape"),
        "oval": ([("s", "M12 5.25C17.1 5.25 21.25 8.25 21.25 12C21.25 15.75 17.1 18.75 12 18.75C6.9 18.75 2.75 15.75 2.75 12C2.75 8.25 6.9 5.25 12 5.25Z")], "oval, ellipse, shape"),
        "rhombus": ([("s", poly([(12, 3.5), (20.5, 12), (12, 20.5), (3.5, 12)]))], "rhombus, shape"),
        "pentagon": ([("s", regular(12, 12.75, 9.75, 5))], "pentagon, shape"),
        "hexagon": ([("s", regular(12, 12, 9.75, 6))], "hexagon, shape"),
        "octagon": ([("s", octagon(12, 12, 9.25))], "octagon, shape"),
        "parallelogram": ([("s", poly([(7.25, 5.75), (21.25, 5.75), (16.75, 18.25), (2.75, 18.25)]))], "parallelogram, shape"),
        "trapezoid": ([("s", poly([(7.25, 5.75), (16.75, 5.75), (21.25, 18.25), (2.75, 18.25)]))], "trapezoid, shape"),
        "semicircle": ([("s", "M2.75 17.25A9.25 9.25 0 0 1 21.25 17.25Z")], "semicircle, half circle, shape"),
        "cross": ([("s", "M9 2.75H15V9H21.25V15H15V21.25H9V15H2.75V9H9Z")], "cross, plus, shape"),
        "cube": ([("s", "M12 2.75L20.25 7.25V16.75L12 21.25L3.75 16.75V7.25Z"), ("cut", "M3.75 7.25L12 11.75L20.25 7.25M12 11.75V21.25")], "cube, 3d, shape"),
        "cylinder": ([("s", "M4.75 6.25C4.75 4.25 8 2.75 12 2.75C16 2.75 19.25 4.25 19.25 6.25V17.75C19.25 19.75 16 21.25 12 21.25C8 21.25 4.75 19.75 4.75 17.75Z"),
                      ("cut", "M4.75 6.25C4.75 8.25 8 9.75 12 9.75C16 9.75 19.25 8.25 19.25 6.25")], "cylinder, 3d, database"),
        "sphere": ([("s", circ(12, 12, 9.25)), ("cut", "M2.75 12C5 14.5 19 14.5 21.25 12")], "sphere, 3d, ball"),
    },
})


# ---------------------------------------------------------------- batch 5 fixes
def no_x(cx, cy, L, d=1.5):
    """Prohibition X, 45 degrees: a line in both variants, with a white halo in Filled.
    The halo is four chevrons so it never cuts through the X itself."""
    a = d * math.sqrt(2)
    chev = [f"M{n(cx + a + L)} {n(cy - L)}L{n(cx + a)} {n(cy)}L{n(cx + a + L)} {n(cy + L)}",
            f"M{n(cx - a - L)} {n(cy - L)}L{n(cx - a)} {n(cy)}L{n(cx - a - L)} {n(cy + L)}",
            f"M{n(cx - L)} {n(cy + a + L)}L{n(cx)} {n(cy + a)}L{n(cx + L)} {n(cy + a + L)}",
            f"M{n(cx - L)} {n(cy - a - L)}L{n(cx)} {n(cy - a)}L{n(cx + L)} {n(cy - a - L)}"]
    x = f"M{n(cx - L)} {n(cy - L)}L{n(cx + L)} {n(cy + L)}M{n(cx + L)} {n(cy - L)}L{n(cx - L)} {n(cy + L)}"
    return [("o", x)] + [("k", c) for c in chev]


L_ = CATEGORIES["🧺 Laundry care"]
L_["do-not-wash"] = ([("s", TUB)] + no_x(12, 12.75, 8.5), L_["do-not-wash"][1])
L_["do-not-bleach"] = ([("s", BLEACH)] + no_x(12, 13, 7.5), L_["do-not-bleach"][1])
L_["do-not-tumble-dry"] = ([("s", DRYER), ("cut", ring(12, 12, 6.25))] + no_x(12, 12, 9.25), L_["do-not-tumble-dry"][1])
L_["do-not-iron"] = ([("s", IRON), ("o", IRON_H)] + no_x(11.75, 13.25, 6.75), L_["do-not-iron"][1])
L_["do-not-dry-clean"] = ([("s", circ(12, 12, 9.25))] + no_x(12, 12, 6.54), L_["do-not-dry-clean"][1])
L_["hand-wash"] = ([("s", TUB), ("cut", "M12 17.25L8 13.25M12 17.25L10.5 11.25M12 17.25L13.5 11.25M12 17.25L16 13.25")], L_["hand-wash"][1])
T_ = CATEGORIES["🔧 Tools"]
T_["sewing-needle"] = ([("o", "M3.25 20.75L16.5 7.5M16.5 7.5L17.5 3.75L21 3L20.25 6.5Z"), ("o", "M17.5 7.5C20.75 11.5 12 13 15.25 17C16.75 18.75 19 18.75 20.75 17.25")], T_["sewing-needle"][1])
D_ = CATEGORIES["🎨 Design"]
D_["pipette"] = (D_["pipette"][0] + [("o", "M12 5.25L18.75 12")], D_["pipette"][1])


def no_x2(cx, cy, L):
    return [("cut", f"M{n(cx - L)} {n(cy - L)}L{n(cx + L)} {n(cy + L)}M{n(cx + L)} {n(cy - L)}L{n(cx - L)} {n(cy + L)}")]


L_["do-not-wash"] = ([("s", TUB)] + no_x2(12, 12.75, 8.5), L_["do-not-wash"][1])
L_["do-not-bleach"] = ([("s", BLEACH)] + no_x2(12, 13, 7.5), L_["do-not-bleach"][1])
L_["do-not-tumble-dry"] = ([("s", DRYER), ("cut", ring(12, 12, 6.25))] + no_x2(12, 12, 9.25), L_["do-not-tumble-dry"][1])
L_["do-not-iron"] = ([("s", IRON), ("o", IRON_H)] + no_x2(11.75, 14.75, 4), L_["do-not-iron"][1])
L_["do-not-dry-clean"] = ([("s", circ(12, 12, 9.25))] + no_x2(12, 12, 6.54), L_["do-not-dry-clean"][1])
L_["hand-wash"] = ([("s", TUB), ("cut", "M7.75 13.25L9.25 16.75H15.25V11.75M11 16.75V10.75M13.25 16.75V10.75")], L_["hand-wash"][1])


# ---------------------------------------------------------------- batch 6
def tr(d, dx=0, dy=0, s=1):
    """Scale and translate an absolute M/L/H/V/Z path."""
    out, cmd, idx = [], None, 0
    for tok in re.findall(r"[MLHVZ]|-?[\d.]+", d):
        if tok in "MLHVZ":
            cmd, idx = tok, 0; out.append(tok); continue
        v = float(tok) * s
        if cmd in "ML":
            out.append(n(v + (dx if idx % 2 == 0 else dy))); idx += 1
            out.append(" " if idx % 2 else "")
        else:
            out.append(n(v + (dx if cmd == "H" else dy)))
    return "".join(out)


GLYPHS = {
    "a": "M0 9L3 1.2L6 9M1.2 6H4.8", "b": "M0 4.5H6V9H0V0H5V4.5", "c": "M6 0H0V9H6", "d": "M0 4.5V0H4L6 2V7L4 9H0V4.5",
    "e": "M6 0H0V9H6M0 4.5H5", "f": "M6 0H0V9M0 4.5H5", "g": "M6 0H0V9H6V4.5H3", "h": "M0 0V9M6 0V9M0 4.5H6",
    "i": "M3 0V9M1 0H5M1 9H5", "j": "M5 0V9H0V6", "k": "M0 0V9M6 0L0 5M2 3.5L6 9", "l": "M0 0V9H6",
    "m": "M0 9V0M8 9V0M0 0L4 5L8 0", "n": "M0 9V0M6 9V0M0 0L6 9", "o": "M3 0H6V9H0V0H3", "p": "M0 9V0H6V5H0",
    "q": "M3 0H6V9H0V0H3M3.5 6L6.75 10", "r": "M0 9V0H6V5H0M2.5 5L6 9", "s": "M6 0H0V4.5H6V9H0", "t": "M0 0H6M3 0V9",
    "u": "M0 0V9H6V0", "v": "M0 0L3 7.8L6 0", "w": "M0 0V9M8 0V9M0 9L4 4L8 9", "x": "M0 0L6 9M6 0L0 9",
    "y": "M0 0L3 4.5L6 0M3 4.5V9", "z": "M0 0H6L0 9H6",
    "0": "M3 0H6V9H0V0H3M2 6.5L4 2.5", "1": "M1 2L3 0V9M1 9H5", "2": "M0 0H6V4.5H0V9H6", "3": "M0 0H6V9H0M1 4.5H6",
    "4": "M0 0V5H6M6 0V9", "5": "M6 0H1V4H6V9H0", "6": "M6 0H0V9H6V4.5H0", "7": "M0 0H6L2.5 9", "8": "M3 0H6V9H0V0H3M0 4.5H6",
    "9": "M6 4.5H0V0H6V9H0",
}
BADGE = "M2.75 2.75H21.25V21.25H2.75Z"


def letter(ch):
    w = 8 if ch in "mw" else 6
    s = 1.1
    return [("s", BADGE), ("cut", tr(GLYPHS[ch], 12 - w * s / 2, 12 - 4.5 * s, s))]


FACE = circ(12, 12, 9.25)
EYES = [("d", circ(8.75, 9.75, 1.25)), ("d", circ(15.25, 9.75, 1.25))]
SMILE = ("cut", "M7.75 14.25C9 16.5 15 16.5 16.25 14.25")
FROWN = ("cut", "M7.75 16.5C9 14.25 15 14.25 16.25 16.5")
GRIN = ("cut", "M7.25 13.25H16.75C16.75 16 14.75 17.75 12 17.75C9.25 17.75 7.25 16 7.25 13.25Z")
HEART_EYE = "M8.75 11.5L6 8.75L7.25 7.25L8.75 8.25L10.25 7.25L11.5 8.75Z"
LENS = "M5 9.25H11.25V11.5L10.25 12.75H7L5.5 11.25Z"
EAR = "M6.75 9.5A5.75 5.75 0 0 1 18.25 9.5C18.25 12.75 15.75 13.5 15 15.25C14.25 17 13.75 20.75 10.75 20.75C9.25 20.75 8.25 19.75 7.75 18.75M9.75 9.75A2.5 2.5 0 0 1 14.75 9.75C14.75 11.25 13.25 11.75 12.5 12.75"


def loader(cx=12, cy=12):
    out = []
    for i in range(8):
        a = math.radians(45 * i - 90)
        out.append(f"M{n(cx + 5.25 * math.cos(a))} {n(cy + 5.25 * math.sin(a))}L{n(cx + 9.25 * math.cos(a))} {n(cy + 9.25 * math.sin(a))}")
    return "".join(out)


CATEGORIES.update({
    "🔢 Mathematics": {
        "equals": ([("o", "M4.75 8.75H19.25M4.75 15.25H19.25")], "equals, total, math"),
        "not-equal": ([("o", "M4.75 8.75H19.25M4.75 15.25H19.25M16.75 3.75L7.25 20.25")], "not equal, math"),
        "divide": ([("o", "M4.75 12H19.25"), ("f", circ(12, 6.5, 1.5)), ("f", circ(12, 17.5, 1.5))], "divide, division, math"),
        "percent": ([("o", "M18.75 5.25L5.25 18.75"), ("s", circ(7, 7, 2.75)), ("s", circ(17, 17, 2.75))], "percent, discount, math"),
        "plus-minus": ([("o", "M12 3.75V14.25M6.75 9H17.25M4.75 20.25H19.25")], "plus minus, tolerance, math"),
        "infinity": ([("o", "M12 12C10 8.75 9.5 7.25 7.5 7.25A4.75 4.75 0 0 0 7.5 16.75C9.5 16.75 10 15.25 12 12C14 8.75 14.5 7.25 16.5 7.25A4.75 4.75 0 0 1 16.5 16.75C14.5 16.75 14 15.25 12 12")], "infinity, unlimited, math"),
        "pi": ([("o", "M3.75 6.75H20.25M8.25 6.75V19.25M15.25 6.75V17.25C15.25 18.5 16 19.25 17.25 19.25H19.25")], "pi, math"),
        "sigma": ([("o", "M18.25 6.75V3.75H5.75L12.75 12L5.75 20.25H18.25V17.25")], "sigma, sum, math"),
        "square-root": ([("o", "M2.75 13.25H6L9.75 20.25L14.25 4.25H21.25")], "square root, math"),
        "function": ([("o", "M16.75 3.75H14.25C12.5 3.75 11.75 4.75 11.5 6.25L9.25 18C9 19.5 8.25 20.25 6.5 20.25H4.75M7.75 9.25H15.75")], "function, formula, math"),
        "greater-than": ([("o", "M6.25 5.25L17.75 12L6.25 18.75")], "greater than, math"),
        "less-than": ([("o", "M17.75 5.25L6.25 12L17.75 18.75")], "less than, math"),
        "approximately": ([("o", "M4.25 9.25C6.5 6.75 9 6.75 12 9.25C15 11.75 17.5 11.75 19.75 9.25M4.25 15.75C6.5 13.25 9 13.25 12 15.75C15 18.25 17.5 18.25 19.75 15.75")], "approximately, math"),
        "brackets": ([("o", "M8.25 3.75H4.75V20.25H8.25M15.75 3.75H19.25V20.25H15.75")], "brackets, math, code"),
    },
    "🔤 Letters & digits": {
        **{f"letter-{c}": (letter(c), f"letter, {c}, alphabet") for c in "abcdefghijklmnopqrstuvwxyz"},
        **{f"digit-{c}": (letter(c), f"digit, {c}, number") for c in "0123456789"},
    },
    "😀 Emoji": {
        "smile": ([("s", FACE)] + EYES + [SMILE], "smile, happy, emoji"),
        "grin": ([("s", FACE)] + EYES + [GRIN], "grin, happy, emoji"),
        "laugh": ([("s", FACE), ("cut", "M6.75 10.25L8.75 8.25L10.75 10.25M13.25 10.25L15.25 8.25L17.25 10.25"), GRIN], "laugh, joy, emoji"),
        "wink": ([("s", FACE), ("d", circ(8.75, 9.75, 1.25)), ("cut", "M13.5 9.75H17"), SMILE], "wink, playful, emoji"),
        "neutral": ([("s", FACE)] + EYES + [("cut", "M8 15H16")], "neutral, meh, emoji"),
        "frown": ([("s", FACE)] + EYES + [FROWN], "sad, frown, emoji"),
        "surprised": ([("s", FACE)] + EYES + [("cut", circ(12, 15.25, 2))], "surprised, wow, emoji"),
        "heart-eyes": ([("s", FACE), ("d", HEART_EYE), ("d", tr(HEART_EYE, 6.5, 0)), SMILE], "love, heart eyes, emoji"),
        "cool": ([("s", FACE), ("d", LENS), ("d", mirror(LENS)), ("cut", "M11.25 10H12.75"), SMILE], "cool, sunglasses, emoji"),
        "angry": ([("s", FACE), ("cut", "M7 8L10.5 9.75M17 8L13.5 9.75"), ("d", circ(9, 11.75, 1.25)), ("d", circ(15, 11.75, 1.25)), FROWN], "angry, mad, emoji"),
        "sleepy": ([("s", FACE), ("cut", "M7 10.25H10.5M13.5 10.25H17"), ("cut", circ(12, 15.5, 1.25))], "sleepy, tired, emoji"),
        "ghost": ([("s", "M12 2.75A7.75 7.75 0 0 1 19.75 10.5V21.25L17 19L14.5 21.25L12 19L9.5 21.25L7 19L4.25 21.25V10.5A7.75 7.75 0 0 1 12 2.75Z"),
                   ("d", circ(9.25, 10, 1.25)), ("d", circ(14.75, 10, 1.25))], "ghost, empty state, emoji"),
    },
    "🖱️ Cursors": {
        "cursor": ([("s", "M4.75 3.75L11 20.25L13.75 13.75L20.25 11Z")], "cursor, pointer, arrow"),
        "cursor-click": ([("s", "M9.75 8.75L14.25 20.25L16.5 15.5L21 13.25Z"), ("o", "M9.25 2.75V5.25M2.75 9.25H5.25M4.75 4.75L6.5 6.5M14 5L12.75 6.25M5 14L6.25 12.75")], "click, tap, cursor"),
        "hand-pointer": ([("s", "M10 11.75V4.25A1.75 1.75 0 0 1 13.5 4.25V10.75L19.25 12.25V17L17.25 21.25H9.75L4.75 15.25L6.25 13.75L10 15.75Z"), ("cut", "M13.5 10.75V14M16.25 11.5V14")], "hand, pointer, tap"),
        "text-cursor": ([("o", "M9 3.25H15M9 20.75H15M12 3.25V20.75")], "text cursor, i-beam, input"),
        "crosshair": ([("o", "M12 2.75V9M12 15V21.25M2.75 12H9M15 12H21.25")], "crosshair, precision, cursor"),
        "resize-column": ([("o", "M12 3.25V20.75M3.75 12H9.25M14.75 12H20.25M6.25 9.5L3.75 12L6.25 14.5M17.75 9.5L20.25 12L17.75 14.5")], "resize, column, width"),
        "resize-row": ([("o", "M3.25 12H20.75M12 3.75V9.25M12 14.75V20.25M9.5 6.25L12 3.75L14.5 6.25M9.5 17.75L12 20.25L14.5 17.75")], "resize, row, height"),
        "resize-diagonal": ([("o", "M4.75 19.25L19.25 4.75M11.75 4.75H19.25V12.25M4.75 11.75V19.25H12.25")], "resize, diagonal, expand"),
        "loader": ([("o", loader())], "loading, spinner, wait"),
    },
    "♿ Accessibility": {
        "accessibility": ([("s", circ(12, 12, 9.25)), ("d", circ(12, 7.25, 1.5)), ("cut", "M6.75 10.25L12 11.25L17.25 10.25M12 11.25V14.25L9 18.75M12 14.25L15 18.75")], "accessibility, inclusive, a11y"),
        "wheelchair": ([("f", circ(10, 4.5, 1.75)), ("o", "M10 7.75V13.75H16L18.75 19.25H20.75M10 10.25H15"), ("o", arc(9.75, 16, 5.25, 230, 30))], "wheelchair, accessible, disabled"),
        "contrast": ([("s", circ(12, 12, 9.25)), ("d", "M12 2.75A9.25 9.25 0 0 1 12 21.25Z")], "contrast, display, a11y"),
        "text-size": ([("o", "M2.75 18.75L7.75 5.25L12.75 18.75M4.5 14.25H11"), ("o", "M14 18.75L17.5 9.75L21 18.75M15.1 15.75H19.9")], "text size, font size, a11y"),
        "closed-captions": ([("s", "M2.75 4.75H21.25V19.25H2.75Z"), ("cut", "M10.75 9.75H6.75V14.25H10.75M17.25 9.75H13.25V14.25H17.25")], "captions, subtitles, cc"),
        "ear": ([("o", EAR)], "ear, hearing, listen"),
        "ear-off": ([("o", EAR)] + SLASH, "hearing impaired, deaf, mute"),
        "braille": ([("f", circ(8.25, 5.25, 2)), ("f", circ(15.75, 5.25, 2)), ("f", circ(8.25, 12, 2)), ("s", circ(15.75, 12, 1.5)),
                     ("s", circ(8.25, 18.75, 1.5)), ("f", circ(15.75, 18.75, 2))], "braille, blind, a11y"),
        "book-open": ([("s", "M2.75 4.75C6.5 4.25 9.75 4.75 12 6.75V20.25C9.75 18.25 6.5 17.75 2.75 18.25Z"),
                       ("s", "M21.25 4.75C17.5 4.25 14.25 4.75 12 6.75V20.25C14.25 18.25 17.5 17.75 21.25 18.25Z"), ("cut", "M12 6.75V20.25")], "book, read, guide"),
    },
})


A_ = CATEGORIES["♿ Accessibility"]
A_["book-open"] = ([("s", "M12 6.75C9.75 4.75 6.5 4.25 2.75 4.75V18.25C6.5 17.75 9.75 18.25 12 20.25"),
                    ("s", "M12 6.75C14.25 4.75 17.5 4.25 21.25 4.75V18.25C17.5 17.75 14.25 18.25 12 20.25"), ("cut", "M12 6.75V20.25")], A_["book-open"][1])


# ---------------------------------------------------------------- expansion 1: ecommerce core (selection from Lucide's categories, redrawn)
NEW = set()


def add(page, items):
    CATEGORIES[page].update(items); NEW.update(items)


def star_half():
    pts = []
    for i in range(5, 11):
        a = math.radians(-90 + i * 36); r = 8.25 if i % 2 == 0 else 4.1
        pts.append((12 + r * math.cos(a), 12.75 + r * math.sin(a)))
    return poly(pts)


TAG = "M2.75 2.75H12L21.25 12L12 21.25L2.75 12Z"
TAG_HOLE = ("d", circ(7.5, 7.5, 1.25))
COUPON = "M2.75 5.75H21.25V9.5A2.5 2.5 0 0 0 21.25 14.5V18.25H2.75V14.5A2.5 2.5 0 0 0 2.75 9.5Z"
HEART = "M12 19.5L4.74 12.26A4.25 4.25 0 1 1 12 9.25A4.25 4.25 0 1 1 19.26 12.26Z"
BADGE8 = star(12, 12, 9, 7.25, 8, -90 + 11.25)
CARD = "M2.75 4.75H21.25V19.25H2.75Z"
CARD_CUT = ("cut", "M2.75 9.25H21.25M6 15.25H10")
BOXC = [("s", BOX_LID), ("s", BOX_BODY), ("cut", "M2.75 7.75H21.25")]
TRUCK_BODY = "M5.31 16.75H2.75V5.75H14.25V9.25H18.25L21.25 12.75V16.75H19.19M15.31 16.75H9.19"
TRUCK = [("s", TRUCK_BODY), ("cut", "M14.25 9.25V16.75M16.25 9.25V12.75H21.25"), ("s", circ(7.25, 17.25, 2)), ("s", circ(17.25, 17.25, 2)),
         ("k", circ(7.25, 17.25, 3.5)), ("k", circ(17.25, 17.25, 3.5))]
BOOKMARK = "M5.25 2.75H18.75V21.25L12 16.75L5.25 21.25Z"
TAKEOFF = "M3.25 11.25L5.25 10.25L8.25 12.25L12 10.25L8.25 5.75L10.75 4.5L16.5 8L19.25 6.5C20.25 6 21.25 6.25 21.25 7.5C21.25 8.5 20.75 9 20 9.5L7 16.25Z"

add("🛍️ Shopping & commerce", {
    "shopping-cart-minus": ([("o", CART_LINE), ("s", CART_BASKET), ("cut", "M11.25 10.5H15.75")] + CART_WHEELS, "cart, remove, minus"),
    "shopping-cart-x": ([("o", CART_LINE), ("s", CART_BASKET), ("cut", "M11.75 8.75L15.25 12.25M15.25 8.75L11.75 12.25")] + CART_WHEELS, "cart, remove, empty"),
    "shopping-bag-minus": ([("s", BAG), ("o", BAG_HANDLE), ("cut", "M9.25 14.5H14.75")], "bag, remove"),
    "shopping-bag-x": ([("s", BAG), ("o", BAG_HANDLE), ("cut", "M9.75 12.25L14.25 16.75M14.25 12.25L9.75 16.75")], "bag, remove, cancel"),
    "tag-plus": ([("s", TAG), TAG_HOLE, ("cut", "M12.5 10V15.5M9.75 12.75H15.25")], "tag, add, label"),
    "tag-x": ([("s", TAG), TAG_HOLE, ("cut", "M10.5 10.75L14.5 14.75M14.5 10.75L10.5 14.75")], "tag, remove, label"),
    "tag-percent": ([("s", TAG), TAG_HOLE, ("cut", "M14.5 10.5L10.75 14.25")], "price tag, sale, discount"),
    "ticket-percent": ([("s", COUPON), ("cut", "M14.75 9L9.25 15"), ("d", circ(9.5, 9.75, 1)), ("d", circ(14.5, 14.25, 1))], "coupon, voucher, discount code"),
    "circle-percent": ([("s", circ(12, 12, 9.25)), ("cut", "M15 9L9 15"), ("d", circ(9.25, 9.25, 1)), ("d", circ(14.75, 14.75, 1))], "discount, sale, percent"),
    "badge-dollar": ([("s", BADGE8), ("cut", "M14.75 9.5H10.75A1.25 1.25 0 0 0 10.75 12H13.25A1.25 1.25 0 0 1 13.25 14.5H9.25M12 7.75V16.25")], "price, deal, offer"),
    "badge-euro": ([("s", BADGE8), ("cut", "M14.75 9.5A3.5 3.5 0 1 0 14.75 14.5M7.75 11H12M7.75 13H12")], "price, deal, offer"),
    "gift-card": ([("s", CARD), ("cut", "M9.25 4.75V19.25M2.75 11.25H21.25"), ("cut", "M9.25 11.25L6.5 7.75M9.25 11.25L12 7.75")], "gift card, voucher, present"),
    "perfume-bottle": ([("s", "M5.25 9.25H18.75V21.25H5.25Z"), ("s", "M9.25 5.25H14.75V9.25H9.25Z"), ("o", "M12 2.75V5.25"), ("cut", "M5.25 9.25H18.75"), ("cut", circ(12, 15.25, 2.25))], "perfume, fragrance, beauty"),
    "tube-lotion": ([("s", "M5.75 2.75H18.25L16.25 16.75H7.75Z"), ("s", "M8.75 16.75H15.25V21.25H8.75Z"), ("cut", "M7.75 16.75H16.25M6.25 6.25H17.75")], "lotion, cream, skincare, beauty"),
    "paper-bag": ([("s", "M4.75 6.75L7 9L9.5 6.75L12 9L14.5 6.75L17 9L19.25 6.75V21.25H4.75Z"), ("cut", "M8.75 14.25H15.25")], "paper bag, takeaway, order"),
    "door-package": ([("s", "M4.75 21.25V2.75H15.25V12.75H11.25V21.25"), ("s", "M11.25 12.75H21.25V21.25H11.25Z"), ("cut", "M11.25 12.75H15.25M16.25 12.75V16"), ("d", circ(8.25, 12, 1))], "doorstep delivery, parcel, drop off"),
    "star-half": ([("s", star(12, 12.75, 8.25, 4.1, 5)), ("d", star_half())], "rating, half star, review"),
    "heart-plus": ([("s", HEART), ("cut", "M12 8.25V14.25M9 11.25H15")], "wishlist, add, save"),
    "heart-minus": ([("s", HEART), ("cut", "M9 11.25H15")], "wishlist, remove"),
    "heart-check": ([("s", HEART), ("cut", "M9 11.25L11.25 13.5L15 9.75")], "wishlist, saved"),
})
add("💳 Paymen & shipping", {
    "credit-card-plus": ([("s", CARD), CARD_CUT, ("cut", "M16.5 11.75V16.75M14 14.25H19")], "add card, payment method"),
    "credit-card-check": ([("s", CARD), CARD_CUT, ("cut", "M13.75 14.25L15.75 16.25L19.25 12.75")], "payment approved, card verified"),
    "credit-card-x": ([("s", CARD), CARD_CUT, ("cut", "M14.5 12.25L18.5 16.25M18.5 12.25L14.5 16.25")], "payment failed, card declined"),
    "card-reader": ([("s", "M5.25 2.75H18.75V21.25H5.25Z"), ("cut", "M8.25 6.25H15.75V10.25H8.25Z")] + [("d", circ(x, y, 1)) for y in (14, 17.75) for x in (9, 15)], "card terminal, pos, checkout"),
    "banknote-check": ([("s", "M2.75 6.75H21.25V17.25H2.75Z"), ("cut", "M8.75 12L11 14.25L15.25 10")], "payment received, paid"),
    "wallet-minimal": ([("s", "M2.75 5.75H21.25V19.25H2.75Z"), ("cut", "M2.75 9.75H17M14.25 14.25H18.25")], "wallet, balance, funds"),
    "box-plus": (BOXC + [("cut", "M12 11V17M9 14H15")], "add package, new shipment"),
    "box-minus": (BOXC + [("cut", "M9 14H15")], "remove package"),
    "box-x": (BOXC + [("cut", "M9.75 11.75L14.25 16.25M14.25 11.75L9.75 16.25")], "cancelled order, lost package"),
    "box-search": (BOXC + [("cut", circ(11.5, 13.25, 2.25)), ("cut", "M13.25 15L15.25 17")], "track package, find order"),
    "box-open": ([("s", "M3.75 9.75H20.25V20.25H3.75Z"), ("o", "M3.75 9.75L6.25 4.75H17.75L20.25 9.75"), ("cut", "M9.75 13.25H14.25")], "unboxing, open package"),
    "package-open": ([("s", "M3.25 9L12 13.5L20.75 9V17L12 21.5L3.25 17Z"), ("o", "M3.25 9L7.63 4.25L12 6.75L16.38 4.25L20.75 9"), ("cut", "M12 13.5V21.5")], "unboxing, open parcel"),
})
add("🚗 Transportation", {
    "truck-check": (TRUCK + [("cut", "M5.5 10.5L7.5 12.5L11.5 8.5")], "delivered, shipped, shipping confirmed"),
    "truck-clock": (TRUCK + [("cut", circ(8.5, 10.75, 2.5))], "delivery time, eta, scheduled delivery"),
    "truck-electric": (TRUCK + [("cut", "M9.25 7.5L7 10.75H10L7.75 14")], "electric delivery, green shipping"),
    "van": ([("s", "M5.31 17.25H2.75V6.25H15.25L21.25 12.25V17.25H19.19M15.31 17.25H9.19"), ("cut", "M13.25 6.25V12.25H21.25"), ("s", circ(7.25, 17.75, 2)), ("s", circ(17.25, 17.75, 2)),
             ("k", circ(7.25, 17.75, 3.5)), ("k", circ(17.25, 17.75, 3.5))], "van, courier, last mile delivery"),
    "trailer": ([("s", "M2.75 6.75H17.25V15.75H2.75Z"), ("o", "M17.25 14.75H21.25"), ("s", circ(9.75, 17.75, 2)), ("k", circ(9.75, 17.75, 3.5))], "trailer, freight, haulage"),
    "hand-truck": ([("o", "M3.25 3.75H6.75L11 17.25H20.75"), ("s", "M10.25 8.25L16.75 6.25L18.75 12.75L12.25 14.75Z"), ("s", circ(10.25, 19.25, 2))], "hand truck, dolly, warehouse, carrier"),
    "pallet": ([("s", "M4.75 3.75H19.25V13.75H4.75Z"), ("cut", "M12 3.75V7.25"), ("o", "M2.75 16.25H21.25M2.75 20.75H21.25M5.25 16.25V20.75M12 16.25V20.75M18.75 16.25V20.75")], "pallet, freight, bulk order, wholesale"),
    "container": ([("s", "M2.75 6.25H21.25V17.75H2.75Z"), ("cut", "M6.75 9.25V14.75M10.25 9.25V14.75M13.75 9.25V14.75M17.25 9.25V14.75")], "container, freight, cargo, import"),
    "warehouse": ([("s", "M2.75 9.25L12 3.25L21.25 9.25V20.75H2.75Z"), ("cut", "M6.75 20.75V12.25H17.25V20.75M6.75 15.25H17.25M6.75 18H17.25")], "warehouse, fulfilment, stock, storage"),
    "forklift": ([("s", "M6.25 5.25H11.25L13.25 11.75V16.75H3.75V11.75H6.25Z"), ("cut", "M6.25 11.75H13.25"), ("o", "M16.25 2.75V19.25H21.25"), ("s", circ(7, 18.25, 2)), ("s", circ(13, 18.25, 2)),
                  ("k", circ(7, 18.25, 3.5)), ("k", circ(13, 18.25, 3.5))], "forklift, warehouse, logistics"),
    "ship-cargo": ([("s", "M2.75 13.25H21.25L19.25 20.75H4.75Z"), ("s", "M5.75 8.25H11.75V13.25H5.75Z"), ("s", "M12.25 8.25H18.25V13.25H12.25Z"), ("s", "M9 3.25H15V8.25H9Z"),
                    ("cut", "M12 8.25V13.25M5.75 13.25H18.25M9 8.25H15")], "cargo ship, sea freight, import"),
    "plane-takeoff": ([("s", TAKEOFF), ("o", "M2.75 20.75H21.25")], "air freight, express shipping"),
    "road": ([("o", "M6.25 3.25L3.25 20.75M17.75 3.25L20.75 20.75M12 3.25V6.25M12 9.25V12.25M12 15.25V18.25")], "road, route, on the way"),
    "ev-charger": ([("s", "M4.75 2.75H14.25V21.25H4.75Z"), ("cut", "M10.25 6.25L7.75 10H11.25L8.75 13.75"), ("o", "M2.75 21.25H16.25"),
                    ("o", "M14.25 13.25H16.25C17.25 13.25 17.75 13.75 17.75 14.75V17C17.75 18.1 20.25 18.1 20.25 17V8.25L17.25 5.25")], "ev charger, electric, charging"),
    "luggage": ([("s", "M5.25 7.25H18.75V19.75H5.25Z"), ("o", "M9 7.25V2.75H15V7.25M8 19.75V21.25M16 19.75V21.25"), ("cut", "M9.25 10.75V16.25M14.75 10.75V16.25")], "luggage, suitcase, travel"),
    "drone": ([("s", "M9.25 10.25H14.75V14.25H9.25Z"), ("o", "M9.25 10.25L5.25 6.25M14.75 10.25L18.75 6.25M9.25 14.25L5.25 18.25M14.75 14.25L18.75 18.25M2.75 5.25H7.75M16.25 5.25H21.25M2.75 19.25H7.75M16.25 19.25H21.25")], "drone, delivery"),
})
add("👗 Fashion & apparel", {
    "glasses": ([("s", circ(6.75, 13.5, 4)), ("s", circ(17.25, 13.5, 4)), ("o", "M10.75 13.5H13.25M2.75 13.5V8.25L5.25 5.75M21.25 13.5V8.25L18.75 5.75")], "glasses, eyewear, optical"),
    "backpack": ([("s", "M4.75 10.25A7.25 7.25 0 0 1 19.25 10.25V21.25H4.75Z"), ("o", "M9.25 4V2.75H14.75V4"), ("cut", "M8.25 14.25H15.75V21.25M8.25 21.25V14.25")], "backpack, bag, school"),
    "briefcase": ([("s", "M2.75 7.25H21.25V20.25H2.75Z"), ("o", "M8.25 7.25V3.75H15.75V7.25"), ("cut", "M2.75 12.75H21.25")], "briefcase, business, work"),
    "ribbon": ([("s", circ(12, 8.75, 6)), ("o", "M8.5 13.75L6.25 21.25L12 18.75L17.75 21.25L15.5 13.75"), ("cut", circ(12, 8.75, 2))], "ribbon, award, best seller"),
    "spool": ([("s", "M5.25 2.75H18.75V6.25H5.25Z"), ("s", "M5.25 17.75H18.75V21.25H5.25Z"), ("s", "M7.25 6.25H16.75V17.75H7.25Z"), ("cut", "M7.25 6.25H16.75M7.25 17.75H16.75M7.25 10L16.75 8.5M7.25 13.75L16.75 12.25")], "thread, spool, sewing, material"),
    "swatch-book": ([("s", "M2.75 2.75H11.75V21.25H2.75Z"), ("s", "M11.75 6.75L16 3.5L21 10L11.75 17.5"), ("cut", "M2.75 14.25H11.75"), ("d", circ(7.25, 17.75, 1.25))], "colour swatch, fabric, variant"),
})
add("👤 People", {
    "user-x": ([("s", US_HEAD), ("s", US_BODY), ("o", "M16.5 9.25L21.25 14M21.25 9.25L16.5 14")], "remove user, block"),
    "user-search": ([("s", US_HEAD), ("s", US_BODY), ("o", circ(18.25, 10.25, 2.25)), ("o", "M19.75 12L21.25 13.5")], "find user, customer search"),
    "user-star": ([("s", US_HEAD), ("s", US_BODY), ("f", star(18.25, 11.75, 3.75, 1.5, 5))], "vip customer, loyalty, member"),
    "venus": ([("o", circ(12, 9, 6.25)), ("o", "M12 15.25V21.25M8.75 18.25H15.25")], "women, female, gender filter"),
    "mars": ([("o", circ(9.75, 14.25, 7)), ("o", "M14.75 9.25L21.25 2.75M15.25 2.75H21.25V8.75")], "men, male, gender filter"),
})
add("🔑 Accounts & access", {
    "bookmark-plus": ([("s", BOOKMARK), ("cut", "M12 6.75V12.25M9.25 9.5H14.75")], "save, add to list"),
    "bookmark-check": ([("s", BOOKMARK), ("cut", "M9 9.5L11.25 11.75L15 8")], "saved, added"),
    "bookmark-x": ([("s", BOOKMARK), ("cut", "M10 7.5L14 11.5M14 7.5L10 11.5")], "remove, unsave"),
    "award": ([("s", circ(12, 9, 6.25)), ("o", "M8.25 14.25L6.75 21.25L12 18.25L17.25 21.25L15.75 14.25")], "loyalty, reward, membership tier"),
})
add("🔔 Notifications", {
    "bell-check": ([("s", BELL)] + BELL_EXTRA + [("cut", "M9 10.75L11.25 13L15 9.25")], "notification on, confirmed"),
    "bell-minus": ([("s", BELL)] + BELL_EXTRA + [("cut", "M9.25 10.75H14.75")], "unsubscribe, remove alert"),
    "siren": ([("s", "M6.25 18.75V12.25A5.75 5.75 0 0 1 17.75 12.25V18.75Z"), ("o", "M3.75 21.25H20.25M12 2.75V4.25M4.25 5L5.5 6.25M19.75 5L18.5 6.25"), ("cut", "M12 9.25V13")], "alert, urgent, flash sale"),
    "check-check": ([("o", "M2.75 12.75L7.5 17.5L16.25 8.25M12.25 15L14.75 17.5L21.25 8.25")], "read, delivered, double check"),
})
add("🧭 Navigation & places", {
    "map-pin-plus": ([("s", PIN), ("cut", "M12 6.75V13.25M8.75 10H15.25")], "add address, new location"),
    "map-pin-x": ([("s", PIN), ("cut", "M9.5 7.5L14.5 12.5M14.5 7.5L9.5 12.5")], "remove address, no delivery"),
    "map-pin-house": ([("s", PIN), ("cut", "M8.75 10L12 7L15.25 10V13.5H8.75Z")], "home address, delivery address"),
    "waypoints": ([("s", circ(12, 5, 2.25)), ("s", circ(5, 19, 2.25)), ("s", circ(19, 19, 2.25)), ("o", "M10.75 6.75L6.25 17M13.25 6.75L17.75 17M7.25 19H16.75")], "stops, network, route"),
})
add("💬 Communication", {
    "message-circle-check": ([("s", BUBBLE), ("cut", "M8.25 12L11 14.75L15.75 10")], "resolved, delivered, chat"),
    "message-circle-x": ([("s", BUBBLE), ("cut", "M9.25 9.25L14.75 14.75M14.75 9.25L9.25 14.75")], "closed, unresolved, chat"),
    "message-circle-question": ([("s", BUBBLE), ("cut", "M9.5 9.5C9.5 8.25 10.5 7.5 12 7.5C13.5 7.5 14.5 8.5 14.5 9.75C14.5 11.5 12 11.75 12 13.5"), ("d", circ(12, 16, 1))], "faq, help, question"),
    "message-text": ([("s", BUBBLE), ("cut", "M7.75 10H16.25M7.75 14H13.25")], "review, comment, feedback"),
    "send-horizontal": ([("s", "M2.75 3.25L21.25 12L2.75 20.75L6.75 12Z"), ("cut", "M6.75 12H12.75")], "send, submit, message"),
    "bot": ([("s", "M4.25 8.75H19.75V20.25H4.25Z"), ("o", "M12 3.5V8.75M2 13V16M22 13V16"), ("f", circ(12, 3.5, 1.25)), ("d", circ(9, 13.25, 1.25)), ("d", circ(15, 13.25, 1.25)), ("cut", "M9 16.75H15")], "chatbot, assistant, ai support"),
})
add("💰 Finance", {
    "dollar-sign": ([("o", "M16.75 6.25H10.25A2.75 2.75 0 0 0 10.25 11.75H13.75A2.75 2.75 0 0 1 13.75 17.25H6.75M12 2.75V21.25")], "price, dollar, currency"),
    "euro-sign": ([("o", "M17.75 6.5A7 7 0 1 0 17.75 17.5M3.75 10.25H13.25M3.75 13.75H13.25")], "price, euro, currency"),
    "pound-circle": ([("s", circ(12, 12, 9.25)), ("cut", "M15.25 8.25C14 6.5 10 6.75 10 10V16.25H15.75M8.25 12.5H13.25")], "price, pound, currency"),
    "receipt-percent": ([("s", "M4.75 2.75H19.25V21.25L16.83 19.75L14.42 21.25L12 19.75L9.58 21.25L7.17 19.75L4.75 21.25Z"), ("cut", "M14.75 7.5L9.25 13.5"), ("d", circ(9.5, 8, 1)), ("d", circ(14.5, 13, 1))], "tax, vat, discount, receipt"),
})
add("🕒 Time & calendar", {
    "calendar-clock": (CAL + [("cut", circ(12, 15.25, 3)), ("cut", "M12 13.75V15.25H13.25")], "delivery slot, booking time"),
    "calendar-range": (CAL + [("cut", "M6.75 13.25H11.75M12.25 17H17.25")], "date range, delivery window"),
    "calendar-heart": (CAL + [("d", "M12 18.5L8.75 15.25L9.75 13.25L12 14.25L14.25 13.25L15.25 15.25Z")], "special date, event, anniversary"),
})
add("🛡️ Security", {
    "shield-user": ([("s", SHIELD), ("cut", circ(12, 9.5, 2)), ("cut", "M7.75 16C8.75 14.5 10.25 13.75 12 13.75C13.75 13.75 15.25 14.5 16.25 16")], "buyer protection, trusted account"),
    "shield-x": ([("s", SHIELD), ("cut", "M9.25 9.25L14.75 14.75M14.75 9.25L9.25 14.75")], "blocked, fraud, unsafe"),
    "shield-plus": ([("s", SHIELD), ("cut", "M12 8.25V15.25M8.5 11.75H15.5")], "extra protection, insurance"),
})


# expansion 1 fixes
S_ = CATEGORIES["🛍️ Shopping & commerce"]
S_["tag-percent"] = ([("s", TAG), TAG_HOLE, ("cut", "M14.75 10.75L10.75 14.75"), ("d", circ(10.75, 11, .9)), ("d", circ(14.75, 14.5, .9))], S_["tag-percent"][1])
S_["door-package"] = ([("s", "M4.75 21.25V2.75H15.25V12.75H11.25V21.25"), ("k", "M9.75 11.25V21.75M9.75 11.25H15.75"), ("s", "M11.25 12.75H21.25V21.25H11.25Z"), ("cut", "M16.25 12.75V15.75"), ("d", circ(7.25, 12, 1))], S_["door-package"][1])
TR_ = CATEGORIES["🚗 Transportation"]
TR_["truck-check"] = (TRUCK + [("cut", "M5.25 9.75L7.25 11.75L11.25 7.75")], TR_["truck-check"][1])
TR_["truck-clock"] = (TRUCK + [("cut", ring(8.25, 9.75, 2.5)), ("cut", "M8.25 8.5V10H9.5")], TR_["truck-clock"][1])
TR_["truck-electric"] = (TRUCK + [("cut", "M9.25 6.75L6.75 10H10.25L7.75 13")], TR_["truck-electric"][1])
TR_["forklift"] = ([("s", "M6.25 5.25H11.25L13.25 11.75V16.75H3.75V11.75H6.25Z"), ("cut", "M6.25 11.75H13.25"), ("o", "M16.25 2.75V19.25H21.25"),
                    ("s", circ(6.25, 18.75, 1.5)), ("s", circ(13.25, 18.75, 1.5)), ("k", circ(6.25, 18.75, 2.75)), ("k", circ(13.25, 18.75, 2.75))], TR_["forklift"][1])
TI_ = CATEGORIES["🕒 Time & calendar"]
TI_["calendar-clock"] = (CAL + [("cut", ring(12, 15.5, 3.25)), ("cut", "M12 13.75V15.5H13.5")], TI_["calendar-clock"][1])
CO_ = CATEGORIES["💬 Communication"]
CO_["bot"] = ([("s", "M5.25 8.75H18.75V20.25H5.25Z"), ("o", "M12 3.5V8.75M2.75 13V16M21.25 13V16"), ("f", circ(12, 3.5, 1.25)), ("d", circ(9.25, 13.25, 1.25)), ("d", circ(14.75, 13.25, 1.25)), ("cut", "M9.25 16.75H14.75")], CO_["bot"][1])


# ---------------------------------------------------------------- complete laundry care set (covers every symbol in the Swoozh Fashion UI Kit)
def tub(dy=0):
    y = lambda v: n(v + dy)
    return (f"M2.75 {y(6.25)}L5 {y(19.75)}H19L21.25 {y(6.25)}C19.25 {y(6.25)} 18.75 {y(8.5)} 16.6 {y(8.5)}C14.6 {y(8.5)} 14 {y(6.25)} 12 {y(6.25)}"
            f"C10 {y(6.25)} 9.4 {y(8.5)} 7.4 {y(8.5)}C5.25 {y(8.5)} 4.75 {y(6.25)} 2.75 {y(6.25)}Z")


def tub_dots(k):
    pos = {1: [(12, 13.5)], 2: [(9.75, 13.5), (14.25, 13.5)], 3: [(8.5, 13.5), (12, 13.5), (15.5, 13.5)],
           4: [(9.75, 11.75), (14.25, 11.75), (9.75, 15.5), (14.25, 15.5)],
           5: [(8.5, 11.75), (12, 11.75), (15.5, 11.75), (9.75, 15.5), (14.25, 15.5)],
           6: [(8.5, 11.75), (12, 11.75), (15.5, 11.75), (8.5, 15.5), (12, 15.5), (15.5, 15.5)]}[k]
    return [("d", circ(x, y, 1)) for x, y in pos]


def dots(y, xs, r=1.25):
    return [("d", circ(x, y, r)) for x in xs]


WRING = "M2.75 7.75C6 7.75 9 10.5 12 12C15 10.5 18 7.75 21.25 7.75V16.25C18 16.25 15 13.5 12 12C9 13.5 6 16.25 2.75 16.25Z"
SQ = ("s", DRYER)
SHADE = ("cut", "M2.75 9.25L9.25 2.75M2.75 14L14 2.75")
DRUM = ("cut", ring(12, 12, 6.25))
IRON_UP, IRON_UP_H = "M2.75 14.75C2.75 9.75 6 6.75 10.25 6.75H18.75L21.25 14.75Z", "M10.75 2.75H17.75L18.75 6.75"
DC = ("s", circ(12, 12, 9.25))
HAND = "M7.75 13.25L9.25 16.75H15.25V11.75M11 16.75V10.75M13.25 16.75V10.75"
LAUNDRY_NEW = {
    "machine-wash": ([("s", tub())], "machine wash, normal cycle, care label"),
    "machine-wash-permanent-press": ([("s", tub(-2.5)), ("o", "M5 20.25H19")], "permanent press, synthetics, care label"),
    "machine-wash-delicate": ([("s", tub(-3.5)), ("o", "M5 18.75H19M5 21.25H19")], "gentle cycle, delicate, wool, care label"),
    "wash-50": ([("s", TUB), ("cut", "M10.25 10.75H7.25V13.5H10.25V16.75H6.75"), ("cut", ZERO)], "wash, 50 degrees, care label"),
    "wash-70": ([("s", TUB), ("cut", "M6.75 10.75H10.25L8 16.75"), ("cut", ZERO)], "wash, 70 degrees, care label"),
    "wash-95": ([("s", TUB), ("cut", "M10.25 13.75H6.75V10.75H10.25V16.75H6.75"), ("cut", ZERO)], "wash, 95 degrees, hot, care label"),
    **{f"wash-{t}-dots": ([("s", TUB)] + tub_dots(i + 1), f"wash, {t} degrees, dots, care label") for i, t in enumerate((30, 40, 50, 60, 70, 95))},
    "wring": ([("s", WRING)], "wring, care label"),
    "do-not-wring": ([("s", WRING)] + no_x2(12, 12, 8), "do not wring, care label"),
    "bleach-non-chlorine": ([("s", BLEACH), ("cut", "M8.5 19.75L12.75 12.2M13 19.75L15.5 15.3")], "non chlorine bleach, oxygen bleach, care label"),
    "dry": ([SQ], "dry, care label"),
    "line-dry": ([SQ, ("cut", "M2.75 6.75C7.5 11.75 16.5 11.75 21.25 6.75")], "line dry, hang to dry, care label"),
    "drip-dry": ([SQ, ("cut", "M8 6.25V17.75M12 6.25V17.75M16 6.25V17.75")], "drip dry, care label"),
    "dry-flat": ([SQ, ("cut", "M6.25 12H17.75")], "dry flat, knitwear, care label"),
    "dry-in-shade": ([SQ, SHADE], "dry in shade, care label"),
    "line-dry-in-shade": ([SQ, SHADE, ("cut", "M9 12.75C12 14.25 15.75 13.5 21.25 7.75")], "line dry in shade, care label"),
    "drip-dry-in-shade": ([SQ, SHADE, ("cut", "M11 12V17.75M14.5 8.5V17.75M18 6.25V17.75")], "drip dry in shade, care label"),
    "dry-flat-in-shade": ([SQ, SHADE, ("cut", "M9.25 16H17.75")], "dry flat in shade, care label"),
    "do-not-dry": ([SQ] + no_x2(12, 12, 9.25), "do not dry, care label"),
    "tumble-dry-medium": ([SQ, DRUM] + dots(12, (10, 14)), "tumble dry medium, care label"),
    "tumble-dry-high": ([SQ, DRUM] + dots(12, (8.75, 12, 15.25), 1), "tumble dry high, care label"),
    "tumble-dry-no-heat": ([SQ, ("d", circ(12, 12, 6.5))], "tumble dry no heat, air dry, care label"),
    "iron-medium": ([("s", IRON), ("o", IRON_H)] + dots(15, (10.25, 14.75)), "iron medium, 150 degrees, care label"),
    "no-steam": ([("s", IRON_UP), ("o", IRON_UP_H), ("o", "M7 17L9.5 21.25M12 17V21.25M17 17L14.5 21.25M4.75 21.25L19.25 16.75")], "no steam, do not steam, care label"),
    "dry-clean-plain": ([DC], "dry clean, professional, care label"),
    "dry-clean-any-solvent": ([DC, ("cut", "M8 16.5L12 7.75L16 16.5M9.5 13.25H14.5")], "dry clean, any solvent, care label"),
    "dry-clean-petroleum": ([DC, ("cut", "M15.25 7.5H9.25V16.75M9.25 12H14")], "dry clean, petroleum solvent, care label"),
    "dry-clean-gentle": ([("s", circ(12, 10.25, 7.5)), ("cut", "M9.75 14.5V6.25H13A2.5 2.5 0 0 1 13 11.25H9.75"), ("o", "M5 20.75H19")], "dry clean gentle, care label"),
    "wet-clean": ([DC, ("cut", "M7.75 8.5L9.75 15.5L12 10.5L14.25 15.5L16.25 8.5")], "wet clean, professional, care label"),
}
CATEGORIES["🧺 Laundry care"].update(LAUNDRY_NEW)


_LC = CATEGORIES["🧺 Laundry care"]
_LC["wash-95"] = ([("s", TUB), ("cut", "M10.25 13.75H6.75V10.75H10.25V16.75H6.75"), ("cut", "M16.25 10.75H13.25V13.5H16.25V16.75H12.75")], _LC["wash-95"][1])
_LC["no-steam"] = ([("s", IRON_UP), ("o", IRON_UP_H), ("o", "M7.75 17L16.25 21.25M16.25 17L7.75 21.25")], _LC["no-steam"][1])


# ---------------------------------------------------------------- corner-badge modifier system
# "e": erased in both variants (closed region), "g": glyph line on top, "gf": glyph fill on top.
BADGE_ERASE = ("e", circ(18, 18, 5.75))
MODS = {
    "plus": [("g", "M18 14.5V21.5M14.5 18H21.5")],
    "minus": [("g", "M14.5 18H21.5")],
    "x": [("g", "M15.25 15.25L20.75 20.75M20.75 15.25L15.25 20.75")],
    "check": [("g", "M14.5 18L16.75 20.25L21.25 15.75")],
    "search": [("g", circ(17.25, 17.25, 2.5)), ("g", "M19.1 19.1L21.25 21.25")],
    "lock": [("gf", "M14.75 17.75H21.25V21.25H14.75Z"), ("g", "M16.25 17.75V16.25A1.75 1.75 0 0 1 19.75 16.25V17.75")],
    "clock": [("g", circ(18, 18, 3.25)), ("g", "M18 16.25V18H19.5")],
    "heart": [("gf", "M18 21.25L14.9 18.15A1.9 1.9 0 0 1 18 15.9A1.9 1.9 0 0 1 21.1 18.15Z")],
    "star": [("gf", star(18, 18.25, 3.75, 1.6, 5))],
    "alert": [("g", "M18 14.5V18.75"), ("gf", circ(18, 21, 0.9))],
    "down": [("g", "M18 14.5V21M15.25 18.5L18 21.25L20.75 18.5")],
    "up": [("g", "M18 21.5V15M15.25 17.5L18 14.75L20.75 17.5")],
}
MOD_TAGS = {"plus": "add, new", "minus": "remove", "x": "remove, cancel, failed", "check": "done, confirmed, approved",
            "search": "find, track, search", "lock": "secure, private, locked", "clock": "pending, scheduled, time",
            "heart": "favourite, wishlist, saved", "star": "featured, rated, vip", "alert": "issue, warning, attention",
            "down": "download, save", "up": "upload, send"}


def find(name):
    for icons in CATEGORIES.values():
        if name in icons:
            return icons[name]
    raise KeyError(name)


def badged(base, mod, elems=None):
    e, tags = (elems, "") if elems else find(base)
    return (list(e) + [BADGE_ERASE] + MODS[mod], f"{tags.split(',')[0] if tags else base.split('-')[0]}, {MOD_TAGS[mod]}")


BADGE_PLAN = {
    "📄 File icons": [("cloud", "check"), ("cloud", "x"), ("cloud", "down"), ("cloud", "lock"),
                      ("file", "search"), ("file", "lock"), ("file", "x"), ("file", "clock"), ("file", "heart"),
                      ("folder", "check"), ("folder", "x"), ("folder", "lock"), ("folder", "search"), ("folder", "heart")],
    "📷 Photography": [("image", "plus"), ("image", "x"), ("image", "check"), ("image", "search")],
    "👤 People": [("user", "lock"), ("user", "heart")],
    "✉️ Mail": [("mail", m) for m in ("plus", "check", "x", "search", "lock", "clock", "heart", "star", "alert")],
    "🛍️ Shopping & commerce": [("shopping-cart", "check"), ("shopping-cart", "lock"), ("shopping-cart", "clock"),
                                ("shopping-bag", "heart"), ("shopping-bag", "clock"), ("shopping-bag", "search"),
                                ("store", "check"), ("store", "x"), ("store", "clock"), ("store", "search"), ("store", "heart"),
                                ("receipt", "check"), ("receipt", "x"), ("receipt", "clock"), ("receipt", "search"),
                                ("coupon", "check"), ("coupon", "x")],
    "🚗 Transportation": [("truck", "search"), ("truck", "x"), ("truck", "alert")],
    "💳 Paymen & shipping": [("package", m) for m in ("check", "x", "search", "plus", "clock", "alert")]
                            + [("credit-card", "lock"), ("credit-card", "clock"), ("credit-card", "alert"),
                               ("wallet", "check"), ("wallet", "plus"), ("wallet", "x")],
    "🔔 Notifications": [("bell", "clock")],
    "🧭 Navigation & places": [("map-pin", "search"), ("map-pin", "clock"), ("map-pin", "star"), ("globe", "lock"), ("globe", "check")],
}
EXP2 = {}
for page, pairs in BADGE_PLAN.items():
    for base, mod in pairs:
        nm = f"{base}-{mod}"
        if nm in {k for v in CATEGORIES.values() for k in v}:
            continue
        EXP2.setdefault(page, {})[nm] = badged(base, mod)

FILE_BACK = ("o", "M8.25 2.75H15.75L20.25 7.25V17.75")
EXP2.setdefault("🏠 Home", {}).update({
    "armchair": ([("s", "M6.75 4.25H17.25V11.75H6.75Z"), ("s", "M3.75 9.75H7.25V14.25H16.75V9.75H20.25V18.75H3.75Z"), ("cut", "M7.25 14.25H16.75"),
                  ("o", "M5.75 18.75V21.25M18.25 18.75V21.25")], "armchair, furniture, living room"),
    "lamp-desk": ([("o", "M5.75 21.25H14.25M9 21.25V17.25L5.75 11.25L11.25 6.25"), ("s", poly([(9.5, 4.75), (13.5, 2.75), (18.75, 9.25), (14.75, 11.25)]))], "desk lamp, lighting, office"),
    "shelving-unit": ([("s", "M3.75 2.75H20.25V21.25H3.75Z"), ("cut", "M3.75 9H20.25M3.75 15.25H20.25")], "shelf, storage, furniture"),
    "mirror-round": ([("s", circ(12, 10.25, 7.5)), ("cut", "M9 8.75L11.25 6.5M9.25 11.25L13.75 6.75"), ("o", "M12 17.75V21.25M8.75 21.25H15.25")], "mirror, decor, beauty"),
    "broom": ([("o", "M20.75 3.25L13.25 10.75"), ("s", "M11 8.75L16.25 14L12.75 17.5C10.75 19.5 7 21 3.25 20.75C3 17 4.5 13.25 6.5 11.25Z"),
               ("cut", "M7.5 19.75L10.25 17M5 17.25L8 14.25")], "broom, cleaning, household"),
    "cooking-pot": ([("s", "M4.75 9.75H19.25V16.25C19.25 19 17.25 20.75 14.5 20.75H9.5C6.75 20.75 4.75 19 4.75 16.25Z"), ("o", "M2.75 9.75H21.25M9.75 6.25H14.25")], "pot, cooking, kitchen"),
})
EXP2.setdefault("🍽️ Food & beverage", {}).update({
    "milk": ([("s", "M6.75 8.25L9 4.75H15L17.25 8.25V21.25H6.75Z"), ("s", "M9 2.75H15V4.75H9Z"), ("cut", "M6.75 8.25H17.25M9.75 13.75H14.25")], "milk, dairy, groceries"),
    "carrot": ([("s", "M3.25 20.75L9.25 9.25C11 7.5 14.25 7.75 15.75 9.25C17.25 10.75 17.5 14 15.75 15.75Z"), ("o", "M15.25 8.75L17.5 3.75M15.25 8.75L20.25 6.5"),
                ("cut", "M8.25 13.75L10.25 15.75M6.25 17.5L7.5 18.75")], "carrot, vegetable, groceries"),
    "banana": ([("s", "M4.25 15.25C8.5 17 14.25 15.25 16.75 10.25C17.75 8.25 18 6 17.75 3.75H19.25C20.25 9.75 18.5 15.25 14 18.5C10.25 21.25 5.5 20.5 3.25 17.25Z")], "banana, fruit, groceries"),
    "bottle-wine": ([("s", "M9.75 2.75H14.25V7.25C16 8.25 17.25 9.75 17.25 12V21.25H6.75V12C6.75 9.75 8 8.25 9.75 7.25Z"), ("cut", "M6.75 13.25H17.25M6.75 17.25H17.25")], "wine bottle, drinks, alcohol"),
    "hamburger": ([("s", "M3.75 9.75C3.75 6 7.5 3.75 12 3.75C16.5 3.75 20.25 6 20.25 9.75Z"), ("o", "M2.75 13.25H21.25"), ("s", "M3.75 16.75H20.25V20.25H3.75Z")], "burger, fast food, takeaway"),
    "egg": ([("s", "M12 2.75C15.5 2.75 18.75 8.25 18.75 13.5C18.75 18 15.75 21.25 12 21.25C8.25 21.25 5.25 18 5.25 13.5C5.25 8.25 8.5 2.75 12 2.75Z")], "egg, breakfast, groceries"),
    "fish": ([("s", "M2.75 12C5.5 7.25 9 5.75 12.25 5.75C16.25 5.75 18.25 8.5 19.25 10L21.25 7.75V16.25L19.25 14C18.25 15.5 16.25 18.25 12.25 18.25C9 18.25 5.5 16.75 2.75 12Z"),
              ("d", circ(7.75, 10.75, 1)), ("cut", "M11 8.25C12 10.25 12 13.75 11 15.75")], "fish, seafood, groceries"),
})
EXP2.setdefault("📱 Devices", {}).update({
    "cctv": ([("s", poly([(2.75, 7.25), (16.75, 4.25), (18.25, 11.25), (4.25, 14.25)])), ("d", circ(14, 8.5, 1)), ("o", "M11.25 13L12.5 17.75H18.75M18.75 15V20.5")], "cctv, camera, surveillance"),
    "smartphone-charging": ([("s", "M6.75 2.75H17.25V21.25H6.75Z"), ("cut", "M12.75 6.75L10 12H14L11.25 17.25")], "charging, phone, battery"),
    "battery-charging": ([("s", "M2.75 7.25H18.75V16.75H2.75Z"), ("o", "M21.25 10V14"), ("cut", "M11.75 9L9.25 12.25H12.25L9.75 15")], "charging, battery, power"),
    "server": ([("s", "M2.75 3.25H21.25V10.25H2.75Z"), ("s", "M2.75 13.75H21.25V20.75H2.75Z"), ("d", circ(6.75, 6.75, 1)), ("d", circ(6.75, 17.25, 1)),
                ("cut", "M10.75 6.75H17.25M10.75 17.25H17.25")], "server, hosting, data"),
})
EXP2.setdefault("📄 File icons", {}).update({
    "files": ([FILE_BACK, ("s", "M3.75 5.75H11.75L16.25 10.25V21.25H3.75Z"), ("cut", "M11.75 5.75V10.25H16.25")], "files, documents, copies"),
})
EXP2.setdefault("📷 Photography", {}).update({
    "image-off": (find("image")[0] + SLASH, "no image, missing photo"),
})
EXP2.setdefault("📊 Charts", {}).update({
    "chart-column-increasing": ([AXES, ("o", "M7.75 17.25V14.25M12 17.25V10.25M16.25 17.25V6.25")], "chart, growth, sales"),
    "kanban": ([("s", "M2.75 2.75H7.25V17.25H2.75Z"), ("s", "M9.75 2.75H14.25V11.25H9.75Z"), ("s", "M16.75 2.75H21.25V21.25H16.75Z")], "kanban, board, order status"),
})
EXP2.setdefault("🎬 Multimedia", {}).update({
    "circle-play": ([("s", circ(12, 12, 9.25)), ("cut", "M10 8.25L15.75 12L10 15.75Z")], "play, video, product video"),
    "gallery-thumbnails": ([("s", "M2.75 2.75H21.25V15.25H2.75Z")] + [("s", f"M{x} 18.25H{n(float(x) + 3.5)}V21.25H{x}Z") for x in ("2.75", "7.6", "12.9", "17.75")], "gallery, thumbnails, product images"),
    "fullscreen": ([("o", "M2.75 7.75V2.75H7.75M16.25 2.75H21.25V7.75M21.25 16.25V21.25H16.25M7.75 21.25H2.75V16.25"), ("s", "M7.25 8.25H16.75V15.75H7.25Z")], "fullscreen, expand, zoom"),
    "picture-in-picture": ([("s", "M2.75 3.75H21.25V20.25H2.75Z"), ("cut", "M11.75 12.25H18.25V17.25H11.75V12.25")], "picture in picture, video"),
})
for page, items in EXP2.items():
    CATEGORIES[page].update(items)
EXP2_NAMES = [k for v in EXP2.values() for k in v]


# ---------------------------------------------------------------- expansion 3
TAG_ELEMS = [("s", TAG), TAG_HOLE]
BADGE_PLAN3 = {
    "🕒 Time & calendar": [("calendar", m) for m in ("search", "alert", "star", "lock")] + [("clock", m) for m in ("plus", "check", "x", "alert")],
    "👤 People": [("user", "clock"), ("user", "alert"), ("users", "plus"), ("users", "check"), ("users", "x")],
    "🧭 Navigation & places": [("home", m) for m in ("check", "heart", "search", "lock", "x")] + [("globe", "search"), ("globe", "x"),
                              ("map", "check"), ("map", "search"), ("map", "plus")],
    "📱 Devices": [("smartphone", m) for m in ("check", "lock", "x", "down")] + [("laptop", m) for m in ("check", "lock", "x")]
                  + [("monitor", m) for m in ("check", "x", "down")],
    "📷 Photography": [("image", m) for m in ("down", "up", "heart", "lock")] + [("camera", "plus"), ("camera", "x")],
    "🎬 Multimedia": [("video", m) for m in ("plus", "check", "x", "lock")],
    "🛍️ Shopping & commerce": [("tag", m) for m in ("check", "heart", "clock", "search", "lock")] + [("gift", "check"), ("gift", "clock"),
                                ("shopping-bag", "lock"), ("shopping-bag", "star"), ("shopping-cart", "heart"), ("shopping-cart", "alert")],
    "💳 Paymen & shipping": [("box", m) for m in ("clock", "heart", "lock")] + [("banknote", "up"), ("banknote", "down"),
                             ("wallet", "lock"), ("wallet", "clock"), ("receipt", "plus")],
    "💬 Communication": [("message-circle", m) for m in ("heart", "star", "lock", "clock")] + [("phone", "check"), ("phone", "clock")],
}
EXP3 = {}
_all = lambda: {k for v in CATEGORIES.values() for k in v}
for page, pairs in BADGE_PLAN3.items():
    for base, mod in pairs:
        nm = f"{base}-{mod}"
        if nm in _all() or nm in EXP3.get(page, {}):
            continue
        EXP3.setdefault(page, {})[nm] = badged(base, mod, TAG_ELEMS if base == "tag" else None)

_SR = find("sunrise")[0]
EXP3.setdefault("🌦️ Weather", {}).update({
    "cloudy": ([("o", "M11.25 8.25A5 5 0 0 1 20.25 10.5A3.25 3.25 0 0 1 18.75 16.75H16.75"),
                ("s", "M5.5 19.25A3 3 0 0 1 5.1 13.3A4.5 4.5 0 0 1 13.9 13.3A3 3 0 0 1 13.5 19.25Z")], "cloudy, overcast, weather"),
    "cloud-drizzle": ([("s", CLOUD_S), ("o", "M8 17.75V18.75M12 17.75V18.75M16 17.75V18.75M10 20.25V21.25M14 20.25V21.25")], "drizzle, light rain, weather"),
    "cloud-fog": ([("s", CLOUD_S), ("o", "M5.75 18.25H18.25M8.25 21.25H15.75")], "fog, mist, weather"),
    "rainbow": ([("o", arc(12, 18.25, 9.25, 180, 360)), ("o", arc(12, 18.25, 6, 180, 360)), ("o", arc(12, 18.25, 2.75, 180, 360))], "rainbow, pride, colourful"),
    "tornado": ([("o", "M3.25 4.75H20.75M5.25 9H18.25M7.75 13.25H16.25M10.25 17.5H15.25M12 21H14.25")], "tornado, storm, weather"),
    "sunset": ([("o", "M2.75 19.25H21.25M4.5 8.75L6.5 10.75M19.5 8.75L17.5 10.75M2.75 15.75H4.25M19.75 15.75H21.25"),
                ("o", "M12 2.75V8.25M9.75 6L12 8.25L14.25 6"), ("s", "M6.75 15.75A5.25 5.25 0 0 1 17.25 15.75Z")], "sunset, evening, dusk"),
    "droplets": ([("s", "M9.5 4.75L13.6 11.9A4.75 4.75 0 1 1 5.4 11.9Z"), ("s", "M17 2.75L19.17 6.5A2.5 2.5 0 1 1 14.83 6.5Z")], "droplets, water, humidity, liquid"),
})
_gc, _gw = (12, 8), (0.7071, 0.7071)
EXP3.setdefault("🔧 Tools", {}).update({
    "paint-bucket": ([("s", "M4.75 8.75H16.75L15.25 20.25H6.25Z"), ("o", "M6.5 8.75V7A4.25 4.25 0 0 1 15 7V8.75"), ("f", "M19.5 13.25L21 16.25A1.6 1.6 0 1 1 18 16.25Z")], "paint bucket, fill, colour"),
    "paint-roller": ([("s", "M3.75 2.75H18.25V7.75H3.75Z"), ("o", "M18.25 5.25H20.75V10.75H11.25V14.25"), ("s", "M9.75 14.25H12.75V21.25H9.75Z")], "paint roller, decorate, renovate"),
    "drill": ([("s", "M2.75 5.25H15.25V11.25H2.75Z"), ("s", "M6.25 11.25H11.25L10.25 20.75H5.25Z"), ("cut", "M6.25 11.25H11.25"), ("o", "M15.25 8.25H21.25")], "drill, diy, tools"),
    "stamp": ([("s", circ(12, 6, 3.25)), ("s", "M10.25 9.25H13.75V12.75H10.25Z"), ("s", "M3.75 12.75H20.25V17.25H3.75Z"), ("cut", "M3.75 12.75H20.25M10.25 9.25H13.75"), ("o", "M5.25 20.75H18.75")],
              "stamp, approved, certified"),
    "gavel": ([("s", poly([(16.77, 6.41), (13.59, 3.23), (7.23, 9.59), (10.41, 12.77)])), ("o", "M13.59 9.59L20.75 16.75M3.25 21.25H13.25")], "auction, legal, bid"),
    "pen": ([("s", "M15.25 3.75L20.25 8.75L9 20H4V15Z"), ("cut", "M13 6L18 11")], "pen, edit, write, sign"),
})
EXP3.setdefault("🎨 Design", {}).update({
    "spray-can": ([("s", "M6.75 9.25H15.25V21.25H6.75Z"), ("s", "M8.75 5.75H13.25V9.25H8.75Z"), ("cut", "M6.75 9.25H15.25M6.75 13.25H15.25"),
                   ("f", circ(17.75, 4.5, .9)), ("f", circ(20.25, 3, .9)), ("f", circ(20.25, 6.25, .9)), ("f", circ(17.75, 7.75, .9))], "spray paint, graffiti, colour"),
    "eraser": ([("s", poly([(13.5, 3.25), (20.75, 10.5), (11.25, 20), (8, 20), (3.25, 15.25)])), ("cut", "M7.75 10.75L13.25 16.25"), ("o", "M11.25 20H20.75")], "eraser, clear, delete"),
})
EXP3.setdefault("🌐 Social", {}).update({
    "sticker": ([("s", "M2.75 2.75H21.25V12.75L12.75 21.25H2.75Z"), ("cut", "M21.25 12.75H12.75V21.25"), ("d", circ(8, 8, 1)), ("d", circ(13, 8, 1))], "sticker, label, fun"),
    "party-popper": ([("s", poly([(2.75, 21.25), (6.75, 9.75), (14.25, 17.25)])), ("o", "M10.5 3.25V5.25M18.75 13.5H20.75M13.5 8.25L16.5 5.25"),
                      ("f", circ(19.75, 9, 1)), ("f", circ(15.25, 2.75 + 0.75, 1))], "celebrate, party, order placed, success"),
    "quote": ([("s", "M3.75 6.75H10.25V13.25L7.25 19.25H4.75L6.75 13.25H3.75Z"), ("s", "M13.75 6.75H20.25V13.25L17.25 19.25H14.75L16.75 13.25H13.75Z")], "quote, testimonial, review"),
})
EXP3.setdefault("🛡️ Security", {}).update({
    "lock-keyhole": ([("s", "M4.75 10.25H19.25V21.25H4.75Z"), ("o", "M7.75 10.25V7A4.25 4.25 0 0 1 16.25 7V10.25"), ("cut", circ(12, 14.5, 1.5)), ("cut", "M12 16V18.25")],
                     "lock, secure, password"),
    "key-round": ([("s", circ(15.5, 8.5, 5.75)), ("d", circ(17, 7, 1.25)), ("o", "M11.5 12.5L3.25 20.75M6.5 17.5L8.75 19.75")], "key, access, login"),
    "shield-half": ([("s", SHIELD), ("d", "M12 2.75L3.75 5.75V11.75C3.75 16.25 7.25 19.5 12 21.25Z")], "partial protection, privacy"),
})
EXP3.setdefault("🕒 Time & calendar", {}).update({
    "calendar-day": (CAL + [("cut", "M10.25 14.25L12 12.75V18.75")], "today, date, day"),
    "timer-off": (find("timer")[0] + SLASH, "timer off, no limit"),
})
EXP3.setdefault("🔔 Notifications", {}).update({
    "vibrate": ([("s", "M8.25 5.25H15.75V18.75H8.25Z"), ("o", "M5.25 8.25V15.75M2.75 9.75V14.25M18.75 8.25V15.75M21.25 9.75V14.25")], "vibrate, silent, haptic"),
    "alarm-clock-off": (find("alarm-clock")[0] + SLASH, "alarm off, snooze"),
})
for page, items in EXP3.items():
    CATEGORIES[page].update(items)
EXP3_NAMES = [k for v in EXP3.values() for k in v]


# ---------------------------------------------------------------- expansion 4: new categories
FR = ("s", "M2.75 3.75H21.25V20.25H2.75Z")
SQF = ("s", "M2.75 2.75H21.25V21.25H2.75Z")


def football():
    out = [("s", circ(12, 12, 9.25)), ("cut", regular(12, 12, 3.75, 5))]
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        out.append(("cut", f"M{n(12 + 3.75 * math.cos(a))} {n(12 + 3.75 * math.sin(a))}L{n(12 + 9.25 * math.cos(a))} {n(12 + 9.25 * math.sin(a))}"))
    return out


EXP4 = {
    "📐 Layout": {
        "panel-left": ([FR, ("cut", "M8.75 3.75V20.25")], "sidebar, panel, layout"),
        "panel-right": ([FR, ("cut", "M15.25 3.75V20.25")], "sidebar, panel, layout"),
        "panel-top": ([FR, ("cut", "M2.75 9.25H21.25")], "header, panel, layout"),
        "panel-bottom": ([FR, ("cut", "M2.75 14.75H21.25")], "footer, panel, layout"),
        "panel-left-close": ([FR, ("cut", "M8.75 3.75V20.25M15.75 9.25L13 12L15.75 14.75")], "collapse sidebar, layout"),
        "panel-left-open": ([FR, ("cut", "M8.75 3.75V20.25M13 9.25L15.75 12L13 14.75")], "expand sidebar, layout"),
        "columns-2": ([FR, ("cut", "M12 3.75V20.25")], "columns, split, layout"),
        "columns-3": ([FR, ("cut", "M8.92 3.75V20.25M15.08 3.75V20.25")], "columns, layout"),
        "rows-2": ([FR, ("cut", "M2.75 12H21.25")], "rows, split, layout"),
        "rows-3": ([FR, ("cut", "M2.75 9.25H21.25M2.75 14.75H21.25")], "rows, layout"),
        "layout-dashboard": ([FR, ("cut", "M9.75 3.75V20.25M9.75 12H21.25")], "dashboard, admin, layout"),
        "layout-template": ([FR, ("cut", "M2.75 9.25H21.25M12 9.25V20.25M12 14.75H21.25")], "template, bento, layout"),
        "app-window": ([FR, ("cut", "M2.75 8.25H21.25"), ("d", circ(5.75, 6, .9)), ("d", circ(8.75, 6, .9))], "browser, window, web"),
        "table": ([FR, ("cut", "M2.75 9H21.25M2.75 14.5H21.25M9.25 9V20.25")], "table, data, spreadsheet"),
        "grid-3x3": ([SQF, ("cut", "M8.92 2.75V21.25M15.08 2.75V21.25M2.75 8.92H21.25M2.75 15.08H21.25")], "grid, gallery, product grid"),
        "layout-list": ([("s", "M2.75 3.75H8.25V9.25H2.75Z"), ("s", "M2.75 14.75H8.25V20.25H2.75Z"), ("o", "M11.25 5.25H21.25M11.25 8H17.25M11.25 16.25H21.25M11.25 19H17.25")], "list view, products, layout"),
        "gallery-vertical": ([("s", "M2.75 7.25H21.25V16.75H2.75Z"), ("o", "M2.75 3.25H21.25M2.75 20.75H21.25")], "gallery, scroll, feed"),
        "gallery-horizontal": ([("s", "M7.25 2.75H16.75V21.25H7.25Z"), ("o", "M3.25 5.25V18.75M20.75 5.25V18.75")], "gallery, swipe, stories"),
        "carousel": ([("s", "M6.25 3.75H17.75V16.75H6.25Z"), ("o", "M2.75 6.25V14.25M21.25 6.25V14.25"), ("f", circ(9, 20.5, 1)), ("f", circ(12, 20.5, 1)), ("f", circ(15, 20.5, 1))], "carousel, slider, banner"),
        "product-cards": ([("s", "M2.75 2.75H10.75V21.25H2.75Z"), ("s", "M13.25 2.75H21.25V21.25H13.25Z"), ("cut", "M2.75 14.25H10.75M13.25 14.25H21.25")], "product cards, catalogue, plp"),
        "masonry": ([("s", "M2.75 2.75H10.75V12.75H2.75Z"), ("s", "M2.75 15.25H10.75V21.25H2.75Z"), ("s", "M13.25 2.75H21.25V8.75H13.25Z"), ("s", "M13.25 11.25H21.25V21.25H13.25Z")], "masonry, lookbook, pinterest"),
    },
    "🔠 Text formatting": {
        "bold": ([("o", "M6.75 3.75H13.25A3.75 3.75 0 0 1 13.25 11.25H6.75V3.75M6.75 11.25H14.25A4.5 4.5 0 0 1 14.25 20.25H6.75V11.25")], "bold, text, format"),
        "italic": ([("o", "M10.25 3.75H18.25M5.75 20.25H13.75M14.25 3.75L9.75 20.25")], "italic, text, format"),
        "underline": ([("o", "M6.75 3.75V11.25A5.25 5.25 0 0 0 17.25 11.25V3.75M4.75 20.75H19.25")], "underline, text, format"),
        "strikethrough": ([("o", "M16.75 5.25C15.75 4 14 3.25 12 3.25C9 3.25 7 4.75 7 7C7 9.25 9 10.25 12 11M4.75 12H19.25M7.25 17.75C8.25 19.5 10 20.75 12.25 20.75C15.25 20.75 17.25 19.25 17.25 16.75C17.25 15.5 16.75 14.5 15.75 13.75")], "strikethrough, old price, format"),
        "heading": ([("o", "M5.75 3.75V20.25M18.25 3.75V20.25M5.75 12H18.25")], "heading, title, text"),
        "heading-1": ([("o", "M3.75 4.75V19.25M13.25 4.75V19.25M3.75 12H13.25M17.25 9.75L19.75 7.75V19.25")], "heading 1, h1, text"),
        "heading-2": ([("o", "M3.75 4.75V19.25M13.25 4.75V19.25M3.75 12H13.25M16.75 8.75H21.25V13.75H16.75V19.25H21.25")], "heading 2, h2, text"),
        "align-left": ([("o", "M3.75 5.25H20.25M3.75 10H14.25M3.75 14.75H20.25M3.75 19.5H14.25")], "align left, text"),
        "align-center": ([("o", "M3.75 5.25H20.25M6.75 10H17.25M3.75 14.75H20.25M6.75 19.5H17.25")], "align center, text"),
        "align-right": ([("o", "M3.75 5.25H20.25M9.75 10H20.25M3.75 14.75H20.25M9.75 19.5H20.25")], "align right, text"),
        "align-justify": ([("o", "M3.75 5.25H20.25M3.75 10H20.25M3.75 14.75H20.25M3.75 19.5H20.25")], "justify, text"),
        "indent-increase": ([("o", "M3.75 5.25H20.25M11.25 10H20.25M11.25 14.75H20.25M3.75 19.5H20.25M3.75 9.5L6.75 12.25L3.75 15")], "indent, text"),
        "indent-decrease": ([("o", "M3.75 5.25H20.25M11.25 10H20.25M11.25 14.75H20.25M3.75 19.5H20.25M6.75 9.5L3.75 12.25L6.75 15")], "outdent, text"),
        "subscript": ([("o", "M3.75 5.25L12.25 15.75M12.25 5.25L3.75 15.75M16.75 14.75H20.75V17.5H16.75V20.25H20.75")], "subscript, text"),
        "superscript": ([("o", "M3.75 8.25L12.25 18.75M12.25 8.25L3.75 18.75M16.75 3.75H20.75V6.5H16.75V9.25H20.75")], "superscript, text"),
        "pilcrow": ([("o", "M12.75 3.75V20.25M16.75 3.75V20.25M19.25 3.75H10.25A4.25 4.25 0 0 0 10.25 12.25H12.75")], "paragraph, pilcrow, text"),
        "code": ([("o", "M8.25 6.75L3.25 12L8.25 17.25M15.75 6.75L20.75 12L15.75 17.25M13.75 4.25L10.25 19.75")], "code, html, embed"),
        "remove-formatting": ([("o", "M4.75 4.75H18.25M11.5 4.75L7.75 20.25M13.75 14.75L19.75 20.75M19.75 14.75L13.75 20.75")], "clear formatting, text"),
        "highlighter": ([("s", poly([(15.25, 3.25), (20.75, 8.75), (12.75, 16.75), (7.25, 11.25)])), ("s", poly([(7.25, 11.25), (12.75, 16.75), (9.25, 20.25), (3.75, 20.25), (3.75, 14.75)])),
                         ("cut", "M7.25 11.25L12.75 16.75")], "highlight, marker, text"),
        "text-color": ([("o", "M6.25 15.25L12 3.25L17.75 15.25M8.25 11H15.75"), ("s", "M2.75 18.25H21.25V21.25H2.75Z")], "text colour, font colour"),
        "wrap-text": ([("o", "M3.75 5.25H20.25M3.75 12H17.25A3.25 3.25 0 0 1 17.25 18.5H12.75M15.25 16L12.75 18.5L15.25 21M3.75 18.75H8.75")], "wrap text, text"),
    },
    "✈️ Travel": {
        "hotel": ([("s", "M3.75 2.75H20.25V21.25H3.75Z"), ("cut", "M7.75 7H9.75M14.25 7H16.25M7.75 11.25H9.75M14.25 11.25H16.25M10 21.25V16.25H14V21.25")], "hotel, stay, booking"),
        "concierge-bell": ([("s", "M3.75 16.75A8.25 8.25 0 0 1 20.25 16.75Z"), ("o", "M2.75 20.25H21.25M12 5.75V8.5M9.75 5.75H14.25")], "service, reception, concierge"),
        "passport": ([("s", "M4.75 2.75H19.25V21.25H4.75Z"), ("cut", ring(12, 10.25, 3.5)), ("cut", "M8.75 17.25H15.25")], "passport, id, travel"),
        "boarding-pass": ([("s", COUPON), ("cut", "M15 5.75V18.25M6.25 10.25H11.25M6.25 13.75H9.75")], "boarding pass, ticket, flight"),
        "suitcase-rolling": ([("s", "M6.25 6.75H17.75V18.25H6.25Z"), ("o", "M9.75 6.75V2.75H14.25V6.75"), ("f", circ(8.5, 20.5, 1.25)), ("f", circ(15.5, 20.5, 1.25)),
                              ("cut", "M10 9.75V15.25M14 9.75V15.25")], "suitcase, luggage, travel"),
        "baggage-claim": ([("o", "M2.75 17.25H17.25L21.25 13.25"), ("s", "M6.25 8.75H14.25V14.25H6.25Z"), ("o", "M8.75 8.75V6.25H11.75V8.75"), ("f", circ(6.75, 20.5, 1.25)), ("f", circ(13.75, 20.5, 1.25))],
                          "baggage claim, airport, luggage"),
        "tent": ([("s", poly([(12, 3.25), (21.25, 20.25), (2.75, 20.25)])), ("cut", "M12 12.5L15.5 20.25H8.5Z")], "tent, camping, outdoor"),
        "mountain": ([("s", poly([(2.75, 20.25), (9.25, 7.75), (13.25, 13.25), (16, 9.75), (21.25, 20.25)]))], "mountain, outdoor, hiking"),
        "parasol": ([("s", "M2.75 11.25A9.25 9.25 0 0 1 21.25 11.25Z"), ("o", "M12 11.25L14.75 21.25M3.25 21.25H20.75")], "beach, summer, holiday, swimwear"),
        "sailboat": ([("s", poly([(11.25, 2.75), (11.25, 15.25), (4.25, 15.25)])), ("s", poly([(13.25, 5.25), (13.25, 15.25), (19.25, 15.25)])), ("s", "M2.75 17.25H21.25L19.25 20.75H4.75Z")], "sailing, boat, holiday"),
        "languages": ([("o", "M2.75 5.25H12.75M7.75 3.25V5.25M10.75 5.25C10 9.75 7.25 13.25 3.25 15.25M5.75 9.25C7.25 11.75 9.25 13.25 11.25 14"),
                       ("o", "M12.75 20.75L16.75 10.75L20.75 20.75M14.25 17.25H19.25")], "language, translate, locale"),
        "id-card-lanyard": ([("s", "M5.25 7.25H18.75V21.25H5.25Z"), ("o", "M9.25 2.75L12 7.25L14.75 2.75"), ("cut", ring(12, 12.25, 2)), ("cut", "M8.75 17.75H15.25")], "badge, pass, event, staff"),
    },
    "⚽ Sports": {
        "dumbbell": ([("s", "M4.75 6.75H8.25V17.25H4.75Z"), ("s", "M15.75 6.75H19.25V17.25H15.75Z"), ("o", "M8.25 12H15.75M2.75 9.25V14.75M21.25 9.25V14.75")], "gym, fitness, training"),
        "kettlebell": ([("s", "M6.25 9.75H17.75L19.25 15C19.25 18.5 16 21.25 12 21.25C8 21.25 4.75 18.5 4.75 15Z"), ("o", "M8.25 9.75V6.25A3.75 3.75 0 0 1 15.75 6.25V9.75")], "kettlebell, fitness, gym"),
        "trophy": ([("s", "M6.75 2.75H17.25V9.5A5.25 5.25 0 0 1 6.75 9.5Z"), ("o", "M6.75 4.75H3.25V7C3.25 9 4.75 10.5 6.75 10.75M17.25 4.75H20.75V7C20.75 9 19.25 10.5 17.25 10.75M12 14.75V19.25"),
                    ("s", "M7.75 19.25H16.25V21.25H7.75Z")], "trophy, winner, best seller"),
        "medal": ([("s", circ(12, 15, 6.25)), ("o", "M8 10.25L4.75 2.75M16 10.25L19.25 2.75"), ("cut", star(12, 15.25, 3.25, 1.4, 5))], "medal, award, top rated"),
        "target": ([("s", circ(12, 12, 9.25)), ("cut", ring(12, 12, 5.5)), ("cut", ring(12, 12, 2))], "target, goal, aim"),
        "basketball": ([("s", circ(12, 12, 9.25)), ("cut", "M2.75 12H21.25M12 2.75V21.25M5.5 5.5C8 8 8 16 5.5 18.5M18.5 5.5C16 8 16 16 18.5 18.5")], "basketball, sport, ball"),
        "tennis-ball": ([("s", circ(12, 12, 9.25)), ("cut", "M5.5 5.5C9 8 9 16 5.5 18.5M18.5 5.5C15 8 15 16 18.5 18.5")], "tennis, padel, ball"),
        "football": (football(), "football, soccer, ball"),
        "jersey": ([("s", "M7.75 2.75H9.75C10 4.5 10.75 5.25 12 5.25C13.25 5.25 14 4.5 14.25 2.75H16.25L17.25 7.75L19.25 8.75V21.25H4.75V8.75L6.75 7.75Z"),
                    ("cut", "M10.25 10.25H13.75V12.75H10.25V15.25H13.75")], "jersey, sportswear, team kit"),
        "skateboard": ([("s", "M3.75 12.25H20.25L18.75 14.25H5.25Z"), ("f", circ(7.25, 17.75, 1.75)), ("f", circ(16.75, 17.75, 1.75))], "skateboard, street, sport"),
        "racket": ([("s", circ(14.25, 9.75, 7)), ("cut", "M14.25 2.75V16.75M7.25 9.75H21.25"), ("o", "M9.25 14.75L3.25 20.75")], "tennis, padel, racket"),
        "golf": ([("o", "M6.75 21.25V2.75M3.25 21.25H13.25"), ("s", "M6.75 2.75L17.25 6.5L6.75 10.25Z")], "golf, flag, goal"),
        "heart-pulse": ([("s", HEART), ("cut", "M5.25 11.25H8.75L10.25 8.75L12.75 13.75L14.25 11.25H18.75")], "heart rate, fitness, health"),
    },
}
for page, items in EXP4.items():
    CATEGORIES[page] = dict(items)
BADGE_PLAN4 = {
    "💳 Paymen & shipping": [("receipt", "down")],
    "👤 People": [("id-card", "check")],
    "🔔 Notifications": [("bell", "alert")],
    "✈️ Travel": [("hotel", "check")],
    "🛍️ Shopping & commerce": [("coupon", "plus"), ("gift", "plus"), ("gift", "heart"), ("store", "plus"), ("star", "check"), ("star", "plus"), ("star", "x")],
    "🚗 Transportation": [("warehouse", "check"), ("warehouse", "x"), ("warehouse", "search")],
    "📱 Devices": [("laptop", "down")],
}
EXP4B = {}
for page, pairs in BADGE_PLAN4.items():
    for base, mod in pairs:
        nm = f"{base}-{mod}"
        if nm not in _all():
            EXP4B.setdefault(page, {})[nm] = badged(base, mod)
for page, items in EXP4B.items():
    CATEGORIES[page].update(items)
EXP4_NAMES = [k for v in EXP4.values() for k in v] + [k for v in EXP4B.values() for k in v]


_SP = CATEGORIES["⚽ Sports"]
_SP["racket"] = ([("s", circ(14.25, 9.75, 7)), ("cut", "M11 3.5V16M14.25 2.75V16.75M17.5 3.5V16M7.75 6.5H20.75M7.25 9.75H21.25M7.75 13H20.75"), ("o", "M9.25 14.75L3.25 20.75")], _SP["racket"][1])
_SP["football"] = ([("s", circ(12, 12, 9.25)), ("d", regular(12, 12, 3.75, 5))] + football()[2:], _SP["football"][1])


def football2():
    P = lambda r, a: (12 + r * math.cos(math.radians(a)), 12 + r * math.sin(math.radians(a)))
    out = [("s", circ(12, 12, 9.25)), ("d", regular(12, 12, 3.5, 5))]
    for i in range(5):
        a = -90 + 72 * i
        r0, r1, r2, r3, r4 = P(9.25, a - 22), P(7.25, a - 18), P(6.25, a), P(7.25, a + 18), P(9.25, a + 22)
        out.append(("d", f"M{n(r0[0])} {n(r0[1])}L{n(r1[0])} {n(r1[1])}L{n(r2[0])} {n(r2[1])}L{n(r3[0])} {n(r3[1])}L{n(r4[0])} {n(r4[1])}A9.25 9.25 0 0 0 {n(r0[0])} {n(r0[1])}Z"))
        v, w = P(3.5, a), P(6.25, a)
        out.append(("cut", f"M{n(v[0])} {n(v[1])}L{n(w[0])} {n(w[1])}"))
    return out


_SP["racket"] = ([("s", circ(14.25, 9.75, 7)), ("cut", "M12 3.25V16.25M16.5 3.25V16.25M7.75 7.5H20.75M7.75 12H20.75"), ("o", "M9.25 14.75L3.25 20.75")], _SP["racket"][1])
_SP["football"] = (football2(), _SP["football"][1])


# ---------------------------------------------------------------- expansion 5
def rot_path(d, ang, cx=12, cy=12):
    """Rotate an absolute M/L/A/C/Z path (degrees, clockwise on screen)."""
    t = math.radians(ang); c, s = math.cos(t), math.sin(t)
    R = lambda x, y: (cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)
    out = []
    for cmd, args in re.findall(r"([MLACZ])([^MLACZ]*)", d):
        v = [float(x) for x in re.findall(r"-?[\d.]+", args)]
        if cmd in "ML":
            pts = [R(v[i], v[i + 1]) for i in range(0, len(v), 2)]
            out.append(cmd + "L".join(f"{n(x)} {n(y)}" for x, y in pts))
        elif cmd == "C":
            pts = [R(v[i], v[i + 1]) for i in range(0, len(v), 2)]
            out.append("C" + " ".join(f"{n(x)} {n(y)}" for x, y in pts))
        elif cmd == "A":
            x, y = R(v[5], v[6])
            out.append(f"A{n(v[0])} {n(v[1])} {n(v[2] + ang)} {int(v[3])} {int(v[4])} {n(x)} {n(y)}")
        else:
            out.append("Z")
    return "".join(out)


def scallop(cx, cy, ri, k, rp, rot=-90):
    pts = [(cx + ri * math.cos(math.radians(rot + 360 * i / k + 180 / k)), cy + ri * math.sin(math.radians(rot + 360 * i / k + 180 / k))) for i in range(k)]
    d = f"M{n(pts[0][0])} {n(pts[0][1])}"
    for i in range(1, k + 1):
        x, y = pts[i % k]
        d += f"A{n(rp)} {n(rp)} 0 1 0 {n(x)} {n(y)}"
    return d + "Z"


def ellipse(cx, cy, rx, ry, ang):
    t = math.radians(ang)
    x1, y1 = cx + rx * math.cos(t), cy + rx * math.sin(t)
    x2, y2 = cx - rx * math.cos(t), cy - rx * math.sin(t)
    return f"M{n(x1)} {n(y1)}A{n(rx)} {n(ry)} {n(ang)} 1 1 {n(x2)} {n(y2)}A{n(rx)} {n(ry)} {n(ang)} 1 1 {n(x1)} {n(y1)}Z"


CAPSULE = "M8.5 8.5L15.5 8.5A3.5 3.5 0 0 1 15.5 15.5L8.5 15.5A3.5 3.5 0 0 1 8.5 8.5Z"
BANDAGE = "M6.75 8.75L17.25 8.75A3.25 3.25 0 0 1 17.25 15.25L6.75 15.25A3.25 3.25 0 0 1 6.75 8.75Z"
BONE = "M7.54 10.75L16.46 10.75A2.5 2.5 0 1 1 19.84 12A2.5 2.5 0 1 1 16.46 13.25L7.54 13.25A2.5 2.5 0 1 1 4.16 12A2.5 2.5 0 1 1 7.54 10.75Z"

EXP5 = {
    "💊 Medical": {
        "pill": ([("s", rot_path(CAPSULE, -45)), ("cut", rot_path("M12 8.5L12 15.5", -45))], "pill, capsule, medicine, supplement"),
        "pill-bottle": ([("s", "M5.75 8.25H18.25V21.25H5.75Z"), ("s", "M4.75 2.75H19.25V8.25H4.75Z"), ("cut", "M4.75 8.25H19.25M12 11.75V17.75M9 14.75H15")], "pharmacy, vitamins, medicine"),
        "syringe": ([("s", rot_path("M6.25 9.5L16.25 9.5L16.25 14.5L6.25 14.5Z", -45)), ("o", rot_path("M16.25 12L19.75 12M19.75 9.75L19.75 14.25M6.25 12L2.25 12", -45)),
                     ("cut", rot_path("M9.25 9.5L9.25 11.5M12.25 9.5L12.25 11.5", -45))], "syringe, vaccine, injection"),
        "stethoscope": ([("o", "M5.75 2.75H4.75V8.25A5 5 0 0 0 14.75 8.25V2.75H13.75M9.75 13.25V15.75A4.5 4.5 0 0 0 18.75 15.75V13.75"), ("s", circ(18.75, 11.25, 2.25))], "doctor, health, checkup"),
        "bandage": ([("s", rot_path(BANDAGE, 45)), ("cut", rot_path("M9.25 8.75L9.25 15.25M14.75 8.75L14.75 15.25", 45)), ("d", circ(11, 12, .8)), ("d", circ(13, 12, .8))], "plaster, first aid, bandage"),
        "first-aid-kit": ([("s", "M2.75 6.75H21.25V20.25H2.75Z"), ("o", "M8.25 6.75V3.25H15.75V6.75"), ("cut", "M12 10V17M8.5 13.5H15.5")], "first aid, emergency, health"),
        "hospital": ([("s", "M3.75 2.75H20.25V21.25H3.75Z"), ("cut", "M12 6V12M9 9H15M10 21.25V16.25H14V21.25")], "hospital, clinic, health"),
        "tooth": ([("s", "M12 5.25C10.25 3.75 7.75 3 6 3.75C3.75 4.75 3.25 7.5 4 10C4.75 12.5 5.75 14.75 6.25 17.75C6.5 19.75 7 21.25 8.25 21.25C9.75 21.25 10 18.75 10.5 17C10.75 16 11.25 15.25 12 15.25C12.75 15.25 13.25 16 13.5 17C14 18.75 14.25 21.25 15.75 21.25C17 21.25 17.5 19.75 17.75 17.75C18.25 14.75 19.25 12.5 20 10C20.75 7.5 20.25 4.75 18 3.75C16.25 3 13.75 3.75 12 5.25Z")],
                  "tooth, dental, oral care"),
        "face-mask": ([("s", "M4.75 7.75C8.5 6.25 15.5 6.25 19.25 7.75V14.25C17.5 17.75 14.5 19.25 12 19.25C9.5 19.25 6.5 17.75 4.75 14.25Z"),
                       ("o", "M4.75 9.75C3 9.75 2.75 10.75 2.75 11.5C2.75 12.75 3.5 13.5 5.25 13.5M19.25 9.75C21 9.75 21.25 10.75 21.25 11.5C21.25 12.75 20.5 13.5 18.75 13.5"),
                       ("cut", "M7.75 10.75H16.25M8.25 14H15.75")], "face mask, protection, health"),
        "weight-scale": ([("s", "M3.75 3.75H20.25V20.25H3.75Z"), ("cut", "M7.25 10.25A4.75 4.75 0 0 1 16.75 10.25H7.25M12 10.25L13.75 7.25")], "scale, weight, bathroom"),
    },
    "💄 Beauty & care": {
        "lipstick": ([("s", "M7.75 12.25H16.25V21.25H7.75Z"), ("s", "M9.25 12.25V6.25L14.75 2.75V12.25Z"), ("cut", "M7.75 15.25H16.25M7.75 12.25H16.25")], "lipstick, makeup, cosmetics"),
        "nail-polish": ([("s", "M6.75 11.25H17.25V21.25H6.75Z"), ("s", "M9.75 2.75H14.25V11.25H9.75Z"), ("cut", "M6.75 11.25H17.25")], "nail polish, manicure, beauty"),
        "comb": ([("s", "M2.75 6.75H21.25V10.75H2.75Z"), ("o", "M4.75 10.75V17.25M8 10.75V17.25M11.25 10.75V17.25M14.5 10.75V17.25M17.75 10.75V17.25")], "comb, hair, grooming"),
        "hair-dryer": ([("s", "M2.75 4.75H13.25A4.75 4.75 0 0 1 13.25 14.25H2.75Z"), ("s", "M8.75 14.25H13.25L12.25 21.25H8.75Z"), ("cut", "M8.75 14.25H13.25"), ("d", circ(13.25, 9.5, 1.25)),
                        ("o", "M19.75 6.75H21.25M19.75 9.5H21.25M19.75 12.25H21.25")], "hair dryer, hair care, styling"),
        "razor": ([("s", "M3.25 3.75H20.75V8.25H3.25Z"), ("cut", "M3.25 6H20.75"), ("s", "M10.25 8.25H13.75V21.25H10.25Z")], "razor, shaving, grooming"),
        "makeup-brush": ([("o", "M3.25 20.75L7.75 16.25"), ("s", "M9.25 12L14.75 6.5C16.75 4.5 19.75 3 21.25 2.75C21 4.25 19.5 7.25 17.5 9.25L12 14.75Z"), ("s", poly([(9.25, 12), (12, 14.75), (9.5, 17.25), (6.75, 14.5)])),
                          ("cut", "M9.25 12L12 14.75")], "makeup brush, cosmetics, beauty"),
        "compact": ([("s", "M2.75 14.25H21.25V16.25A5 5 0 0 1 16.25 21.25H7.75A5 5 0 0 1 2.75 16.25Z"), ("s", "M2.75 11.25V9.25A6.5 6.5 0 0 1 9.25 2.75H14.75A6.5 6.5 0 0 1 21.25 9.25V11.25Z")], "powder, compact, makeup"),
        "soap": ([("s", "M3.75 12.25H18.25V20.25H3.75Z"), ("o", circ(16.75, 6.75, 2.75)), ("o", circ(10.25, 6.75, 1.75))], "soap, wash, hygiene"),
        "spray-bottle": ([("s", "M7.25 9.25H15.75V21.25H7.25Z"), ("s", "M8.75 4.75H14.75V9.25H8.75Z"), ("o", "M14.75 2.75H8.75V4.75M14.75 6.25H18.25"), ("cut", "M7.25 9.25H15.75M7.25 13.25H15.75")], "spray, mist, toner"),
        "cream-jar": ([("s", "M3.75 4.75H20.25V9.25H3.75Z"), ("s", "M4.75 9.25H19.25V19.25H4.75Z"), ("cut", "M3.75 9.25H20.25M8.75 13.25H15.25")], "cream, moisturiser, skincare"),
    },
    "🌿 Nature": {
        "flower": ([("s", scallop(12, 9, 3.25, 5, 2.4)), ("cut", circ(12, 9, 1.5)), ("o", "M12 14.75V21.25M12 18.5C10.5 17 8.5 16.5 6.75 16.75")], "flower, bloom, spring, gift"),
        "tree-deciduous": ([("s", circ(12, 8.75, 6)), ("o", "M12 14.75V21.25M8.75 21.25H15.25"), ("cut", "M12 9.5V14.75M12 12L14.25 9.75")], "tree, nature, park"),
        "clover": ([("s", scallop(12, 10, 3, 4, 3.3, -45)), ("o", "M12 14.5L13.5 21.25")], "clover, luck, nature"),
        "feather": ([("s", "M20.75 3.25C14 3.25 7.75 7.5 6.25 14.25L5.25 18.75L9.75 17.75C16.5 16.25 20.75 10 20.75 3.25Z"), ("cut", "M7.75 16.25L14.75 9.25"), ("o", "M3.25 20.75L5.75 18.25")], "feather, light, soft"),
        "waves": ([("o", "M2.75 7.75C5 6 7 6 9.25 7.75C11.5 9.5 13.5 9.5 15.75 7.75C18 6 20 6 21.25 7.25M2.75 12.5C5 10.75 7 10.75 9.25 12.5C11.5 14.25 13.5 14.25 15.75 12.5C18 10.75 20 10.75 21.25 12M2.75 17.25C5 15.5 7 15.5 9.25 17.25C11.5 19 13.5 19 15.75 17.25C18 15.5 20 15.5 21.25 16.75")], "waves, water, sea"),
        "cactus": ([("s", "M9.75 21.25V5.25A2.25 2.25 0 0 1 14.25 5.25V21.25Z"), ("o", "M9.75 13.25H7.25A2 2 0 0 1 5.25 11.25V8.75M14.25 11.25H16.75A2 2 0 0 0 18.75 9.25V6.75M6.75 21.25H17.25")], "cactus, plant, desert"),
        "trees": ([("s", poly([(8, 3.25), (13, 13.25), (3, 13.25)])), ("s", poly([(16, 6.25), (21, 16.25), (11, 16.25)])), ("o", "M8 13.25V21.25M16 16.25V21.25")], "forest, trees, nature"),
    },
    "🐾 Animals": {
        "paw-print": ([("s", "M12 11.25C9 11.25 6.75 14.5 6.75 17C6.75 19.5 9 20.25 12 19.25C15 20.25 17.25 19.5 17.25 17C17.25 14.5 15 11.25 12 11.25Z"),
                       ("s", circ(5.25, 10.25, 1.75)), ("s", circ(9.25, 5.75, 1.75)), ("s", circ(14.75, 5.75, 1.75)), ("s", circ(18.75, 10.25, 1.75))], "pet, paw, pet supplies"),
        "bone": ([("s", rot_path(BONE, -45))], "bone, dog treat, pet"),
        "dog": ([("s", "M6.25 7.75H17.75V15.25C17.75 18.5 15.25 20.75 12 20.75C8.75 20.75 6.25 18.5 6.25 15.25Z"), ("s", "M6.25 6.75L2.75 4.25V12.75L6.25 11.25"), ("s", "M17.75 6.75L21.25 4.25V12.75L17.75 11.25"),
                 ("d", circ(9.5, 11, 1)), ("d", circ(14.5, 11, 1)), ("d", "M10.75 14.75H13.25L12 16.25Z")], "dog, pet, puppy"),
        "cat": ([("s", "M4.75 9.75L4.25 3.25L9.25 6.75H14.75L19.75 3.25L19.25 9.75V14.25C19.25 18.25 16 21.25 12 21.25C8 21.25 4.75 18.25 4.75 14.25Z"),
                 ("d", circ(9, 12.25, 1)), ("d", circ(15, 12.25, 1)), ("d", "M10.75 15.25H13.25L12 16.75Z")], "cat, pet, kitten"),
        "bird": ([("s", "M3.25 13.75C3.25 9.5 6.5 6.25 10.75 6.25C11 4.25 12.75 2.75 14.75 2.75C17 2.75 18.75 4.5 18.75 6.75L21.25 8.25L18.75 9.75C18.75 15.75 14.5 19.25 9.25 19.25L6.25 21.25V18.5C4.25 17.5 3.25 15.75 3.25 13.75Z"),
                  ("d", circ(15, 6, 1)), ("cut", "M7.25 13.25C9.5 13.25 12.25 12 13.25 9.75")], "bird, pet, nature"),
        "rabbit": ([("s", "M7.75 10V5A2 2 0 0 1 11.75 5V9.25"), ("s", "M12.25 9.25V5A2 2 0 0 1 16.25 5V10"), ("s", circ(12, 15.25, 6)), ("k", circ(12, 15.25, 7.5)),
                    ("d", circ(9.75, 14.5, 1)), ("d", circ(14.25, 14.5, 1))], "rabbit, bunny, pet, easter"),
        "pet-bowl": ([("s", "M2.75 13.25H21.25L19.25 20.25H4.75Z"), ("o", "M5.75 13.25C6.5 10.75 9 9.25 12 9.25C15 9.25 17.5 10.75 18.25 13.25")], "pet food, bowl, pet supplies"),
        "bug": ([("s", "M7.75 9.25H16.25V14.25A4.25 4.25 0 0 1 7.75 14.25Z"), ("s", "M9.25 9.25A2.75 2.75 0 0 1 14.75 9.25"), ("cut", "M7.75 9.25H16.25M12 9.25V18.5"),
                 ("o", "M7.75 11.25H3.75M7.75 15L4.25 17.5M16.25 11.25H20.25M16.25 15L19.75 17.5M9.75 4.75L8.5 2.75M14.25 4.75L15.5 2.75")], "bug, insect, issue"),
    },
    "🎮 Gaming": {
        "gamepad": ([("s", "M6.25 6.75H17.75C20 6.75 21.25 8.5 21.25 11V15.25C21.25 17 20.25 18.25 18.75 18.25C17.5 18.25 16.75 17.25 15.75 16.25H8.25C7.25 17.25 6.5 18.25 5.25 18.25C3.75 18.25 2.75 17 2.75 15.25V11C2.75 8.5 4 6.75 6.25 6.75Z"),
                     ("cut", "M8 10V14M6 12H10"), ("d", circ(15.25, 11, 1)), ("d", circ(17.25, 13, 1))], "gaming, controller, console"),
        "dice": ([("s", "M3.75 3.75H20.25V20.25H3.75Z")] + [("d", circ(x, y, 1.25)) for x, y in ((8, 8), (16, 8), (12, 12), (8, 16), (16, 16))], "dice, random, game"),
        "puzzle": ([("s", "M3.75 7.25H8.25A2.25 2.25 0 1 1 12.75 7.25H17.25V11.25A2.25 2.25 0 1 1 17.25 15.75V20.25H3.75Z")], "puzzle, piece, toys, integration"),
        "joystick": ([("s", "M4.75 15.75H19.25V20.25H4.75Z"), ("o", "M12 15.75V8.25"), ("s", circ(12, 5.75, 3)), ("d", circ(16.5, 18, 1))], "joystick, arcade, gaming"),
        "sword": ([("o", "M21.25 2.75H17.25L7.75 12.25M21.25 2.75V6.75L11.75 16.25M5.75 10.25L13.75 18.25M8.75 15.25L3.25 20.75")], "sword, game, battle"),
        "vr-headset": ([("s", "M2.75 7.25H21.25V16.75H15.25L12 13.75L8.75 16.75H2.75Z"), ("cut", "M6.25 10.75H9.25M14.75 10.75H17.75")], "vr, virtual reality, ar try-on"),
    },
    "🔬 Science": {
        "flask": ([("s", "M10 3.25V8.75L3.25 21.25H20.75L14 8.75V3.25Z"), ("o", "M8.25 3.25H15.75"), ("cut", "M6.25 15.75H17.75")], "flask, lab, ingredients, formula"),
        "test-tube": ([("s", "M9.25 3.25H14.75V17.25A2.75 2.75 0 0 1 9.25 17.25Z"), ("o", "M7.75 3.25H16.25"), ("cut", "M9.25 11.25H14.75")], "test tube, sample, lab"),
        "microscope": ([("s", poly([(9.25, 4.25), (12.25, 2.75), (15.75, 10.25), (12.75, 11.75)])), ("o", "M4.75 21.25H19.25M14.25 11L18.25 18.25H11.75M8.75 15.25H13.25")], "microscope, research, lab"),
        "atom": ([("o", ellipse(12, 12, 9.25, 3.5, 0)), ("o", ellipse(12, 12, 9.25, 3.5, 60)), ("o", ellipse(12, 12, 9.25, 3.5, 120)), ("f", circ(12, 12, 1.75))], "atom, science, physics"),
        "dna": ([("o", "M7.25 2.75C7.25 9 16.75 15 16.75 21.25M16.75 2.75C16.75 9 7.25 15 7.25 21.25M8.5 5.75H15.5M8.5 18.25H15.5M10.25 9H13.75M10.25 15H13.75")], "dna, genetics, biology"),
        "magnet": ([("s", "M4.75 2.75H9.75V12A2.25 2.25 0 0 0 14.25 12V2.75H19.25V12A7.25 7.25 0 0 1 4.75 12Z"), ("cut", "M4.75 6.75H9.75M14.25 6.75H19.25")], "magnet, attract, retention"),
    },
    "🍼 Baby & kids": {
        "baby-bottle": ([("s", "M8.25 9.25H15.75V21.25H8.25Z"), ("s", "M9.25 6.25H14.75V9.25H9.25Z"), ("s", "M10.75 6.25V4.25A1.25 1.25 0 0 1 13.25 4.25V6.25"), ("cut", "M8.25 9.25H15.75M8.25 13.5H11M8.25 17H11")],
                        "baby bottle, feeding, baby"),
        "pacifier": ([("o", circ(12, 5.25, 2.5)), ("s", "M4.75 9.25H19.25C19.25 12 17 14 14.25 14.25V15.75H9.75V14.25C7 14 4.75 12 4.75 9.25Z"),
                      ("s", "M9.75 15.75H14.25C14.25 18.75 13.25 21.25 12 21.25C10.75 21.25 9.75 18.75 9.75 15.75Z"), ("cut", "M9.75 15.75H14.25")], "pacifier, dummy, baby"),
        "stroller": ([("s", "M12 2.75A8.25 8.25 0 0 1 20.25 11H12Z"), ("s", "M3.75 11H20.25C20.25 14.25 17.5 16.25 12 16.25C6.5 16.25 3.75 14.25 3.75 11Z"), ("cut", "M3.75 11H20.25"),
                      ("o", "M3.75 11L2.75 6.25"), ("f", circ(7, 19.5, 1.75)), ("f", circ(17, 19.5, 1.75))], "stroller, pram, baby"),
        "baby": ([("s", circ(12, 13, 8.25)), ("o", "M12 4.75C12 3.25 13.25 2.25 14.75 2.75"), ("d", circ(9, 12.5, 1)), ("d", circ(15, 12.5, 1)), ("cut", "M9.75 16C10.75 17.25 13.25 17.25 14.25 16")], "baby, kids, infant"),
        "toy-blocks": ([("s", "M2.75 12.25H11.25V20.75H2.75Z"), ("s", "M12.75 12.25H21.25V20.75H12.75Z"), ("s", "M7.75 3.75H16.25V12.25H7.75Z"), ("cut", "M2.75 12.25H21.25")], "toys, blocks, kids"),
    },
}
for page, items in EXP5.items():
    CATEGORIES[page] = dict(items)
BADGE_PLAN5 = {"👗 Fashion & apparel": [("hanger", "plus"), ("hanger", "check"), ("t-shirt", "heart"), ("t-shirt", "plus"), ("dress", "heart"), ("sneaker", "heart"), ("handbag", "heart")]}
EXP5B = {}
for page, pairs in BADGE_PLAN5.items():
    for base, mod in pairs:
        EXP5B.setdefault(page, {})[f"{base}-{mod}"] = badged(base, mod)
EXP5B["👗 Fashion & apparel"]["size-tag"] = ([("s", TAG), TAG_HOLE, ("cut", "M9.75 15.75V10.75L12 13.5L14.25 10.75V15.75")], "size, size guide, fit")
for page, items in EXP5B.items():
    CATEGORIES[page].update(items)
EXP5_NAMES = [k for v in EXP5.values() for k in v] + [k for v in EXP5B.values() for k in v]


_MD = CATEGORIES["💊 Medical"]
_MD = {("capsule-pill" if k == "pill" else k): v for k, v in _MD.items()}
CATEGORIES["💊 Medical"] = _MD
EXP5_NAMES = [("capsule-pill" if k == "pill" else k) for k in EXP5_NAMES]


# expansion 5 fixes
_NA = CATEGORIES["🌿 Nature"]
_NA["flower"] = ([("s", "M6.25 4.25L9.25 6.75L12 3.25L14.75 6.75L17.75 4.25V9.25A5.75 5.75 0 0 1 6.25 9.25Z"), ("o", "M12 15V21.25"),
                  ("s", "M12 19C12 16.75 14 15.25 17 15.25C17 17.5 15 19 12 19Z")], _NA["flower"][1])
del _NA["clover"]
_NA["mushroom"] = ([("s", "M3.25 12.25A8.75 8.75 0 0 1 20.75 12.25Z"), ("s", "M9.25 12.25H14.75L15.25 21.25H8.75Z"), ("cut", "M3.25 12.25H20.75"),
                    ("d", circ(9, 8.25, 1)), ("d", circ(14.5, 7.5, 1))], "mushroom, nature, forest")
_AN = CATEGORIES["🐾 Animals"]
_AN["rabbit"] = ([("s", "M7.5 8.25V5.25A1.625 1.625 0 0 1 10.75 5.25V8.25"), ("s", "M13.25 8.25V5.25A1.625 1.625 0 0 1 16.5 5.25V8.25"), ("s", circ(12, 16, 5.25)),
                  ("d", circ(10, 15.5, 1)), ("d", circ(14, 15.5, 1))], _AN["rabbit"][1])
_BE = CATEGORIES["💄 Beauty & care"]
del _BE["compact"]
_BE["cream-jar"] = ([("s", "M5.75 4.75H18.25V8.75H5.75Z"), ("s", "M3.75 8.75H20.25V17.25C20.25 19.5 18.5 20.25 16.75 20.25H7.25C5.5 20.25 3.75 19.5 3.75 17.25Z"),
                     ("cut", "M3.75 8.75H20.25M8.75 13.75H15.25")], _BE["cream-jar"][1])
_BK = CATEGORIES["🍼 Baby & kids"]
_BK["toy-blocks"] = (_BK["toy-blocks"][0] + [("cut", "M12 12.25V20.75")], _BK["toy-blocks"][1])


def _swap(page, name, old, new):
    e, t = CATEGORIES[page][name]
    CATEGORIES[page][name] = ([(k, d.replace(old, new) if k == "cut" else d) for k, d in e], t)


_swap("🍼 Baby & kids", "toy-blocks", "M2.75 12.25H21.25", "M2 12.25H22")
_swap("🌿 Nature", "mushroom", "M3.25 12.25H20.75", "M2 12.25H22")
_swap("💄 Beauty & care", "cream-jar", "M3.75 8.75H20.25", "M3 8.75H21")


_swap("🍼 Baby & kids", "toy-blocks", "M2 12.25H22", "M2.75 12.25H21.25")
_swap("🌿 Nature", "mushroom", "M2 12.25H22", "M3.25 12.25H20.75")
_swap("💄 Beauty & care", "cream-jar", "M3 8.75H21", "M3.75 8.75H20.25")
for _p, _n, _k in (("🍼 Baby & kids", "toy-blocks", "M2 12.25H22"), ("🌿 Nature", "mushroom", "M2 12.25H22"), ("💄 Beauty & care", "cream-jar", "M3 8.75H21")):
    _e, _t = CATEGORIES[_p][_n]
    CATEGORIES[_p][_n] = (_e + [("k", _k)], _t)


# ---------------------------------------------------------------- expansion 6
BADGE_PLAN6 = {
    "👗 Fashion & apparel": [("jacket", "heart"), ("skirt", "heart"), ("pants", "heart"), ("cap", "heart"), ("watch", "heart"),
                             ("sunglasses", "heart"), ("backpack", "heart"), ("high-heel", "heart"), ("t-shirt", "check"), ("t-shirt", "x"),
                             ("dress", "plus"), ("sneaker", "plus"), ("handbag", "plus"), ("hanger", "x")],
    "🛍️ Shopping & commerce": [("basket", m) for m in ("plus", "check", "heart", "x", "clock")] + [("gift", "x"), ("coupon", "clock"), ("store", "star")],
    "💳 Paymen & shipping": [("coins", "plus"), ("coins", "check"), ("contactless", "check"), ("box", "alert"), ("box", "down"), ("box", "up"),
                             ("package", "down"), ("package", "up"), ("package", "lock"), ("package", "heart"), ("banknote", "x"), ("credit-card", "search")],
    "👤 People": [("id-card", "x"), ("id-card", "lock"), ("users", "heart"), ("users", "search"), ("user-circle", "check")],
    "🔔 Notifications": [("inbox", "check"), ("inbox", "down"), ("bell", "heart"), ("bell", "star"), ("bell", "x")],
    "💬 Communication": [("phone", "x"), ("phone", "plus"), ("headset", "check"), ("message-circle", "alert"), ("message-circle", "search")],
    "✉️ Mail": [("mail", "down"), ("mail", "up")],
    "🕒 Time & calendar": [("alarm-clock", "check"), ("alarm-clock", "plus"), ("calendar", "down")],
    "🛡️ Security": [("shield", "clock"), ("shield", "search")],
    "📄 File icons": [("file", m) for m in ("up", "star", "alert")] + [("folder", m) for m in ("down", "up", "star", "clock", "alert")]
                     + [("cloud", m) for m in ("plus", "clock", "alert")],
    "🔑 Accounts & access": [("award", "check"), ("settings", "alert"), ("key", "check")],
    "🧭 Navigation & places": [("building", "check"), ("building", "search"), ("route", "check")],
    "📱 Devices": [("tablet", "check"), ("smartwatch", "check"), ("printer", "check"), ("printer", "x"), ("server", "check"), ("server", "x"), ("server", "alert")],
    "🎬 Multimedia": [("music", "plus"), ("music", "heart"), ("tv", "check")],
    "📷 Photography": [("images", "plus"), ("camera", "check")],
    "🚗 Transportation": [("car", "check"), ("car", "x"), ("bus", "clock"), ("plane", "clock"), ("plane", "check"), ("train", "clock"),
                          ("ship", "clock"), ("container", "check"), ("pallet", "check"), ("van", "check"), ("van", "clock")],
    "✈️ Travel": [("hotel", "x"), ("hotel", "search")],
    "💰 Finance": [("landmark", "check"), ("piggy-bank", "plus")],
}
EXP6 = {}
for page, pairs in BADGE_PLAN6.items():
    for base, mod in pairs:
        nm = f"{base}-{mod}"
        if nm in _all() or nm in EXP6.get(page, {}):
            continue
        EXP6.setdefault(page, {})[nm] = badged(base, mod, TAG_ELEMS if base == "tag" else None)


def _off(base, tags):
    return (find(base)[0] + SLASH, tags)


EXP6.setdefault("📷 Photography", {})["camera-off"] = _off("camera", "camera off, no camera")
EXP6.setdefault("🎬 Multimedia", {})["video-off"] = _off("video", "video off, no video")
EXP6.setdefault("🧭 Navigation & places", {})["map-pin-off"] = _off("map-pin", "location off, unavailable")
EXP6.setdefault("📄 File icons", {})["cloud-off"] = _off("cloud", "offline, no connection, sync off")
EXP6.setdefault("🛍️ Shopping & commerce", {})["heart-off"] = _off("heart", "remove from wishlist, unfavourite")

_CORNERS = "M2.75 7.25V2.75H7.25M16.75 2.75H21.25V7.25M21.25 16.75V21.25H16.75M7.25 21.25H2.75V16.75"
EXP6["🛍️ Shopping & commerce"].update({
    "scan-barcode": ([("o", _CORNERS), ("o", "M7.25 7.75V16.25M10.25 7.75V16.25M13.75 7.75V16.25M16.75 7.75V16.25"), ("f", "M11.25 7.75H12.75V16.25H11.25Z")], "scan, barcode, product lookup"),
    "scan-line": ([("o", _CORNERS), ("o", "M6.25 12H17.75")], "scan, scanner, self checkout"),
    "cash-register": ([("s", "M3.75 11.25H20.25V21.25H3.75Z"), ("s", "M5.75 2.75H14.25V7.75H5.75Z"), ("o", "M10 7.75V11.25"), ("cut", "M3.75 17.25H20.25"),
                       ("d", circ(7.5, 14.25, .9)), ("d", circ(10.75, 14.25, .9)), ("d", circ(14, 14.25, .9))], "pos, cash register, checkout, in store"),
})
EXP6["💳 Paymen & shipping"]["parcel-locker"] = ([("s", "M2.75 3.75H21.25V20.25H2.75Z"), ("cut", "M9.25 3.75V20.25M15.25 3.75V20.25M2.75 12H9.25M15.25 9.25H21.25M15.25 14.75H21.25"),
                                                 ("d", circ(11, 12, .9))], "parcel locker, pickup point, delivery")
EXP6["👗 Fashion & apparel"].update({
    "jewelry-ring": ([("o", circ(12, 14.75, 6.5)), ("s", poly([(9.25, 5.75), (10.75, 2.75), (13.25, 2.75), (14.75, 5.75), (12, 8.25)]))], "ring, jewellery, engagement"),
    "necklace": ([("o", "M5.25 2.75C5.25 9.25 8.25 12.75 12 12.75C15.75 12.75 18.75 9.25 18.75 2.75"), ("s", "M12 12.75L15 16.75L12 20.75L9 16.75Z")], "necklace, pendant, jewellery"),
    "boot": ([("s", "M5.75 2.75H13.25V12.75L18.75 14.75C20.25 15.25 21.25 16.25 21.25 18V20.25H5.75Z"), ("cut", "M5.75 17.25H21.25")], "boot, shoes, footwear"),
    "belt": ([("s", "M2.75 9.75H8.25V14.25H2.75Z"), ("s", "M15.75 9.75H21.25V14.25H15.75Z"), ("o", "M8.25 6.75H15.75V17.25H8.25Z"), ("o", "M8.25 12H12.75"),
              ("d", circ(18.5, 12, .9))], "belt, accessories, leather"),
    "tie": ([("s", "M9.75 2.75H14.25L13.25 6.75H10.75Z"), ("s", "M10.75 6.75H13.25L15.25 17.75L12 21.25L8.75 17.75Z"), ("cut", "M10.75 6.75H13.25")], "tie, formal, menswear"),
    "bow-tie": ([("s", poly([(2.75, 6.75), (10.25, 10.25), (10.25, 13.75), (2.75, 17.25)])), ("s", poly([(21.25, 6.75), (13.75, 10.25), (13.75, 13.75), (21.25, 17.25)])),
                 ("s", "M10.25 9.75H13.75V14.25H10.25Z"), ("cut", "M10.25 9.75V14.25M13.75 9.75V14.25")], "bow tie, formal, party"),
    "sewing-button": ([("s", circ(12, 12, 9.25))] + [("d", circ(x, y, 1)) for x, y in ((10, 10), (14, 10), (10, 14), (14, 14))], "button, sewing, haberdashery"),
})
EXP6["📶 Connectivity"] = {
    "signal": ([("s", "M2.75 17.25H5.5V21.25H2.75Z"), ("s", "M8 13.25H10.75V21.25H8Z"), ("s", "M13.25 9.25H16V21.25H13.25Z"), ("s", "M18.5 2.75H21.25V21.25H18.5Z")], "signal, reception, network"),
    "signal-medium": ([("s", "M2.75 17.25H5.5V21.25H2.75Z"), ("s", "M8 13.25H10.75V21.25H8Z"), ("s", "M13.25 9.25H16V21.25H13.25Z"), ("o", "M18.5 2.75H21.25V21.25H18.5Z")], "signal, reception, network"),
    "signal-low": ([("s", "M2.75 17.25H5.5V21.25H2.75Z"), ("s", "M8 13.25H10.75V21.25H8Z"), ("o", "M13.25 9.25H16V21.25H13.25Z"), ("o", "M18.5 2.75H21.25V21.25H18.5Z")], "weak signal, reception"),
    "router": ([("s", "M2.75 13.25H21.25V20.25H2.75Z"), ("o", "M6.75 13.25L4.75 4.75M17.25 13.25L19.25 4.75"), ("d", circ(6.75, 16.75, 1)), ("d", circ(10.25, 16.75, 1)),
                ("cut", "M14.25 16.75H17.75")], "router, wifi, internet"),
    "usb-plug": ([("s", "M7.75 2.75H16.25V9.25H7.75Z"), ("d", "M9.75 5.25H11.25V6.75H9.75Z"), ("d", "M12.75 5.25H14.25V6.75H12.75Z"),
                  ("s", "M5.75 9.25H18.25V18.25A3 3 0 0 1 15.25 21.25H8.75A3 3 0 0 1 5.75 18.25Z"), ("cut", "M5.75 9.25H18.25")], "usb, cable, connector"),
    "radio-tower": ([("o", "M12 9.75L8 21.25M12 9.75L16 21.25M9.25 17.25H14.75"), ("s", circ(12, 7.25, 1.75)),
                     ("o", arc(12, 7.25, 5, 135, 225)), ("o", arc(12, 7.25, 5, -45, 45)), ("o", arc(12, 7.25, 8.5, 140, 220)), ("o", arc(12, 7.25, 8.5, -40, 40))], "broadcast, tower, signal"),
    "ethernet-port": ([("s", "M3.75 4.75H20.25V17.75H15.75V20.25H8.25V17.75H3.75Z"), ("cut", "M9 9.25V12.25M12 9.25V12.25M15 9.25V12.25")], "ethernet, lan, network"),
    "wifi-off": ([e for e in find("wifi")[0]] + SLASH, "offline, no wifi, disconnected"),
    "bluetooth-off": (find("bluetooth")[0] + SLASH, "bluetooth off, disconnected"),
}
EXP6["🏢 Buildings"] = {
    "factory": ([("s", poly([(2.75, 21.25), (2.75, 10.25), (8, 6.75), (8, 10.25), (13.25, 6.75), (13.25, 10.25), (17.25, 10.25), (17.25, 2.75), (21.25, 2.75), (21.25, 21.25)])),
                 ("cut", "M5.75 15.75H8.25M10.75 15.75H13.25M15.75 15.75H18.25")], "factory, manufacturing, production"),
    "school": ([("s", "M3.75 10.75L12 6.25L20.25 10.75V21.25H3.75Z"), ("o", "M12 6.25V2.75H15.25"), ("cut", "M10 21.25V16.75H14V21.25"), ("cut", circ(12, 11.75, 1.5))], "school, education, back to school"),
    "castle": ([("s", "M3.75 21.25V4.75H7.25V7.25H10.25V4.75H13.75V7.25H16.75V4.75H20.25V21.25Z"), ("cut", "M9.75 21.25V16.5A2.25 2.25 0 0 1 14.25 16.5V21.25")], "castle, landmark, fairytale"),
    "garage": ([("s", "M2.75 9.25L12 3.25L21.25 9.25V21.25H2.75Z"), ("cut", "M6.75 21.25V12.75H17.25V21.25M6.75 15.5H17.25M6.75 18.25H17.25")], "garage, parking, pickup"),
    "construction-cone": ([("s", "M9.75 2.75H14.25L18 18.25H6Z"), ("s", "M2.75 18.25H21.25V21.25H2.75Z"), ("cut", "M8.25 8.25H15.75M7 13.25H17M2.75 18.25H21.25")],
                          "under construction, maintenance, roadwork"),
}
EXP6["💻 Development"] = {
    "terminal": ([("s", "M2.75 3.75H21.25V20.25H2.75Z"), ("cut", "M6.75 9L9.75 12L6.75 15M11.75 15.25H17.25")], "terminal, console, command line"),
    "square-code": ([("s", "M2.75 3.75H21.25V20.25H2.75Z"), ("cut", "M9.25 9L6.25 12L9.25 15M14.75 9L17.75 12L14.75 15")], "code, embed, html"),
    "git-commit": ([("o", "M2.75 12H7.75M16.25 12H21.25"), ("s", circ(12, 12, 4.25))], "commit, version, git"),
    "git-branch": ([("s", circ(6.75, 5.25, 2.5)), ("s", circ(6.75, 18.75, 2.5)), ("s", circ(17.25, 6.75, 2.5)),
                    ("o", "M6.75 7.75V16.25M17.25 9.25C17.25 14.25 14 18.75 9.25 18.75")], "branch, version, git"),
    "git-merge": ([("s", circ(6.75, 5.25, 2.5)), ("s", circ(6.75, 18.75, 2.5)), ("s", circ(17.25, 15.25, 2.5)),
                   ("o", "M6.75 7.75V16.25M6.75 7.75C6.75 12 10.5 15.25 14.75 15.25")], "merge, version, git"),
    "git-pull-request": ([("s", circ(6.25, 5.25, 2.5)), ("s", circ(6.25, 18.75, 2.5)), ("s", circ(17.75, 18.75, 2.5)),
                          ("o", "M6.25 7.75V16.25M17.75 16.25V9.25C17.75 7.5 16.5 6.25 14.75 6.25H10.75M13 4L10.75 6.25L13 8.5")], "pull request, review, git"),
    "database": ([("s", "M4.75 5.75C4.75 4 8 2.75 12 2.75C16 2.75 19.25 4 19.25 5.75V18.25C19.25 20 16 21.25 12 21.25C8 21.25 4.75 20 4.75 18.25Z"),
                  ("cut", "M4.75 5.75C4.75 7.5 8 8.75 12 8.75C16 8.75 19.25 7.5 19.25 5.75M4.75 12C4.75 13.75 8 15 12 15C16 15 19.25 13.75 19.25 12")], "database, data, storage"),
    "cpu": ([("s", "M6.25 6.25H17.75V17.75H6.25Z"), ("cut", "M9.75 9.75H14.25V14.25H9.75Z"),
             ("o", "M9.5 2.75V6.25M14.5 2.75V6.25M9.5 17.75V21.25M14.5 17.75V21.25M2.75 9.5H6.25M2.75 14.5H6.25M17.75 9.5H21.25M17.75 14.5H21.25")], "cpu, processor, chip"),
    "braces": ([("o", "M8.25 3.25C6.5 3.25 5.75 4 5.75 5.75V9.75C5.75 11 5 12 3.25 12C5 12 5.75 13 5.75 14.25V18.25C5.75 20 6.5 20.75 8.25 20.75"),
                ("o", "M15.75 3.25C17.5 3.25 18.25 4 18.25 5.75V9.75C18.25 11 19 12 20.75 12C19 12 18.25 13 18.25 14.25V18.25C18.25 20 17.5 20.75 15.75 20.75")], "braces, json, code"),
    "sitemap": ([("s", "M9.25 2.75H14.75V8.25H9.25Z"), ("s", "M2.75 15.75H8.25V21.25H2.75Z"), ("s", "M9.25 15.75H14.75V21.25H9.25Z"), ("s", "M15.75 15.75H21.25V21.25H15.75Z"),
                 ("o", "M12 8.25V15.75M5.5 15.75V12H18.5V15.75")], "sitemap, structure, categories"),
}
for page, items in EXP6.items():
    CATEGORIES.setdefault(page, {}).update(items)
EXP6_NAMES = [k for v in EXP6.values() for k in v]

# expansion 6 fixes
_DV = CATEGORIES["💻 Development"]
_DV["sitemap"] = ([("s", "M9.25 2.75H14.75V8.25H9.25Z"), ("s", "M2.75 16.25H7.25V21.25H2.75Z"), ("s", "M9.75 16.25H14.25V21.25H9.75Z"), ("s", "M16.75 16.25H21.25V21.25H16.75Z"),
                   ("o", "M12 8.25V16.25M5 16.25V12.25H19V16.25")], _DV["sitemap"][1])
_DV["database"] = ([("s", "M4.75 5.75C4.75 4 8 2.75 12 2.75C16 2.75 19.25 4 19.25 5.75V18.25C19.25 20 16 21.25 12 21.25C8 21.25 4.75 20 4.75 18.25Z"),
                    ("cut", "M4.75 5.75C4.75 7.5 8 8.75 12 8.75C16 8.75 19.25 7.5 19.25 5.75"), ("cut", "M4.75 12C4.75 13.75 8 15 12 15C16 15 19.25 13.75 19.25 12")], _DV["database"][1])
_DV["sitemap"] = ([("s", "M9.25 2.75H14.75V8.25H9.25Z"), ("s", "M2.75 16.25H6.75V21.25H2.75Z"), ("s", "M10 16.25H14V21.25H10Z"), ("s", "M17.25 16.25H21.25V21.25H17.25Z"),
                   ("o", "M12 8.25V16.25M4.75 16.25V12.25H19.25V16.25")], _DV["sitemap"][1])
_DV["database"] = (_DV["database"][0] + [("k", "M3.25 11.25C4.75 13.75 8 15 12 15C16 15 19.25 13.75 20.75 11.25")], _DV["database"][1])
_DV["sitemap"] = ([("s", "M9 2.75H15V8.25H9Z"), ("s", "M2.75 15.75H8.75V21.25H2.75Z"), ("s", "M15.25 15.75H21.25V21.25H15.25Z"),
                   ("o", "M12 8.25V12M5.75 15.75V12H18.25V15.75")], _DV["sitemap"][1])


# ---------------------------------------------------------------- expansion 7
EXP7 = {}
EXP7["👗 Fashion & apparel"] = {
    "hoodie": ([("s", "M6.25 5.25C7.5 4 9.5 3 12 3C14.5 3 16.5 4 17.75 5.25V21.25H6.25Z"), ("s", "M6.25 5.25L3.25 8.25L2.75 19.25H5.25L6.25 11.75Z"),
                ("s", "M17.75 5.25L20.75 8.25L21.25 19.25H18.75L17.75 11.75Z"),
                ("cut", "M9.5 4.25C9.5 6.75 10.5 8.25 12 8.25C13.5 8.25 14.5 6.75 14.5 4.25M8.75 15.25H15.25M6.25 5.25V11.75M17.75 5.25V11.75")], "hoodie, sweatshirt, casual"),
    "coat": ([("s", "M7.25 2.75H16.75L20.25 6.25V21.25H3.75V6.25Z"), ("cut", "M7.25 2.75L12 9.25L16.75 2.75M12 9.25V21.25M3.75 14.25H20.25"),
              ("d", circ(14.5, 11.5, .9)), ("d", circ(14.5, 17.75, .9))], "coat, outerwear, winter"),
    "scarf": ([("s", "M5.75 3.75H18.25V8.25H5.75Z"), ("s", "M12.25 8.25H17.25L18.25 18.75H13.25Z"), ("s", "M7.75 8.25H12.25L11.25 16.75H6.75Z"),
               ("cut", "M5.75 8.25H18.25M12.25 8.25L13.25 18.75"), ("o", "M14.5 18.75V21.25M17 18.75V21.25")], "scarf, winter, accessories"),
    "mitten": ([("s", "M7.25 17.25V7.25A4.75 4.75 0 0 1 16.75 7.25V12.25L18.75 10.25A1.6 1.6 0 0 1 21 12.5L16.75 17.25Z"), ("s", "M7.25 17.25H16.75V21.25H7.25Z"),
                ("cut", "M7.25 17.25H16.75")], "gloves, mittens, winter"),
    "swimsuit": ([("s", "M7.25 2.75V7.25C7.25 9 6.75 10.5 5.75 11.75C5.75 14.5 8.75 17.25 10.25 21.25H13.75C15.25 17.25 18.25 14.5 18.25 11.75C17.25 10.5 16.75 9 16.75 7.25V2.75C16.75 5.75 14.75 8.25 12 8.25C9.25 8.25 7.25 5.75 7.25 2.75Z")],
                 "swimwear, swimsuit, beach"),
    "earrings": ([("o", "M7 2.75V7.25M17 2.75V7.25"), ("s", "M7 7.25L9.48 12.31A2.75 2.75 0 1 1 4.52 12.31Z"), ("s", "M17 7.25L19.48 12.31A2.75 2.75 0 1 1 14.52 12.31Z")],
                 "earrings, jewellery, accessories"),
    "hat": ([("s", "M6.75 14.25V8.75C6.75 6 9 4.75 12 4.75C15 4.75 17.25 6 17.25 8.75V14.25Z"), ("s", "M2.75 14.25H21.25C21.25 16.75 17.5 18.25 12 18.25C6.5 18.25 2.75 16.75 2.75 14.25Z"),
             ("cut", "M6.75 11.25H17.25M2.75 14.25H21.25")], "hat, headwear, accessories"),
    "fitting-room": ([("o", "M2.75 3.25H21.25"), ("s", "M4.25 3.25H10.75C10.75 9 9.5 15 8 21.25H4.25Z"), ("s", "M19.75 3.25H13.25C13.25 9 14.5 15 16 21.25H19.75Z")],
                     "fitting room, try on, changing room"),
    "mannequin": ([("s", "M7.75 4.75H16.25C16.25 8 15.25 10 14.25 11.25C15.25 12.5 16.25 14 16.25 16.75H7.75C7.75 14 8.75 12.5 9.75 11.25C8.75 10 7.75 8 7.75 4.75Z"),
                   ("o", "M12 2.75V4.75M12 16.75V21.25M8.75 21.25H15.25")], "mannequin, display, tailoring"),
}
EXP7["💳 Paymen & shipping"] = {
    "invoice": ([("s", "M4.75 2.75H19.25V21.25H4.75Z"), ("cut", "M8.25 6.75H12.75M8.25 10.25H15.75M8.25 13.75H15.75M12.75 17.25H15.75")], "invoice, pay later, bill"),
    "installments": ([("o", circ(12, 12, 9.25)), ("f", "M12 12V2.75A9.25 9.25 0 0 1 21.25 12Z"), ("o", "M12 2.75V21.25M2.75 12H21.25")], "installments, part payment, pay later"),
    "return-label": ([("s", "M3.75 3.75H20.25V20.25H3.75Z"), ("cut", "M9.25 6.75L6.75 9.25L9.25 11.75M6.75 9.25H14.25A3.25 3.25 0 0 1 14.25 15.75H11.75")], "returns, return label, exchange"),
}
EXP7["🛍️ Shopping & commerce"] = {
    "scale-balance": ([("o", "M12 3.25V20.75M8.25 20.75H15.75M5.25 6.25H18.75"),
                       ("s", "M2.75 13.25L5.25 6.25L7.75 13.25C7.75 14.75 6.5 15.75 5.25 15.75C4 15.75 2.75 14.75 2.75 13.25Z"),
                       ("s", "M16.25 13.25L18.75 6.25L21.25 13.25C21.25 14.75 20 15.75 18.75 15.75C17.5 15.75 16.25 14.75 16.25 13.25Z")], "compare, balance, fair"),
}
_DIAG = "M6.25 17.75L17.75 6.25M8.25 6.25H17.75V15.75"
EXP7["➡️ Arrows"] = {
    "arrow-up-right": ([("o", _DIAG)], "arrow, diagonal, external"),
    "arrow-up-left": ([("o", rot_path(_DIAG, -90))], "arrow, diagonal"),
    "arrow-down-right": ([("o", rot_path(_DIAG, 90))], "arrow, diagonal"),
    "arrow-down-left": ([("o", rot_path(_DIAG, 180))], "arrow, diagonal"),
    "rotate-ccw": ([("o", "M3.25 12A8.75 8.75 0 1 0 12 3.25C9.6 3.25 7.4 4.25 5.8 5.8L3.25 8.25M3.25 3.25V8.25H8.25")], "rotate, undo, reset"),
    "chevrons-up-down": ([("o", "M7.75 8.75L12 4.5L16.25 8.75M7.75 15.25L12 19.5L16.25 15.25")], "select, dropdown, sort"),
    "corner-down-right": ([("o", "M5.75 3.75V11.25C5.75 13.25 7 14.75 9.25 14.75H19.25M15 10.5L19.25 14.75L15 19")], "arrow, corner, reply"),
    "corner-down-left": ([("o", "M18.25 3.75V11.25C18.25 13.25 17 14.75 14.75 14.75H4.75M9 10.5L4.75 14.75L9 19")], "arrow, corner, enter"),
    "arrow-down-up": ([("o", "M7.25 3.25V20.75M3.5 7L7.25 3.25L11 7M16.75 20.75V3.25M13 17L16.75 20.75L20.5 17")], "sort, swap, order"),
}
EXP7["📱 UI"] = {
    "circle-dot": ([("o", circ(12, 12, 9.25)), ("f", circ(12, 12, 4))], "radio, selected, option"),
    "grip-vertical": ([("f", circ(x, y, 1.4)) for x in (9, 15) for y in (5.5, 12, 18.5)], "drag, handle, reorder"),
    "grip-horizontal": ([("f", circ(x, y, 1.4)) for y in (9, 15) for x in (5.5, 12, 18.5)], "drag, handle, reorder"),
    "copy": ([("s", "M8.75 8.75H21.25V21.25H8.75Z"), ("o", "M15.25 8.75V2.75H2.75V15.25H8.75")], "copy, duplicate, clipboard"),
    "list-filter": ([("o", "M2.75 6.25H21.25M6.25 12H17.75M9.75 17.75H14.25")], "filter, refine, sort"),
    "pin": ([("s", "M9.25 2.75H14.75V9.25L17.75 13.25H6.25L9.25 9.25Z"), ("o", "M12 13.25V21.25")], "pin, keep, attach"),
    "grid-2x2": ([("s", "M2.75 2.75H10.75V10.75H2.75Z"), ("s", "M13.25 2.75H21.25V10.75H13.25Z"), ("s", "M2.75 13.25H10.75V21.25H2.75Z"), ("s", "M13.25 13.25H21.25V21.25H13.25Z")],
                 "grid, view, products"),
    "list-plus": ([("o", "M2.75 6.25H15.25M2.75 12H15.25M2.75 17.75H9.75M17.5 13.75V21.25M13.75 17.5H21.25")], "add to list, playlist, wishlist"),
    "info": ([("o", "M12 10.25V21.25M9.75 10.25H12M9.75 21.25H14.25"), ("f", circ(12, 5, 1.5))], "info, details, about"),
}
for page, items in EXP7.items():
    CATEGORIES.setdefault(page, {}).update(items)
EXP7["💳 Paymen & shipping"]["bank-transfer"] = (badged("landmark", "up")[0], "bank transfer, payment, wire")

BADGE_PLAN7 = {
    "👗 Fashion & apparel": [("jacket", "plus"), ("skirt", "plus"), ("pants", "plus"), ("sock", "heart"), ("glasses", "heart"), ("briefcase", "heart"),
                             ("diamond", "heart"), ("hoodie", "heart"), ("coat", "heart"), ("hat", "heart")],
    "🛍️ Shopping & commerce": [("basket", "search"), ("basket", "lock"), ("store", "lock"), ("gift", "search"), ("coupon", "search"), ("perfume-bottle", "heart")],
    "💳 Paymen & shipping": [("coins", "x"), ("coins", "clock"), ("wallet", "heart"), ("wallet", "search"), ("credit-card", "heart"), ("contactless", "x"),
                             ("package", "star"), ("box", "star"), ("banknote", "clock"), ("invoice", "check"), ("invoice", "clock"), ("invoice", "x"), ("invoice", "alert")],
    "🏠 Home": [("sofa", "heart"), ("bed", "heart"), ("lamp", "heart"), ("chair", "heart"), ("plant", "heart")],
    "🍽️ Food & beverage": [("coffee", "heart"), ("wine", "heart"), ("coffee", "plus")],
    "💄 Beauty & care": [("lipstick", "heart"), ("cream-jar", "heart"), ("nail-polish", "heart"), ("soap", "heart")],
    "🍼 Baby & kids": [("stroller", "heart"), ("baby-bottle", "heart")],
    "🐾 Animals": [("paw-print", "heart"), ("pet-bowl", "heart")],
    "⚽ Sports": [("dumbbell", "heart"), ("trophy", "check")],
    "📱 Devices": [("smartphone", "heart"), ("laptop", "heart"), ("smartwatch", "heart"), ("tablet", "heart")],
    "🎬 Multimedia": [("headphones", "heart"), ("film", "heart"), ("playlist", "plus")],
    "✈️ Travel": [("suitcase-rolling", "check"), ("passport", "check"), ("boarding-pass", "check")],
    "👤 People": [("id-card", "search")],
    "💬 Communication": [("headset", "clock"), ("headset", "heart")],
    "🛡️ Security": [("shield", "heart"), ("vault", "check")],
    "🚗 Transportation": [("bicycle", "heart"), ("car", "clock"), ("car", "search"), ("forklift", "check")],
    "🧭 Navigation & places": [("map-pin", "heart"), ("map-pin", "lock"), ("route", "clock")],
}
for page, pairs in BADGE_PLAN7.items():
    for base, mod in pairs:
        nm = f"{base}-{mod}"
        if nm in _all() or nm in EXP7.get(page, {}):
            continue
        EXP7.setdefault(page, {})[nm] = badged(base, mod)
for page, items in EXP7.items():
    CATEGORIES.setdefault(page, {}).update(items)
EXP7_NAMES = [k for v in EXP7.values() for k in v]

# expansion 7 fixes
_D2 = "M6.25 17.75L17.75 6.25M8.25 6.25L17.75 6.25L17.75 15.75"
_AR = CATEGORIES["➡️ Arrows"]
for _n, _a in (("arrow-up-right", 0), ("arrow-up-left", -90), ("arrow-down-right", 90), ("arrow-down-left", 180)):
    _AR[_n] = ([("o", rot_path(_D2, _a) if _a else _D2)], _AR[_n][1])
CATEGORIES["👗 Fashion & apparel"]["fitting-room"] = ([("o", "M2.75 2.75H21.25"), ("s", "M3.75 2.75H10.25C10.25 7.5 8.5 10.5 6.5 12.25C8.5 14 10.25 17 10.25 21.25H3.75Z"),
                                                       ("s", "M20.25 2.75H13.75C13.75 7.5 15.5 10.5 17.5 12.25C15.5 14 13.75 17 13.75 21.25H20.25Z")], "fitting room, try on, changing room")
