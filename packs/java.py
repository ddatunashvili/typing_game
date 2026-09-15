"""Java snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Snippets are method or class
bodies as you would type them, not whole compilation units.
"""
LANGUAGE = "java"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
public static int add(int a, int b) {
    return a + b;
}
''', r'''add(2, 3) => 5'''),
    ("very-easy", "math", r'''
public static boolean isEven(int n) {
    return n % 2 == 0;
}
''', r'''isEven(10) => true'''),
    ("very-easy", "strings", r'''
public static String shout(String text) {
    return text.toUpperCase() + "!";
}
''', r'''shout("hello") => HELLO!'''),
    ("very-easy", "strings", r'''
public static String reverse(String text) {
    return new StringBuilder(text).reverse().toString();
}
''', r'''reverse("java") => avaj'''),
    ("very-easy", "math", r'''
public static double celsius(double f) {
    return (f - 32) * 5 / 9;
}
''', r'''celsius(212.0) => 100.0'''),
    ("very-easy", "math", r'''
public static int clamp(int n, int low, int high) {
    return Math.max(low, Math.min(n, high));
}
''', r'''clamp(42, 0, 10) => 10'''),
    ("very-easy", "algorithms", r'''
public static int largest(int[] numbers) {
    int best = numbers[0];
    for (int n : numbers) {
        if (n > best) {
            best = n;
        }
    }
    return best;
}
''', r'''largest([3, 9, 4]) => 9'''),
    ("very-easy", "algorithms", r'''
public static void countUp(int n) {
    for (int i = 1; i <= n; i++) {
        System.out.println(i);
    }
}
''', r'''countUp(3)
1
2
3'''),
    ("very-easy", "algorithms", r'''
public static int sum(int[] numbers) {
    int total = 0;
    for (int n : numbers) {
        total += n;
    }
    return total;
}
''', r'''sum([1, 2, 3, 4]) => 10'''),
    ("very-easy", "oop", r'''
public class Dog {
    private final String name;

    public Dog(String name) {
        this.name = name;
    }

    public String speak() {
        return name + " says woof";
    }
}
''', r'''new Dog("Rex").speak() => Rex says woof'''),
    ("very-easy", "strings", r'''
public static boolean isBlank(String text) {
    return text == null || text.trim().isEmpty();
}
''', r'''isBlank("   ") => true'''),
    ("very-easy", "data-structures", r'''
public static List<String> names() {
    return List.of("ada", "grace", "linus");
}
''', r'''names() => [ada, grace, linus]'''),
    ("very-easy", "data-structures", r'''
public static Map<String, Integer> scores() {
    Map<String, Integer> out = new HashMap<>();
    out.put("ada", 98);
    out.put("grace", 104);
    return out;
}
''', r'''scores() => {ada=98, grace=104}'''),
    ("very-easy", "errors", r'''
public static int safeInt(String text, int fallback) {
    try {
        return Integer.parseInt(text);
    } catch (NumberFormatException e) {
        return fallback;
    }
}
''', r'''safeInt("oops", 0) => 0'''),
    ("very-easy", "functional", r'''
public static List<Integer> doubled(List<Integer> numbers) {
    return numbers.stream().map(n -> n * 2).toList();
}
''', r'''doubled([1, 2, 3]) => [2, 4, 6]'''),
    ("very-easy", "functional", r'''
public static List<Integer> evens(List<Integer> numbers) {
    return numbers.stream().filter(n -> n % 2 == 0).toList();
}
''', r'''evens([1, 2, 3, 4]) => [2, 4]'''),
    ("very-easy", "strings", r'''
public static String initials(String first, String last) {
    return "" + first.charAt(0) + last.charAt(0);
}
''', r'''initials("Ada", "Lovelace") => AL'''),
    ("very-easy", "oop", r'''
public record Point(int x, int y) {
    public int manhattan() {
        return Math.abs(x) + Math.abs(y);
    }
}
''', r'''new Point(3, -4).manhattan() => 7'''),
    ("very-easy", "math", r'''
public static double average(int[] numbers) {
    if (numbers.length == 0) {
        return 0;
    }
    return (double) sum(numbers) / numbers.length;
}
''', r'''average([2, 4, 6]) => 4.0'''),
    ("very-easy", "data-structures", r'''
public static <T> T firstOrNull(List<T> items) {
    return items.isEmpty() ? null : items.get(0);
}
''', r'''firstOrNull([]) => null'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
public static void fizzbuzz(int n) {
    for (int i = 1; i <= n; i++) {
        if (i % 15 == 0) {
            System.out.println("FizzBuzz");
        } else if (i % 3 == 0) {
            System.out.println("Fizz");
        } else if (i % 5 == 0) {
            System.out.println("Buzz");
        } else {
            System.out.println(i);
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
public static long fib(int n) {
    long a = 0;
    long b = 1;
    for (int i = 0; i < n; i++) {
        long next = a + b;
        a = b;
        b = next;
    }
    return a;
}
''', r'''fib(10) => 55'''),
    ("easy", "algorithms", r'''
public static long factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}
''', r'''factorial(6) => 720'''),
    ("easy", "strings", r'''
public static boolean isPalindrome(String text) {
    String clean = text.replaceAll("[^A-Za-z0-9]", "").toLowerCase();
    int i = 0;
    int j = clean.length() - 1;
    while (i < j) {
        if (clean.charAt(i++) != clean.charAt(j--)) {
            return false;
        }
    }
    return true;
}
''', r'''isPalindrome("A man, a plan, a canal: Panama") => true'''),
    ("easy", "strings", r'''
public static boolean isAnagram(String a, String b) {
    char[] left = a.toLowerCase().toCharArray();
    char[] right = b.toLowerCase().toCharArray();
    Arrays.sort(left);
    Arrays.sort(right);
    return Arrays.equals(left, right);
}
''', r'''isAnagram("listen", "silent") => true'''),
    ("easy", "strings", r'''
public static String titleCase(String text) {
    return Arrays.stream(text.split(" "))
        .map(word -> word.substring(0, 1).toUpperCase() + word.substring(1).toLowerCase())
        .collect(Collectors.joining(" "));
}
''', r'''titleCase("hello wide world") => Hello Wide World'''),
    ("easy", "functional", r'''
public List<String> activeNames(List<User> users) {
    return users.stream()
        .filter(User::isActive)
        .map(User::getName)
        .sorted()
        .collect(Collectors.toList());
}
''', r'''[ada, grace, linus]'''),
    ("easy", "functional", r'''
public static Map<Integer, List<String>> byLength(List<String> words) {
    return words.stream().collect(Collectors.groupingBy(String::length));
}
''', r'''byLength([a, bb, cc]) => {1=[a], 2=[bb, cc]}'''),
    ("easy", "functional", r'''
public static int sumOfSquares(List<Integer> numbers) {
    return numbers.stream().mapToInt(n -> n * n).sum();
}
''', r'''sumOfSquares([1, 2, 3]) => 14'''),
    ("easy", "data-structures", r'''
public static <T> List<T> unique(List<T> items) {
    return new ArrayList<>(new LinkedHashSet<>(items));
}
''', r'''unique([1, 2, 2, 3]) => [1, 2, 3]'''),
    ("easy", "data-structures", r'''
public static <T> List<List<T>> chunk(List<T> items, int size) {
    List<List<T>> out = new ArrayList<>();
    for (int i = 0; i < items.size(); i += size) {
        out.add(items.subList(i, Math.min(items.size(), i + size)));
    }
    return out;
}
''', r'''chunk([1, 2, 3, 4, 5], 2) => [[1, 2], [3, 4], [5]]'''),
    ("easy", "math", r'''
public static boolean isPrime(int n) {
    if (n < 2) {
        return false;
    }
    for (int d = 2; (long) d * d <= n; d++) {
        if (n % d == 0) {
            return false;
        }
    }
    return true;
}
''', r'''isPrime(97) => true'''),
    ("easy", "math", r'''
public static int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return Math.abs(a);
}
''', r'''gcd(48, 18) => 6'''),
    ("easy", "oop", r'''
public class Counter {
    private int count;

    public int bump(int by) {
        count += by;
        return count;
    }

    public int value() {
        return count;
    }
}
''', r'''new Counter().bump(3) => 3'''),
    ("easy", "oop", r'''
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
''', r'''new Invoice(1, "ada", BigDecimal.TEN).isLarge() => false'''),
    ("easy", "errors", r'''
public static double divide(double a, double b) {
    if (b == 0) {
        throw new IllegalArgumentException("cannot divide by zero");
    }
    return a / b;
}
''', r'''divide(1, 0)
IllegalArgumentException: cannot divide by zero'''),
    ("easy", "data", r'''
public static List<String> readLines(Path path) throws IOException {
    try (Stream<String> lines = Files.lines(path)) {
        return lines.filter(line -> !line.isBlank()).toList();
    }
}
''', r'''readLines(names.txt) => [ada, grace, linus]'''),
    ("easy", "async", r'''
public static void runLater(Runnable task, long millis) {
    CompletableFuture.runAsync(
        task,
        CompletableFuture.delayedExecutor(millis, TimeUnit.MILLISECONDS)
    );
}
''', r'''runLater(() -> System.out.println("late"), 200)
late'''),
    ("easy", "web", r'''
public static String buildUrl(String base, Map<String, String> params) {
    String query = params.entrySet().stream()
        .map(e -> e.getKey() + "=" + e.getValue())
        .collect(Collectors.joining("&"));
    return query.isEmpty() ? base : base + "?" + query;
}
''', r'''buildUrl("/search", {q=code}) => /search?q=code'''),
    ("easy", "strings", r'''
public static String truncate(String text, int max) {
    if (text.length() <= max) {
        return text;
    }
    return text.substring(0, max - 1) + "…";
}
''', r'''truncate("a very long sentence", 10) => a very lo…'''),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
public static int binarySearch(int[] items, int target) {
    int low = 0;
    int high = items.length - 1;
    while (low <= high) {
        int mid = (low + high) >>> 1;
        if (items[mid] == target) {
            return mid;
        }
        if (items[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}
''', r'''binarySearch([1, 3, 5, 7, 9], 7) => 3'''),
    ("medium", "algorithms", r'''
public static void bubbleSort(int[] items) {
    for (int i = 0; i < items.length; i++) {
        for (int j = 0; j < items.length - i - 1; j++) {
            if (items[j] > items[j + 1]) {
                int t = items[j];
                items[j] = items[j + 1];
                items[j + 1] = t;
            }
        }
    }
}
''', r'''[5, 1, 4, 2] => [1, 2, 4, 5]'''),
    ("medium", "algorithms", r'''
public static int[] twoSum(int[] numbers, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < numbers.length; i++) {
        Integer partner = seen.get(target - numbers[i]);
        if (partner != null) {
            return new int[] {partner, i};
        }
        seen.put(numbers[i], i);
    }
    return new int[0];
}
''', r'''twoSum([2, 7, 11, 15], 9) => [0, 1]'''),
    ("medium", "algorithms", r'''
public static int maxSubarray(int[] numbers) {
    int best = numbers[0];
    int current = numbers[0];
    for (int i = 1; i < numbers.length; i++) {
        current = Math.max(numbers[i], current + numbers[i]);
        best = Math.max(best, current);
    }
    return best;
}
''', r'''maxSubarray([-2, 1, -3, 4, -1, 2, 1]) => 6'''),
    ("medium", "data-structures", r'''
public class Stack<T> {
    private final Deque<T> items = new ArrayDeque<>();

    public void push(T item) {
        items.push(item);
    }

    public T pop() {
        if (items.isEmpty()) {
            throw new NoSuchElementException("stack is empty");
        }
        return items.pop();
    }

    public Optional<T> peek() {
        return Optional.ofNullable(items.peek());
    }
}
''', r'''push(1); push(2); pop() => 2'''),
    ("medium", "data-structures", r'''
public class Node<T> {
    final T value;
    Node<T> next;

    Node(T value, Node<T> next) {
        this.value = value;
        this.next = next;
    }

    public List<T> toList() {
        List<T> out = new ArrayList<>();
        for (Node<T> cursor = this; cursor != null; cursor = cursor.next) {
            out.add(cursor.value);
        }
        return out;
    }
}
''', r'''1 -> 2 -> 3 => [1, 2, 3]'''),
    ("medium", "data-structures", r'''
public static <T> Map<T, Long> frequencies(List<T> items) {
    return items.stream()
        .collect(Collectors.groupingBy(item -> item, Collectors.counting()));
}
''', r'''frequencies([a, b, a]) => {a=2, b=1}'''),
    ("medium", "oop", r'''
public class Repository<T> {
    private final Map<Long, T> rows = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong();

    public long save(T row) {
        long id = sequence.incrementAndGet();
        rows.put(id, row);
        return id;
    }

    public Optional<T> find(long id) {
        return Optional.ofNullable(rows.get(id));
    }
}
''', r'''save("ada") => 1; find(1) => Optional[ada]'''),
    ("medium", "oop", r'''
public sealed interface Shape permits Circle, Rect {
    double area();
}

public record Circle(double radius) implements Shape {
    public double area() {
        return Math.PI * radius * radius;
    }
}

public record Rect(double width, double height) implements Shape {
    public double area() {
        return width * height;
    }
}
''', r'''new Rect(3, 4).area() => 12.0'''),
    ("medium", "functional", r'''
public static <T, R> List<R> mapAll(List<T> rows, Function<T, R> fn) {
    return rows.stream().map(fn).collect(Collectors.toUnmodifiableList());
}

public static <T> Optional<T> firstMatch(List<T> rows, Predicate<T> test) {
    return rows.stream().filter(test).findFirst();
}
''', r'''firstMatch([1, 2, 3], n -> n > 1) => Optional[2]'''),
    ("medium", "functional", r'''
public static Map<Boolean, List<Integer>> split(List<Integer> numbers) {
    return numbers.stream()
        .collect(Collectors.partitioningBy(n -> n % 2 == 0));
}
''', r'''split([1, 2, 3, 4]) => {false=[1, 3], true=[2, 4]}'''),
    ("medium", "errors", r'''
public class ValidationException extends RuntimeException {
    private final String field;

    public ValidationException(String field, String message) {
        super(field + ": " + message);
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
''', r'''new ValidationException("email", "is required").getMessage()
email: is required'''),
    ("medium", "errors", r'''
public static <T> T withRetry(Supplier<T> task, int attempts) {
    RuntimeException last = null;
    for (int i = 0; i < attempts; i++) {
        try {
            return task.get();
        } catch (RuntimeException e) {
            last = e;
        }
    }
    throw last;
}
''', r'''withRetry(flaky, 3)
IllegalStateException: boom   // after 3 attempts'''),
    ("medium", "async", r'''
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
''', r'''buildAll([a, b, c]) => 3 reports'''),
    ("medium", "async", r'''
public static CompletableFuture<String> firstToFinish(
    CompletableFuture<String> a,
    CompletableFuture<String> b
) {
    return a.applyToEither(b, value -> "winner: " + value);
}
''', r'''firstToFinish(slow, fast) => winner: fast'''),
    ("medium", "data", r'''
public static List<User> findActive(DataSource source) throws SQLException {
    String sql = "SELECT id, name FROM users WHERE active = true";
    try (Connection conn = source.getConnection();
         PreparedStatement stmt = conn.prepareStatement(sql);
         ResultSet rows = stmt.executeQuery()) {
        List<User> users = new ArrayList<>();
        while (rows.next()) {
            users.add(new User(rows.getLong("id"), rows.getString("name")));
        }
        return users;
    }
}
''', r'''findActive(ds) => [User[1, ada], User[2, grace]]'''),
    ("medium", "web", r'''
@GetMapping("/users/{id}")
public ResponseEntity<User> findUser(@PathVariable long id) {
    return repository.find(id)
        .map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.notFound().build());
}
''', r'''GET /users/99 => 404 Not Found'''),
    ("medium", "strings", r'''
public static String slugify(String text) {
    String clean = Normalizer.normalize(text, Normalizer.Form.NFKD)
        .toLowerCase()
        .replaceAll("[^a-z0-9]+", "-");
    return clean.replaceAll("^-+|-+$", "");
}
''', r'''slugify("  Hello, World!  ") => hello-world'''),
    ("medium", "math", r'''
public static double percentile(double[] values, double p) {
    double[] sorted = values.clone();
    Arrays.sort(sorted);
    double index = (sorted.length - 1) * (p / 100);
    int low = (int) Math.floor(index);
    int high = (int) Math.ceil(index);
    if (low == high) {
        return sorted[low];
    }
    return sorted[low] + (sorted[high] - sorted[low]) * (index - low);
}
''', r'''percentile([10, 20, 30, 40], 50) => 25.0'''),
    ("medium", "oop", r'''
public class Builder {
    private String name = "";
    private int rating = 1200;

    public Builder name(String name) {
        this.name = name;
        return this;
    }

    public Builder rating(int rating) {
        this.rating = rating;
        return this;
    }

    public Player build() {
        return new Player(name, rating);
    }
}
''', r'''new Builder().name("ada").rating(1400).build()
Player[name=ada, rating=1400]'''),

    # --------------------------------------------------------------------- hard
    ("hard", "data-structures", r'''
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
''', r'''capacity 2: put a, put b, get a, put c => b evicted'''),
    ("hard", "data-structures", r'''
public class Trie {
    private final Map<Character, Trie> children = new HashMap<>();
    private boolean word;

    public void insert(String text) {
        Trie node = this;
        for (char c : text.toCharArray()) {
            node = node.children.computeIfAbsent(c, key -> new Trie());
        }
        node.word = true;
    }

    public boolean contains(String text) {
        Trie node = this;
        for (char c : text.toCharArray()) {
            node = node.children.get(c);
            if (node == null) {
                return false;
            }
        }
        return node.word;
    }
}
''', r'''insert("code"); contains("code") => true; contains("cod") => false'''),
    ("hard", "data-structures", r'''
public class MinHeap {
    private final List<Integer> items = new ArrayList<>();

    public void add(int value) {
        items.add(value);
        int i = items.size() - 1;
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (items.get(parent) <= items.get(i)) {
                break;
            }
            Collections.swap(items, parent, i);
            i = parent;
        }
    }

    public int peek() {
        return items.get(0);
    }
}
''', r'''add(5); add(2); add(8); peek() => 2'''),
    ("hard", "algorithms", r'''
public static void quicksort(int[] a, int lo, int hi) {
    if (lo >= hi) {
        return;
    }
    int pivot = a[(lo + hi) >>> 1];
    int i = lo;
    int j = hi;
    while (i <= j) {
        while (a[i] < pivot) {
            i++;
        }
        while (a[j] > pivot) {
            j--;
        }
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
''', r'''[3, 6, 1, 8, 2] => [1, 2, 3, 6, 8]'''),
    ("hard", "algorithms", r'''
public static int levenshtein(String a, String b) {
    int[] previous = new int[b.length() + 1];
    for (int j = 0; j <= b.length(); j++) {
        previous[j] = j;
    }
    for (int i = 1; i <= a.length(); i++) {
        int[] current = new int[b.length() + 1];
        current[0] = i;
        for (int j = 1; j <= b.length(); j++) {
            int cost = a.charAt(i - 1) == b.charAt(j - 1) ? 0 : 1;
            current[j] = Math.min(
                Math.min(previous[j] + 1, current[j - 1] + 1),
                previous[j - 1] + cost
            );
        }
        previous = current;
    }
    return previous[b.length()];
}
''', r'''levenshtein("kitten", "sitting") => 3'''),
    ("hard", "algorithms", r'''
public static Map<String, Integer> dijkstra(
    Map<String, Map<String, Integer>> graph,
    String start
) {
    Map<String, Integer> distances = new HashMap<>();
    PriorityQueue<Map.Entry<String, Integer>> queue =
        new PriorityQueue<>(Map.Entry.comparingByValue());
    distances.put(start, 0);
    queue.add(Map.entry(start, 0));
    while (!queue.isEmpty()) {
        Map.Entry<String, Integer> head = queue.poll();
        for (var edge : graph.getOrDefault(head.getKey(), Map.of()).entrySet()) {
            int candidate = head.getValue() + edge.getValue();
            if (candidate < distances.getOrDefault(edge.getKey(), Integer.MAX_VALUE)) {
                distances.put(edge.getKey(), candidate);
                queue.add(Map.entry(edge.getKey(), candidate));
            }
        }
    }
    return distances;
}
''', r'''dijkstra({a={b=1}, b={c=2}}, "a") => {a=0, b=1, c=3}'''),
    ("hard", "async", r'''
public static <T> List<T> runAll(List<Callable<T>> tasks) throws InterruptedException {
    try (ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor()) {
        return pool.invokeAll(tasks).stream()
            .map(future -> {
                try {
                    return future.get();
                } catch (Exception e) {
                    throw new CompletionException(e);
                }
            })
            .toList();
    }
}
''', r'''runAll(tasks) => every task completed on a virtual thread'''),
    ("hard", "async", r'''
public class RateLimiter {
    private final Semaphore permits;
    private final ScheduledExecutorService clock =
        Executors.newSingleThreadScheduledExecutor();

    public RateLimiter(int perSecond) {
        this.permits = new Semaphore(perSecond);
        clock.scheduleAtFixedRate(
            () -> permits.release(perSecond - permits.availablePermits()),
            1, 1, TimeUnit.SECONDS
        );
    }

    public void acquire() throws InterruptedException {
        permits.acquire();
    }
}
''', r'''new RateLimiter(5) => at most five acquires per second'''),
    ("hard", "async", r'''
public static CompletableFuture<Void> pipeline(List<String> ids) {
    return CompletableFuture
        .supplyAsync(() -> ids.stream().map(Repository::load).toList())
        .thenApply(rows -> rows.stream().filter(Objects::nonNull).toList())
        .thenAccept(rows -> rows.forEach(System.out::println))
        .exceptionally(error -> {
            System.err.println("pipeline failed: " + error.getMessage());
            return null;
        });
}
''', r'''pipeline([a, b]) => rows printed, errors swallowed and logged'''),
    ("hard", "oop", r'''
public class Registry {
    private static final Map<String, Supplier<Handler>> FACTORIES = new HashMap<>();

    public static void register(String name, Supplier<Handler> factory) {
        FACTORIES.put(name, factory);
    }

    public static Handler create(String name) {
        Supplier<Handler> factory = FACTORIES.get(name);
        if (factory == null) {
            throw new IllegalArgumentException("no handler named " + name);
        }
        return factory.get();
    }
}
''', r'''register("greet", GreetHandler::new); create("greet")
GreetHandler@1b6d'''),
    ("hard", "oop", r'''
public static String describe(Object value) {
    return switch (value) {
        case Integer i when i > 100 -> "big number " + i;
        case Integer i -> "number " + i;
        case String s -> "text of length " + s.length();
        case null -> "nothing";
        default -> "a " + value.getClass().getSimpleName();
    };
}
''', r'''describe(404) => big number 404
describe(null) => nothing'''),
    ("hard", "functional", r'''
public static <T> Collector<T, ?, Map<Boolean, Long>> countingBy(Predicate<T> test) {
    return Collectors.partitioningBy(test, Collectors.counting());
}

public static <T, R> Function<T, R> memoize(Function<T, R> fn) {
    Map<T, R> cache = new ConcurrentHashMap<>();
    return key -> cache.computeIfAbsent(key, fn);
}
''', r'''memoize(slowSquare).apply(9) => 81   (second call is cached)'''),
    ("hard", "functional", r'''
public static Stream<int[]> pairs(int[] numbers) {
    return IntStream.range(0, numbers.length)
        .boxed()
        .flatMap(i -> IntStream.range(i + 1, numbers.length)
            .mapToObj(j -> new int[] {numbers[i], numbers[j]}));
}
''', r'''pairs([1, 2, 3]).count() => 3'''),
    ("hard", "data", r'''
public static void batchInsert(DataSource source, List<Race> races) throws SQLException {
    String sql = "INSERT INTO races (user_id, wpm, acc) VALUES (?, ?, ?)";
    try (Connection conn = source.getConnection();
         PreparedStatement stmt = conn.prepareStatement(sql)) {
        conn.setAutoCommit(false);
        for (Race race : races) {
            stmt.setLong(1, race.userId());
            stmt.setDouble(2, race.wpm());
            stmt.setDouble(3, race.accuracy());
            stmt.addBatch();
        }
        stmt.executeBatch();
        conn.commit();
    }
}
''', r'''batchInsert(ds, 500 races) => one transaction, 500 rows'''),
    ("hard", "data", r'''
public static Map<String, Double> averageByLanguage(List<Race> races) {
    return races.stream().collect(Collectors.groupingBy(
        Race::language,
        TreeMap::new,
        Collectors.averagingDouble(Race::wpm)
    ));
}
''', r'''averageByLanguage(races) => {java=88.5, python=94.0}'''),
    ("hard", "web", r'''
public static HttpResponse<String> post(String url, String body) throws Exception {
    HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .followRedirects(HttpClient.Redirect.NORMAL)
        .build();
    HttpRequest request = HttpRequest.newBuilder(URI.create(url))
        .header("content-type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(body))
        .build();
    return client.send(request, HttpResponse.BodyHandlers.ofString());
}
''', r'''post("/api/races", "{}") => 201 Created'''),
    ("hard", "errors", r'''
public static <T extends AutoCloseable> void useAll(List<T> resources, Consumer<T> work) {
    List<Exception> failures = new ArrayList<>();
    for (T resource : resources) {
        try (T open = resource) {
            work.accept(open);
        } catch (Exception e) {
            failures.add(e);
        }
    }
    if (!failures.isEmpty()) {
        RuntimeException error = new RuntimeException(failures.size() + " failed");
        failures.forEach(error::addSuppressed);
        throw error;
    }
}
''', r'''useAll(handles, this::flush)
RuntimeException: 2 failed  (suppressed: IOException, IOException)'''),
    ("hard", "strings", r'''
public static Map<String, Long> topWords(String text, int limit) {
    return Arrays.stream(text.toLowerCase().split("\\W+"))
        .filter(word -> !word.isBlank())
        .collect(Collectors.groupingBy(word -> word, Collectors.counting()))
        .entrySet().stream()
        .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
        .limit(limit)
        .collect(Collectors.toMap(
            Map.Entry::getKey, Map.Entry::getValue, (a, b) -> a, LinkedHashMap::new));
}
''', r'''topWords("the cat the hat the end", 2) => {the=3, cat=1}'''),
    ("hard", "math", r'''
public static double[][] multiply(double[][] a, double[][] b) {
    int rows = a.length;
    int inner = b.length;
    int cols = b[0].length;
    double[][] out = new double[rows][cols];
    for (int i = 0; i < rows; i++) {
        for (int k = 0; k < inner; k++) {
            double value = a[i][k];
            if (value == 0) {
                continue;
            }
            for (int j = 0; j < cols; j++) {
                out[i][j] += value * b[k][j];
            }
        }
    }
    return out;
}
''', r'''[[1, 2]] x [[3], [4]] => [[11.0]]'''),
    ("hard", "oop", r'''
public class ObjectPool<T> {
    private final Queue<T> idle = new ConcurrentLinkedQueue<>();
    private final Supplier<T> factory;

    public ObjectPool(Supplier<T> factory) {
        this.factory = factory;
    }

    public T borrow() {
        T item = idle.poll();
        return item != null ? item : factory.get();
    }

    public void give(T item) {
        idle.offer(item);
    }
}
''', r'''borrow() => new instance; give(it); borrow() => the same instance'''),
]
