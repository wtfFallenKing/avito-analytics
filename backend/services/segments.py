from typing import Optional


async def get_segments_by_user_id(user_id: int) -> Optional[list[int]]:
    segments = {
        2100: [156, 278],
        2200: [168, 290, 412],
        2300: [180],
        2400: [192, 314, 436, 158],
        2500: [592, 370, 148, 326, 204],
        2600: [216],
        2700: [472, 194, 228, 350],
        2800: [42],
        2900: [240, 484, 362, 428, 206],
        3000: [252, 374],
        3100: [264, 386, 508, 230],
        3200: [276, 398],
        3300: [288, 410, 532, 254],
        3400: [544, 300, 422, 166],
        3500: [312, 434],
        3600: [568, 324, 446, 190],
        3700: [336, 458],
        3800: [592, 348, 470, 214],
        3900: [360, 482, 226, 604],
        4000: [616, 372, 494, 238],
        4100: [384, 506, 250, 628],
        4200: [640, 396, 518, 262],
    }

    return segments.get(user_id, [])
