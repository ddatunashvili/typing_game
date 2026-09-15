"""Expected console output for snippets, shown in the simulated run panel.

Nothing here is executed. Each entry is the output the snippet *would* print,
written by hand, plus a short demo call where the snippet only defines things.
Because every racer types the same snippet, the result is deterministic, so a
stored transcript is accurate for what it claims to be: a simulated run.

An entry is (language, marker, transcript). `marker` is any substring unique to
that snippet within its language.
"""
from typing import Dict, List, Tuple

DEMOS: List[Tuple[str, str, str]] = [
    # ---------- python ----------
    ("python", "def greet(name):", """>>> greet("world")
'hello world'"""),
    ("python", "def square(n):", """>>> square(7)
49
>>> square(-3)
9"""),
    ("python", "def word_count(text):", """>>> word_count("the cat the hat")
{'the': 2, 'cat': 1, 'hat': 1}"""),
    ("python", "def gcd(a, b):", """>>> gcd(48, 18)
6
>>> lcm(4, 6)
12"""),
    ("python", "def binary_search", """>>> binary_search([1, 3, 5, 7, 9, 11], 7)
3
>>> binary_search([1, 3, 5], 4)
-1"""),
    ("python", "class Cache:", """>>> c = Cache(limit=2)
>>> c.put("a", 1); c.put("b", 2)
>>> c.get("a")
1
>>> c.put("c", 3)   # evicts the oldest key
>>> c.get("a", "gone")
'gone'"""),
    ("python", "def retry(", """>>> @retry(times=3, delay=0.1)
... def flaky(): raise IOError("boom")
>>> flaky()
Traceback (most recent call last):
OSError: boom     # after 3 attempts"""),
    ("python", "def top_revenue", """>>> top_revenue(orders, "vip", limit=2)
[(1043, 980.5), (1017, 612.0)]"""),

    # ---------- javascript ----------
    ("javascript", "const double =", """> double(21)
42
> half(9)
4.5"""),
    ("javascript", "function greet(name)", """> greet("world")
'hello world'"""),
    ("javascript", "const unique =", """> unique([1, 2, 2, 3, 3, 3])
[ 1, 2, 3 ]
> average([2, 4, 6])
4"""),
    ("javascript", "function slugify(text)", """> slugify("  Hello, World!  ")
'hello-world'"""),
    ("javascript", 'document.querySelector("#todos")', """// click a list item
<li class="done">Buy milk</li>"""),
    ("javascript", "function debounce", """> const log = debounce(() => console.log("fired"), 200);
> log(); log(); log();
fired        // once, 200ms after the last call"""),
    ("javascript", "const groupBy =", """> groupBy([{t:"a",v:1},{t:"b",v:2},{t:"a",v:3}], "t")
{ a: [ {t:'a',v:1}, {t:'a',v:3} ], b: [ {t:'b',v:2} ] }"""),
    ("javascript", "class EventBus", """> const bus = new EventBus();
> const off = bus.on("tick", (n) => console.log("tick", n));
> bus.emit("tick", 1);
tick 1
> off(); bus.emit("tick", 2);
// nothing: the handler is gone"""),

    # ---------- typescript ----------
    ("typescript", "export function add(", """> add(2, 3)
5"""),
    ("typescript", "export function isAdmin", """> isAdmin({ id: 1, name: "ada", roles: ["admin"] })
true"""),
    ("typescript", "export const clamp", """> clamp(42, 0, 10)
10
> round(3.14159)
3.14"""),
    ("typescript", "export async function safe", """> await safe(async () => 1)
{ ok: true, value: 1 }
> await safe(async () => { throw new Error("nope") })
{ ok: false, error: 'Error: nope' }"""),
    ("typescript", "export function pluck", """> pluck([{ id: 1 }, { id: 2 }], "id")
[ 1, 2 ]"""),

    # ---------- go ----------
    ("go", "func Add(", """Add(2, 3) = 5"""),
    ("go", "func Greet(", """Greet("world") = hello world"""),
    ("go", "func Sum(", """Sum([]int{1, 2, 3, 4}) = 10"""),
    ("go", "func Reverse(", """Reverse("golang") = gnalog"""),
    ("go", "func LoadConfig", """read config.json: open config.json: no such file or directory"""),
    ("go", "func Workers(", """worker pool: 3 workers, 9 jobs
all results collected"""),

    # ---------- rust ----------
    ("rust", "fn add(", """add(2, 3) = 5"""),
    ("rust", "fn gcd(", """gcd(48, 18) = 6"""),
    ("rust", "fn largest", """largest(&[1, 7, 3]) = 7"""),
    ("rust", "fn load_port", """Err("port must be >= 1024")"""),
    ("rust", "pub fn initials", """initials("ada lovelace") = AL"""),
    ("rust", "pub fn top_words", """[("the", 3), ("cat", 2), ("sat", 1)]"""),

    # ---------- java ----------
    ("java", "public static int add", """add(2, 3) => 5"""),
    ("java", "public class Fib", """fib(10) => 55"""),
    ("java", "isPalindrome", """isPalindrome("A man, a plan, a canal: Panama") => true"""),
    ("java", "activeNames", """[ada, grace, linus]"""),

    # ---------- c ----------
    ("c", "int add(", """add(2, 3) = 5"""),
    ("c", "void hello(void)", """hello world"""),
    ("c", "int gcd(", """gcd(48, 18) = 6"""),
    ("c", "size_t str_len", """str_len("hello") = 5"""),
    ("c", "int *merge(", """merged: 1 2 3 4 5 6"""),
    ("c", "void quicksort", """sorted: 1 2 3 5 8 9"""),

    # ---------- cpp ----------
    ("cpp", "int add(", """add(2, 3) = 5"""),
    ("cpp", "int sum(const std::vector<int>", """sum = 10
sorted desc: 4 3 2 1"""),
    ("cpp", "std::vector<std::string> split", """split("a,b,c", ',') -> [a] [b] [c]"""),

    # ---------- csharp ----------
    ("csharp", "public static int Add", """Add(2, 3) => 5"""),
    ("csharp", "ActiveNames", """ada
grace
linus"""),
    ("csharp", "public static string Slugify", """Slugify("  Hello, World! ") => hello-world"""),

    # ---------- php ----------
    ("php", "function greet", """php > echo greet("world");
hello world"""),
    ("php", "function slugify", """php > echo slugify("  Hello, World!  ");
hello-world"""),
    ("php", "function average", """php > echo average([2, 4, 6]);
4"""),

    # ---------- ruby ----------
    ("ruby", "def greet(name)", """irb> greet("world")
=> "hello world\""""),
    ("ruby", "def titleize", """irb> titleize("hello wide world")
=> "Hello Wide World\""""),
    ("ruby", "def primes_below", """irb> primes_below(20)
=> [2, 3, 5, 7, 11, 13, 17, 19]"""),
    ("ruby", "class Inventory", """irb> Inventory.new([{price: 3, qty: 2}]).total
=> 6"""),

    # ---------- sql ----------
    ("sql", "SELECT id, name\nFROM users;", """ id | name
----+-------
  1 | ada
  2 | grace
  3 | linus
(3 rows)"""),
    ("sql", "SELECT COUNT(*)", """ count
-------
    42
(1 row)"""),
    ("sql", "SELECT id, name, email", """ id | name  | email
----+-------+------------------
  1 | ada   | ada@example.com
  2 | grace | grace@example.com
(2 rows)"""),
    ("sql", "INSERT INTO tags", """INSERT 0 1
UPDATE 1"""),
    ("sql", "LEFT JOIN orders", """ id | name  | order_count
----+-------+-------------
  2 | grace |           7
  1 | ada   |           4
(2 rows)"""),
    ("sql", "WITH monthly AS", """   month    | revenue
------------+----------
 2024-03-01 | 18240.00
 2024-04-01 | 21980.50
(2 rows)"""),

    # ---------- css / html ----------
    ("css", "body {", """No console output - styles applied.
body: margin 0, text #eee"""),
    ("css", ".btn {", """No console output - styles applied.
.btn: 10px 18px, radius 8px, background #4f8cff"""),
    ("css", ".center {", """No console output - styles applied.
.center: flex, centred, min-height 100vh"""),
    ("markup", "<h1>Hello</h1>", """Rendered:
  Hello
  Type this line."""),
    ("markup", 'class="hero"', """Rendered:
  Race your friends
  Type real code, not lorem ipsum.
  [ Create lobby ]"""),
    ("markup", 'class="topnav"', """Rendered:
  Home | Lobbies | Stats"""),

    # ---------- bash ----------
    ("bash", 'echo "hello world"', """$ ./hello.sh
hello world"""),
    ("bash", "for file in", """$ ./tail-logs.sh
== ./logs/app.log
[12:01:44] request finished in 31ms
== ./logs/error.log
[12:01:02] connection reset"""),
    ("bash", "DATABASE_URL", """$ ./check.sh
./check.sh: line 4: DATABASE_URL: DATABASE_URL is required"""),
    ("bash", "deploy() {", """$ deploy staging
Successfully tagged app:staging
The push refers to repository [registry.local/app]"""),
    ("bash", "SERVER_PORT", """$ ./healthcheck.sh
healthy on 25616"""),
    ("bash", "getopts", """$ ./deploy.sh -e prod -t v1.4.2
deploying v1.4.2 to prod"""),
]


def attach(snippets: Dict[str, List[dict]]) -> int:
    """Fill in `output` for every snippet with a matching demo. Returns the count."""
    filled = 0
    for language, pool in snippets.items():
        demos = [(marker, text) for lang, marker, text in DEMOS if lang == language]
        for item in pool:
            if item.get("output"):
                continue
            for marker, text in demos:
                if marker in item["code"]:
                    item["output"] = text
                    filled += 1
                    break
    return filled
