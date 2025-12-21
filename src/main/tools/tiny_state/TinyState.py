import os
import sys
import random
from random import randint

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

###takes a dictionary of items with a keys that have list values as data 

class TinyState:

    def __init__(self, list_count=10, **kwargs):
        super().__init__(**kwargs)

        self.subset_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        self.list_count = list_count
        self.subset_size = list_count * 4


        self.get_seed(self.test_data())




    def set_count(self, count):
        self.list_count = count
        self.subset_size = count * 4


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
    

    def set_preferences(self, data, length=5):
        self.preferences = list(data.keys())
        self.top_preferences = sorted(self.preferences, key=lambda x: data[x]["rating"], reverse=True)[:length]
        print("\n\nSTATESHAPER COMPRESSION DEMO\n\nThis demonstration shows how app related storage data can be reduced by over 80%.\n\n")
        print("\n\nRandom interest list has been generated. The highest rated preferences are:\n")
        print(self.top_preferences)
        print("\n\n")



    def get_seed(self, data):
        start = [] 
        partial = []
        side = []
        export = []
        seed = ""
        relevant_seed = ""
        side_seed = ""

        self.set_preferences(data)

        for interest in data.items():        
            for item in interest[1]["events"]:
                if len(start) < self.list_count:
                    idx1 = list(data.keys()).index(interest[0])
                    idx2 = interest[1]["events"].index(item)
                    seed = seed + f"{idx1:02d}{idx2:02d}"

                    if len([x for x in item["attributes"] if x in self.top_preferences and interest[0] == self.top_preferences[0]]) > 0:
                        start.append({"data": item["item"], "index": f"{idx1:02d}{idx2:02d}"})
                        export.append(item["item"])
                        relevant_seed = relevant_seed + f"{idx1:02d}{idx2:02d}"
                    elif len([x for x in item["attributes"] if x in self.top_preferences]) > 0 and len([y for y in self.top_preferences if interest[0] == y]) > 0:
                        partial.append({"data": item["item"], "index": f"{idx1:02d}{idx2:02d}"})
                    elif len([x for x in item["attributes"] if x in self.top_preferences]) > 0:
                        side.append({"data": item["item"], "index": f"{idx1:02d}{idx2:02d}"})


        self.most_relevant = len(start)
        self.partially_relevant = len(partial)

        print(f"\n\n\n{self.most_relevant} highly relevant data have been added to the list:\n")

        print(start)

        print(f"\n\n{self.partially_relevant} partially relevant data have been added to the list:\n")

        print(partial)

        while len(start) < self.list_count:
            side_place = randint(0, len(side)-1)
            side_ad = side[side_place]["data"]
            seed2 = side[side_place]["index"]

            if len(partial) > 0:
                start.append(partial[0])
                export.append(partial[0]["data"])
                relevant_seed = relevant_seed + partial[0]["index"]
                partial.pop(0) 
            else:
                start.append(side_ad)
                export.append(side_ad)
                relevant_seed = relevant_seed + seed2
            
        self.seed = relevant_seed 

        if len(self.seed) < self.list_count:
            self.seed = self.seed + side_seed[:self.subset_size-len(self.seed)]

        self.original_seed = seed 

        self.compressed_seed = self.compress(seed)

        self.compressed_subset = self.encode_subset_seed(seed, relevant_seed)

        self.decoded_subset = self.decode_subset_seed(seed, self.compressed_subset)

        print("\n\n\nFull list based on ratings profile:\n")
        print(start)

        print("\n\n\nCompressed Tiny State format for entire list:\n")
        print(self.compressed_seed)

        print("\n\n\nCompressed seed for chosen data set:\n")
        print(self.compressed_subset)

        print("\n\n\n List rebuilt from extracted seed:\n")
        print(self.rebuild_data(self.compressed_seed, self.compressed_subset))
        print("\n\n")
        
        print("\nCompare to final list:\n")
        self.exported_data = export
        print(export)
        print("\n\n")

        return [self.compressed_seed, self.compressed_subset]
    

    def rebuild_data(self, compressed_seed, compressed_subset, data=None):
        data = self.test_data()
        origin_seed = self.decode(compressed_seed)
        decoded = self.decoded = self.decode_subset_seed(origin_seed, compressed_subset)
        export = []
        while len(export)<self.list_count:
            parent = decoded[:2]
            child = decoded[2:4]
            export.append(data[list(data.keys())[int(parent)]]["events"][int(child)]["item"])
            decoded = decoded[4:]
        return export
    

    def test_data(self):
        # return {
        #     "team": {
        #         "rating": 55,
        #         "events": [
        #             {"item": "football.png", "attributes": ["team", "contact", "outdoor"]},
        #             {"item": "basketball.png", "attributes": ["team", "indoor", "fast-paced"]},
        #             {"item": "soccer.png", "attributes": ["team", "endurance", "outdoor"]}
        #         ]
        #     },

        #     "individual": {
        #         "rating": 97,
        #         "events": [
        #             {"item": "tennis.png", "attributes": ["individual", "court", "precision"]},
        #             {"item": "golf.png", "attributes": ["individual", "outdoor", "precision"]},
        #             {"item": "climbing.png", "attributes": ["individual", "strength", "indoor"]}
        #         ]
        #     },

        #     "combat": {
        #         "rating": 71,
        #         "events": [
        #             {"item": "boxing.png", "attributes": ["combat", "individual", "indoor"]},
        #             {"item": "mma.png", "attributes": ["combat", "discipline", "individual"]},
        #             {"item": "wrestling.png", "attributes": ["combat", "grappling", "mat"]}
        #         ]
        #     },

        #     "water": {
        #         "rating": 88,
        #         "events": [
        #             {"item": "swimming.png", "attributes": ["water", "endurance", "individual"]},
        #             {"item": "surfing.png", "attributes": ["water", "balance", "outdoor"]},
        #             {"item": "waterpolo.png", "attributes": ["water", "team", "endurance"]}
        #         ]
        #     },

        #     "cycling": {
        #         "rating": 66,
        #         "events": [
        #             {"item": "cycling.png", "attributes": ["cycling", "endurance", "outdoor"]},
        #             {"item": "mountain_biking.png", "attributes": ["cycling", "terrain", "outdoor"]},
        #             {"item": "bmx.png", "attributes": ["cycling", "stunts", "individual"]}
        #         ]
        #     },

        #     "track": {
        #         "rating": 59,
        #         "events": [
        #             {"item": "sprinting.png", "attributes": ["track", "speed", "individual"]},
        #             {"item": "marathon.png", "attributes": ["track", "endurance", "road"]},
        #             {"item": "relay.png", "attributes": ["track", "team", "speed"]}
        #         ]
        #     },

        #     "winter": {
        #         "rating": 66,
        #         "events": [
        #             {"item": "skiing.png", "attributes": ["winter", "outdoor", "individual"]},
        #             {"item": "snowboarding.png", "attributes": ["winter", "balance", "outdoor"]},
        #             {"item": "biathlon.png", "attributes": ["winter", "endurance", "precision"]}
        #         ]
        #     },

        #     "recreation": {
        #         "rating": 42,
        #         "events": [
        #             {"item": "skateboarding.png", "attributes": ["recreation", "balance", "stunts"]},
        #             {"item": "surfskate.png", "attributes": ["recreation", "outdoor", "balance"]},
        #             {"item": "parkour.png", "attributes": ["recreation", "agility", "urban"]}
        #         ]
        #     },

        #     "precision": {
        #         "rating": 50,
        #         "events": [
        #             {"item": "archery.png", "attributes": ["precision", "focus", "individual"]},
        #             {"item": "shooting.png", "attributes": ["precision", "control", "individual"]},
        #             {"item": "golf_putting.png", "attributes": ["precision", "technique", "individual"]}
        #         ]
        #     },

        #     "digital": {
        #         "rating": 88,
        #         "events": [
        #             {"item": "esports.png", "attributes": ["digital", "competitive", "team"]},
        #             {"item": "sim_racing.png", "attributes": ["digital", "precision", "individual"]},
        #             {"item": "virtual_chess.png", "attributes": ["digital", "strategy", "mental"]}
        #         ]
        #     }
        # }

        return {
            "strength": {
                "rating": 78,
                "events": [
                    {"item": "powerlifting.png", "attributes": ["strength", "barbell", "individual"]},
                    {"item": "strongman.png", "attributes": ["strength", "carry", "outdoor"]},
                    {"item": "weightlifting.png", "attributes": ["strength", "olympic", "precision"]}
                ]
            },

            "endurance": {
                "rating": 82,
                "events": [
                    {"item": "ultramarathon.png", "attributes": ["endurance", "distance", "road"]},
                    {"item": "cycling_stage.png", "attributes": ["endurance", "cycling", "outdoor"]},
                    {"item": "rowing.png", "attributes": ["endurance", "water", "team"]}
                ]
            },

            "speed": {
                "rating": 74,
                "events": [
                    {"item": "100m.png", "attributes": ["speed", "track", "individual"]},
                    {"item": "drag_racing.png", "attributes": ["speed", "motor", "reaction"]},
                    {"item": "speed_skating.png", "attributes": ["speed", "ice", "individual"]}
                ]
            },

            "agility": {
                "rating": 69,
                "events": [
                    {"item": "parkour.png", "attributes": ["agility", "urban", "movement"]},
                    {"item": "gymnastics.png", "attributes": ["agility", "balance", "precision"]},
                    {"item": "fencing.png", "attributes": ["agility", "combat", "reaction"]}
                ]
            },

            "balance": {
                "rating": 63,
                "events": [
                    {"item": "slackline.png", "attributes": ["balance", "control", "outdoor"]},
                    {"item": "surfing.png", "attributes": ["balance", "water", "outdoor"]},
                    {"item": "paddleboard.png", "attributes": ["balance", "water", "endurance"]}
                ]
            },

            "coordination": {
                "rating": 66,
                "events": [
                    {"item": "table_tennis.png", "attributes": ["coordination", "reaction", "indoor"]},
                    {"item": "badminton.png", "attributes": ["coordination", "speed", "court"]},
                    {"item": "juggling.png", "attributes": ["coordination", "skill", "practice"]}
                ]
            },

            "reaction": {
                "rating": 71,
                "events": [
                    {"item": "goalkeeping.png", "attributes": ["reaction", "team", "reflex"]},
                    {"item": "esports_fps.png", "attributes": ["reaction", "digital", "precision"]},
                    {"item": "boxing_mitts.png", "attributes": ["reaction", "combat", "training"]}
                ]
            },

            "precision": {
                "rating": 85,
                "events": [
                    {"item": "archery.png", "attributes": ["precision", "focus", "individual"]},
                    {"item": "darts.png", "attributes": ["precision", "aim", "indoor"]},
                    {"item": "rifle.png", "attributes": ["precision", "control", "range"]}
                ]
            },

            "strategy": {
                "rating": 88,
                "events": [
                    {"item": "chess.png", "attributes": ["strategy", "mental", "individual"]},
                    {"item": "go.png", "attributes": ["strategy", "territory", "mental"]},
                    {"item": "poker.png", "attributes": ["strategy", "probability", "competition"]}
                ]
            },

            "teamwork": {
                "rating": 76,
                "events": [
                    {"item": "basketball.png", "attributes": ["teamwork", "court", "fast-paced"]},
                    {"item": "volleyball.png", "attributes": ["teamwork", "coordination", "court"]},
                    {"item": "rowing_team.png", "attributes": ["teamwork", "endurance", "water"]}
                ]
            },

            "leadership": {
                "rating": 70,
                "events": [
                    {"item": "quarterback.png", "attributes": ["leadership", "team", "decision"]},
                    {"item": "captaincy.png", "attributes": ["leadership", "strategy", "communication"]},
                    {"item": "coach_sim.png", "attributes": ["leadership", "planning", "analysis"]}
                ]
            },

            "focus": {
                "rating": 83,
                "events": [
                    {"item": "meditative_archery.png", "attributes": ["focus", "precision", "calm"]},
                    {"item": "snooker.png", "attributes": ["focus", "aim", "indoor"]},
                    {"item": "free_throw.png", "attributes": ["focus", "routine", "control"]}
                ]
            },

            "power": {
                "rating": 79,
                "events": [
                    {"item": "shot_put.png", "attributes": ["power", "throw", "track"]},
                    {"item": "hammer_throw.png", "attributes": ["power", "rotation", "track"]},
                    {"item": "sledge_training.png", "attributes": ["power", "conditioning", "outdoor"]}
                ]
            },

            "flexibility": {
                "rating": 61,
                "events": [
                    {"item": "yoga.png", "attributes": ["flexibility", "balance", "control"]},
                    {"item": "martial_forms.png", "attributes": ["flexibility", "flow", "discipline"]},
                    {"item": "stretching.png", "attributes": ["flexibility", "recovery", "practice"]}
                ]
            },

            "stamina": {
                "rating": 77,
                "events": [
                    {"item": "boxing_rounds.png", "attributes": ["stamina", "combat", "endurance"]},
                    {"item": "crossfit.png", "attributes": ["stamina", "conditioning", "mixed"]},
                    {"item": "soccer_match.png", "attributes": ["stamina", "team", "field"]}
                ]
            },

            "control": {
                "rating": 72,
                "events": [
                    {"item": "gym_rings.png", "attributes": ["control", "strength", "gymnastics"]},
                    {"item": "balance_beam.png", "attributes": ["control", "balance", "precision"]},
                    {"item": "freestyle_ski.png", "attributes": ["control", "air", "winter"]}
                ]
            },

            "timing": {
                "rating": 68,
                "events": [
                    {"item": "baseball_hitting.png", "attributes": ["timing", "bat", "reaction"]},
                    {"item": "cricket_batting.png", "attributes": ["timing", "precision", "field"]},
                    {"item": "jump_rope.png", "attributes": ["timing", "coordination", "rhythm"]}
                ]
            },

            "rhythm": {
                "rating": 64,
                "events": [
                    {"item": "speed_bag.png", "attributes": ["rhythm", "boxing", "coordination"]},
                    {"item": "rowing_stroke.png", "attributes": ["rhythm", "team", "water"]},
                    {"item": "aerobics.png", "attributes": ["rhythm", "endurance", "movement"]}
                ]
            },

            "conditioning": {
                "rating": 75,
                "events": [
                    {"item": "interval_training.png", "attributes": ["conditioning", "intensity", "fitness"]},
                    {"item": "hill_sprints.png", "attributes": ["conditioning", "power", "outdoor"]},
                    {"item": "sled_push.png", "attributes": ["conditioning", "strength", "drive"]}
                ]
            },

            "mobility": {
                "rating": 60,
                "events": [
                    {"item": "joint_flow.png", "attributes": ["mobility", "control", "health"]},
                    {"item": "animal_moves.png", "attributes": ["mobility", "agility", "ground"]},
                    {"item": "dynamic_warmup.png", "attributes": ["mobility", "prep", "routine"]}
                ]
            },

        }
