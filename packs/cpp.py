"""C++ snippet pack: 20 per level, modern C++17/20 style.

Entries are (level, topic, code, expected_output).
"""
LANGUAGE = "cpp"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
int add(int a, int b) {
    return a + b;
}
''', r'''add(2, 3) = 5'''),
    ("very-easy", "math", r'''
bool is_even(int n) {
    return n % 2 == 0;
}
''', r'''is_even(10) = true'''),
    ("very-easy", "math", r'''
constexpr long square(long n) {
    return n * n;
}
''', r'''square(7) = 49'''),
    ("very-easy", "math", r'''
int clamp_to(int n, int low, int high) {
    return std::max(low, std::min(n, high));
}
''', r'''clamp_to(42, 0, 10) = 10'''),
    ("very-easy", "strings", r'''
std::string shout(const std::string &text) {
    std::string out = text;
    std::transform(out.begin(), out.end(), out.begin(), ::toupper);
    return out + "!";
}
''', r'''shout("hello") = HELLO!'''),
    ("very-easy", "strings", r'''
std::string reverse(std::string text) {
    std::reverse(text.begin(), text.end());
    return text;
}
''', r'''reverse("c++") = ++c'''),
    ("very-easy", "strings", r'''
void hello() {
    std::cout << "hello world" << std::endl;
}
''', r'''hello world'''),
    ("very-easy", "algorithms", r'''
int sum(const std::vector<int> &nums) {
    return std::accumulate(nums.begin(), nums.end(), 0);
}
''', r'''sum({1, 2, 3, 4}) = 10'''),
    ("very-easy", "algorithms", r'''
int largest(const std::vector<int> &nums) {
    return *std::max_element(nums.begin(), nums.end());
}
''', r'''largest({3, 9, 4}) = 9'''),
    ("very-easy", "algorithms", r'''
void count_up(int n) {
    for (int i = 1; i <= n; ++i) {
        std::cout << i << "\n";
    }
}
''', r'''count_up(3)
1
2
3'''),
    ("very-easy", "data-structures", r'''
std::vector<std::string> names() {
    return {"ada", "grace", "linus"};
}
''', r'''names() = [ada, grace, linus]'''),
    ("very-easy", "data-structures", r'''
std::map<std::string, int> scores() {
    return {{"ada", 98}, {"grace", 104}};
}
''', r'''scores() = {ada: 98, grace: 104}'''),
    ("very-easy", "functional", r'''
std::vector<int> doubled(const std::vector<int> &nums) {
    std::vector<int> out;
    out.reserve(nums.size());
    std::transform(nums.begin(), nums.end(), std::back_inserter(out),
                   [](int n) { return n * 2; });
    return out;
}
''', r'''doubled({1, 2, 3}) = [2, 4, 6]'''),
    ("very-easy", "functional", r'''
std::vector<int> evens(const std::vector<int> &nums) {
    std::vector<int> out;
    std::copy_if(nums.begin(), nums.end(), std::back_inserter(out),
                 [](int n) { return n % 2 == 0; });
    return out;
}
''', r'''evens({1, 2, 3, 4}) = [2, 4]'''),
    ("very-easy", "oop", r'''
class Dog {
public:
    explicit Dog(std::string name) : name_(std::move(name)) {}

    std::string speak() const {
        return name_ + " says woof";
    }

private:
    std::string name_;
};
''', r'''Dog("Rex").speak() = Rex says woof'''),
    ("very-easy", "oop", r'''
struct Point {
    int x = 0;
    int y = 0;

    int manhattan() const {
        return std::abs(x) + std::abs(y);
    }
};
''', r'''Point{3, -4}.manhattan() = 7'''),
    ("very-easy", "errors", r'''
std::optional<int> safe_parse(const std::string &text) {
    try {
        return std::stoi(text);
    } catch (const std::exception &) {
        return std::nullopt;
    }
}
''', r'''safe_parse("oops") = nullopt'''),
    ("very-easy", "math", r'''
double average(const std::vector<double> &nums) {
    if (nums.empty()) {
        return 0.0;
    }
    return std::accumulate(nums.begin(), nums.end(), 0.0) / nums.size();
}
''', r'''average({2, 4, 6}) = 4'''),
    ("very-easy", "strings", r'''
bool is_blank(const std::string &text) {
    return std::all_of(text.begin(), text.end(),
                       [](unsigned char c) { return std::isspace(c); });
}
''', r'''is_blank("   ") = true'''),
    ("very-easy", "data-structures", r'''
std::optional<int> first(const std::vector<int> &nums) {
    if (nums.empty()) {
        return std::nullopt;
    }
    return nums.front();
}
''', r'''first({}) = nullopt'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
void fizzbuzz(int n) {
    for (int i = 1; i <= n; ++i) {
        if (i % 15 == 0) {
            std::cout << "FizzBuzz\n";
        } else if (i % 3 == 0) {
            std::cout << "Fizz\n";
        } else if (i % 5 == 0) {
            std::cout << "Buzz\n";
        } else {
            std::cout << i << "\n";
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
long fib(int n) {
    long a = 0;
    long b = 1;
    for (int i = 0; i < n; ++i) {
        long next = a + b;
        a = b;
        b = next;
    }
    return a;
}
''', r'''fib(10) = 55'''),
    ("easy", "algorithms", r'''
void sort_desc(std::vector<int> &nums) {
    std::sort(nums.begin(), nums.end(), std::greater<int>());
}
''', r'''{1, 4, 2} -> [4, 2, 1]'''),
    ("easy", "strings", r'''
std::vector<std::string> split(const std::string &text, char sep) {
    std::vector<std::string> parts;
    std::stringstream stream(text);
    std::string part;
    while (std::getline(stream, part, sep)) {
        parts.push_back(part);
    }
    return parts;
}
''', r'''split("a,b,c", ',') = [a, b, c]'''),
    ("easy", "strings", r'''
bool is_palindrome(const std::string &text) {
    std::string clean;
    for (unsigned char c : text) {
        if (std::isalnum(c)) {
            clean.push_back(static_cast<char>(std::tolower(c)));
        }
    }
    return std::equal(clean.begin(), clean.begin() + clean.size() / 2,
                      clean.rbegin());
}
''', r'''is_palindrome("A man, a plan, a canal: Panama") = true'''),
    ("easy", "strings", r'''
std::string join(const std::vector<std::string> &parts, const std::string &sep) {
    std::string out;
    for (std::size_t i = 0; i < parts.size(); ++i) {
        if (i) {
            out += sep;
        }
        out += parts[i];
    }
    return out;
}
''', r'''join({"a", "b"}, ", ") = "a, b"'''),
    ("easy", "strings", r'''
std::string trim(std::string text) {
    auto not_space = [](unsigned char c) { return !std::isspace(c); };
    text.erase(text.begin(), std::find_if(text.begin(), text.end(), not_space));
    text.erase(std::find_if(text.rbegin(), text.rend(), not_space).base(),
               text.end());
    return text;
}
''', r'''trim("  hello  ") = "hello"'''),
    ("easy", "data-structures", r'''
std::vector<int> unique(std::vector<int> nums) {
    std::sort(nums.begin(), nums.end());
    nums.erase(std::unique(nums.begin(), nums.end()), nums.end());
    return nums;
}
''', r'''unique({1, 2, 2, 3}) = [1, 2, 3]'''),
    ("easy", "data-structures", r'''
std::map<std::string, int> word_count(const std::string &text) {
    std::map<std::string, int> counts;
    std::stringstream stream(text);
    std::string word;
    while (stream >> word) {
        ++counts[word];
    }
    return counts;
}
''', r'''word_count("the cat the") = {cat: 1, the: 2}'''),
    ("easy", "data-structures", r'''
std::vector<std::vector<int>> chunk(const std::vector<int> &nums, std::size_t size) {
    std::vector<std::vector<int>> out;
    for (std::size_t i = 0; i < nums.size(); i += size) {
        auto end = std::min(nums.size(), i + size);
        out.emplace_back(nums.begin() + i, nums.begin() + end);
    }
    return out;
}
''', r'''chunk({1, 2, 3, 4, 5}, 2) = [[1, 2], [3, 4], [5]]'''),
    ("easy", "math", r'''
int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return std::abs(a);
}
''', r'''gcd(48, 18) = 6'''),
    ("easy", "math", r'''
bool is_prime(int n) {
    if (n < 2) {
        return false;
    }
    for (int d = 2; static_cast<long>(d) * d <= n; ++d) {
        if (n % d == 0) {
            return false;
        }
    }
    return true;
}
''', r'''is_prime(97) = true'''),
    ("easy", "oop", r'''
class Counter {
public:
    int bump(int by = 1) {
        count_ += by;
        return count_;
    }

    int value() const noexcept {
        return count_;
    }

private:
    int count_ = 0;
};
''', r'''Counter().bump(3) = 3'''),
    ("easy", "oop", r'''
class FileHandle {
public:
    explicit FileHandle(const std::string &path)
        : stream_(path, std::ios::binary) {
        if (!stream_) {
            throw std::runtime_error("cannot open " + path);
        }
    }

    std::istream &stream() {
        return stream_;
    }

private:
    std::ifstream stream_;
};
''', r'''FileHandle("missing.bin")
terminate called: cannot open missing.bin'''),
    ("easy", "errors", r'''
double divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("cannot divide by zero");
    }
    return a / b;
}
''', r'''divide(1, 0)
std::invalid_argument: cannot divide by zero'''),
    ("easy", "functional", r'''
int count_if_even(const std::vector<int> &nums) {
    return static_cast<int>(
        std::count_if(nums.begin(), nums.end(), [](int n) { return n % 2 == 0; }));
}
''', r'''count_if_even({1, 2, 3, 4}) = 2'''),
    ("easy", "functional", r'''
std::pair<std::vector<int>, std::vector<int>> partition(const std::vector<int> &nums) {
    std::vector<int> yes;
    std::vector<int> no;
    for (int n : nums) {
        (n % 2 == 0 ? yes : no).push_back(n);
    }
    return {yes, no};
}
''', r'''partition({1, 2, 3, 4}) = ([2, 4], [1, 3])'''),
    ("easy", "data", r'''
std::vector<std::string> read_lines(const std::string &path) {
    std::ifstream file(path);
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) {
            lines.push_back(line);
        }
    }
    return lines;
}
''', r'''read_lines("names.txt") = [ada, grace, linus]'''),
    ("easy", "algorithms", r'''
int binary_search(const std::vector<int> &nums, int target) {
    auto hit = std::lower_bound(nums.begin(), nums.end(), target);
    if (hit == nums.end() || *hit != target) {
        return -1;
    }
    return static_cast<int>(std::distance(nums.begin(), hit));
}
''', r'''binary_search({1, 3, 5, 7}, 5) = 2'''),
    ("easy", "math", r'''
std::pair<int, int> min_max(const std::vector<int> &nums) {
    auto [lo, hi] = std::minmax_element(nums.begin(), nums.end());
    return {*lo, *hi};
}
''', r'''min_max({3, 9, 1}) = (1, 9)'''),

    # ------------------------------------------------------------------- medium
    ("medium", "data-structures", r'''
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
''', r'''push(1); push(2); pop() = 2'''),
    ("medium", "data-structures", r'''
template <typename T>
class Queue {
public:
    void enqueue(T value) { items_.push_back(std::move(value)); }

    std::optional<T> dequeue() {
        if (items_.empty()) {
            return std::nullopt;
        }
        T front = std::move(items_.front());
        items_.pop_front();
        return front;
    }

private:
    std::deque<T> items_;
};
''', r'''enqueue("a"); dequeue() = "a"'''),
    ("medium", "data-structures", r'''
struct Node {
    int value = 0;
    std::unique_ptr<Node> next;
};

std::vector<int> to_vector(const Node *head) {
    std::vector<int> out;
    for (const Node *cursor = head; cursor; cursor = cursor->next.get()) {
        out.push_back(cursor->value);
    }
    return out;
}
''', r'''1 -> 2 -> 3 => [1, 2, 3]'''),
    ("medium", "oop", r'''
class Resource {
public:
    Resource() : handle_(std::make_unique<int>(0)) {}

    Resource(const Resource &) = delete;
    Resource &operator=(const Resource &) = delete;

    Resource(Resource &&) noexcept = default;
    Resource &operator=(Resource &&) noexcept = default;

    ~Resource() = default;

private:
    std::unique_ptr<int> handle_;
};
''', r'''Resource is movable but not copyable'''),
    ("medium", "oop", r'''
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;

    virtual std::string describe() const {
        return "area " + std::to_string(area());
    }
};

class Rect : public Shape {
public:
    Rect(double w, double h) : w_(w), h_(h) {}

    double area() const override { return w_ * h_; }

private:
    double w_;
    double h_;
};
''', r'''Rect(3, 4).describe() = area 12.000000'''),
    ("medium", "functional", r'''
std::map<std::string, int> tally(const std::vector<Event> &events) {
    std::map<std::string, int> counts;
    std::for_each(events.begin(), events.end(), [&counts](const Event &e) {
        if (e.kind.empty()) return;
        counts[e.kind] += e.weight;
    });
    return counts;
}
''', r'''tally(events) = {finish: 3, start: 1}'''),
    ("medium", "functional", r'''
template <typename T, typename Key>
auto group_by(const std::vector<T> &items, Key key) {
    std::map<decltype(key(items.front())), std::vector<T>> out;
    for (const auto &item : items) {
        out[key(item)].push_back(item);
    }
    return out;
}
''', r'''group_by(nums, parity) = {even: [2, 4], odd: [1, 3]}'''),
    ("medium", "algorithms", r'''
std::vector<int> merge_sorted(const std::vector<int> &a, const std::vector<int> &b) {
    std::vector<int> out;
    out.reserve(a.size() + b.size());
    std::merge(a.begin(), a.end(), b.begin(), b.end(), std::back_inserter(out));
    return out;
}
''', r'''merge_sorted({1, 4}, {2, 3, 5}) = [1, 2, 3, 4, 5]'''),
    ("medium", "algorithms", r'''
int max_subarray(const std::vector<int> &nums) {
    int best = nums.front();
    int current = nums.front();
    for (std::size_t i = 1; i < nums.size(); ++i) {
        current = std::max(nums[i], current + nums[i]);
        best = std::max(best, current);
    }
    return best;
}
''', r'''max_subarray({-2, 1, -3, 4, -1, 2, 1}) = 6'''),
    ("medium", "algorithms", r'''
std::optional<std::pair<std::size_t, std::size_t>> two_sum(
    const std::vector<int> &nums, int target) {
    std::unordered_map<int, std::size_t> seen;
    for (std::size_t i = 0; i < nums.size(); ++i) {
        auto hit = seen.find(target - nums[i]);
        if (hit != seen.end()) {
            return std::make_pair(hit->second, i);
        }
        seen.emplace(nums[i], i);
    }
    return std::nullopt;
}
''', r'''two_sum({2, 7, 11}, 9) = (0, 1)'''),
    ("medium", "errors", r'''
class ValidationError : public std::runtime_error {
public:
    ValidationError(std::string field, const std::string &message)
        : std::runtime_error(field + ": " + message), field_(std::move(field)) {}

    const std::string &field() const noexcept { return field_; }

private:
    std::string field_;
};
''', r'''ValidationError("email", "is required").what()
email: is required'''),
    ("medium", "async", r'''
std::vector<int> parallel_squares(const std::vector<int> &nums) {
    std::vector<std::future<int>> futures;
    for (int n : nums) {
        futures.push_back(std::async(std::launch::async, [n] { return n * n; }));
    }
    std::vector<int> out;
    for (auto &future : futures) {
        out.push_back(future.get());
    }
    return out;
}
''', r'''parallel_squares({1, 2, 3}) = [1, 4, 9]'''),
    ("medium", "async", r'''
class Counter {
public:
    void bump() {
        std::lock_guard<std::mutex> guard(lock_);
        ++count_;
    }

    int value() {
        std::lock_guard<std::mutex> guard(lock_);
        return count_;
    }

private:
    std::mutex lock_;
    int count_ = 0;
};
''', r'''8 threads bumping 1000 times each => 8000'''),
    ("medium", "strings", r'''
std::string slugify(const std::string &text) {
    std::string out;
    bool dash = true;
    for (unsigned char c : text) {
        if (std::isalnum(c)) {
            out.push_back(static_cast<char>(std::tolower(c)));
            dash = false;
        } else if (!dash) {
            out.push_back('-');
            dash = true;
        }
    }
    while (!out.empty() && out.back() == '-') {
        out.pop_back();
    }
    return out;
}
''', r'''slugify("  Hello, World!  ") = hello-world'''),
    ("medium", "math", r'''
double percentile(std::vector<double> values, double p) {
    std::sort(values.begin(), values.end());
    double index = (values.size() - 1) * p / 100.0;
    auto low = static_cast<std::size_t>(std::floor(index));
    auto high = static_cast<std::size_t>(std::ceil(index));
    if (low == high) {
        return values[low];
    }
    return values[low] + (values[high] - values[low]) * (index - low);
}
''', r'''percentile({10, 20, 30, 40}, 50) = 25'''),
    ("medium", "oop", r'''
class ServerBuilder {
public:
    ServerBuilder &port(int value) {
        port_ = value;
        return *this;
    }

    ServerBuilder &host(std::string value) {
        host_ = std::move(value);
        return *this;
    }

    std::string build() const {
        return host_ + ":" + std::to_string(port_);
    }

private:
    std::string host_ = "0.0.0.0";
    int port_ = 8000;
};
''', r'''ServerBuilder().port(25616).build() = 0.0.0.0:25616'''),
    ("medium", "data", r'''
void write_csv(const std::string &path, const std::vector<Race> &races) {
    std::ofstream file(path);
    file << "language,wpm\n";
    for (const auto &race : races) {
        file << race.language << "," << race.wpm << "\n";
    }
}
''', r'''write_csv("out.csv", races) => language,wpm ...'''),
    ("medium", "functional", r'''
template <typename... Args>
std::string concat(const Args &...args) {
    std::ostringstream out;
    (out << ... << args);
    return out.str();
}
''', r'''concat("wpm=", 98, " acc=", 99) = "wpm=98 acc=99"'''),
    ("medium", "data-structures", r'''
template <typename T>
class RingBuffer {
public:
    explicit RingBuffer(std::size_t capacity) : items_(capacity) {}

    void push(T value) {
        items_[(head_ + size_) % items_.size()] = std::move(value);
        if (size_ == items_.size()) {
            head_ = (head_ + 1) % items_.size();
        } else {
            ++size_;
        }
    }

private:
    std::vector<T> items_;
    std::size_t head_ = 0;
    std::size_t size_ = 0;
};
''', r'''RingBuffer<int>(3), push 1..4 => oldest dropped'''),
    ("medium", "algorithms", r'''
void rotate_left(std::vector<int> &nums, std::size_t by) {
    if (nums.empty()) {
        return;
    }
    by %= nums.size();
    std::rotate(nums.begin(), nums.begin() + by, nums.end());
}
''', r'''{1, 2, 3, 4, 5} rotate 2 => [3, 4, 5, 1, 2]'''),

    # --------------------------------------------------------------------- hard
    ("hard", "data-structures", r'''
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
''', r'''capacity 2: put a, put b, put c => a evicted'''),
    ("hard", "data-structures", r'''
class Trie {
public:
    void insert(const std::string &word) {
        Trie *node = this;
        for (char c : word) {
            auto &child = node->children_[c];
            if (!child) {
                child = std::make_unique<Trie>();
            }
            node = child.get();
        }
        node->word_ = true;
    }

    bool contains(const std::string &word) const {
        const Trie *node = this;
        for (char c : word) {
            auto hit = node->children_.find(c);
            if (hit == node->children_.end()) {
                return false;
            }
            node = hit->second.get();
        }
        return node->word_;
    }

private:
    std::unordered_map<char, std::unique_ptr<Trie>> children_;
    bool word_ = false;
};
''', r'''insert("code"); contains("code") = true; contains("cod") = false'''),
    ("hard", "algorithms", r'''
std::unordered_map<std::string, int> dijkstra(
    const std::unordered_map<std::string, std::vector<std::pair<std::string, int>>> &graph,
    const std::string &start) {
    using Item = std::pair<int, std::string>;
    std::priority_queue<Item, std::vector<Item>, std::greater<Item>> queue;
    std::unordered_map<std::string, int> distances{{start, 0}};
    queue.emplace(0, start);

    while (!queue.empty()) {
        auto [cost, node] = queue.top();
        queue.pop();
        if (cost > distances[node]) {
            continue;
        }
        auto edges = graph.find(node);
        if (edges == graph.end()) {
            continue;
        }
        for (const auto &[next, weight] : edges->second) {
            int candidate = cost + weight;
            auto known = distances.find(next);
            if (known == distances.end() || candidate < known->second) {
                distances[next] = candidate;
                queue.emplace(candidate, next);
            }
        }
    }
    return distances;
}
''', r'''dijkstra(graph, "a") = {a: 0, b: 1, c: 3}'''),
    ("hard", "algorithms", r'''
std::size_t levenshtein(const std::string &a, const std::string &b) {
    std::vector<std::size_t> previous(b.size() + 1);
    std::iota(previous.begin(), previous.end(), 0);

    for (std::size_t i = 1; i <= a.size(); ++i) {
        std::vector<std::size_t> current(b.size() + 1);
        current[0] = i;
        for (std::size_t j = 1; j <= b.size(); ++j) {
            std::size_t cost = a[i - 1] == b[j - 1] ? 0 : 1;
            current[j] = std::min({previous[j] + 1, current[j - 1] + 1,
                                   previous[j - 1] + cost});
        }
        previous = std::move(current);
    }
    return previous[b.size()];
}
''', r'''levenshtein("kitten", "sitting") = 3'''),
    ("hard", "algorithms", r'''
template <typename T>
void quicksort(std::vector<T> &items, int lo, int hi) {
    if (lo >= hi) {
        return;
    }
    T pivot = items[(lo + hi) / 2];
    int i = lo;
    int j = hi;
    while (i <= j) {
        while (items[i] < pivot) ++i;
        while (items[j] > pivot) --j;
        if (i <= j) {
            std::swap(items[i], items[j]);
            ++i;
            --j;
        }
    }
    quicksort(items, lo, j);
    quicksort(items, i, hi);
}
''', r'''{3, 6, 1, 8, 2} => [1, 2, 3, 6, 8]'''),
    ("hard", "oop", r'''
template <typename Derived>
class Shape {
public:
    double area() const {
        return static_cast<const Derived *>(this)->area_impl();
    }

    std::string describe() const {
        return "area " + std::to_string(area());
    }
};

class Square : public Shape<Square> {
public:
    explicit Square(double side) : side_(side) {}

    double area_impl() const { return side_ * side_; }

private:
    double side_;
};
''', r'''Square(3).describe() = area 9.000000'''),
    ("hard", "oop", r'''
class Any {
public:
    template <typename T>
    explicit Any(T value)
        : holder_(std::make_unique<Holder<T>>(std::move(value))) {}

    const std::type_info &type() const { return holder_->type(); }

private:
    struct Base {
        virtual ~Base() = default;
        virtual const std::type_info &type() const = 0;
    };

    template <typename T>
    struct Holder : Base {
        explicit Holder(T value) : value(std::move(value)) {}
        const std::type_info &type() const override { return typeid(T); }
        T value;
    };

    std::unique_ptr<Base> holder_;
};
''', r'''Any(42).type().name() = i'''),
    ("hard", "functional", r'''
template <typename F, typename G>
auto compose(F f, G g) {
    return [f, g](auto &&...args) {
        return g(f(std::forward<decltype(args)>(args)...));
    };
}

template <typename F>
auto memoize(F fn) {
    return [fn, cache = std::map<int, int>{}](int key) mutable {
        auto hit = cache.find(key);
        if (hit != cache.end()) {
            return hit->second;
        }
        return cache.emplace(key, fn(key)).first->second;
    };
}
''', r'''auto f = memoize([](int n) { return n * n; }); f(9) = 81'''),
    ("hard", "functional", r'''
std::vector<std::string> pipeline(const std::vector<std::string> &rows) {
    std::vector<std::string> out;
    std::copy_if(rows.begin(), rows.end(), std::back_inserter(out),
                 [](const std::string &row) { return !row.empty(); });
    std::transform(out.begin(), out.end(), out.begin(), [](std::string row) {
        std::transform(row.begin(), row.end(), row.begin(), ::tolower);
        return row;
    });
    return out;
}
''', r'''pipeline({"Ada", "", "GRACE"}) = [ada, grace]'''),
    ("hard", "async", r'''
class ThreadPool {
public:
    explicit ThreadPool(std::size_t count) {
        for (std::size_t i = 0; i < count; ++i) {
            workers_.emplace_back([this] { run(); });
        }
    }

    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> guard(lock_);
            stopping_ = true;
        }
        ready_.notify_all();
        for (auto &worker : workers_) {
            worker.join();
        }
    }

    void submit(std::function<void()> task) {
        {
            std::lock_guard<std::mutex> guard(lock_);
            tasks_.push(std::move(task));
        }
        ready_.notify_one();
    }

private:
    void run() {
        while (true) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> guard(lock_);
                ready_.wait(guard, [this] { return stopping_ || !tasks_.empty(); });
                if (stopping_ && tasks_.empty()) {
                    return;
                }
                task = std::move(tasks_.front());
                tasks_.pop();
            }
            task();
        }
    }

    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex lock_;
    std::condition_variable ready_;
    bool stopping_ = false;
};
''', r'''ThreadPool(4); submit(work) => work runs on a pool thread'''),
    ("hard", "async", r'''
template <typename T>
class Channel {
public:
    void send(T value) {
        {
            std::lock_guard<std::mutex> guard(lock_);
            items_.push(std::move(value));
        }
        ready_.notify_one();
    }

    T receive() {
        std::unique_lock<std::mutex> guard(lock_);
        ready_.wait(guard, [this] { return !items_.empty(); });
        T value = std::move(items_.front());
        items_.pop();
        return value;
    }

private:
    std::queue<T> items_;
    std::mutex lock_;
    std::condition_variable ready_;
};
''', r'''send(1); receive() = 1  (blocks while empty)'''),
    ("hard", "async", r'''
std::vector<int> parallel_sum_chunks(const std::vector<int> &nums, std::size_t threads) {
    std::vector<int> totals(threads, 0);
    std::vector<std::thread> workers;
    std::size_t step = nums.size() / threads;

    for (std::size_t t = 0; t < threads; ++t) {
        std::size_t start = t * step;
        std::size_t end = (t == threads - 1) ? nums.size() : start + step;
        workers.emplace_back([&nums, &totals, t, start, end] {
            totals[t] = std::accumulate(nums.begin() + start, nums.begin() + end, 0);
        });
    }
    for (auto &worker : workers) {
        worker.join();
    }
    return totals;
}
''', r'''parallel_sum_chunks(nums, 4) = one subtotal per thread'''),
    ("hard", "errors", r'''
template <typename T>
class Result {
public:
    static Result ok(T value) { return Result(std::move(value), {}); }
    static Result error(std::string message) { return Result({}, std::move(message)); }

    bool is_ok() const { return !error_.has_value(); }

    const T &value() const {
        if (!is_ok()) {
            throw std::logic_error("value() on an error result");
        }
        return *value_;
    }

private:
    Result(std::optional<T> value, std::optional<std::string> error)
        : value_(std::move(value)), error_(std::move(error)) {}

    std::optional<T> value_;
    std::optional<std::string> error_;
};
''', r'''Result<int>::error("nope").is_ok() = false'''),
    ("hard", "errors", r'''
void process_all(const std::vector<std::string> &paths) {
    std::vector<std::string> failures;
    for (const auto &path : paths) {
        try {
            process(path);
        } catch (const std::exception &e) {
            failures.push_back(path + ": " + e.what());
        }
    }
    if (!failures.empty()) {
        throw std::runtime_error(
            std::to_string(failures.size()) + " file(s) failed: " + failures.front());
    }
}
''', r'''process_all(paths)
std::runtime_error: 2 file(s) failed: a.txt: cannot open'''),
    ("hard", "strings", r'''
std::vector<std::pair<std::string, int>> top_words(const std::string &text, int limit) {
    std::unordered_map<std::string, int> counts;
    std::string word;
    for (unsigned char c : text) {
        if (std::isalnum(c)) {
            word.push_back(static_cast<char>(std::tolower(c)));
        } else if (!word.empty()) {
            ++counts[word];
            word.clear();
        }
    }
    if (!word.empty()) {
        ++counts[word];
    }
    std::vector<std::pair<std::string, int>> ranked(counts.begin(), counts.end());
    std::sort(ranked.begin(), ranked.end(), [](const auto &a, const auto &b) {
        return a.second != b.second ? a.second > b.second : a.first < b.first;
    });
    ranked.resize(std::min<std::size_t>(ranked.size(), limit));
    return ranked;
}
''', r'''top_words("the cat the hat the end", 2) = [(the, 3), (cat, 1)]'''),
    ("hard", "math", r'''
std::vector<std::vector<double>> multiply(
    const std::vector<std::vector<double>> &a,
    const std::vector<std::vector<double>> &b) {
    std::size_t rows = a.size();
    std::size_t inner = b.size();
    std::size_t cols = b.front().size();
    std::vector<std::vector<double>> out(rows, std::vector<double>(cols, 0.0));

    for (std::size_t i = 0; i < rows; ++i) {
        for (std::size_t k = 0; k < inner; ++k) {
            double value = a[i][k];
            if (value == 0.0) {
                continue;
            }
            for (std::size_t j = 0; j < cols; ++j) {
                out[i][j] += value * b[k][j];
            }
        }
    }
    return out;
}
''', r'''[[1, 2]] x [[3], [4]] = [[11]]'''),
    ("hard", "oop", r'''
class Visitor;

class Node {
public:
    virtual ~Node() = default;
    virtual void accept(Visitor &visitor) const = 0;
};

class Number : public Node {
public:
    explicit Number(double value) : value(value) {}
    void accept(Visitor &visitor) const override;
    double value;
};

class Visitor {
public:
    virtual ~Visitor() = default;
    virtual void visit(const Number &node) = 0;
};

void Number::accept(Visitor &visitor) const {
    visitor.visit(*this);
}
''', r'''tree.accept(printer) => dispatches to visit(const Number &)'''),
    ("hard", "data", r'''
std::vector<Race> load_races(const std::string &path) {
    std::ifstream file(path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("cannot open " + path);
    }
    std::uint64_t count = 0;
    file.read(reinterpret_cast<char *>(&count), sizeof(count));

    std::vector<Race> races(count);
    file.read(reinterpret_cast<char *>(races.data()),
              static_cast<std::streamsize>(count * sizeof(Race)));
    if (!file) {
        throw std::runtime_error("truncated file: " + path);
    }
    return races;
}
''', r'''load_races("races.bin") = 500 records'''),
    ("hard", "functional", r'''
template <typename Range, typename Predicate>
auto filter_view(Range &&range, Predicate keep) {
    return std::forward<Range>(range) | std::views::filter(std::move(keep));
}

std::vector<int> fast_wpm(const std::vector<Race> &races) {
    auto view = races
        | std::views::filter([](const Race &r) { return r.wpm > 90; })
        | std::views::transform([](const Race &r) { return r.wpm; });
    return {view.begin(), view.end()};
}
''', r'''fast_wpm(races) = [98, 104]'''),
    ("hard", "web", r'''
std::string handle(const Request &request) {
    static const std::unordered_map<std::string, std::function<std::string()>> routes{
        {"/healthz", [] { return "ok"; }},
        {"/version", [] { return "1.0.0"; }},
    };
    auto hit = routes.find(request.path);
    if (hit == routes.end()) {
        return "404 not found";
    }
    return hit->second();
}
''', r'''handle({"/healthz"}) = ok'''),
]
