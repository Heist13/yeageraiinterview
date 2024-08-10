# O(N) time complexity (N length of fragment), O(N) space
def simple_hash(data: str) -> str:
    hash_value = 0
    for char in data:
        hash_value = (hash_value << 3) + ord(char)
        hash_value %= 10 ** 30  # avoid overflow by modulo with 30 exponent
    return str(hash_value).zfill(30)  # pad final value with 0s to ensure 30 chars fixed-length


def is_hash_valid(data: str, stored_hash: str) -> bool:
    return simple_hash(data) == stored_hash


def is_fragments_complete(fragments: dict) -> bool:
    if not fragments:
        return True

    keys = fragments.keys()
    min_key, max_key = min(keys), max(keys)
    return set(keys) == set(range(min_key, max_key + 1))


# O(NL) time complexity: N number of fragments, L max fragment size, O(N) space
def reconstruct_data(fragments: dict) -> str:
    if not is_fragments_complete(fragments):
        raise ValueError("Missing fragment")

    reconstructed_data = []
    for key in sorted(fragments.keys()):
        fragment = fragments[key]
        data, stored_hash = fragment['data'], fragment['hash']
        if not is_hash_valid(data, stored_hash):
            raise ValueError("Data integrity check failed")
        reconstructed_data.append(data)
    return ''.join(reconstructed_data)


assert reconstruct_data({
    1: {'data': 'Hello', 'hash': simple_hash('Hello')},
    2: {'data': 'World', 'hash': simple_hash('World')},
    3: {'data': '!', 'hash': simple_hash('!')}
}) == "HelloWorld!"

assert reconstruct_data({
    1: {'data': 'New', 'hash': simple_hash('New')},
    2: {'data': 'Data', 'hash': simple_hash('Data')},
    3: {'data': ' Hashed', 'hash': simple_hash(' Hashed')},
    4: {'data': 'Correctly', 'hash': simple_hash('Correctly')}
}) == "NewData HashedCorrectly"

assert reconstruct_data({}) == ""

try:
    reconstruct_data({
        1: {'data': 'New', 'hash': simple_hash('New')},
        2: {'data': 'Data', 'hash': simple_hash('Data')},
        3: {'data': ' HashedInvalid', 'hash': simple_hash(' Hashed')},
        4: {'data': 'Correctly', 'hash': simple_hash('Correctly')}
    }) == "NewData HashedCorrectly"
except ValueError as e:
    assert str(e) == "Data integrity check failed"

try:
    # Missing fragment
    reconstruct_data({
        1: {'data': 'New', 'hash': simple_hash('New')},
        2: {'data': 'Data', 'hash': simple_hash('Data')},
        4: {'data': 'Correctly', 'hash': simple_hash('Correctly')}
    }) == "NewData HashedCorrectly"
except ValueError as e:
    assert str(e) == "Missing fragment"

print("Test passed")
