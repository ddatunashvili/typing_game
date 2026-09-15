"""Rust snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Four-space indentation, as
rustfmt writes it.
"""
LANGUAGE = "rust"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
fn add(a: i32, b: i32) -> i32 {
    a + b
}
''', r'''add(2, 3) = 5'''),
    ("very-easy", "math", r'''
fn is_even(n: i32) -> bool {
    n % 2 == 0
}
''', r'''is_even(10) = true'''),
    ("very-easy", "math", r'''
fn square(n: i64) -> i64 {
    n * n
}
''', r'''square(7) = 49'''),
    ("very-easy", "strings", r'''
fn shout(text: &str) -> String {
    format!("{}!", text.to_uppercase())
}
''', r'''shout("hello") = HELLO!'''),
    ("very-easy", "strings", r'''
fn reverse(text: &str) -> String {
    text.chars().rev().collect()
}
''', r'''reverse("rust") = tsur'''),
    ("very-easy", "strings", r'''
fn greet(name: &str) -> String {
    format!("hello {name}")
}
''', r'''greet("world") = hello world'''),
    ("very-easy", "strings", r'''
fn is_blank(text: &str) -> bool {
    text.trim().is_empty()
}
''', r'''is_blank("   ") = true'''),
    ("very-easy", "math", r'''
fn clamp(n: i32, low: i32, high: i32) -> i32 {
    n.max(low).min(high)
}
''', r'''clamp(42, 0, 10) = 10'''),
    ("very-easy", "algorithms", r'''
fn sum(nums: &[i32]) -> i32 {
    let mut total = 0;
    for n in nums {
        total += n;
    }
    total
}
''', r'''sum(&[1, 2, 3, 4]) = 10'''),
    ("very-easy", "algorithms", r'''
fn count_up(n: u32) {
    for i in 1..=n {
        println!("{i}");
    }
}
''', r'''count_up(3)
1
2
3'''),
    ("very-easy", "functional", r'''
fn doubled(nums: &[i32]) -> Vec<i32> {
    nums.iter().map(|n| n * 2).collect()
}
''', r'''doubled(&[1, 2, 3]) = [2, 4, 6]'''),
    ("very-easy", "functional", r'''
fn evens(nums: &[i32]) -> Vec<i32> {
    nums.iter().copied().filter(|n| n % 2 == 0).collect()
}
''', r'''evens(&[1, 2, 3, 4]) = [2, 4]'''),
    ("very-easy", "data-structures", r'''
fn names() -> Vec<String> {
    vec!["ada".to_string(), "grace".to_string()]
}
''', r'''names() = ["ada", "grace"]'''),
    ("very-easy", "data-structures", r'''
fn first(nums: &[i32]) -> Option<&i32> {
    nums.first()
}
''', r'''first(&[]) = None'''),
    ("very-easy", "oop", r'''
struct Dog {
    name: String,
}

impl Dog {
    fn speak(&self) -> String {
        format!("{} says woof", self.name)
    }
}
''', r'''Dog { name: "Rex" }.speak() = Rex says woof'''),
    ("very-easy", "oop", r'''
#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn manhattan(&self) -> i32 {
        self.x.abs() + self.y.abs()
    }
}
''', r'''Point { x: 3, y: -4 }.manhattan() = 7'''),
    ("very-easy", "errors", r'''
fn safe_parse(text: &str, fallback: i32) -> i32 {
    text.parse().unwrap_or(fallback)
}
''', r'''safe_parse("oops", 0) = 0'''),
    ("very-easy", "errors", r'''
fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        None
    } else {
        Some(a / b)
    }
}
''', r'''divide(1.0, 0.0) = None'''),
    ("very-easy", "math", r'''
fn average(nums: &[f64]) -> f64 {
    if nums.is_empty() {
        return 0.0;
    }
    nums.iter().sum::<f64>() / nums.len() as f64
}
''', r'''average(&[2.0, 4.0, 6.0]) = 4.0'''),
    ("very-easy", "strings", r'''
fn initials(first: &str, last: &str) -> String {
    first.chars().take(1).chain(last.chars().take(1)).collect()
}
''', r'''initials("Ada", "Lovelace") = AL'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
fn fizzbuzz(n: u32) {
    for i in 1..=n {
        match (i % 3, i % 5) {
            (0, 0) => println!("FizzBuzz"),
            (0, _) => println!("Fizz"),
            (_, 0) => println!("Buzz"),
            _ => println!("{i}"),
        }
    }
}
''', r'''fizzbuzz(5)
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
fn fib(n: u32) -> u64 {
    let (mut a, mut b) = (0u64, 1u64);
    for _ in 0..n {
        let next = a + b;
        a = b;
        b = next;
    }
    a
}
''', r'''fib(10) = 55'''),
    ("easy", "algorithms", r'''
fn factorial(n: u64) -> u64 {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
''', r'''factorial(6) = 720'''),
    ("easy", "algorithms", r'''
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }
    largest
}
''', r'''largest(&[1, 7, 3]) = 7'''),
    ("easy", "strings", r'''
fn is_palindrome(text: &str) -> bool {
    let clean: Vec<char> = text
        .chars()
        .filter(|c| c.is_alphanumeric())
        .map(|c| c.to_ascii_lowercase())
        .collect();
    clean.iter().eq(clean.iter().rev())
}
''', r'''is_palindrome("A man, a plan, a canal: Panama") = true'''),
    ("easy", "strings", r'''
fn title_case(text: &str) -> String {
    text.split_whitespace()
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
                None => String::new(),
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}
''', r'''title_case("hello wide world") = Hello Wide World'''),
    ("easy", "strings", r'''
pub fn initials(full_name: &str) -> String {
    full_name
        .split_whitespace()
        .filter_map(|part| part.chars().next())
        .map(|c| c.to_ascii_uppercase())
        .collect()
}
''', r'''initials("ada lovelace") = AL'''),
    ("easy", "data-structures", r'''
fn unique(items: &[i32]) -> Vec<i32> {
    let mut seen = HashSet::new();
    items
        .iter()
        .copied()
        .filter(|item| seen.insert(*item))
        .collect()
}
''', r'''unique(&[1, 2, 2, 3]) = [1, 2, 3]'''),
    ("easy", "data-structures", r'''
fn chunk(items: &[i32], size: usize) -> Vec<Vec<i32>> {
    items.chunks(size).map(|c| c.to_vec()).collect()
}
''', r'''chunk(&[1, 2, 3, 4, 5], 2) = [[1, 2], [3, 4], [5]]'''),
    ("easy", "data-structures", r'''
fn word_count(text: &str) -> HashMap<&str, usize> {
    let mut counts = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }
    counts
}
''', r'''word_count("the cat the") = {"the": 2, "cat": 1}'''),
    ("easy", "math", r'''
fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}
''', r'''gcd(48, 18) = 6'''),
    ("easy", "math", r'''
fn is_prime(n: u64) -> bool {
    if n < 2 {
        return false;
    }
    let mut d = 2;
    while d * d <= n {
        if n % d == 0 {
            return false;
        }
        d += 1;
    }
    true
}
''', r'''is_prime(97) = true'''),
    ("easy", "oop", r'''
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
''', r'''Point { x: 0.0, y: 0.0 }.dist(&Point { x: 3.0, y: 4.0 }) = 5.0'''),
    ("easy", "oop", r'''
#[derive(Default)]
struct Counter {
    count: u32,
}

impl Counter {
    fn bump(&mut self, by: u32) -> u32 {
        self.count += by;
        self.count
    }
}
''', r'''Counter::default().bump(3) = 3'''),
    ("easy", "errors", r'''
fn load_port(path: &str) -> Result<u16, Box<dyn Error>> {
    let raw = fs::read_to_string(path)?;
    let port: u16 = raw.trim().parse()?;
    if port < 1024 {
        return Err("port must be >= 1024".into());
    }
    Ok(port)
}
''', r'''load_port("port.txt") = Err("port must be >= 1024")'''),
    ("easy", "errors", r'''
fn first_line(text: &str) -> Result<&str, String> {
    text.lines()
        .next()
        .ok_or_else(|| "the text is empty".to_string())
}
''', r'''first_line("") = Err("the text is empty")'''),
    ("easy", "functional", r'''
fn sum_of_squares(nums: &[i32]) -> i32 {
    nums.iter().map(|n| n * n).sum()
}

fn any_negative(nums: &[i32]) -> bool {
    nums.iter().any(|n| *n < 0)
}
''', r'''sum_of_squares(&[1, 2, 3]) = 14'''),
    ("easy", "functional", r'''
fn partition(nums: &[i32]) -> (Vec<i32>, Vec<i32>) {
    nums.iter().partition(|n| *n % 2 == 0)
}
''', r'''partition(&[1, 2, 3, 4]) = ([2, 4], [1, 3])'''),
    ("easy", "data", r'''
fn read_lines(path: &str) -> io::Result<Vec<String>> {
    let file = File::open(path)?;
    BufReader::new(file).lines().collect()
}
''', r'''read_lines("names.txt") = Ok(["ada", "grace"])'''),
    ("easy", "oop", r'''
enum Status {
    Waiting,
    Racing,
    Finished { wpm: u32 },
}

fn describe(status: &Status) -> String {
    match status {
        Status::Waiting => "waiting".to_string(),
        Status::Racing => "racing".to_string(),
        Status::Finished { wpm } => format!("finished at {wpm} wpm"),
    }
}
''', r'''describe(&Status::Finished { wpm: 98 }) = finished at 98 wpm'''),

    ("easy", "math", r"""
fn sum_to(n: u64) -> u64 {
    (1..=n).sum()
}
""", r"""sum_to(10) = 55"""),
    ("easy", "data-structures", r"""
fn most_common(items: &[&str]) -> Option<String> {
    let mut counts: HashMap<&str, usize> = HashMap::new();
    for item in items {
        *counts.entry(item).or_insert(0) += 1;
    }
    counts
        .into_iter()
        .max_by_key(|(_, count)| *count)
        .map(|(item, _)| item.to_string())
}
""", r"""most_common(&["a", "b", "a"]) = Some("a")"""),
    ("easy", "functional", r"""
fn running_total(nums: &[i32]) -> Vec<i32> {
    nums.iter()
        .scan(0, |acc, n| {
            *acc += n;
            Some(*acc)
        })
        .collect()
}
""", r"""running_total(&[1, 2, 3]) = [1, 3, 6]"""),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
fn binary_search(items: &[i32], target: i32) -> Option<usize> {
    let mut low = 0usize;
    let mut high = items.len();
    while low < high {
        let mid = low + (high - low) / 2;
        match items[mid].cmp(&target) {
            Ordering::Equal => return Some(mid),
            Ordering::Less => low = mid + 1,
            Ordering::Greater => high = mid,
        }
    }
    None
}
''', r'''binary_search(&[1, 3, 5, 7], 5) = Some(2)'''),
    ("medium", "algorithms", r'''
fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    let mut seen: HashMap<i32, usize> = HashMap::new();
    for (i, n) in nums.iter().enumerate() {
        if let Some(&j) = seen.get(&(target - n)) {
            return Some((j, i));
        }
        seen.insert(*n, i);
    }
    None
}
''', r'''two_sum(&[2, 7, 11], 9) = Some((0, 1))'''),
    ("medium", "algorithms", r'''
fn max_subarray(nums: &[i32]) -> i32 {
    let mut best = nums[0];
    let mut current = nums[0];
    for &n in &nums[1..] {
        current = n.max(current + n);
        best = best.max(current);
    }
    best
}
''', r'''max_subarray(&[-2, 1, -3, 4, -1, 2, 1]) = 6'''),
    ("medium", "algorithms", r'''
fn merge_sorted(left: &[i32], right: &[i32]) -> Vec<i32> {
    let mut out = Vec::with_capacity(left.len() + right.len());
    let (mut i, mut j) = (0, 0);
    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            out.push(left[i]);
            i += 1;
        } else {
            out.push(right[j]);
            j += 1;
        }
    }
    out.extend_from_slice(&left[i..]);
    out.extend_from_slice(&right[j..]);
    out
}
''', r'''merge_sorted(&[1, 4], &[2, 3, 5]) = [1, 2, 3, 4, 5]'''),
    ("medium", "data-structures", r'''
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
''', r'''push(1); push(2); pop() = Some(2)'''),
    ("medium", "data-structures", r'''
pub struct Queue<T> {
    items: VecDeque<T>,
}

impl<T> Queue<T> {
    pub fn new() -> Self {
        Queue {
            items: VecDeque::new(),
        }
    }

    pub fn enqueue(&mut self, item: T) {
        self.items.push_back(item);
    }

    pub fn dequeue(&mut self) -> Option<T> {
        self.items.pop_front()
    }
}
''', r'''enqueue("a"); enqueue("b"); dequeue() = Some("a")'''),
    ("medium", "data-structures", r'''
#[derive(Debug)]
enum Tree {
    Leaf(i32),
    Node(Box<Tree>, Box<Tree>),
}

fn total(tree: &Tree) -> i32 {
    match tree {
        Tree::Leaf(value) => *value,
        Tree::Node(left, right) => total(left) + total(right),
    }
}
''', r'''total(&Tree::Node(Leaf(1).into(), Leaf(2).into())) = 3'''),
    ("medium", "functional", r'''
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
''', r'''top_words("the cat the hat the end", 2) = [("the", 3), ("cat", 1)]'''),
    ("medium", "functional", r'''
fn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {
    words.iter().fold(BTreeMap::new(), |mut acc, word| {
        acc.entry(word.len()).or_insert_with(Vec::new).push(word.to_string());
        acc
    })
}
''', r'''group_by_len(&["a", "bb", "cc"]) = {1: ["a"], 2: ["bb", "cc"]}'''),
    ("medium", "oop", r'''
trait Shape {
    fn area(&self) -> f64;

    fn describe(&self) -> String {
        format!("area {:.2}", self.area())
    }
}

struct Rect {
    w: f64,
    h: f64,
}

impl Shape for Rect {
    fn area(&self) -> f64 {
        self.w * self.h
    }
}
''', r'''Rect { w: 3.0, h: 4.0 }.describe() = area 12.00'''),
    ("medium", "oop", r'''
#[derive(Debug, Default)]
struct ServerBuilder {
    port: u16,
    host: String,
}

impl ServerBuilder {
    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    fn host(mut self, host: &str) -> Self {
        self.host = host.to_string();
        self
    }

    fn build(self) -> String {
        format!("{}:{}", self.host, self.port)
    }
}
''', r'''ServerBuilder::default().host("0.0.0.0").port(25616).build()
0.0.0.0:25616'''),
    ("medium", "errors", r'''
#[derive(Debug)]
enum ConfigError {
    Missing(String),
    Invalid { field: String, reason: String },
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConfigError::Missing(field) => write!(f, "{field} is required"),
            ConfigError::Invalid { field, reason } => write!(f, "{field}: {reason}"),
        }
    }
}
''', r'''ConfigError::Missing("port".into()) => port is required'''),
    ("medium", "errors", r'''
fn parse_all(values: &[&str]) -> Result<Vec<i32>, ParseIntError> {
    values.iter().map(|v| v.parse::<i32>()).collect()
}
''', r'''parse_all(&["1", "x"]) = Err(ParseIntError { kind: InvalidDigit })'''),
    ("medium", "async", r'''
async fn fetch_all(urls: Vec<String>) -> Vec<String> {
    let mut handles = Vec::new();
    for url in urls {
        handles.push(tokio::spawn(async move { fetch(url).await }));
    }
    let mut out = Vec::new();
    for handle in handles {
        if let Ok(Ok(body)) = handle.await {
            out.push(body);
        }
    }
    out
}
''', r'''fetch_all(urls).await => bodies of whichever requests succeeded'''),
    ("medium", "async", r'''
async fn with_timeout(work: impl Future<Output = u32>, ms: u64) -> Option<u32> {
    match tokio::time::timeout(Duration::from_millis(ms), work).await {
        Ok(value) => Some(value),
        Err(_) => None,
    }
}
''', r'''with_timeout(slow(), 100).await = None'''),
    ("medium", "strings", r'''
fn slugify(text: &str) -> String {
    let mut out = String::new();
    let mut dash = true;
    for c in text.chars() {
        if c.is_alphanumeric() {
            out.extend(c.to_lowercase());
            dash = false;
        } else if !dash {
            out.push('-');
            dash = true;
        }
    }
    out.trim_matches('-').to_string()
}
''', r'''slugify("  Hello, World!  ") = hello-world'''),
    ("medium", "data", r'''
#[derive(Debug, Serialize, Deserialize)]
struct Race {
    id: u64,
    wpm: f64,
    language: String,
}

fn best(races: &[Race]) -> Option<&Race> {
    races.iter().max_by(|a, b| a.wpm.total_cmp(&b.wpm))
}
''', r'''best(&races) = Some(Race { id: 2, wpm: 104.0, .. })'''),
    ("medium", "math", r'''
fn percentile(values: &[f64], p: f64) -> f64 {
    let mut sorted = values.to_vec();
    sorted.sort_by(f64::total_cmp);
    let index = (sorted.len() - 1) as f64 * p / 100.0;
    let low = index.floor() as usize;
    let high = index.ceil() as usize;
    if low == high {
        return sorted[low];
    }
    sorted[low] + (sorted[high] - sorted[low]) * (index - low as f64)
}
''', r'''percentile(&[10.0, 20.0, 30.0, 40.0], 50.0) = 25.0'''),
    ("medium", "web", r'''
async fn handler(Path(id): Path<u64>) -> Result<Json<Race>, StatusCode> {
    match load_race(id).await {
        Some(race) => Ok(Json(race)),
        None => Err(StatusCode::NOT_FOUND),
    }
}
''', r'''GET /races/99 => 404 Not Found'''),
    ("medium", "functional", r'''
fn pipeline(text: &str) -> Vec<String> {
    text.lines()
        .map(str::trim)
        .filter(|line| !line.is_empty())
        .map(str::to_lowercase)
        .collect()
}
''', r'''pipeline(" Ada \n\n GRACE ") = ["ada", "grace"]'''),

    # --------------------------------------------------------------------- hard
    ("hard", "data-structures", r'''
pub struct LruCache<K, V> {
    capacity: usize,
    map: HashMap<K, V>,
    order: VecDeque<K>,
}

impl<K: Eq + Hash + Clone, V> LruCache<K, V> {
    pub fn put(&mut self, key: K, value: V) {
        if self.map.insert(key.clone(), value).is_none() && self.map.len() > self.capacity {
            if let Some(oldest) = self.order.pop_front() {
                self.map.remove(&oldest);
            }
        }
        self.order.retain(|k| k != &key);
        self.order.push_back(key);
    }
}
''', r'''capacity 2: put a, put b, put c => a evicted'''),
    ("hard", "data-structures", r'''
#[derive(Default)]
pub struct Trie {
    children: HashMap<char, Trie>,
    word: bool,
}

impl Trie {
    pub fn insert(&mut self, text: &str) {
        let mut node = self;
        for c in text.chars() {
            node = node.children.entry(c).or_default();
        }
        node.word = true;
    }

    pub fn contains(&self, text: &str) -> bool {
        let mut node = self;
        for c in text.chars() {
            match node.children.get(&c) {
                Some(child) => node = child,
                None => return false,
            }
        }
        node.word
    }
}
''', r'''insert("code"); contains("code") = true; contains("cod") = false'''),
    ("hard", "data-structures", r'''
pub struct RingBuffer<T> {
    items: Vec<Option<T>>,
    head: usize,
    len: usize,
}

impl<T> RingBuffer<T> {
    pub fn with_capacity(capacity: usize) -> Self {
        RingBuffer {
            items: (0..capacity).map(|_| None).collect(),
            head: 0,
            len: 0,
        }
    }

    pub fn push(&mut self, item: T) {
        let slot = (self.head + self.len) % self.items.len();
        self.items[slot] = Some(item);
        if self.len == self.items.len() {
            self.head = (self.head + 1) % self.items.len();
        } else {
            self.len += 1;
        }
    }
}
''', r'''with_capacity(3), push 1..4 => oldest dropped'''),
    ("hard", "algorithms", r'''
fn levenshtein(a: &str, b: &str) -> usize {
    let b: Vec<char> = b.chars().collect();
    let mut previous: Vec<usize> = (0..=b.len()).collect();
    for (i, ca) in a.chars().enumerate() {
        let mut current = vec![i + 1];
        for (j, cb) in b.iter().enumerate() {
            let cost = usize::from(ca != *cb);
            current.push(
                (previous[j + 1] + 1)
                    .min(current[j] + 1)
                    .min(previous[j] + cost),
            );
        }
        previous = current;
    }
    previous[b.len()]
}
''', r'''levenshtein("kitten", "sitting") = 3'''),
    ("hard", "algorithms", r'''
fn dijkstra(graph: &HashMap<&str, Vec<(&str, u32)>>, start: &str) -> HashMap<String, u32> {
    let mut distances: HashMap<String, u32> = HashMap::new();
    let mut heap = BinaryHeap::new();
    distances.insert(start.to_string(), 0);
    heap.push(Reverse((0u32, start.to_string())));

    while let Some(Reverse((cost, node))) = heap.pop() {
        if cost > *distances.get(&node).unwrap_or(&u32::MAX) {
            continue;
        }
        for (next, weight) in graph.get(node.as_str()).unwrap_or(&vec![]) {
            let candidate = cost + weight;
            if candidate < *distances.get(*next).unwrap_or(&u32::MAX) {
                distances.insert(next.to_string(), candidate);
                heap.push(Reverse((candidate, next.to_string())));
            }
        }
    }
    distances
}
''', r'''dijkstra(&graph, "a") = {"a": 0, "b": 1, "c": 3}'''),
    ("hard", "algorithms", r'''
fn quicksort<T: PartialOrd + Copy>(items: &mut [T]) {
    if items.len() < 2 {
        return;
    }
    let pivot = items[items.len() / 2];
    let (mut left, mut right) = (0usize, items.len() - 1);
    loop {
        while items[left] < pivot {
            left += 1;
        }
        while items[right] > pivot {
            right -= 1;
        }
        if left >= right {
            break;
        }
        items.swap(left, right);
        left += 1;
        if right > 0 {
            right -= 1;
        }
    }
    let (a, b) = items.split_at_mut(left);
    quicksort(a);
    quicksort(b);
}
''', r'''[3, 6, 1, 8, 2] => [1, 2, 3, 6, 8]'''),
    ("hard", "oop", r'''
trait Plugin: Send + Sync {
    fn name(&self) -> &str;
    fn run(&self, input: &str) -> String;
}

struct Registry {
    plugins: Vec<Box<dyn Plugin>>,
}

impl Registry {
    fn dispatch(&self, name: &str, input: &str) -> Option<String> {
        self.plugins
            .iter()
            .find(|plugin| plugin.name() == name)
            .map(|plugin| plugin.run(input))
    }
}
''', r'''dispatch("upper", "hi") = Some("HI")'''),
    ("hard", "oop", r'''
use std::ops::Add;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Meters(f64);

impl Add for Meters {
    type Output = Meters;

    fn add(self, other: Meters) -> Meters {
        Meters(self.0 + other.0)
    }
}

impl fmt::Display for Meters {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:.1}m", self.0)
    }
}
''', r'''Meters(1.5) + Meters(2.0) => 3.5m'''),
    ("hard", "async", r'''
async fn pool<F, Fut, T>(items: Vec<String>, limit: usize, work: F) -> Vec<T>
where
    F: Fn(String) -> Fut + Clone + Send + 'static,
    Fut: Future<Output = T> + Send,
    T: Send + 'static,
{
    let semaphore = Arc::new(Semaphore::new(limit));
    let mut handles = Vec::new();
    for item in items {
        let permit = semaphore.clone().acquire_owned().await.unwrap();
        let work = work.clone();
        handles.push(tokio::spawn(async move {
            let result = work(item).await;
            drop(permit);
            result
        }));
    }
    let mut out = Vec::new();
    for handle in handles {
        if let Ok(value) = handle.await {
            out.push(value);
        }
    }
    out
}
''', r'''pool(urls, 4, fetch).await => at most four requests in flight'''),
    ("hard", "async", r'''
async fn run_until_shutdown(mut shutdown: broadcast::Receiver<()>) {
    let mut ticker = tokio::time::interval(Duration::from_secs(1));
    loop {
        tokio::select! {
            _ = ticker.tick() => {
                println!("tick");
            }
            _ = shutdown.recv() => {
                println!("shutting down");
                break;
            }
        }
    }
}
''', r'''tick
tick
shutting down'''),
    ("hard", "async", r'''
pub struct Debouncer {
    handle: Option<JoinHandle<()>>,
    delay: Duration,
}

impl Debouncer {
    pub fn call<F>(&mut self, fun: F)
    where
        F: FnOnce() + Send + 'static,
    {
        if let Some(handle) = self.handle.take() {
            handle.abort();
        }
        let delay = self.delay;
        self.handle = Some(tokio::spawn(async move {
            tokio::time::sleep(delay).await;
            fun();
        }));
    }
}
''', r'''call(a); call(b) => only b runs, after the delay'''),
    ("hard", "errors", r'''
#[derive(Debug)]
pub enum AppError {
    Io(io::Error),
    Parse(ParseIntError),
}

impl From<io::Error> for AppError {
    fn from(err: io::Error) -> Self {
        AppError::Io(err)
    }
}

impl From<ParseIntError> for AppError {
    fn from(err: ParseIntError) -> Self {
        AppError::Parse(err)
    }
}

fn read_port(path: &str) -> Result<u16, AppError> {
    let raw = fs::read_to_string(path)?;
    Ok(raw.trim().parse()?)
}
''', r'''read_port("missing") = Err(Io(NotFound))'''),
    ("hard", "functional", r'''
fn compose<A, B, C>(f: impl Fn(A) -> B, g: impl Fn(B) -> C) -> impl Fn(A) -> C {
    move |value| g(f(value))
}

fn memoize<F>(fun: F) -> impl FnMut(u64) -> u64
where
    F: Fn(u64) -> u64,
{
    let mut cache: HashMap<u64, u64> = HashMap::new();
    move |key| *cache.entry(key).or_insert_with(|| fun(key))
}
''', r'''let mut f = memoize(|n| n * n); f(9) = 81'''),
    ("hard", "functional", r'''
struct Fibs {
    a: u64,
    b: u64,
}

impl Iterator for Fibs {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let value = self.a;
        self.a = self.b;
        self.b = value + self.b;
        Some(value)
    }
}
''', r'''Fibs { a: 0, b: 1 }.take(7).collect::<Vec<_>>()
[0, 1, 1, 2, 3, 5, 8]'''),
    ("hard", "oop", r'''
pub struct Shared<T> {
    inner: Arc<Mutex<T>>,
}

impl<T> Shared<T> {
    pub fn new(value: T) -> Self {
        Shared {
            inner: Arc::new(Mutex::new(value)),
        }
    }

    pub fn with<R>(&self, work: impl FnOnce(&mut T) -> R) -> R {
        let mut guard = self.inner.lock().expect("poisoned lock");
        work(&mut guard)
    }
}

impl<T> Clone for Shared<T> {
    fn clone(&self) -> Self {
        Shared {
            inner: Arc::clone(&self.inner),
        }
    }
}
''', r'''let s = Shared::new(0); s.with(|n| *n += 1);'''),
    ("hard", "data", r'''
fn insert_races(conn: &mut Connection, races: &[Race]) -> Result<usize, rusqlite::Error> {
    let tx = conn.transaction()?;
    let mut inserted = 0;
    {
        let mut stmt = tx.prepare("INSERT INTO races (wpm, language) VALUES (?1, ?2)")?;
        for race in races {
            inserted += stmt.execute(params![race.wpm, race.language])?;
        }
    }
    tx.commit()?;
    Ok(inserted)
}
''', r'''insert_races(&mut conn, &races) = Ok(500)'''),
    ("hard", "strings", r'''
fn tokenize(source: &str) -> Vec<Token> {
    let mut out = Vec::new();
    let mut chars = source.chars().peekable();
    while let Some(&c) = chars.peek() {
        match c {
            ' ' | '\t' => {
                chars.next();
            }
            '0'..='9' => {
                let mut value = String::new();
                while let Some(&d) = chars.peek() {
                    if !d.is_ascii_digit() {
                        break;
                    }
                    value.push(d);
                    chars.next();
                }
                out.push(Token::Number(value.parse().unwrap()));
            }
            _ => {
                chars.next();
                out.push(Token::Symbol(c));
            }
        }
    }
    out
}
''', r'''tokenize("1 + 20") => [Number(1), Symbol('+'), Number(20)]'''),
    ("hard", "math", r'''
fn multiply(a: &[Vec<f64>], b: &[Vec<f64>]) -> Vec<Vec<f64>> {
    let rows = a.len();
    let inner = b.len();
    let cols = b[0].len();
    let mut out = vec![vec![0.0; cols]; rows];
    for i in 0..rows {
        for k in 0..inner {
            let value = a[i][k];
            if value == 0.0 {
                continue;
            }
            for j in 0..cols {
                out[i][j] += value * b[k][j];
            }
        }
    }
    out
}
''', r'''[[1, 2]] x [[3], [4]] = [[11.0]]'''),
    ("hard", "web", r'''
async fn router() -> Router {
    Router::new()
        .route("/healthz", get(|| async { "ok" }))
        .route("/races/:id", get(handler))
        .layer(TraceLayer::new_for_http())
        .layer(TimeoutLayer::new(Duration::from_secs(10)))
}
''', r'''GET /healthz => ok'''),
    ("hard", "data-structures", r'''
pub struct Graph {
    edges: HashMap<String, HashSet<String>>,
}

impl Graph {
    pub fn link(&mut self, from: &str, to: &str) {
        self.edges
            .entry(from.to_string())
            .or_default()
            .insert(to.to_string());
    }

    pub fn reachable(&self, start: &str) -> HashSet<String> {
        let mut seen = HashSet::from([start.to_string()]);
        let mut stack = vec![start.to_string()];
        while let Some(node) = stack.pop() {
            for next in self.edges.get(&node).into_iter().flatten() {
                if seen.insert(next.clone()) {
                    stack.push(next.clone());
                }
            }
        }
        seen
    }
}
''', r'''link(a, b); link(b, c); reachable("a") = {"a", "b", "c"}'''),
]
