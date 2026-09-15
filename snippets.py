"""Code snippets used as typing prompts, tagged by language, level and topic."""
from typing import Dict, Iterable, List, Optional, Sequence

LANGUAGES = [
    ("python", "Python"),
    ("javascript", "JavaScript"),
    ("typescript", "TypeScript"),
    ("go", "Go"),
    ("rust", "Rust"),
    ("java", "Java"),
    ("c", "C"),
    ("cpp", "C++"),
    ("csharp", "C#"),
    ("php", "PHP"),
    ("ruby", "Ruby"),
    ("sql", "SQL"),
    ("css", "CSS"),
    ("markup", "HTML"),
    ("bash", "Bash"),
]

# Level is about typing load: symbol density, nesting and length.
LEVELS = [
    ("very-easy", "Really easy"),
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]

TOPICS = [
    ("algorithms", "Algorithms"),
    ("data-structures", "Data structures"),
    ("strings", "Strings"),
    ("math", "Math"),
    ("async", "Async"),
    ("web", "Web & HTTP"),
    ("oop", "OOP & types"),
    ("functional", "Functional"),
    ("errors", "Error handling"),
    ("data", "Databases"),
    ("ui", "UI & markup"),
    ("devops", "Shell & DevOps"),
]

LEVEL_IDS = [lid for lid, _ in LEVELS]
TOPIC_IDS = [tid for tid, _ in TOPICS]


def normalize(code: str) -> str:
    lines = [line.rstrip() for line in code.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip("\n")


def snip(level: str, topic: str, code: str) -> dict:
    if level not in LEVEL_IDS:
        raise ValueError("unknown level: " + level)
    if topic not in TOPIC_IDS:
        raise ValueError("unknown topic: " + topic)
    return {"level": level, "topic": topic, "code": normalize(code)}


SNIPPETS: Dict[str, List[dict]] = {
    "python": [
        snip("very-easy", "strings", r'''
def greet(name):
    return "hello " + name
'''),
        snip("very-easy", "math", r'''
def square(n):
    return n * n
'''),
        snip("easy", "strings", r'''
def word_count(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
'''),
        snip("easy", "math", r'''
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0
'''),
        snip("medium", "algorithms", r'''
def binary_search(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
'''),
        snip("medium", "data-structures", r'''
class Cache:
    def __init__(self, limit=128):
        self.limit = limit
        self.store = {}

    def get(self, key, default=None):
        return self.store.get(key, default)

    def put(self, key, value):
        if len(self.store) >= self.limit:
            self.store.pop(next(iter(self.store)))
        self.store[key] = value
'''),
        snip("medium", "web", r'''
@app.get("/users/{user_id}")
async def read_user(user_id: int, include_orders: bool = False):
    user = await db.fetch_one(users.select().where(users.c.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    payload = dict(user)
    if include_orders:
        payload["orders"] = await load_orders(user_id)
    return payload
'''),
        snip("hard", "async", r'''
async def fetch_all(urls, session):
    results = []
    for url in urls:
        async with session.get(url) as resp:
            if resp.status != 200:
                continue
            payload = await resp.json()
            results.append(payload["data"])
    return sorted(results, key=lambda r: r["id"])
'''),
        snip("hard", "errors", r'''
def retry(times=3, delay=0.5, exceptions=(IOError,)):
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            last = None
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last = exc
                    time.sleep(delay * (2 ** attempt))
            raise last
        return inner
    return wrapper
'''),
        snip("hard", "functional", r'''
@dataclass(frozen=True)
class Order:
    id: int
    total: float
    tags: frozenset


def top_revenue(orders, tag, limit=5):
    matching = (o for o in orders if tag in o.tags)
    ranked = sorted(matching, key=lambda o: -o.total)
    return [(o.id, round(o.total, 2)) for o in ranked[:limit]]
'''),
    ],
    "javascript": [
        snip("very-easy", "math", r'''
const double = (n) => n * 2;

const half = (n) => n / 2;
'''),
        snip("very-easy", "strings", r'''
function greet(name) {
  return `hello ${name}`;
}
'''),
        snip("easy", "functional", r'''
const unique = (items) => [...new Set(items)];

const sum = (nums) => nums.reduce((a, b) => a + b, 0);

const average = (nums) => (nums.length ? sum(nums) / nums.length : 0);
'''),
        snip("easy", "strings", r'''
function slugify(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
'''),
        snip("easy", "ui", r'''
const list = document.querySelector("#todos");

list.addEventListener("click", (event) => {
  const item = event.target.closest("li");
  if (!item) return;
  item.classList.toggle("done");
});
'''),
        snip("medium", "functional", r'''
function debounce(fn, wait = 250) {
  let timer = null;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}
'''),
        snip("medium", "data-structures", r'''
const groupBy = (items, key) =>
  items.reduce((acc, item) => {
    const bucket = item[key];
    if (!acc[bucket]) acc[bucket] = [];
    acc[bucket].push(item);
    return acc;
  }, {});
'''),
        snip("hard", "web", r'''
async function loadUsers(page = 1) {
  const res = await fetch(`/api/users?page=${page}`);
  if (!res.ok) {
    throw new Error(`request failed: ${res.status}`);
  }
  const { data, total } = await res.json();
  return { users: data.filter((u) => u.active), total };
}
'''),
        snip("hard", "async", r'''
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
'''),
        snip("hard", "oop", r'''
class EventBus {
  #handlers = new Map();

  on(event, fn) {
    if (!this.#handlers.has(event)) this.#handlers.set(event, new Set());
    this.#handlers.get(event).add(fn);
    return () => this.off(event, fn);
  }

  off(event, fn) {
    this.#handlers.get(event)?.delete(fn);
  }

  emit(event, payload) {
    for (const fn of this.#handlers.get(event) ?? []) fn(payload);
  }
}
'''),
    ],
    "typescript": [
        snip("very-easy", "math", r'''
export function add(a: number, b: number): number {
  return a + b;
}
'''),
        snip("easy", "oop", r'''
interface User {
  id: number;
  name: string;
  roles: string[];
}

export function isAdmin(user: User): boolean {
  return user.roles.includes("admin");
}
'''),
        snip("easy", "math", r'''
export const clamp = (n: number, min: number, max: number): number =>
  Math.min(Math.max(n, min), max);

export function round(value: number, places = 2): number {
  const factor = 10 ** places;
  return Math.round(value * factor) / factor;
}
'''),
        snip("medium", "errors", r'''
type Result<T> = { ok: true; value: T } | { ok: false; error: string };

export async function safe<T>(fn: () => Promise<T>): Promise<Result<T>> {
  try {
    return { ok: true, value: await fn() };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}
'''),
        snip("medium", "data-structures", r'''
export class Registry<T> {
  private items = new Map<string, T>();

  set(key: string, value: T): this {
    this.items.set(key, value);
    return this;
  }

  get(key: string): T | undefined {
    return this.items.get(key);
  }

  get size(): number {
    return this.items.size;
  }
}
'''),
        snip("medium", "functional", r'''
export const byName = (a: User, b: User): number =>
  a.name.localeCompare(b.name);

export function partition<T>(rows: T[], keep: (row: T) => boolean): [T[], T[]] {
  const yes: T[] = [];
  const no: T[] = [];
  for (const row of rows) (keep(row) ? yes : no).push(row);
  return [yes, no];
}
'''),
        snip("hard", "oop", r'''
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type KeysOfType<T, V> = {
  [K in keyof T]-?: T[K] extends V ? K : never;
}[keyof T];

export function pluck<T, K extends keyof T>(rows: T[], key: K): T[K][] {
  return rows.map((row) => row[key]);
}
'''),
        snip("hard", "web", r'''
export async function getJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...init,
    headers: { accept: "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText} for ${url}`);
  }
  return (await res.json()) as T;
}
'''),
    ],
    "go": [
        snip("very-easy", "math", r'''
func Add(a int, b int) int {
	return a + b
}
'''),
        snip("very-easy", "strings", r'''
func Greet(name string) string {
	return "hello " + name
}
'''),
        snip("easy", "algorithms", r'''
func Sum(nums []int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}
'''),
        snip("easy", "strings", r'''
func Reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}
'''),
        snip("medium", "web", r'''
func handler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		http.Error(w, "missing id", http.StatusBadRequest)
		return
	}
	user, err := store.Find(r.Context(), id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(user)
}
'''),
        snip("medium", "errors", r'''
func LoadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read %s: %w", path, err)
	}
	cfg := &Config{}
	if err := json.Unmarshal(data, cfg); err != nil {
		return nil, fmt.Errorf("parse %s: %w", path, err)
	}
	return cfg, nil
}
'''),
        snip("medium", "data", r'''
func (s *Store) ListActive(ctx context.Context) ([]User, error) {
	rows, err := s.db.QueryContext(ctx, `SELECT id, name FROM users WHERE active`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Name); err != nil {
			return nil, err
		}
		users = append(users, u)
	}
	return users, rows.Err()
}
'''),
        snip("hard", "async", r'''
func Workers(jobs <-chan Job, n int) []Result {
	var wg sync.WaitGroup
	out := make(chan Result, n)
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for job := range jobs {
				out <- job.Run()
			}
		}()
	}
	go func() {
		wg.Wait()
		close(out)
	}()

	results := []Result{}
	for r := range out {
		results = append(results, r)
	}
	return results
}
'''),
        snip("hard", "data-structures", r'''
type Store struct {
	mu    sync.RWMutex
	items map[string][]byte
}

func (s *Store) Get(key string) ([]byte, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	v, ok := s.items[key]
	return v, ok
}

func (s *Store) Put(key string, value []byte) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.items == nil {
		s.items = make(map[string][]byte)
	}
	s.items[key] = value
}
'''),
    ],
    "rust": [
        snip("very-easy", "math", r'''
fn add(a: i32, b: i32) -> i32 {
    a + b
}
'''),
        snip("easy", "math", r'''
fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}
'''),
        snip("easy", "algorithms", r'''
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }
    largest
}
'''),
        snip("medium", "oop", r'''
#[derive(Debug, Clone)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

impl Point {
    pub fn dist(&self, other: &Point) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        (dx * dx + dy * dy).sqrt()
    }
}
'''),
        snip("medium", "errors", r'''
fn load_port(path: &str) -> Result<u16, Box<dyn Error>> {
    let raw = fs::read_to_string(path)?;
    let port: u16 = raw.trim().parse()?;
    if port < 1024 {
        return Err("port must be >= 1024".into());
    }
    Ok(port)
}
'''),
        snip("medium", "strings", r'''
pub fn initials(full_name: &str) -> String {
    full_name
        .split_whitespace()
        .filter_map(|part| part.chars().next())
        .map(|c| c.to_ascii_uppercase())
        .collect::<Vec<char>>()
        .iter()
        .collect()
}
'''),
        snip("hard", "functional", r'''
pub fn top_words(text: &str, limit: usize) -> Vec<(String, usize)> {
    let mut counts: HashMap<String, usize> = HashMap::new();
    for word in text.split_whitespace() {
        let key = word
            .trim_matches(|c: char| !c.is_alphanumeric())
            .to_lowercase();
        if key.is_empty() {
            continue;
        }
        *counts.entry(key).or_insert(0) += 1;
    }
    let mut ranked: Vec<(String, usize)> = counts.into_iter().collect();
    ranked.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
    ranked.into_iter().take(limit).collect()
}
'''),
        snip("hard", "data-structures", r'''
pub struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    pub fn new() -> Self {
        Stack { items: Vec::new() }
    }

    pub fn push(&mut self, item: T) {
        self.items.push(item);
    }

    pub fn pop(&mut self) -> Option<T> {
        self.items.pop()
    }

    pub fn peek(&self) -> Option<&T> {
        self.items.last()
    }
}
'''),
    ],
    "java": [
        snip("very-easy", "math", r'''
public static int add(int a, int b) {
    return a + b;
}
'''),
        snip("easy", "math", r'''
public class Fib {
    public static long fib(int n) {
        long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            long next = a + b;
            a = b;
            b = next;
        }
        return a;
    }
}
'''),
        snip("easy", "strings", r'''
public static boolean isPalindrome(String text) {
    String clean = text.replaceAll("[^A-Za-z0-9]", "").toLowerCase();
    int i = 0, j = clean.length() - 1;
    while (i < j) {
        if (clean.charAt(i++) != clean.charAt(j--)) {
            return false;
        }
    }
    return true;
}
'''),
        snip("medium", "functional", r'''
public List<String> activeNames(List<User> users) {
    return users.stream()
        .filter(User::isActive)
        .map(User::getName)
        .sorted()
        .collect(Collectors.toList());
}
'''),
        snip("medium", "oop", r'''
public record Invoice(long id, String customer, BigDecimal total) {

    public Invoice {
        if (total.signum() < 0) {
            throw new IllegalArgumentException("total must not be negative");
        }
    }

    public boolean isLarge() {
        return total.compareTo(BigDecimal.valueOf(1000)) > 0;
    }
}
'''),
        snip("hard", "data-structures", r'''
public class LruCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public LruCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
'''),
        snip("hard", "async", r'''
public List<Report> buildAll(List<String> ids) throws Exception {
    ExecutorService pool = Executors.newFixedThreadPool(8);
    try {
        List<CompletableFuture<Report>> futures = ids.stream()
            .map(id -> CompletableFuture.supplyAsync(() -> build(id), pool))
            .collect(Collectors.toList());
        return futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());
    } finally {
        pool.shutdown();
    }
}
'''),
    ],
    "c": [
        snip("very-easy", "math", r'''
int add(int a, int b) {
    return a + b;
}
'''),
        snip("very-easy", "strings", r'''
void hello(void) {
    printf("hello world");
}
'''),
        snip("easy", "math", r'''
int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a < 0 ? -a : a;
}
'''),
        snip("easy", "strings", r'''
size_t str_len(const char *s) {
    size_t n = 0;
    while (s[n] != '\0') {
        n++;
    }
    return n;
}
'''),
        snip("medium", "algorithms", r'''
int *merge(int *a, int n, int *b, int m) {
    int *out = malloc(sizeof(int) * (n + m));
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        out[k++] = a[i] < b[j] ? a[i++] : b[j++];
    }
    while (i < n) out[k++] = a[i++];
    while (j < m) out[k++] = b[j++];
    return out;
}
'''),
        snip("medium", "data-structures", r'''
typedef struct Node {
    int value;
    struct Node *next;
} Node;

Node *push(Node *head, int value) {
    Node *node = malloc(sizeof(Node));
    if (node == NULL) {
        return head;
    }
    node->value = value;
    node->next = head;
    return node;
}
'''),
        snip("hard", "algorithms", r'''
void quicksort(int *a, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = a[(lo + hi) / 2];
    int i = lo, j = hi;
    while (i <= j) {
        while (a[i] < pivot) i++;
        while (a[j] > pivot) j--;
        if (i <= j) {
            int t = a[i];
            a[i] = a[j];
            a[j] = t;
            i++;
            j--;
        }
    }
    quicksort(a, lo, j);
    quicksort(a, i, hi);
}
'''),
        snip("hard", "errors", r'''
int read_file(const char *path, char **out, size_t *len) {
    FILE *fp = fopen(path, "rb");
    if (fp == NULL) {
        return -1;
    }
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    rewind(fp);

    char *buf = malloc((size_t)size + 1);
    if (buf == NULL) {
        fclose(fp);
        return -1;
    }
    if (fread(buf, 1, (size_t)size, fp) != (size_t)size) {
        free(buf);
        fclose(fp);
        return -1;
    }
    buf[size] = '\0';
    fclose(fp);
    *out = buf;
    *len = (size_t)size;
    return 0;
}
'''),
    ],
    "cpp": [
        snip("very-easy", "math", r'''
int add(int a, int b) {
    return a + b;
}
'''),
        snip("easy", "algorithms", r'''
int sum(const std::vector<int> &nums) {
    return std::accumulate(nums.begin(), nums.end(), 0);
}

void sort_desc(std::vector<int> &nums) {
    std::sort(nums.begin(), nums.end(), std::greater<int>());
}
'''),
        snip("easy", "strings", r'''
std::vector<std::string> split(const std::string &text, char sep) {
    std::vector<std::string> parts;
    std::stringstream stream(text);
    std::string part;
    while (std::getline(stream, part, sep)) {
        parts.push_back(part);
    }
    return parts;
}
'''),
        snip("medium", "data-structures", r'''
template <typename T>
class Stack {
public:
    void push(const T &value) { data_.push_back(value); }

    T pop() {
        T top = data_.back();
        data_.pop_back();
        return top;
    }

    bool empty() const { return data_.empty(); }

private:
    std::vector<T> data_;
};
'''),
        snip("medium", "oop", r'''
class FileHandle {
public:
    explicit FileHandle(const std::string &path)
        : stream_(path, std::ios::binary) {
        if (!stream_) {
            throw std::runtime_error("cannot open " + path);
        }
    }

    ~FileHandle() = default;

    std::istream &stream() { return stream_; }

private:
    std::ifstream stream_;
};
'''),
        snip("hard", "functional", r'''
std::map<std::string, int> tally(const std::vector<Event> &events) {
    std::map<std::string, int> counts;
    std::for_each(events.begin(), events.end(), [&counts](const Event &e) {
        if (e.kind.empty()) return;
        counts[e.kind] += e.weight;
    });
    return counts;
}
'''),
        snip("hard", "data-structures", r'''
template <typename K, typename V>
class LruCache {
public:
    explicit LruCache(std::size_t cap) : cap_(cap) {}

    void put(const K &key, const V &value) {
        auto it = index_.find(key);
        if (it != index_.end()) {
            order_.erase(it->second);
        } else if (index_.size() >= cap_) {
            index_.erase(order_.back().first);
            order_.pop_back();
        }
        order_.emplace_front(key, value);
        index_[key] = order_.begin();
    }

private:
    std::size_t cap_;
    std::list<std::pair<K, V>> order_;
    std::unordered_map<K, typename std::list<std::pair<K, V>>::iterator> index_;
};
'''),
    ],
    "csharp": [
        snip("very-easy", "math", r'''
public static int Add(int a, int b)
{
    return a + b;
}
'''),
        snip("easy", "functional", r'''
public static IEnumerable<string> ActiveNames(IEnumerable<User> users)
{
    return users
        .Where(u => u.IsActive)
        .Select(u => u.Name)
        .OrderBy(name => name);
}
'''),
        snip("easy", "strings", r'''
public static string Slugify(string text)
{
    var lower = text.Trim().ToLowerInvariant();
    var clean = Regex.Replace(lower, "[^a-z0-9]+", "-");
    return clean.Trim('-');
}
'''),
        snip("medium", "oop", r'''
public class Repository<T> where T : class
{
    private readonly DbContext _context;

    public Repository(DbContext context)
    {
        _context = context;
    }

    public async Task<T?> FindAsync(int id)
    {
        return await _context.Set<T>().FindAsync(id);
    }
}
'''),
        snip("medium", "async", r'''
public async Task<Report> BuildAsync(int id, CancellationToken token)
{
    var response = await _http.GetAsync($"/api/orders/{id}", token);
    response.EnsureSuccessStatusCode();

    var order = await response.Content.ReadFromJsonAsync<Order>(token);
    if (order is null)
    {
        throw new InvalidOperationException($"order {id} returned no body");
    }
    return new Report(order.Id, order.Total);
}
'''),
        snip("hard", "oop", r'''
public abstract record Shape
{
    public sealed record Circle(double Radius) : Shape;
    public sealed record Rect(double W, double H) : Shape;

    public double Area() => this switch
    {
        Circle c => Math.PI * c.Radius * c.Radius,
        Rect r => r.W * r.H,
        _ => throw new NotSupportedException(GetType().Name),
    };
}
'''),
        snip("hard", "data-structures", r'''
public sealed class RingBuffer<T>
{
    private readonly T[] _items;
    private int _head;
    private int _count;

    public RingBuffer(int capacity)
    {
        _items = new T[capacity];
    }

    public void Add(T item)
    {
        _items[(_head + _count) % _items.Length] = item;
        if (_count == _items.Length)
        {
            _head = (_head + 1) % _items.Length;
        }
        else
        {
            _count++;
        }
    }
}
'''),
    ],
    "php": [
        snip("very-easy", "strings", r'''
<?php

function greet(string $name): string
{
    return "hello " . $name;
}
'''),
        snip("easy", "strings", r'''
<?php

function slugify(string $text): string
{
    $text = strtolower(trim($text));
    $text = preg_replace('/[^a-z0-9]+/', '-', $text);
    return trim($text, '-');
}
'''),
        snip("easy", "math", r'''
<?php

function average(array $numbers): float
{
    if ($numbers === []) {
        return 0.0;
    }
    return array_sum($numbers) / count($numbers);
}
'''),
        snip("medium", "oop", r'''
<?php

final class Money
{
    public function __construct(
        private readonly int $amount,
        private readonly string $currency = 'USD',
    ) {
    }

    public function plus(Money $other): self
    {
        return new self($this->amount + $other->amount, $this->currency);
    }
}
'''),
        snip("medium", "data", r'''
<?php

function findUser(PDO $db, int $id): ?array
{
    $stmt = $db->prepare('SELECT id, name, email FROM users WHERE id = :id');
    $stmt->execute(['id' => $id]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    return $row === false ? null : $row;
}
'''),
        snip("hard", "web", r'''
<?php

function dispatch(array $routes, string $method, string $path): Response
{
    foreach ($routes as $route) {
        if ($route['method'] !== $method) {
            continue;
        }
        $pattern = '#^' . preg_replace('#\{(\w+)\}#', '(?P<$1>[^/]+)', $route['path']) . '$#';
        if (preg_match($pattern, $path, $matches)) {
            return ($route['handler'])(array_filter($matches, 'is_string', ARRAY_FILTER_USE_KEY));
        }
    }
    return new Response(404, 'not found');
}
'''),
        snip("hard", "functional", r'''
<?php

final class Collection implements Countable
{
    public function __construct(private array $items = [])
    {
    }

    public function map(callable $fn): self
    {
        return new self(array_map($fn, $this->items));
    }

    public function filter(callable $fn): self
    {
        return new self(array_values(array_filter($this->items, $fn)));
    }

    public function count(): int
    {
        return count($this->items);
    }
}
'''),
    ],
    "ruby": [
        snip("very-easy", "strings", r'''
def greet(name)
  "hello #{name}"
end
'''),
        snip("easy", "strings", r'''
def titleize(text)
  text.split.map(&:capitalize).join(" ")
end

def blank?(value)
  value.nil? || value.to_s.strip.empty?
end
'''),
        snip("easy", "math", r'''
def primes_below(limit)
  (2...limit).select do |n|
    (2..Integer.sqrt(n)).none? { |d| (n % d).zero? }
  end
end
'''),
        snip("medium", "oop", r'''
class Inventory
  attr_reader :items

  def initialize(items = [])
    @items = items
  end

  def total
    items.sum { |item| item[:price] * item[:qty] }
  end

  def in_stock
    items.reject { |item| item[:qty].zero? }
  end
end
'''),
        snip("medium", "functional", r'''
def group_by_status(orders)
  orders.each_with_object({}) do |order, acc|
    (acc[order.status] ||= []) << order.id
  end
end
'''),
        snip("hard", "oop", r'''
module Trackable
  def self.included(base)
    base.extend(ClassMethods)
  end

  module ClassMethods
    def track(*fields)
      fields.each do |field|
        define_method("#{field}_changed?") do
          instance_variable_get("@old_#{field}") != public_send(field)
        end
      end
    end
  end
end
'''),
        snip("hard", "web", r'''
class OrdersController < ApplicationController
  before_action :set_order, only: %i[show update]

  def index
    orders = Order.where(user: current_user).order(created_at: :desc)
    render json: orders.limit(params.fetch(:limit, 25).to_i)
  end

  def update
    if @order.update(order_params)
      render json: @order
    else
      render json: { errors: @order.errors.full_messages }, status: :unprocessable_entity
    end
  end
end
'''),
    ],
    "sql": [
        snip("very-easy", "data", r'''
SELECT id, name
FROM users;
'''),
        snip("very-easy", "data", r'''
SELECT COUNT(*)
FROM orders
WHERE paid = true;
'''),
        snip("easy", "data", r'''
SELECT id, name, email
FROM users
WHERE active = true
ORDER BY name
LIMIT 50;
'''),
        snip("easy", "data", r'''
INSERT INTO tags (name, slug)
VALUES ('Databases', 'databases');

UPDATE users
SET last_seen_at = NOW()
WHERE id = 42;
'''),
        snip("medium", "data", r'''
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 3
ORDER BY order_count DESC
LIMIT 20;
'''),
        snip("medium", "data", r'''
WITH monthly AS (
    SELECT date_trunc('month', created_at) AS month,
           SUM(total) AS revenue
    FROM orders
    WHERE status = 'paid'
    GROUP BY 1
)
SELECT month, revenue
FROM monthly
WHERE revenue > 10000
ORDER BY month;
'''),
        snip("hard", "data", r'''
SELECT
    user_id,
    total,
    RANK() OVER (PARTITION BY user_id ORDER BY total DESC) AS rank_in_user,
    SUM(total) OVER (PARTITION BY user_id) AS lifetime_value,
    LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order_at
FROM orders
WHERE created_at >= NOW() - INTERVAL '12 months';
'''),
        snip("hard", "data", r'''
INSERT INTO daily_stats (day, plays, avg_wpm)
SELECT date_trunc('day', finished_at), COUNT(*), AVG(wpm)
FROM races
GROUP BY 1
ON CONFLICT (day) DO UPDATE
SET plays = EXCLUDED.plays,
    avg_wpm = EXCLUDED.avg_wpm;

CREATE INDEX CONCURRENTLY idx_races_finished_at ON races (finished_at DESC);
'''),
    ],
    "css": [
        snip("very-easy", "ui", r'''
body {
  margin: 0;
  color: #eee;
}
'''),
        snip("easy", "ui", r'''
.btn {
  padding: 10px 18px;
  border: 0;
  border-radius: 8px;
  background: #4f8cff;
  color: #fff;
  cursor: pointer;
}

.btn:hover {
  background: #3f78e0;
}
'''),
        snip("easy", "ui", r'''
.center {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 12px;
}
'''),
        snip("medium", "ui", r'''
.card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  background: #16181d;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
}

.card:hover {
  transform: translateY(-2px);
}
'''),
        snip("medium", "ui", r'''
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
'''),
        snip("hard", "ui", r'''
:root {
  --bg: #0e1013;
  --fg: #e6e9ef;
  --accent: #4f8cff;
  --radius: 12px;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
}

.badge[data-state="racing"] {
  animation: pulse 1.2s ease-in-out infinite;
  background: color-mix(in srgb, var(--accent) 25%, transparent);
}
'''),
        snip("hard", "ui", r'''
.form:has(input:invalid) .submit {
  opacity: 0.5;
  pointer-events: none;
}

.list > li:not(:last-child)::after {
  content: "";
  display: block;
  height: 1px;
  margin: 8px 0;
  background: linear-gradient(90deg, transparent, #2a2f3a, transparent);
}
'''),
    ],
    "markup": [
        snip("very-easy", "ui", r'''
<h1>Hello</h1>
<p>Type this line.</p>
'''),
        snip("easy", "ui", r'''
<section class="hero">
  <h1 class="title">Race your friends</h1>
  <p class="subtitle">Type real code, not lorem ipsum.</p>
  <a class="btn" href="/lobby">Create lobby</a>
</section>
'''),
        snip("easy", "ui", r'''
<nav class="topnav">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/lobby">Lobbies</a></li>
    <li><a href="/stats">Stats</a></li>
  </ul>
</nav>
'''),
        snip("medium", "ui", r'''
<form class="signup" method="post" action="/api/signup">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required autocomplete="email" />

  <label for="name">Display name</label>
  <input id="name" name="name" maxlength="18" required />

  <button type="submit">Create account</button>
</form>
'''),
        snip("medium", "ui", r'''
<table class="results">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Player</th>
      <th scope="col">WPM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>ada</td>
      <td>118</td>
    </tr>
  </tbody>
</table>
'''),
        snip("hard", "ui", r'''
<article class="post" itemscope itemtype="https://schema.org/BlogPosting">
  <header>
    <h2 itemprop="headline">Typing faster in code</h2>
    <time itemprop="datePublished" datetime="2026-09-15">15 Sep 2026</time>
  </header>
  <picture>
    <source srcset="/img/hero.avif" type="image/avif" />
    <source srcset="/img/hero.webp" type="image/webp" />
    <img src="/img/hero.png" alt="A keyboard lit from the side" loading="lazy" />
  </picture>
</article>
'''),
        snip("hard", "ui", r'''
<dialog id="settings" aria-labelledby="settings-title">
  <h2 id="settings-title">Settings</h2>
  <details open>
    <summary>Difficulty</summary>
    <fieldset>
      <legend>Levels</legend>
      <label><input type="checkbox" name="level" value="easy" checked /> Easy</label>
      <label><input type="checkbox" name="level" value="hard" /> Hard</label>
    </fieldset>
  </details>
  <button type="button" data-close="settings" aria-label="Close settings">&times;</button>
</dialog>
'''),
    ],
    "bash": [
        snip("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "hello world"
'''),
        snip("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

for file in ./logs/*.log; do
  echo "== $file"
  tail -n 5 "$file"
done
'''),
        snip("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?DATABASE_URL is required}"

if ! command -v psql >/dev/null 2>&1; then
  echo "psql not installed" >&2
  exit 1
fi
'''),
        snip("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

deploy() {
  local env="$1"
  if [[ -z "$env" ]]; then
    echo "usage: deploy <env>" >&2
    return 1
  fi
  docker build -t app:"$env" .
  docker push registry.local/app:"$env"
}
'''),
        snip("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

tar -czf "$workdir/backup.tar.gz" -C /var/lib/app data
find /backups -name '*.tar.gz' -mtime +14 -delete
mv "$workdir/backup.tar.gz" "/backups/app-$(date +%F).tar.gz"
'''),
        snip("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

port="${SERVER_PORT:-8000}"
retries=10

while (( retries > 0 )); do
  if curl -fsS "http://127.0.0.1:${port}/healthz" >/dev/null; then
    echo "healthy on ${port}"
    exit 0
  fi
  retries=$(( retries - 1 ))
  sleep 2
done

echo "service never became healthy" >&2
exit 1
'''),
        snip("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

usage() { echo "usage: $0 [-e env] [-t tag] [-v]" >&2; exit 64; }

env="staging"
tag="latest"
verbose=0

while getopts ":e:t:v" opt; do
  case "$opt" in
    e) env="$OPTARG" ;;
    t) tag="$OPTARG" ;;
    v) verbose=1 ;;
    \?) usage ;;
  esac
done
shift $(( OPTIND - 1 ))

(( verbose )) && set -x
echo "deploying ${tag} to ${env}"
'''),
    ],
}


def languages() -> List[dict]:
    return [{"id": lid, "label": label} for lid, label in LANGUAGES]


def levels() -> List[dict]:
    return [{"id": lid, "label": label} for lid, label in LEVELS]


def topics() -> List[dict]:
    return [{"id": tid, "label": label} for tid, label in TOPICS]


def clean_ids(values: Optional[Iterable[str]], allowed: Sequence[str]) -> List[str]:
    """Keep only known ids, in the canonical order, without duplicates."""
    if not values:
        return []
    wanted = {str(v).strip() for v in values}
    return [v for v in allowed if v in wanted]


def parse_ids(raw: str, allowed: Sequence[str]) -> List[str]:
    """Parse a comma-separated query-string list of ids."""
    return clean_ids((raw or "").split(","), allowed)
