"""Python snippet pack: 20 per level, the classics you would actually be asked.

Entries are (level, topic, code, expected_output). The output is a short demo
transcript for the simulated run panel - nothing is executed.
"""
LANGUAGE = "python"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
def add(a, b):
    return a + b
''', r'''>>> add(2, 3)
5'''),
    ("very-easy", "math", r'''
def is_even(n):
    return n % 2 == 0
''', r'''>>> is_even(10)
True
>>> is_even(7)
False'''),
    ("very-easy", "strings", r'''
def shout(text):
    return text.upper() + "!"
''', r'''>>> shout("hello")
'HELLO!' '''),
    ("very-easy", "strings", r'''
def reverse(text):
    return text[::-1]
''', r'''>>> reverse("python")
'nohtyp' '''),
    ("very-easy", "strings", r'''
def initials(first, last):
    return first[0] + last[0]
''', r'''>>> initials("Ada", "Lovelace")
'AL' '''),
    ("very-easy", "math", r'''
def average(numbers):
    return sum(numbers) / len(numbers)
''', r'''>>> average([2, 4, 6])
4.0'''),
    ("very-easy", "math", r'''
def celsius(f):
    return (f - 32) * 5 / 9
''', r'''>>> celsius(212)
100.0'''),
    ("very-easy", "algorithms", r'''
def largest(numbers):
    biggest = numbers[0]
    for n in numbers:
        if n > biggest:
            biggest = n
    return biggest
''', r'''>>> largest([3, 9, 4])
9'''),
    ("very-easy", "algorithms", r'''
def count_up(n):
    for i in range(1, n + 1):
        print(i)
''', r'''>>> count_up(3)
1
2
3'''),
    ("very-easy", "data-structures", r'''
def first_or_none(items):
    return items[0] if items else None
''', r'''>>> first_or_none([])
>>> first_or_none([7, 8])
7'''),
    ("very-easy", "data-structures", r'''
def merge(a, b):
    result = dict(a)
    result.update(b)
    return result
''', r'''>>> merge({"a": 1}, {"b": 2})
{'a': 1, 'b': 2}'''),
    ("very-easy", "functional", r'''
def doubled(numbers):
    return [n * 2 for n in numbers]
''', r'''>>> doubled([1, 2, 3])
[2, 4, 6]'''),
    ("very-easy", "functional", r'''
def evens(numbers):
    return [n for n in numbers if n % 2 == 0]
''', r'''>>> evens([1, 2, 3, 4])
[2, 4]'''),
    ("very-easy", "strings", r'''
def is_empty(text):
    return len(text.strip()) == 0
''', r'''>>> is_empty("   ")
True'''),
    ("very-easy", "errors", r'''
def safe_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default
''', r'''>>> safe_int("42")
42
>>> safe_int("oops")
0'''),
    ("very-easy", "oop", r'''
class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return self.name + " says woof"
''', r'''>>> Dog("Rex").speak()
'Rex says woof' '''),
    ("very-easy", "math", r'''
def clamp(n, low, high):
    return max(low, min(n, high))
''', r'''>>> clamp(42, 0, 10)
10'''),
    ("very-easy", "algorithms", r'''
def total(prices):
    running = 0
    for price in prices:
        running += price
    return running
''', r'''>>> total([1.5, 2.5, 3])
7.0'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
''', r'''>>> fizzbuzz(5)
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
''', r'''>>> [fib(i) for i in range(7)]
[0, 1, 1, 2, 3, 5, 8]'''),
    ("easy", "algorithms", r'''
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
''', r'''>>> factorial(6)
720'''),
    ("easy", "strings", r'''
def is_palindrome(text):
    clean = "".join(c.lower() for c in text if c.isalnum())
    return clean == clean[::-1]
''', r'''>>> is_palindrome("A man, a plan, a canal: Panama")
True'''),
    ("easy", "strings", r'''
def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())
''', r'''>>> is_anagram("listen", "silent")
True'''),
    ("easy", "strings", r'''
def title_case(text):
    return " ".join(word.capitalize() for word in text.split())
''', r'''>>> title_case("hello wide world")
'Hello Wide World' '''),
    ("easy", "strings", r'''
def vowel_count(text):
    return sum(1 for c in text.lower() if c in "aeiou")
''', r'''>>> vowel_count("programming")
3'''),
    ("easy", "data-structures", r'''
def unique(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
''', r'''>>> unique([1, 2, 2, 3, 1])
[1, 2, 3]'''),
    ("easy", "data-structures", r'''
def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]
''', r'''>>> chunk([1, 2, 3, 4, 5], 2)
[[1, 2], [3, 4], [5]]'''),
    ("easy", "data-structures", r'''
def flatten(nested):
    return [item for group in nested for item in group]
''', r'''>>> flatten([[1, 2], [3], [4, 5]])
[1, 2, 3, 4, 5]'''),
    ("easy", "functional", r'''
def group_by_length(words):
    groups = {}
    for word in words:
        groups.setdefault(len(word), []).append(word)
    return groups
''', r'''>>> group_by_length(["a", "bb", "cc"])
{1: ['a'], 2: ['bb', 'cc']}'''),
    ("easy", "functional", r'''
from functools import reduce

def product(numbers):
    return reduce(lambda a, b: a * b, numbers, 1)
''', r'''>>> product([2, 3, 4])
24'''),
    ("easy", "math", r'''
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True
''', r'''>>> [n for n in range(10) if is_prime(n)]
[2, 3, 5, 7]'''),
    ("easy", "math", r'''
def digits_sum(n):
    total = 0
    while n:
        total += n % 10
        n //= 10
    return total
''', r'''>>> digits_sum(1234)
10'''),
    ("easy", "oop", r'''
class Counter:
    def __init__(self):
        self.count = 0

    def bump(self, by=1):
        self.count += by
        return self.count

    def reset(self):
        self.count = 0
''', r'''>>> c = Counter()
>>> c.bump(); c.bump(3)
4'''),
    ("easy", "errors", r'''
def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b
''', r'''>>> divide(10, 2)
5.0
>>> divide(1, 0)
ValueError: cannot divide by zero'''),
    ("easy", "data", r'''
def read_rows(path):
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]
''', r'''>>> read_rows("names.txt")
['ada', 'grace', 'linus']'''),
    ("easy", "web", r'''
def build_url(base, **params):
    from urllib.parse import urlencode
    return base + "?" + urlencode(params)
''', r'''>>> build_url("/search", q="typing", page=2)
'/search?q=typing&page=2' '''),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
def bubble_sort(items):
    data = list(items)
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data
''', r'''>>> bubble_sort([5, 1, 4, 2])
[1, 2, 4, 5]'''),
    ("medium", "algorithms", r'''
def merge_sorted(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out
''', r'''>>> merge_sorted([1, 4], [2, 3, 5])
[1, 2, 3, 4, 5]'''),
    ("medium", "algorithms", r'''
def two_sum(numbers, target):
    seen = {}
    for i, n in enumerate(numbers):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None
''', r'''>>> two_sum([2, 7, 11, 15], 9)
(0, 1)'''),
    ("medium", "algorithms", r'''
def max_subarray(numbers):
    best = current = numbers[0]
    for n in numbers[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best
''', r'''>>> max_subarray([-2, 1, -3, 4, -1, 2, 1])
6'''),
    ("medium", "data-structures", r'''
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None
''', r'''>>> s = Stack()
>>> s.push(1); s.push(2); s.pop()
2'''),
    ("medium", "data-structures", r'''
class Queue:
    def __init__(self):
        from collections import deque
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        return self._items.popleft() if self._items else None

    def __len__(self):
        return len(self._items)
''', r'''>>> q = Queue()
>>> q.enqueue("a"); q.enqueue("b"); q.dequeue()
'a' '''),
    ("medium", "data-structures", r'''
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def to_list(head):
    out = []
    while head is not None:
        out.append(head.value)
        head = head.next
    return out
''', r'''>>> to_list(Node(1, Node(2, Node(3))))
[1, 2, 3]'''),
    ("medium", "strings", r'''
def word_frequencies(text, limit=3):
    from collections import Counter
    words = [w.strip(".,!?").lower() for w in text.split()]
    return Counter(w for w in words if w).most_common(limit)
''', r'''>>> word_frequencies("the cat the hat the end")
[('the', 3), ('cat', 1), ('hat', 1)]'''),
    ("medium", "strings", r'''
def caesar(text, shift):
    out = []
    for char in text:
        if char.isalpha():
            base = ord("a") if char.islower() else ord("A")
            out.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            out.append(char)
    return "".join(out)
''', r'''>>> caesar("attack at dawn", 3)
'dwwdfn dw gdzq' '''),
    ("medium", "functional", r'''
def compose(*functions):
    def inner(value):
        for fn in reversed(functions):
            value = fn(value)
        return value
    return inner
''', r'''>>> compose(str.upper, str.strip)("  hi  ")
'HI' '''),
    ("medium", "functional", r'''
def memoize(fn):
    import functools
    cache = {}

    @functools.wraps(fn)
    def inner(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return inner
''', r'''>>> slow = memoize(lambda n: n * n)
>>> slow(9); slow(9)   # second call is cached
81'''),
    ("medium", "oop", r'''
from dataclasses import dataclass, field


@dataclass
class Cart:
    items: list = field(default_factory=list)

    def add(self, name, price):
        self.items.append((name, price))

    @property
    def total(self):
        return round(sum(price for _, price in self.items), 2)
''', r'''>>> c = Cart()
>>> c.add("book", 12.5); c.add("pen", 1.5); c.total
14.0'''),
    ("medium", "oop", r'''
class Temperature:
    def __init__(self, celsius=0.0):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9
''', r'''>>> t = Temperature(100)
>>> t.fahrenheit
212.0'''),
    ("medium", "errors", r'''
class ValidationError(Exception):
    def __init__(self, field, message):
        super().__init__(f"{field}: {message}")
        self.field = field


def require(payload, *fields):
    for field in fields:
        if not payload.get(field):
            raise ValidationError(field, "is required")
    return payload
''', r'''>>> require({"name": "ada"}, "name", "email")
ValidationError: email: is required'''),
    ("medium", "data", r'''
def top_customers(rows, limit=3):
    totals = {}
    for row in rows:
        totals[row["customer"]] = totals.get(row["customer"], 0) + row["total"]
    ranked = sorted(totals.items(), key=lambda pair: -pair[1])
    return ranked[:limit]
''', r'''>>> top_customers([{"customer": "ada", "total": 20}])
[('ada', 20)]'''),
    ("medium", "data", r'''
import csv


def write_report(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "wpm"])
        writer.writeheader()
        writer.writerows(rows)
''', r'''>>> write_report("out.csv", [{"name": "ada", "wpm": 98}])
# out.csv
name,wpm
ada,98'''),
    ("medium", "web", r'''
def paginate(items, page=1, per_page=10):
    start = (page - 1) * per_page
    window = items[start:start + per_page]
    return {
        "page": page,
        "pages": (len(items) + per_page - 1) // per_page,
        "items": window,
    }
''', r'''>>> paginate(list(range(25)), page=3, per_page=10)
{'page': 3, 'pages': 3, 'items': [20, 21, 22, 23, 24]}'''),

    # --------------------------------------------------------------------- hard
    ("hard", "algorithms", r'''
def quicksort(items):
    if len(items) <= 1:
        return list(items)
    pivot = items[len(items) // 2]
    smaller = [n for n in items if n < pivot]
    equal = [n for n in items if n == pivot]
    larger = [n for n in items if n > pivot]
    return quicksort(smaller) + equal + quicksort(larger)
''', r'''>>> quicksort([3, 6, 1, 6, 2])
[1, 2, 3, 6, 6]'''),
    ("hard", "algorithms", r'''
def dijkstra(graph, start):
    import heapq
    distances = {start: 0}
    queue = [(0, start)]
    while queue:
        cost, node = heapq.heappop(queue)
        if cost > distances.get(node, float("inf")):
            continue
        for neighbour, weight in graph.get(node, {}).items():
            candidate = cost + weight
            if candidate < distances.get(neighbour, float("inf")):
                distances[neighbour] = candidate
                heapq.heappush(queue, (candidate, neighbour))
    return distances
''', r'''>>> dijkstra({"a": {"b": 1}, "b": {"c": 2}}, "a")
{'a': 0, 'b': 1, 'c': 3}'''),
    ("hard", "algorithms", r'''
def levenshtein(a, b):
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + (ca != cb),
            ))
        previous = current
    return previous[-1]
''', r'''>>> levenshtein("kitten", "sitting")
3'''),
    ("hard", "algorithms", r'''
def permutations(items):
    if len(items) <= 1:
        yield list(items)
        return
    for i, item in enumerate(items):
        rest = items[:i] + items[i + 1:]
        for tail in permutations(rest):
            yield [item] + tail
''', r'''>>> list(permutations([1, 2, 3]))[:2]
[[1, 2, 3], [1, 3, 2]]'''),
    ("hard", "data-structures", r'''
class LruCache:
    def __init__(self, capacity=128):
        from collections import OrderedDict
        self.capacity = capacity
        self._store = OrderedDict()

    def get(self, key, default=None):
        if key not in self._store:
            return default
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key, value):
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self.capacity:
            self._store.popitem(last=False)
''', r'''>>> c = LruCache(2)
>>> c.put("a", 1); c.put("b", 2); c.get("a"); c.put("c", 3)
>>> c.get("b", "evicted")
'evicted' '''),
    ("hard", "data-structures", r'''
class Trie:
    def __init__(self):
        self.children = {}
        self.word = False

    def insert(self, text):
        node = self
        for char in text:
            node = node.children.setdefault(char, Trie())
        node.word = True

    def search(self, text):
        node = self
        for char in text:
            node = node.children.get(char)
            if node is None:
                return False
        return node.word
''', r'''>>> t = Trie()
>>> t.insert("code"); t.search("code"), t.search("cod")
(True, False)'''),
    ("hard", "async", r'''
import asyncio


async def gather_limited(coros, limit=4):
    semaphore = asyncio.Semaphore(limit)

    async def run(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(run(c) for c in coros))
''', r'''>>> asyncio.run(gather_limited([sleep_then(1), sleep_then(2)]))
[1, 2]'''),
    ("hard", "async", r'''
import asyncio


async def with_timeout(coro, seconds, default=None):
    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        return default
''', r'''>>> asyncio.run(with_timeout(slow(), 0.1, default="gave up"))
'gave up' '''),
    ("hard", "async", r'''
import asyncio


class Debouncer:
    def __init__(self, delay=0.25):
        self.delay = delay
        self._task = None

    def call(self, fn, *args):
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = asyncio.create_task(self._later(fn, *args))

    async def _later(self, fn, *args):
        await asyncio.sleep(self.delay)
        fn(*args)
''', r'''>>> d = Debouncer(0.2)
>>> d.call(print, "once")
once'''),
    ("hard", "functional", r'''
def pipeline(*stages):
    def run(rows):
        for stage in stages:
            rows = stage(rows)
        return list(rows)
    return run


drop_blank = lambda rows: (r for r in rows if r.strip())
normalise = lambda rows: (r.strip().lower() for r in rows)
''', r'''>>> pipeline(drop_blank, normalise)([" Ada ", "  ", "GRACE"])
['ada', 'grace']'''),
    ("hard", "functional", r'''
import functools


def curry(fn):
    @functools.wraps(fn)
    def inner(*args):
        if len(args) >= fn.__code__.co_argcount:
            return fn(*args)
        return lambda *rest: inner(*(args + rest))
    return inner
''', r'''>>> add = curry(lambda a, b, c: a + b + c)
>>> add(1)(2)(3)
6'''),
    ("hard", "oop", r'''
class Registry:
    _handlers = {}

    @classmethod
    def register(cls, name):
        def wrap(fn):
            cls._handlers[name] = fn
            return fn
        return wrap

    @classmethod
    def dispatch(cls, name, *args):
        handler = cls._handlers.get(name)
        if handler is None:
            raise KeyError(f"no handler for {name!r}")
        return handler(*args)
''', r'''>>> @Registry.register("greet")
... def greet(who): return "hi " + who
>>> Registry.dispatch("greet", "ada")
'hi ada' '''),
    ("hard", "oop", r'''
class Meters:
    def __init__(self, value):
        self.value = float(value)

    def __add__(self, other):
        return Meters(self.value + float(other))

    def __repr__(self):
        return f"Meters({self.value:.1f})"

    def __eq__(self, other):
        return isinstance(other, Meters) and self.value == other.value
''', r'''>>> Meters(1.5) + Meters(2)
Meters(3.5)'''),
    ("hard", "errors", r'''
import contextlib


@contextlib.contextmanager
def suppress_and_log(*exceptions, logger=print):
    try:
        yield
    except exceptions as exc:
        logger(f"{type(exc).__name__}: {exc}")
''', r'''>>> with suppress_and_log(ZeroDivisionError):
...     1 / 0
ZeroDivisionError: division by zero'''),
    ("hard", "web", r'''
import json
import urllib.request


def post_json(url, payload, timeout=10):
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url, data=body, headers={"content-type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))
''', r'''>>> post_json("https://api.example.com/races", {"wpm": 98})
{'id': 1041, 'ok': True}'''),
    ("hard", "data", r'''
import sqlite3
from contextlib import closing


def leaderboard(path, limit=10):
    with closing(sqlite3.connect(path)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT name, MAX(wpm) AS best FROM races "
            "GROUP BY name ORDER BY best DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
''', r'''>>> leaderboard("races.db", limit=2)
[{'name': 'ada', 'best': 118}, {'name': 'grace', 'best': 104}]'''),
    ("hard", "math", r'''
def matrix_multiply(a, b):
    rows, inner, cols = len(a), len(b), len(b[0])
    out = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            if not a[i][k]:
                continue
            for j in range(cols):
                out[i][j] += a[i][k] * b[k][j]
    return out
''', r'''>>> matrix_multiply([[1, 2]], [[3], [4]])
[[11]]'''),
]
