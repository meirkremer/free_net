import time


class StoreChunk:
    def __init__(self):
        self._chunk_list = []

    def insert_chunk(self, chunk: bytes | None):
        self._chunk_list.append(chunk)

    def get_len_chunk(self):
        return len(self._chunk_list)

    def fetch_chunks(self, size: int):
        chunk = b''
        progress = True
        if self.get_len_chunk() < 1:
            time.sleep(1)
            return chunk, progress
        if self.get_len_chunk() < size and self._chunk_list[-1] is not None:
            time.sleep(2)
            return chunk, progress
        if self._chunk_list[-1] is None and (self.get_len_chunk() - 1) <= size:
            progress = False
            size = self.get_len_chunk() - 1
        for i in range(size):
            chunk += self._chunk_list[0]
            del self._chunk_list[0]
        return chunk, progress
