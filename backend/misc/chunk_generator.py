from typing import List, Dict

from aiomisc import chunk_list

MAX_UNITS_PER_INSERT = int(5 * 1e3)


def chunks_generator(data: List[Dict]):
    for obj in data:
        yield obj


def make_chunks(data: List[Dict]):
    return chunk_list(chunks_generator(data), MAX_UNITS_PER_INSERT)
