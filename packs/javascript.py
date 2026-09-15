"""JavaScript snippet pack: 20 per level of the things you actually write.

Entries are (level, topic, code, expected_output). The output is a short demo
transcript for the simulated run panel - nothing is executed.
"""
LANGUAGE = "javascript"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
function add(a, b) {
  return a + b;
}
''', r'''> add(2, 3)
5'''),
    ("very-easy", "math", r'''
const isEven = (n) => n % 2 === 0;
''', r'''> isEven(10)
true
> isEven(7)
false'''),
    ("very-easy", "strings", r'''
function shout(text) {
  return text.toUpperCase() + "!";
}
''', r'''> shout("hello")
'HELLO!' '''),
    ("very-easy", "strings", r'''
const reverse = (text) => text.split("").reverse().join("");
''', r'''> reverse("javascript")
'tpircsavaj' '''),
    ("very-easy", "math", r'''
function celsius(f) {
  return ((f - 32) * 5) / 9;
}
''', r'''> celsius(212)
100'''),
    ("very-easy", "math", r'''
const clamp = (n, min, max) => Math.min(Math.max(n, min), max);
''', r'''> clamp(42, 0, 10)
10'''),
    ("very-easy", "data-structures", r'''
function firstOrNull(items) {
  return items.length ? items[0] : null;
}
''', r'''> firstOrNull([])
null
> firstOrNull([7, 8])
7'''),
    ("very-easy", "data-structures", r'''
const merge = (a, b) => ({ ...a, ...b });
''', r'''> merge({ a: 1 }, { b: 2 })
{ a: 1, b: 2 }'''),
    ("very-easy", "functional", r'''
const doubled = (numbers) => numbers.map((n) => n * 2);
''', r'''> doubled([1, 2, 3])
[ 2, 4, 6 ]'''),
    ("very-easy", "functional", r'''
const evens = (numbers) => numbers.filter((n) => n % 2 === 0);
''', r'''> evens([1, 2, 3, 4])
[ 2, 4 ]'''),
    ("very-easy", "algorithms", r'''
function largest(numbers) {
  let best = numbers[0];
  for (const n of numbers) {
    if (n > best) best = n;
  }
  return best;
}
''', r'''> largest([3, 9, 4])
9'''),
    ("very-easy", "algorithms", r'''
function countUp(n) {
  for (let i = 1; i <= n; i++) {
    console.log(i);
  }
}
''', r'''> countUp(3)
1
2
3'''),
    ("very-easy", "strings", r'''
const isBlank = (text) => text.trim().length === 0;
''', r'''> isBlank("   ")
true'''),
    ("very-easy", "oop", r'''
class Dog {
  constructor(name) {
    this.name = name;
  }

  speak() {
    return this.name + " says woof";
  }
}
''', r'''> new Dog("Rex").speak()
'Rex says woof' '''),
    ("very-easy", "errors", r'''
function safeParse(text, fallback = null) {
  try {
    return JSON.parse(text);
  } catch {
    return fallback;
  }
}
''', r'''> safeParse("{bad}")
null'''),
    ("very-easy", "ui", r'''
const button = document.querySelector("#save");

button.addEventListener("click", () => {
  console.log("saved");
});
''', r'''// click the button
saved'''),
    ("very-easy", "math", r'''
const sum = (numbers) => numbers.reduce((a, b) => a + b, 0);
''', r'''> sum([1, 2, 3, 4])
10'''),
    ("very-easy", "async", r'''
function later(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
''', r'''> await later(200);
// resolves after 200ms'''),
    ("very-easy", "data-structures", r'''
const last = (items) => items[items.length - 1];
''', r'''> last([1, 2, 3])
3'''),
    ("very-easy", "strings", r'''
function initials(first, last) {
  return first[0] + last[0];
}
''', r'''> initials("Ada", "Lovelace")
'AL' '''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
function fizzbuzz(n) {
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) console.log("FizzBuzz");
    else if (i % 3 === 0) console.log("Fizz");
    else if (i % 5 === 0) console.log("Buzz");
    else console.log(i);
  }
}
''', r'''> fizzbuzz(5)
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
function fib(n) {
  let a = 0;
  let b = 1;
  for (let i = 0; i < n; i++) {
    [a, b] = [b, a + b];
  }
  return a;
}
''', r'''> [0, 1, 2, 3, 4, 5, 6].map(fib)
[ 0, 1, 1, 2, 3, 5, 8 ]'''),
    ("easy", "algorithms", r'''
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
''', r'''> factorial(6)
720'''),
    ("easy", "strings", r'''
function isPalindrome(text) {
  const clean = text.toLowerCase().replace(/[^a-z0-9]/g, "");
  return clean === [...clean].reverse().join("");
}
''', r'''> isPalindrome("A man, a plan, a canal: Panama")
true'''),
    ("easy", "strings", r'''
function isAnagram(a, b) {
  const key = (s) => [...s.toLowerCase()].sort().join("");
  return key(a) === key(b);
}
''', r'''> isAnagram("listen", "silent")
true'''),
    ("easy", "strings", r'''
function titleCase(text) {
  return text
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}
''', r'''> titleCase("hello wide world")
'Hello Wide World' '''),
    ("easy", "strings", r'''
function truncate(text, max = 20) {
  return text.length <= max ? text : text.slice(0, max - 1) + "…";
}
''', r'''> truncate("a very long sentence indeed", 12)
'a very long…' '''),
    ("easy", "data-structures", r'''
const unique = (items) => [...new Set(items)];

const counts = (items) =>
  items.reduce((acc, item) => ({ ...acc, [item]: (acc[item] || 0) + 1 }), {});
''', r'''> unique([1, 2, 2, 3])
[ 1, 2, 3 ]
> counts(["a", "b", "a"])
{ a: 2, b: 1 }'''),
    ("easy", "data-structures", r'''
function chunk(items, size) {
  const out = [];
  for (let i = 0; i < items.length; i += size) {
    out.push(items.slice(i, i + size));
  }
  return out;
}
''', r'''> chunk([1, 2, 3, 4, 5], 2)
[ [ 1, 2 ], [ 3, 4 ], [ 5 ] ]'''),
    ("easy", "data-structures", r'''
const flatten = (nested) => nested.flat(Infinity);

const zip = (a, b) => a.map((item, i) => [item, b[i]]);
''', r'''> flatten([1, [2, [3, 4]]])
[ 1, 2, 3, 4 ]
> zip([1, 2], ["a", "b"])
[ [ 1, 'a' ], [ 2, 'b' ] ]'''),
    ("easy", "functional", r'''
const sortBy = (items, key) =>
  [...items].sort((a, b) => (a[key] > b[key] ? 1 : a[key] < b[key] ? -1 : 0));
''', r'''> sortBy([{ n: 2 }, { n: 1 }], "n")
[ { n: 1 }, { n: 2 } ]'''),
    ("easy", "functional", r'''
const pick = (source, keys) =>
  Object.fromEntries(keys.filter((k) => k in source).map((k) => [k, source[k]]));
''', r'''> pick({ a: 1, b: 2, c: 3 }, ["a", "c"])
{ a: 1, c: 3 }'''),
    ("easy", "math", r'''
function isPrime(n) {
  if (n < 2) return false;
  for (let d = 2; d * d <= n; d++) {
    if (n % d === 0) return false;
  }
  return true;
}
''', r'''> [...Array(10).keys()].filter(isPrime)
[ 2, 3, 5, 7 ]'''),
    ("easy", "math", r'''
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
''', r'''> randomInt(1, 6)
4'''),
    ("easy", "oop", r'''
class Counter {
  #count = 0;

  bump(by = 1) {
    this.#count += by;
    return this.#count;
  }

  get value() {
    return this.#count;
  }
}
''', r'''> const c = new Counter();
> c.bump(); c.bump(3);
4'''),
    ("easy", "errors", r'''
function divide(a, b) {
  if (b === 0) {
    throw new RangeError("cannot divide by zero");
  }
  return a / b;
}
''', r'''> divide(10, 2)
5
> divide(1, 0)
RangeError: cannot divide by zero'''),
    ("easy", "web", r'''
function buildUrl(base, params) {
  const query = new URLSearchParams(params).toString();
  return query ? base + "?" + query : base;
}
''', r'''> buildUrl("/search", { q: "typing", page: 2 })
'/search?q=typing&page=2' '''),
    ("easy", "async", r'''
async function loadJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("HTTP " + res.status);
  return res.json();
}
''', r'''> await loadJson("/api/me")
{ name: 'ada', rating: 1240 }'''),
    ("easy", "ui", r'''
const list = document.querySelector("#todos");

list.addEventListener("click", (event) => {
  const item = event.target.closest("li");
  if (item) item.classList.toggle("done");
});
''', r'''// click a list item
<li class="done">Buy milk</li>'''),
    ("easy", "data", r'''
function toCsv(rows) {
  const header = Object.keys(rows[0]).join(",");
  const body = rows.map((row) => Object.values(row).join(","));
  return [header, ...body].join("\n");
}
''', r'''> toCsv([{ name: "ada", wpm: 98 }])
name,wpm
ada,98'''),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
function binarySearch(items, target) {
  let low = 0;
  let high = items.length - 1;
  while (low <= high) {
    const mid = (low + high) >> 1;
    if (items[mid] === target) return mid;
    if (items[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return -1;
}
''', r'''> binarySearch([1, 3, 5, 7, 9], 7)
3'''),
    ("medium", "algorithms", r'''
function quickSort(items) {
  if (items.length <= 1) return items;
  const [pivot, ...rest] = items;
  return [
    ...quickSort(rest.filter((n) => n < pivot)),
    pivot,
    ...quickSort(rest.filter((n) => n >= pivot)),
  ];
}
''', r'''> quickSort([3, 6, 1, 2])
[ 1, 2, 3, 6 ]'''),
    ("medium", "algorithms", r'''
function twoSum(numbers, target) {
  const seen = new Map();
  for (let i = 0; i < numbers.length; i++) {
    if (seen.has(target - numbers[i])) {
      return [seen.get(target - numbers[i]), i];
    }
    seen.set(numbers[i], i);
  }
  return null;
}
''', r'''> twoSum([2, 7, 11, 15], 9)
[ 0, 1 ]'''),
    ("medium", "algorithms", r'''
function maxSubarray(numbers) {
  let best = numbers[0];
  let current = numbers[0];
  for (const n of numbers.slice(1)) {
    current = Math.max(n, current + n);
    best = Math.max(best, current);
  }
  return best;
}
''', r'''> maxSubarray([-2, 1, -3, 4, -1, 2, 1])
6'''),
    ("medium", "functional", r'''
function debounce(fn, wait = 250) {
  let timer = null;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}
''', r'''> const log = debounce(() => console.log("fired"), 200);
> log(); log(); log();
fired'''),
    ("medium", "functional", r'''
function throttle(fn, wait = 200) {
  let last = 0;
  return (...args) => {
    const now = Date.now();
    if (now - last >= wait) {
      last = now;
      fn(...args);
    }
  };
}
''', r'''> const ping = throttle(() => console.log("ping"), 500);
> ping(); ping();
ping'''),
    ("medium", "functional", r'''
const groupBy = (items, key) =>
  items.reduce((acc, item) => {
    const bucket = typeof key === "function" ? key(item) : item[key];
    (acc[bucket] ||= []).push(item);
    return acc;
  }, {});
''', r'''> groupBy([1, 2, 3, 4], (n) => (n % 2 ? "odd" : "even"))
{ odd: [ 1, 3 ], even: [ 2, 4 ] }'''),
    ("medium", "functional", r'''
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) cache.set(key, fn(...args));
    return cache.get(key);
  };
}
''', r'''> const square = memoize((n) => n * n);
> square(9); square(9);
81'''),
    ("medium", "data-structures", r'''
class Stack {
  #items = [];

  push(item) {
    this.#items.push(item);
    return this;
  }

  pop() {
    if (!this.#items.length) throw new Error("stack is empty");
    return this.#items.pop();
  }

  get size() {
    return this.#items.length;
  }
}
''', r'''> new Stack().push(1).push(2).pop()
2'''),
    ("medium", "data-structures", r'''
class Queue {
  #items = new Map();
  #head = 0;
  #tail = 0;

  enqueue(item) {
    this.#items.set(this.#tail++, item);
  }

  dequeue() {
    if (this.#head === this.#tail) return undefined;
    const value = this.#items.get(this.#head);
    this.#items.delete(this.#head++);
    return value;
  }
}
''', r'''> const q = new Queue();
> q.enqueue("a"); q.enqueue("b"); q.dequeue();
'a' '''),
    ("medium", "oop", r'''
class EventBus {
  #handlers = new Map();

  on(event, fn) {
    if (!this.#handlers.has(event)) this.#handlers.set(event, new Set());
    this.#handlers.get(event).add(fn);
    return () => this.#handlers.get(event)?.delete(fn);
  }

  emit(event, payload) {
    for (const fn of this.#handlers.get(event) ?? []) fn(payload);
  }
}
''', r'''> const bus = new EventBus();
> const off = bus.on("tick", (n) => console.log("tick", n));
> bus.emit("tick", 1);
tick 1'''),
    ("medium", "async", r'''
async function retry(fn, times = 3, delay = 200) {
  let lastError;
  for (let attempt = 0; attempt < times; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      await new Promise((r) => setTimeout(r, delay * 2 ** attempt));
    }
  }
  throw lastError;
}
''', r'''> await retry(() => fetch("/flaky"))
Error: HTTP 500     // after 3 attempts'''),
    ("medium", "async", r'''
async function loadUsers(page = 1) {
  const res = await fetch(`/api/users?page=${page}`);
  if (!res.ok) {
    throw new Error(`request failed: ${res.status}`);
  }
  const { data, total } = await res.json();
  return { users: data.filter((u) => u.active), total };
}
''', r'''> await loadUsers(2)
{ users: [ { id: 4, active: true } ], total: 51 }'''),
    ("medium", "web", r'''
async function withTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}
''', r'''> await withTimeout("/slow", 100)
AbortError: The operation was aborted'''),
    ("medium", "ui", r'''
function observe(selector, onVisible) {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) onVisible(entry.target);
    }
  });
  document.querySelectorAll(selector).forEach((el) => observer.observe(el));
  return observer;
}
''', r'''> observe(".card", (el) => el.classList.add("seen"))
// each card gains .seen as it scrolls into view'''),
    ("medium", "strings", r'''
function slugify(text) {
  return text
    .normalize("NFKD")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
''', r'''> slugify("  Héllo, World!  ")
'hello-world' '''),
    ("medium", "strings", r'''
function template(text, values) {
  return text.replace(/\{(\w+)\}/g, (_, key) =>
    key in values ? String(values[key]) : `{${key}}`
  );
}
''', r'''> template("hi {name}, you are #{place}", { name: "ada", place: 1 })
'hi ada, you are #1' '''),
    ("medium", "errors", r'''
class HttpError extends Error {
  constructor(status, body) {
    super(`HTTP ${status}`);
    this.name = "HttpError";
    this.status = status;
    this.body = body;
  }

  get retryable() {
    return this.status >= 500 || this.status === 429;
  }
}
''', r'''> new HttpError(503, "busy").retryable
true'''),
    ("medium", "data", r'''
function upsert(rows, row, key = "id") {
  const index = rows.findIndex((item) => item[key] === row[key]);
  if (index === -1) return [...rows, row];
  return rows.map((item, i) => (i === index ? { ...item, ...row } : item));
}
''', r'''> upsert([{ id: 1, n: "a" }], { id: 1, n: "b" })
[ { id: 1, n: 'b' } ]'''),
    ("medium", "math", r'''
function percentile(values, p) {
  const sorted = [...values].sort((a, b) => a - b);
  const index = (sorted.length - 1) * (p / 100);
  const low = Math.floor(index);
  const high = Math.ceil(index);
  if (low === high) return sorted[low];
  return sorted[low] + (sorted[high] - sorted[low]) * (index - low);
}
''', r'''> percentile([10, 20, 30, 40], 50)
25'''),

    # --------------------------------------------------------------------- hard
    ("hard", "async", r'''
async function pool(tasks, limit = 4) {
  const running = new Set();
  const done = [];
  for (const task of tasks) {
    const p = task().then((value) => {
      running.delete(p);
      done.push(value);
    });
    running.add(p);
    if (running.size >= limit) await Promise.race(running);
  }
  await Promise.all(running);
  return done;
}
''', r'''> await pool(urls.map((u) => () => fetch(u)), 3)
[ Response, Response, Response ]'''),
    ("hard", "async", r'''
async function* paginate(url) {
  let next = url;
  while (next) {
    const res = await fetch(next);
    const { items, nextUrl } = await res.json();
    yield* items;
    next = nextUrl;
  }
}
''', r'''> for await (const item of paginate("/api/races")) console.log(item.id);
1041
1042'''),
    ("hard", "async", r'''
function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}
''', r'''> const d = deferred();
> d.resolve(42); await d.promise;
42'''),
    ("hard", "async", r'''
class Semaphore {
  #queue = [];
  #free;

  constructor(limit = 1) {
    this.#free = limit;
  }

  async acquire() {
    if (this.#free > 0) {
      this.#free -= 1;
      return;
    }
    await new Promise((resolve) => this.#queue.push(resolve));
  }

  release() {
    const next = this.#queue.shift();
    if (next) next();
    else this.#free += 1;
  }
}
''', r'''> const gate = new Semaphore(2);
> await gate.acquire(); gate.release();
// at most two holders at a time'''),
    ("hard", "data-structures", r'''
class LruCache {
  #items = new Map();

  constructor(capacity = 128) {
    this.capacity = capacity;
  }

  get(key) {
    if (!this.#items.has(key)) return undefined;
    const value = this.#items.get(key);
    this.#items.delete(key);
    this.#items.set(key, value);
    return value;
  }

  set(key, value) {
    this.#items.delete(key);
    this.#items.set(key, value);
    if (this.#items.size > this.capacity) {
      this.#items.delete(this.#items.keys().next().value);
    }
  }
}
''', r'''> const c = new LruCache(2);
> c.set("a", 1); c.set("b", 2); c.get("a"); c.set("c", 3);
> c.get("b")
undefined'''),
    ("hard", "data-structures", r'''
class Trie {
  #root = new Map();

  insert(word) {
    let node = this.#root;
    for (const char of word) {
      if (!node.has(char)) node.set(char, new Map());
      node = node.get(char);
    }
    node.set("$", true);
  }

  has(word) {
    let node = this.#root;
    for (const char of word) {
      node = node.get(char);
      if (!node) return false;
    }
    return node.has("$");
  }
}
''', r'''> const t = new Trie();
> t.insert("code"); [t.has("code"), t.has("cod")]
[ true, false ]'''),
    ("hard", "oop", r'''
const tracked = (target) =>
  new Proxy(target, {
    get(obj, key) {
      console.log("read", String(key));
      return Reflect.get(obj, key);
    },
    set(obj, key, value) {
      console.log("write", String(key), value);
      return Reflect.set(obj, key, value);
    },
  });
''', r'''> const state = tracked({ wpm: 0 });
> state.wpm = 98;
write wpm 98'''),
    ("hard", "oop", r'''
function mixin(Base, ...behaviours) {
  return behaviours.reduce((Current, behaviour) => behaviour(Current), Base);
}

const Serializable = (Base) =>
  class extends Base {
    toJSON() {
      return { ...this, type: this.constructor.name };
    }
  };
''', r'''> class Race {}
> new (mixin(Race, Serializable))().toJSON()
{ type: 'Race' }'''),
    ("hard", "functional", r'''
const curry = (fn) => {
  const collect = (...args) =>
    args.length >= fn.length ? fn(...args) : (...rest) => collect(...args, ...rest);
  return collect;
};

const pipe = (...fns) => (value) => fns.reduce((acc, fn) => fn(acc), value);
''', r'''> const add3 = curry((a, b, c) => a + b + c);
> add3(1)(2)(3)
6'''),
    ("hard", "functional", r'''
function deepEqual(a, b) {
  if (a === b) return true;
  if (typeof a !== "object" || typeof b !== "object" || !a || !b) return false;
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);
  if (keysA.length !== keysB.length) return false;
  return keysA.every((key) => deepEqual(a[key], b[key]));
}
''', r'''> deepEqual({ a: [1, { b: 2 }] }, { a: [1, { b: 2 }] })
true'''),
    ("hard", "functional", r'''
function deepFreeze(target) {
  for (const key of Object.getOwnPropertyNames(target)) {
    const value = target[key];
    if (value && typeof value === "object") deepFreeze(value);
  }
  return Object.freeze(target);
}
''', r'''> const cfg = deepFreeze({ db: { host: "localhost" } });
> cfg.db.host = "x";
TypeError: Cannot assign to read only property'''),
    ("hard", "algorithms", r'''
function levenshtein(a, b) {
  let previous = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const current = [i];
    for (let j = 1; j <= b.length; j++) {
      current[j] = Math.min(
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      );
    }
    previous = current;
  }
  return previous[b.length];
}
''', r'''> levenshtein("kitten", "sitting")
3'''),
    ("hard", "algorithms", r'''
function dijkstra(graph, start) {
  const distances = { [start]: 0 };
  const queue = [[0, start]];
  while (queue.length) {
    queue.sort((a, b) => a[0] - b[0]);
    const [cost, node] = queue.shift();
    for (const [next, weight] of Object.entries(graph[node] ?? {})) {
      const candidate = cost + weight;
      if (candidate < (distances[next] ?? Infinity)) {
        distances[next] = candidate;
        queue.push([candidate, next]);
      }
    }
  }
  return distances;
}
''', r'''> dijkstra({ a: { b: 1 }, b: { c: 2 } }, "a")
{ a: 0, b: 1, c: 3 }'''),
    ("hard", "algorithms", r'''
function* permutations(items) {
  if (items.length <= 1) {
    yield items;
    return;
  }
  for (let i = 0; i < items.length; i++) {
    const rest = [...items.slice(0, i), ...items.slice(i + 1)];
    for (const tail of permutations(rest)) {
      yield [items[i], ...tail];
    }
  }
}
''', r'''> [...permutations([1, 2, 3])].length
6'''),
    ("hard", "ui", r'''
function virtualList(container, rows, rowHeight, render) {
  const draw = () => {
    const start = Math.floor(container.scrollTop / rowHeight);
    const count = Math.ceil(container.clientHeight / rowHeight) + 1;
    container.innerHTML = "";
    for (const row of rows.slice(start, start + count)) {
      container.append(render(row));
    }
  };
  container.addEventListener("scroll", draw, { passive: true });
  draw();
}
''', r'''> virtualList(box, rows, 32, renderRow)
// only the visible ~20 rows exist in the DOM'''),
    ("hard", "ui", r'''
class Counter extends HTMLElement {
  static observedAttributes = ["value"];

  connectedCallback() {
    this.attachShadow({ mode: "open" });
    this.render();
  }

  attributeChangedCallback() {
    if (this.shadowRoot) this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `<b>${this.getAttribute("value") ?? 0}</b>`;
  }
}

customElements.define("x-counter", Counter);
''', r'''> document.body.innerHTML = '<x-counter value="7"></x-counter>';
// renders: 7'''),
    ("hard", "web", r'''
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((hit) => {
      if (hit) return hit;
      return fetch(event.request).then((res) => {
        const copy = res.clone();
        caches.open("v1").then((cache) => cache.put(event.request, copy));
        return res;
      });
    })
  );
});
''', r'''// service worker: cache first, then network
[SW] serving /static/app.js from cache'''),
    ("hard", "errors", r'''
function withErrorBoundary(fn, onError) {
  return async (...args) => {
    try {
      return await fn(...args);
    } catch (err) {
      onError(err instanceof Error ? err : new Error(String(err)));
      return undefined;
    }
  };
}
''', r'''> const safe = withErrorBoundary(boom, (e) => console.log("caught", e.message));
> await safe();
caught kaboom'''),
    ("hard", "data", r'''
function createStore(reducer, initial) {
  let state = initial;
  const listeners = new Set();
  return {
    getState: () => state,
    dispatch(action) {
      state = reducer(state, action);
      listeners.forEach((fn) => fn(state));
      return action;
    },
    subscribe(fn) {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
  };
}
''', r'''> const store = createStore((s, a) => a.type === "inc" ? s + 1 : s, 0);
> store.dispatch({ type: "inc" }); store.getState();
1'''),
    ("hard", "math", r'''
function matrixMultiply(a, b) {
  return a.map((row) =>
    b[0].map((_, j) => row.reduce((sum, value, k) => sum + value * b[k][j], 0))
  );
}
''', r'''> matrixMultiply([[1, 2]], [[3], [4]])
[ [ 11 ] ]'''),
]
