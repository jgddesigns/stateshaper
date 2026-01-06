import random
import sys
from .lesson_list import lesson_list
from .lesson_list import lesson_ratings

class LessonPlan:


    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)

        self.adjusted = []
        self.current_lessons = []
        self.lesson_vocab = []
        self.sorted_data = None
        self.data = lesson_list if not data else data
        self.compressed_vocab = None
        self.compressed_subset = None
        self.current_ratings = None
        self.lesson_ratings = lesson_ratings
        self.current_questions = None


  

    def after_test(self, results):
        for question in results:
            self.adjust_related(question["question"]["question"], question["question"]["answer"])
        
    
    def adjust_related(self, question, answer):
        adjust = 5 if answer == True else -5
        ratings_adjust = 1 if answer == True else -1
        item_pos = list(self.data["input"][[self.data["input"].index(i) for i in self.data["input"] if list(i.keys())[0] == question][0]].values())[0]["data"]
        for item in self.data["input"]:
            for term in item[list(item.keys())[0]]["data"]:
                print("Adjusted #" + str(self.data["input"].index(item)) + " " + list(item.keys())[0]) if len([x for x in term["attributes"] if x in item_pos[0]["attributes"]]) > 0 else None
                print("Current Rating: " + str(item[list(item.keys())[0]]["rating"])) if len([x for x in term["attributes"] if x in item_pos[0]["attributes"]]) > 0 else None
                self.adjusted.append(item) if len([x for x in term["attributes"] if x in item_pos[0]["attributes"]]) > 0 else None
                item[list(item.keys())[0]]["rating"] = item[list(item.keys())[0]]["rating"] + adjust if len([x for x in term["attributes"] if x in item_pos[0]["attributes"]]) > 0 else item[list(item.keys())[0]]["rating"]
                print("New Rating: " + str(item[list(item.keys())[0]]["rating"]) + "\n") if len([x for x in term["attributes"] if x in item_pos[0]["attributes"]]) > 0 else None
        
        for key in list(self.lesson_ratings.keys()):
            self.lesson_ratings[key] = self.lesson_ratings[key] + ratings_adjust if key in item_pos[0]["attributes"] else self.lesson_ratings[key]


    def sort_ratings(self):
        self.adjust_ratings()
        sort = sorted(self.data["input"], key=lambda x: list(x.values())[0]["rating"], reverse=True)
        self.sorted_data = sort
        self.data["input"] = sort
        return self.data
    

    def adjust_ratings(self):
        ratings = list(self.lesson_ratings.keys())
        for item in self.data["input"]:
            if item[list(item.keys())[0]]["data"][0]["attributes"][0] in ratings:
                item[list(item.keys())[0]]["rating"] = round((item[list(item.keys())[0]]["rating"] + self.lesson_ratings[item[list(item.keys())[0]]["data"][0]["attributes"][0]]) / 2)
        

    def ratings_data(self):
        sort = sorted(self.lesson_ratings, key=lambda x: self.lesson_ratings[x], reverse=True)
        self.current_ratings = [{"attribute": i, "rating": self.lesson_ratings[i]} for i in sort]


    def set_preferences(self, data, length=10):
        self.lesson_vocab = [list(i.keys())[0] for i in self.sorted_data]
        self.current_lessons = self.lesson_vocab[:length if not self.data["length"] else self.data["length"]]
        return self.current_lessons


    def get_data(self, count):
        self.ratings_data()
        for _ in range(count):
            sorted_data = self.sort_ratings()
            current_lessons = self.set_preferences(sorted_data)
            test_data = self.test_data(current_lessons)

        return test_data


    def test_data(self, data):
        test = []             
                                                                                          
        
        while len(test) < len(data):
            answer = list(self.data["input"][[self.data["input"].index(i) for i in self.data["input"] if list(i.keys())[0] == data[len(test)]][0]].values())[0]["data"][0]["answer"]   
            result = random.randint(0, 1)
            test.append({"question": data[len(test)], "answer": answer}) if data[len(test)] not in test else None

        print("\n\nTest Selections\n\n")
        print(test)
        print()

        self.current_questions = test
    
        return test
    

    def get_lessons(self):
        lessons = [] 
        partial = []
        side = []
        seed = ""
        subseed = ""

        for item in self.data["input"]:
            key = list(item.keys())[0]
            for term in item[list(item.keys())[0]]["data"]:
                idx1 = self.data["input"].index(item)
                idx2 = item[list(item.keys())[0]]["data"].index(term)
                if len(lessons) < len(self.current_lessons):
                    if len([x for x in term["attributes"] if x in self.current_lessons and key == self.current_lessons[0]]) > 0:
                        lessons.append(f"{idx1:02d}{idx2:02d}")
                    elif len([x for x in term["attributes"] if x in self.current_lessons]) > 0 and len([y for y in self.current_lessons if key == y]) > 0:
                        partial.append(f"{idx1:02d}{idx2:02d}")
                    elif len([x for x in term["attributes"] if x in self.current_lessons]) > 0:
                        side.append(f"{idx1:02d}{idx2:02d}")

                seed = seed + f"{idx1:02d}{idx2:02d}"


        subseed = lessons + partial + side

        subseed = "".join(subseed)

        self.seed = subseed

        self.original_seed = seed 

        self.compressed_seed = self.compress(seed)

        self.compressed_subset = self.encode_subset_seed(seed, subseed)

        self.decoded_subset = self.decode_subset_seed(seed, self.compressed_subset)

        print("\n\n\nFull list based on ratings profile:\n")
        print(self.current_lessons)

        print("\n\n\nCompressed Tiny State format for entire list:\n")
        print(self.compressed_seed)

        print("\n\n\nCompressed seed for chosen data set:\n")
        print(self.compressed_subset)

        print("\nCompare to final list:\n")
        self.exported_data = self.current_lessons
        print(self.current_lessons)
        print("\n\n")

        return [self.compressed_seed, self.compressed_subset]


    def _encode_letters_from_int(self, n: int) -> str:
        """Encode 0 <= n < 26^3 into three uppercase letters."""
        if not (0 <= n < 26**3):
            raise ValueError("Letter block out of range")
        a = n // (26 * 26)
        b = (n // 26) % 26
        c = n % 26
        return "".join(chr(65 + x) for x in (a, b, c))


    def _decode_letters_to_int(self, letters: str) -> int:
        """Decode three uppercase letters into an integer."""
        if len(letters) != 3 or not all("A" <= ch <= "Z" for ch in letters):
            raise ValueError("Letters must be 3 A–Z characters")
        return ((ord(letters[0]) - 65) * 26 + (ord(letters[1]) - 65)) * 26 + (ord(letters[2]) - 65)


    def _encode_params(self, num_keys: int, num_items: int) -> str:
        """
        Pack (num_keys, num_items) into 'ABC12345'.

        We assume:
          1 <= num_keys <= 99
          1 <= num_items <= 99

        Encoding:
          param_index = num_keys * 100 + num_items   (max 9900)
          block_int   = param_index // 100000        (0 for these sizes)
          num_int     = param_index % 100000
          seed        = ABC + 5-digit decimal
        """
        if not (1 <= num_keys <= 99 and 1 <= num_items <= 99):
            raise ValueError("num_keys / num_items out of supported range (1–99)")

        param_index = num_keys * 100 + num_items  # max 9900

        block_int = param_index // 100000         # will be 0 here
        num_int = param_index % 100000

        letters = self._encode_letters_from_int(block_int)  # 'AAA' for now
        digits = f"{num_int:05d}"                           # 00000..99999
        return letters + digits                             # e.g. 'AAA01005'
    

    def _decode_params(self, seed: str) -> tuple[int, int]:
        """
        Inverse of _encode_params: 'ABC12345' -> (num_keys, num_items).

        NOTE:
          This only encodes the LAYOUT (grid shape), not any sparse subset.
        """
        if len(seed) != 8:
            raise ValueError("Seed must be exactly 8 characters: 'ABC12345'")

        letters = seed[:3]
        digits = seed[3:]

        if not digits.isdigit():
            raise ValueError("Last 5 characters must be digits")

        block_int = self._decode_letters_to_int(letters)
        num_int = int(digits)

        param_index = block_int * 100000 + num_int
        num_keys = param_index // 100
        num_items = param_index % 100

        if num_keys <= 0 or num_items <= 0:
            raise ValueError("Decoded invalid num_keys / num_items")

        return num_keys, num_items


    def _infer_grid_dimensions(self, s: str) -> tuple[int, int]:
        """
        From a long 'DDIIDDIIDDII...' string, infer:
          - number of distinct dict indices (num_keys)
          - number of distinct item indices (num_items)

        STRICT MODE — Assumes:
          - length is multiple of 4
          - each 4-char block is 'DDII' with 2-digit decimal ints
          - the sequence enumerates ALL (dict_idx, item_idx) in row-major:
                dict_idx 0..num_keys-1
                item_idx 0..num_items-1
            in order:
                (0,0),(0,1)...(0,num_items-1),
                (1,0)...(num_keys-1,num_items-1)
        """
        if len(s) % 4 != 0:
            raise ValueError("Input length must be a multiple of 4 (DDII blocks)")

        blocks = [s[i:i+4] for i in range(0, len(s), 4)]
        pairs = [(int(b[:2]), int(b[2:])) for b in blocks]

        dict_indices = sorted({d for d, _ in pairs})
        item_indices = sorted({i for _, i in pairs})

        if not dict_indices or dict_indices[0] != 0 or dict_indices != list(range(dict_indices[-1] + 1)):
            raise ValueError("Dict indices are not contiguous starting at 0")
        if not item_indices or item_indices[0] != 0 or item_indices != list(range(item_indices[-1] + 1)):
            raise ValueError("Item indices are not contiguous starting at 0")

        num_keys = len(dict_indices)
        num_items = len(item_indices)

        expected = [(d, i) for d in range(num_keys) for i in range(num_items)]
        if expected != pairs:
            raise ValueError("Sequence is not in row-major (dict, item) order")

        return num_keys, num_items


    def _subset_from_original(self, original: str, new: str) -> str:
        """
        Return the subset of DDII blocks from `original` that are present in `new`,
        keeping the order they appear in `original`.

        Both strings must be concatenations of 4-char 'DDII' blocks (len % 4 == 0).
        """
        if len(original) % 4 != 0 or len(new) % 4 != 0:
            raise ValueError("Strings must be multiples of 4 (DDII blocks)")

        orig_blocks = [original[i:i+4] for i in range(0, len(original), 4)]
        new_blocks = set(new[i:i+4] for i in range(0, len(new), 4))

        subset_blocks = [blk for blk in orig_blocks if blk in new_blocks]
        return "".join(subset_blocks)


    def compress(self, big_string: str) -> str:
        """
        Compress a long STRICT 'DDIIDDIIDDI...' string into 'ABC12345'.

        This expects a FULL contiguous grid in row-major order:
          - dict_idx  0..num_keys-1
          - item_idx  0..num_items-1
          - all positions present
        """
        num_keys, num_items = self._infer_grid_dimensions(big_string)
        return self._encode_params(num_keys, num_items)


    def decode(self, seed: str) -> str:
        """
        Decode 'ABC12345' back into the full STRICT 'DDIIDDIIDDI...' grid string.

        Uses the encoded (num_keys, num_items) and regenerates
        the canonical row-major order:
            for dict_idx in 0..num_keys-1:
                for item_idx in 0..num_items-1:
                    append f"{dict_idx:02d}{item_idx:02d}"
        """
        num_keys, num_items = self._decode_params(seed)

        parts = []
        for d in range(num_keys):
            for i in range(num_items):
                parts.append(f"{d:02d}{i:02d}")
        return "".join(parts)


    def _build_block_index(self, full_grid: str) -> list[str]:
        """
        Split a full-grid DDII string into blocks.

        Returns list of 4-char blocks in order. Used as the index for bitmask.
        """
        if len(full_grid) % 4 != 0:
            raise ValueError("full_grid must be a multiple of 4 characters")

        blocks = [full_grid[i:i+4] for i in range(0, len(full_grid), 4)]
        return blocks

    def encode_subset_seed(self, full_grid: str, subset: str) -> str:
        """
        Encode a sparse DDII subset as positions within the full grid,
        using a single character per position from subset_alphabet.

        - full_grid: canonical DDII full grid from decode(layout_seed)
        - subset:    sparse DDII string (blocks taken from full_grid)

        Example:
            full_grid blocks indices: 0..39
            positions [0,1,2,7,37,39] might encode as: '012Hb d'
            (depending on alphabet; with the alphabet below, it's '012Hb d'
             but without spaces: '012Hbd')
        """
        if len(full_grid) % 4 != 0 or len(subset) % 4 != 0:
            raise ValueError("Strings must be multiples of 4 (DDII blocks)")

        full_blocks = [full_grid[i:i+4] for i in range(0, len(full_grid), 4)]
        subset_blocks = [subset[i:i+4] for i in range(0, len(subset), 4)]

        n = len(full_blocks)
        if n > len(self.subset_alphabet):
            raise ValueError(
                f"Subset alphabet only supports {len(self.subset_alphabet)} positions, "
                f"but full_grid has {n}"
            )

        index_map = {blk: idx for idx, blk in enumerate(full_blocks)}

        chars = []
        for blk in subset_blocks:
            if blk not in index_map:
                raise ValueError(f"Subset block {blk!r} not found in full_grid")
            pos = index_map[blk]
            chars.append(self.subset_alphabet[pos])

        return "".join(chars)
    

    def decode_subset_seed(self, full_grid: str, compressed_subset: str) -> str:
        """
        Decode a subset seed created by encode_subset_seed back into a sparse
        DDII string, using the same full_grid.

        - full_grid: canonical DDII full grid from decode(layout_seed)
        - subset_seed: string of characters from subset_alphabet
        """
        if len(full_grid) % 4 != 0:
            raise ValueError("full_grid must be a multiple of 4 characters")

        full_blocks = [full_grid[i:i+4] for i in range(0, len(full_grid), 4)]
        n = len(full_blocks)
        if n > len(self.subset_alphabet):
            raise ValueError(
                f"Subset alphabet only supports {len(self.subset_alphabet)} positions, "
                f"but full_grid has {n}"
            )

        sparse_blocks = []
        for ch in compressed_subset:
            try:
                pos = self.subset_alphabet.index(ch)
            except ValueError:
                raise ValueError(f"Invalid subset seed character {ch!r}")

            if pos >= n:
                raise ValueError(
                    f"Subset index {pos} out of range for full_grid size {n}"
                )

            sparse_blocks.append(full_blocks[pos])

        return "".join(sparse_blocks)
    

    def decode_subset(self, layout_seed: str, compressed_subset: str) -> str:
        """
        High-level API:
          - layout_seed: ABC12345 (grid shape, used to build full_grid)
          - compressed_subset: positions-only string encoded with letters/digits

        Returns:
          Reconstructed sparse DDII string.
        """
        full_grid = self.decode(layout_seed)  
        return self.decode_subset_seed(full_grid, compressed_subset)
