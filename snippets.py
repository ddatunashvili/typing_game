"""Code snippets used as typing prompts, grouped by language."""
import random

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

SNIPPETS = {
    "python": [
        '''def binary_search(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1''',
        '''class Cache:
    def __init__(self, limit=128):
        self.limit = limit
        self.store = {}

    def get(self, key, default=None):
        return self.store.get(key, default)

    def put(self, key, value):
        if len(self.store) >= self.limit:
            self.store.pop(next(iter(self.store)))
        self.store[key] = value''',
        '''async def fetch_all(urls, session):
    results = []
    for url in urls:
        async with session.get(url) as resp:
            if resp.status != 200:
                continue
            payload = await resp.json()
            results.append(payload["data"])
    return sorted(results, key=lambda r: r["id"])''',
    ],
    "javascript": [
        '''function debounce(fn, wait = 250) {
  let timer = null;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}''',
        '''const groupBy = (items, key) =>
  items.reduce((acc, item) => {
    const bucket = item[key];
    if (!acc[bucket]) acc[bucket] = [];
    acc[bucket].push(item);
    return acc;
  }, {});''',
        '''async function loadUsers(page = 1) {
  const res = await fetch(`/api/users?page=${page}`);
  if (!res.ok) {
    throw new Error(`request failed: ${res.status}`);
  }
  const { data, total } = await res.json();
  return { users: data.filter((u) => u.active), total };
}''',
    ],
    "typescript": [
        '''interface User {
  id: number;
  name: string;
  roles: string[];
}

export function isAdmin(user: User): boolean {
  return user.roles.includes("admin");
}

export const byName = (a: User, b: User): number =>
  a.name.localeCompare(b.name);''',
        '''type Result<T> = { ok: true; value: T } | { ok: false; error: string };

export async function safe<T>(fn: () => Promise<T>): Promise<Result<T>> {
  try {
    return { ok: true, value: await fn() };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}''',
    ],
    "go": [
        '''func Sum(nums []int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}''',
        '''func handler(w http.ResponseWriter, r *http.Request) {
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
}''',
    ],
    "rust": [
        '''fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }
    largest
}''',
        '''#[derive(Debug, Clone)]
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
}''',
    ],
    "java": [
        '''public class Fib {
    public static long fib(int n) {
        long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            long next = a + b;
            a = b;
            b = next;
        }
        return a;
    }
}''',
        '''public List<String> activeNames(List<User> users) {
    return users.stream()
        .filter(User::isActive)
        .map(User::getName)
        .sorted()
        .collect(Collectors.toList());
}''',
    ],
    "c": [
        '''int *merge(int *a, int n, int *b, int m) {
    int *out = malloc(sizeof(int) * (n + m));
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        out[k++] = a[i] < b[j] ? a[i++] : b[j++];
    }
    while (i < n) out[k++] = a[i++];
    while (j < m) out[k++] = b[j++];
    return out;
}''',
    ],
    "cpp": [
        '''template <typename T>
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
};''',
    ],
    "csharp": [
        '''public class Repository<T> where T : class
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
}''',
    ],
    "php": [
        '''<?php

function slugify(string $text): string
{
    $text = strtolower(trim($text));
    $text = preg_replace('/[^a-z0-9]+/', '-', $text);
    return trim($text, '-');
}''',
    ],
    "ruby": [
        '''class Inventory
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
end''',
    ],
    "sql": [
        '''SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 3
ORDER BY order_count DESC
LIMIT 20;''',
    ],
    "css": [
        '''.card {
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
}''',
    ],
    "markup": [
        '''<section class="hero">
  <h1 class="title">Race your friends</h1>
  <p class="subtitle">Type real code, not lorem ipsum.</p>
  <a class="btn" href="/lobby">Create lobby</a>
</section>''',
    ],
    "bash": [
        '''#!/usr/bin/env bash
set -euo pipefail

deploy() {
  local env="$1"
  if [[ -z "$env" ]]; then
    echo "usage: deploy <env>" >&2
    return 1
  fi
  docker build -t app:"$env" .
  docker push registry.local/app:"$env"
}''',
    ],
}


def normalize(code: str) -> str:
    lines = [line.rstrip() for line in code.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip("\n")


def random_snippet(language: str, avoid: str = "") -> str:
    pool = SNIPPETS.get(language) or SNIPPETS["python"]
    choices = [normalize(s) for s in pool]
    options = [c for c in choices if c != avoid] or choices
    return random.choice(options)
