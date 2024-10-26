from pprint import pprint

import pandas as pd
import numpy as np

dfs = pd.date_range(
    "2023-01-01 00:00:00",
    "2023-01-01 00:00:05",
    freq="s"
)

# немного изменила входной фрейм, сделала его динамичным
random_counts = np.random.randint(1, 6, size=len(dfs))  # случайное количество строк (от 1 до 5 для каждой dt)
df = pd.DataFrame({"dt": dfs.repeat(random_counts)})


def chunk_cutting(splitting_df, chunk_size):
    all_chunks = []
    current_chunk = []
    grouped = splitting_df.groupby('dt')

    nums = 0

    for _, group in grouped:
        nums += len(group)
        current_chunk.append(group)

        if nums >= chunk_size:
            all_chunks.append(current_chunk)
            current_chunk = []
            nums = 0

    if current_chunk:
        all_chunks.append(current_chunk)

    return all_chunks


if __name__ == '__main__':
    print('splitting_df')
    print(df)
    result = chunk_cutting(splitting_df=df, chunk_size=6)
    pprint(result)
