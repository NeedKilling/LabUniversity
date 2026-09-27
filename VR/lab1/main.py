import math
#
print("ЗАДАНИЕ 1")
def classify(immersion, sees_real):
    if immersion == True and sees_real == False:
        return "VR"
    if immersion == False and sees_real == True:
        return "AR"
    elif immersion == True and sees_real == True:
        return "MR"
    else: 
        return "real"
print(f"\t",classify(False,True))

#
print("ЗАДАНИЕ 2")
def in_fov(angle, fov):
    for item in angle:
        result = False   
        if abs(item) <= fov/2: 
            result = True
        else:
            result = False
        print(f"\tугол {item}° при FOV {fov}° -> {result}")

in_fov([10,45,60], 110)

#
print("ЗАДАНИЕ 3")
def distance(p1, p2): 
    result = 0
    for i in range(len(p1)):
        result += math.pow((p1[i] - p2[i]),2)
    return math.sqrt(result)
print(f"\t",distance((0,0,0),(1,2,2)))

#

print("ЗАДАНИЕ 4")
def latency_ok(ms):
    return ms <= 20

for ms in [12, 20, 35]:
    if latency_ok(ms):
        print(f"\t{ms} мс -> комфортно")
    else:
        print(f"\t{ms} мс -> риск укачивания")


#
print("ЗАДАНИЕ 5")
def to_radians(deg):
    return deg * math.pi / 180

for deg in [0, 90, 180]:
    print(f"\t{deg}° = {to_radians(deg):.3f} рад")


#
print("ЗАДАНИЕ 6")

def normalize(v):
    length = math.sqrt(sum(x * x for x in v))

    if length == 0:
        return (0.0, 0.0, 0.0)

    return tuple(x / length for x in v)

print(f"\t",normalize((0, 3, 4)))


#
print("ЗАДАНИЕ 7")

def fps_ok(frames, seconds, target=90):
    fps = frames / seconds
    return fps, fps >= target


fps, ok = fps_ok(540, 6)

print(f"\tFPS = {fps}, комфортно для VR: {ok}")


#
print("ЗАДАНИЕ 8")

prices = {
    "Cardboard": 5000,
    "Quest 2": 35000,
    "Quest 3": 60000
}


def affordable(budget):
    return [
        name for name, price in prices.items()
        if price <= budget
    ]

print(f"\tДо 35000 ₽:", affordable(35000))


#
print("ЗАДАНИЕ 9")

def count_areas(items):
    counts = {}

    for item in items:
        counts[item] = counts.get(item, 0) + 1

    return counts

items = [
    "игры",
    "медицина",
    "игры",
    "образование",
    "медицина",
    "игры"
]

print(f"\t",count_areas(items))


#
print("ЗАДАНИЕ 10")

def most_common(items):
    counts = count_areas(items)

    return max(counts, key=counts.get)

print(f"\t","Чаще всего:", most_common(items))


#
print("ЗАДАНИЕ 11")

def lerp(a, b, t):
    return a + (b - a) * t

for t in [0, 0.5, 1]:
    print(f"\tt={t}: {lerp(0, 10, t)}")


#
print("ЗАДАНИЕ 12")
def can_grab(hand, obj, reach=0.3):
    return distance(hand, obj) <= reach

print(f"\t",can_grab((0, 0, 0), (0.1, 0.1, 0.1)))
print(f"\t",can_grab((0, 0, 0), (1, 1, 1)))


#
print("ЗАДАНИЕ 13")
def get_vr_devices(devices):
    return [
        d["name"] for d in devices
        if d["type"] == "VR"
    ]

devices = [
    {"name": "Quest 3", "type": "VR"},
    {"name": "HoloLens", "type": "AR"},
    {"name": "Vive Pro", "type": "VR"}
]

print(f"\tVR-устройства:", get_vr_devices(devices))


#
print("ЗАДАНИЕ 14")
def total_latency(network, render, display):
    total = network + render + display
    return total, total <= 20


total, suitable = total_latency(8, 6, 4)

print(f"\tСуммарная задержка: {total} мс")
print(f"\tПригодно для VR: {suitable}")


#
print("ЗАДАНИЕ 15")
def simulate_movement(speed, fps, frames):
    dt = 1 / fps
    position = 0

    for frame in range(1, frames + 1):
        position += speed * dt
        print(f"\tКадр {frame}: позиция = {position:.4f}")


simulate_movement(2, 90, 3)