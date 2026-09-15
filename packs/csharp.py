"""C# snippet pack: 20 per level, modern .NET style.

Entries are (level, topic, code, expected_output).
"""
LANGUAGE = "csharp"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
public static int Add(int a, int b)
{
    return a + b;
}
''', r'''Add(2, 3) => 5'''),
    ("very-easy", "math", r'''
public static bool IsEven(int n) => n % 2 == 0;
''', r'''IsEven(10) => true'''),
    ("very-easy", "math", r'''
public static long Square(long n) => n * n;
''', r'''Square(7) => 49'''),
    ("very-easy", "math", r'''
public static int Clamp(int n, int low, int high)
{
    return Math.Max(low, Math.Min(n, high));
}
''', r'''Clamp(42, 0, 10) => 10'''),
    ("very-easy", "strings", r'''
public static string Shout(string text)
{
    return text.ToUpperInvariant() + "!";
}
''', r'''Shout("hello") => HELLO!'''),
    ("very-easy", "strings", r'''
public static string Reverse(string text)
{
    var chars = text.ToCharArray();
    Array.Reverse(chars);
    return new string(chars);
}
''', r'''Reverse("csharp") => prahsc'''),
    ("very-easy", "strings", r'''
public static string Greet(string name) => $"hello {name}";
''', r'''Greet("world") => hello world'''),
    ("very-easy", "strings", r'''
public static bool IsBlank(string? text) => string.IsNullOrWhiteSpace(text);
''', r'''IsBlank("   ") => true'''),
    ("very-easy", "algorithms", r'''
public static int Sum(int[] numbers)
{
    var total = 0;
    foreach (var n in numbers)
    {
        total += n;
    }
    return total;
}
''', r'''Sum([1, 2, 3, 4]) => 10'''),
    ("very-easy", "algorithms", r'''
public static void CountUp(int n)
{
    for (var i = 1; i <= n; i++)
    {
        Console.WriteLine(i);
    }
}
''', r'''CountUp(3)
1
2
3'''),
    ("very-easy", "functional", r'''
public static IEnumerable<int> Doubled(IEnumerable<int> numbers)
{
    return numbers.Select(n => n * 2);
}
''', r'''Doubled([1, 2, 3]) => [2, 4, 6]'''),
    ("very-easy", "functional", r'''
public static IEnumerable<int> Evens(IEnumerable<int> numbers)
{
    return numbers.Where(n => n % 2 == 0);
}
''', r'''Evens([1, 2, 3, 4]) => [2, 4]'''),
    ("very-easy", "data-structures", r'''
public static List<string> Names()
{
    return new List<string> { "ada", "grace", "linus" };
}
''', r'''Names() => [ada, grace, linus]'''),
    ("very-easy", "data-structures", r'''
public static Dictionary<string, int> Scores()
{
    return new Dictionary<string, int>
    {
        ["ada"] = 98,
        ["grace"] = 104,
    };
}
''', r'''Scores() => {ada: 98, grace: 104}'''),
    ("very-easy", "oop", r'''
public class Dog
{
    public Dog(string name) => Name = name;

    public string Name { get; }

    public string Speak() => $"{Name} says woof";
}
''', r'''new Dog("Rex").Speak() => Rex says woof'''),
    ("very-easy", "oop", r'''
public record Point(int X, int Y)
{
    public int Manhattan => Math.Abs(X) + Math.Abs(Y);
}
''', r'''new Point(3, -4).Manhattan => 7'''),
    ("very-easy", "errors", r'''
public static int SafeInt(string text, int fallback = 0)
{
    return int.TryParse(text, out var value) ? value : fallback;
}
''', r'''SafeInt("oops") => 0'''),
    ("very-easy", "math", r'''
public static double Average(int[] numbers)
{
    return numbers.Length == 0 ? 0 : numbers.Average();
}
''', r'''Average([2, 4, 6]) => 4'''),
    ("very-easy", "data-structures", r'''
public static T? FirstOrDefaultValue<T>(IEnumerable<T> items) where T : struct
{
    foreach (var item in items)
    {
        return item;
    }
    return null;
}
''', r'''FirstOrDefaultValue(new int[0]) => null'''),
    ("very-easy", "strings", r'''
public static string Initials(string first, string last)
{
    return $"{first[0]}{last[0]}";
}
''', r'''Initials("Ada", "Lovelace") => AL'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
public static void FizzBuzz(int n)
{
    for (var i = 1; i <= n; i++)
    {
        if (i % 15 == 0) Console.WriteLine("FizzBuzz");
        else if (i % 3 == 0) Console.WriteLine("Fizz");
        else if (i % 5 == 0) Console.WriteLine("Buzz");
        else Console.WriteLine(i);
    }
}
''', r'''FizzBuzz(5)
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
public static long Fib(int n)
{
    long a = 0;
    long b = 1;
    for (var i = 0; i < n; i++)
    {
        (a, b) = (b, a + b);
    }
    return a;
}
''', r'''Fib(10) => 55'''),
    ("easy", "algorithms", r'''
public static long Factorial(int n)
{
    return n <= 1 ? 1 : n * Factorial(n - 1);
}
''', r'''Factorial(6) => 720'''),
    ("easy", "strings", r'''
public static bool IsPalindrome(string text)
{
    var clean = new string(text.Where(char.IsLetterOrDigit).ToArray()).ToLowerInvariant();
    return clean.SequenceEqual(clean.Reverse());
}
''', r'''IsPalindrome("A man, a plan, a canal: Panama") => true'''),
    ("easy", "strings", r'''
public static string TitleCase(string text)
{
    return string.Join(' ', text.Split(' ')
        .Select(word => char.ToUpperInvariant(word[0]) + word[1..].ToLowerInvariant()));
}
''', r'''TitleCase("hello wide world") => Hello Wide World'''),
    ("easy", "strings", r'''
public static string Slugify(string text)
{
    var lower = text.Trim().ToLowerInvariant();
    var clean = Regex.Replace(lower, "[^a-z0-9]+", "-");
    return clean.Trim('-');
}
''', r'''Slugify("  Hello, World! ") => hello-world'''),
    ("easy", "strings", r'''
public static string Truncate(string text, int max = 20)
{
    return text.Length <= max ? text : text[..(max - 1)] + "…";
}
''', r'''Truncate("a very long sentence", 10) => a very lo…'''),
    ("easy", "functional", r'''
public static IEnumerable<string> ActiveNames(IEnumerable<User> users)
{
    return users
        .Where(u => u.IsActive)
        .Select(u => u.Name)
        .OrderBy(name => name);
}
''', r'''ada
grace
linus'''),
    ("easy", "functional", r'''
public static Dictionary<int, List<string>> ByLength(IEnumerable<string> words)
{
    return words
        .GroupBy(word => word.Length)
        .ToDictionary(group => group.Key, group => group.ToList());
}
''', r'''ByLength(["a", "bb", "cc"]) => {1: [a], 2: [bb, cc]}'''),
    ("easy", "functional", r'''
public static int SumOfSquares(IEnumerable<int> numbers)
{
    return numbers.Sum(n => n * n);
}
''', r'''SumOfSquares([1, 2, 3]) => 14'''),
    ("easy", "data-structures", r'''
public static List<T> Unique<T>(IEnumerable<T> items)
{
    return items.Distinct().ToList();
}

public static List<List<T>> Chunk<T>(IEnumerable<T> items, int size)
{
    return items.Chunk(size).Select(c => c.ToList()).ToList();
}
''', r'''Chunk([1, 2, 3, 4, 5], 2) => [[1, 2], [3, 4], [5]]'''),
    ("easy", "data-structures", r'''
public static Dictionary<string, int> WordCount(string text)
{
    return text.Split(' ', StringSplitOptions.RemoveEmptyEntries)
        .GroupBy(word => word.ToLowerInvariant())
        .ToDictionary(group => group.Key, group => group.Count());
}
''', r'''WordCount("the cat the") => {the: 2, cat: 1}'''),
    ("easy", "math", r'''
public static bool IsPrime(int n)
{
    if (n < 2) return false;
    for (var d = 2; (long)d * d <= n; d++)
    {
        if (n % d == 0) return false;
    }
    return true;
}
''', r'''IsPrime(97) => true'''),
    ("easy", "math", r'''
public static int Gcd(int a, int b)
{
    while (b != 0)
    {
        (a, b) = (b, a % b);
    }
    return Math.Abs(a);
}
''', r'''Gcd(48, 18) => 6'''),
    ("easy", "oop", r'''
public class Counter
{
    private int _count;

    public int Bump(int by = 1)
    {
        _count += by;
        return _count;
    }

    public int Value => _count;
}
''', r'''new Counter().Bump(3) => 3'''),
    ("easy", "oop", r'''
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
''', r'''await FindAsync(1) => the entity, or null'''),
    ("easy", "errors", r'''
public static double Divide(double a, double b)
{
    if (b == 0)
    {
        throw new DivideByZeroException("cannot divide by zero");
    }
    return a / b;
}
''', r'''Divide(1, 0)
DivideByZeroException: cannot divide by zero'''),
    ("easy", "async", r'''
public static async Task<string> LoadAsync(HttpClient http, string url)
{
    using var response = await http.GetAsync(url);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadAsStringAsync();
}
''', r'''await LoadAsync(http, "/api/me") => {"name":"ada"}'''),
    ("easy", "data", r'''
public static async Task<List<string>> ReadLinesAsync(string path)
{
    var lines = await File.ReadAllLinesAsync(path);
    return lines.Where(line => !string.IsNullOrWhiteSpace(line)).ToList();
}
''', r'''await ReadLinesAsync("names.txt") => [ada, grace, linus]'''),
    ("easy", "web", r'''
public static string BuildUrl(string basePath, Dictionary<string, string> query)
{
    var parts = query.Select(pair => $"{pair.Key}={Uri.EscapeDataString(pair.Value)}");
    return query.Count == 0 ? basePath : $"{basePath}?{string.Join('&', parts)}";
}
''', r'''BuildUrl("/search", {q: "code race"}) => /search?q=code%20race'''),

    ("easy", "math", r"""
public static int SumTo(int n)
{
    return Enumerable.Range(1, n).Sum();
}
""", r"""SumTo(10) => 55"""),
    ("easy", "data-structures", r"""
public static string? MostCommon(IEnumerable<string> items)
{
    return items
        .GroupBy(item => item)
        .OrderByDescending(group => group.Count())
        .Select(group => group.Key)
        .FirstOrDefault();
}
""", r"""MostCommon(["a", "b", "a"]) => a"""),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
public static int BinarySearch(int[] items, int target)
{
    var low = 0;
    var high = items.Length - 1;
    while (low <= high)
    {
        var mid = low + (high - low) / 2;
        if (items[mid] == target) return mid;
        if (items[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
''', r'''BinarySearch([1, 3, 5, 7, 9], 7) => 3'''),
    ("medium", "algorithms", r'''
public static (int, int)? TwoSum(int[] numbers, int target)
{
    var seen = new Dictionary<int, int>();
    for (var i = 0; i < numbers.Length; i++)
    {
        if (seen.TryGetValue(target - numbers[i], out var partner))
        {
            return (partner, i);
        }
        seen[numbers[i]] = i;
    }
    return null;
}
''', r'''TwoSum([2, 7, 11, 15], 9) => (0, 1)'''),
    ("medium", "algorithms", r'''
public static int MaxSubarray(int[] numbers)
{
    var best = numbers[0];
    var current = numbers[0];
    for (var i = 1; i < numbers.Length; i++)
    {
        current = Math.Max(numbers[i], current + numbers[i]);
        best = Math.Max(best, current);
    }
    return best;
}
''', r'''MaxSubarray([-2, 1, -3, 4, -1, 2, 1]) => 6'''),
    ("medium", "data-structures", r'''
public class Stack<T>
{
    private readonly List<T> _items = new();

    public void Push(T item) => _items.Add(item);

    public T Pop()
    {
        if (_items.Count == 0)
        {
            throw new InvalidOperationException("the stack is empty");
        }
        var item = _items[^1];
        _items.RemoveAt(_items.Count - 1);
        return item;
    }

    public int Count => _items.Count;
}
''', r'''Push(1); Push(2); Pop() => 2'''),
    ("medium", "data-structures", r'''
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
''', r'''capacity 3, add 1..4 => oldest dropped'''),
    ("medium", "data-structures", r'''
public class Node<T>
{
    public Node(T value, Node<T>? next = null)
    {
        Value = value;
        Next = next;
    }

    public T Value { get; }
    public Node<T>? Next { get; set; }

    public IEnumerable<T> Walk()
    {
        for (var cursor = this; cursor is not null; cursor = cursor.Next)
        {
            yield return cursor.Value;
        }
    }
}
''', r'''1 -> 2 -> 3 => [1, 2, 3]'''),
    ("medium", "oop", r'''
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
''', r'''new Shape.Rect(3, 4).Area() => 12'''),
    ("medium", "oop", r'''
public class ServerBuilder
{
    private string _host = "0.0.0.0";
    private int _port = 8000;

    public ServerBuilder Host(string host)
    {
        _host = host;
        return this;
    }

    public ServerBuilder Port(int port)
    {
        _port = port;
        return this;
    }

    public string Build() => $"{_host}:{_port}";
}
''', r'''new ServerBuilder().Port(25616).Build() => 0.0.0.0:25616'''),
    ("medium", "async", r'''
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
''', r'''await BuildAsync(7, token) => Report { Id = 7 }'''),
    ("medium", "async", r'''
public static async Task<List<T>> WhenAllLimited<T>(
    IEnumerable<Func<Task<T>>> tasks,
    int limit)
{
    using var gate = new SemaphoreSlim(limit);
    var running = tasks.Select(async task =>
    {
        await gate.WaitAsync();
        try
        {
            return await task();
        }
        finally
        {
            gate.Release();
        }
    });
    return (await Task.WhenAll(running)).ToList();
}
''', r'''await WhenAllLimited(fetches, 4) => at most four at a time'''),
    ("medium", "async", r'''
public static async Task<T?> WithTimeoutAsync<T>(Task<T> task, TimeSpan timeout)
{
    var timer = Task.Delay(timeout);
    var winner = await Task.WhenAny(task, timer);
    return winner == task ? await task : default;
}
''', r'''await WithTimeoutAsync(slow, 100ms) => null'''),
    ("medium", "functional", r'''
public static Func<T, TResult> Memoize<T, TResult>(Func<T, TResult> fn)
    where T : notnull
{
    var cache = new Dictionary<T, TResult>();
    return key =>
    {
        if (!cache.TryGetValue(key, out var value))
        {
            value = fn(key);
            cache[key] = value;
        }
        return value;
    };
}
''', r'''var square = Memoize<int, int>(n => n * n); square(9) => 81'''),
    ("medium", "functional", r'''
public static IEnumerable<TResult> ZipWith<T1, T2, TResult>(
    IEnumerable<T1> left,
    IEnumerable<T2> right,
    Func<T1, T2, TResult> combine)
{
    return left.Zip(right, combine);
}
''', r'''ZipWith([1, 2], ["a", "b"], (n, s) => $"{n}{s}") => [1a, 2b]'''),
    ("medium", "errors", r'''
public class ValidationException : Exception
{
    public ValidationException(string field, string message)
        : base($"{field}: {message}")
    {
        Field = field;
    }

    public string Field { get; }
}
''', r'''new ValidationException("email", "is required").Message
email: is required'''),
    ("medium", "errors", r'''
public static async Task<T> RetryAsync<T>(Func<Task<T>> work, int attempts = 3)
{
    Exception? last = null;
    for (var attempt = 0; attempt < attempts; attempt++)
    {
        try
        {
            return await work();
        }
        catch (Exception e)
        {
            last = e;
            await Task.Delay(TimeSpan.FromMilliseconds(200 * Math.Pow(2, attempt)));
        }
    }
    throw new AggregateException($"failed after {attempts} attempts", last!);
}
''', r'''await RetryAsync(flaky)
AggregateException: failed after 3 attempts'''),
    ("medium", "data", r'''
public static async Task<List<User>> FindActiveAsync(string connectionString)
{
    await using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    await using var command = new SqlCommand(
        "SELECT id, name FROM users WHERE active = 1", connection);
    await using var rows = await command.ExecuteReaderAsync();

    var users = new List<User>();
    while (await rows.ReadAsync())
    {
        users.Add(new User(rows.GetInt32(0), rows.GetString(1)));
    }
    return users;
}
''', r'''await FindActiveAsync(cs) => [User(1, ada), User(2, grace)]'''),
    ("medium", "web", r'''
app.MapGet("/races/{id:int}", async (int id, IRaceStore store) =>
{
    var race = await store.FindAsync(id);
    return race is null ? Results.NotFound() : Results.Ok(race);
});
''', r'''GET /races/99 => 404 Not Found'''),
    ("medium", "math", r'''
public static double Percentile(double[] values, double p)
{
    var sorted = values.OrderBy(v => v).ToArray();
    var index = (sorted.Length - 1) * (p / 100);
    var low = (int)Math.Floor(index);
    var high = (int)Math.Ceiling(index);
    if (low == high) return sorted[low];
    return sorted[low] + (sorted[high] - sorted[low]) * (index - low);
}
''', r'''Percentile([10, 20, 30, 40], 50) => 25'''),
    ("medium", "oop", r'''
public interface IClock
{
    DateTimeOffset Now { get; }
}

public sealed class SystemClock : IClock
{
    public DateTimeOffset Now => DateTimeOffset.UtcNow;
}

public sealed class FrozenClock : IClock
{
    public FrozenClock(DateTimeOffset now) => Now = now;

    public DateTimeOffset Now { get; }
}
''', r'''new FrozenClock(epoch).Now => 1970-01-01T00:00:00+00:00'''),
    ("medium", "data-structures", r'''
public static Dictionary<TKey, int> Frequencies<T, TKey>(
    IEnumerable<T> items,
    Func<T, TKey> key) where TKey : notnull
{
    return items
        .GroupBy(key)
        .ToDictionary(group => group.Key, group => group.Count());
}
''', r'''Frequencies(["a", "b", "a"], s => s) => {a: 2, b: 1}'''),

    ("medium", "strings", r"""
public static string Template(string text, IDictionary<string, object> values)
{
    return Regex.Replace(text, @"\{(\w+)\}", match =>
        values.TryGetValue(match.Groups[1].Value, out var value)
            ? value.ToString() ?? string.Empty
            : match.Value);
}
""", r"""Template("hi {name}", {name: "ada"}) => hi ada"""),
    ("medium", "functional", r"""
public static IEnumerable<T> DistinctBy2<T, TKey>(
    IEnumerable<T> items,
    Func<T, TKey> key)
{
    var seen = new HashSet<TKey>();
    foreach (var item in items)
    {
        if (seen.Add(key(item)))
        {
            yield return item;
        }
    }
}
""", r"""DistinctBy2(races, r => r.Language) => one race per language"""),

    # --------------------------------------------------------------------- hard
    ("hard", "data-structures", r'''
public sealed class LruCache<TKey, TValue> where TKey : notnull
{
    private readonly int _capacity;
    private readonly Dictionary<TKey, LinkedListNode<(TKey Key, TValue Value)>> _index = new();
    private readonly LinkedList<(TKey Key, TValue Value)> _order = new();

    public LruCache(int capacity) => _capacity = capacity;

    public bool TryGet(TKey key, out TValue value)
    {
        if (!_index.TryGetValue(key, out var node))
        {
            value = default!;
            return false;
        }
        _order.Remove(node);
        _order.AddFirst(node);
        value = node.Value.Value;
        return true;
    }

    public void Put(TKey key, TValue value)
    {
        if (_index.TryGetValue(key, out var existing))
        {
            _order.Remove(existing);
        }
        else if (_index.Count >= _capacity)
        {
            var last = _order.Last!;
            _index.Remove(last.Value.Key);
            _order.RemoveLast();
        }
        _index[key] = _order.AddFirst((key, value));
    }
}
''', r'''capacity 2: Put a, Put b, Put c => a evicted'''),
    ("hard", "data-structures", r'''
public sealed class Trie
{
    private readonly Dictionary<char, Trie> _children = new();
    private bool _word;

    public void Insert(string word)
    {
        var node = this;
        foreach (var c in word)
        {
            if (!node._children.TryGetValue(c, out var child))
            {
                child = new Trie();
                node._children[c] = child;
            }
            node = child;
        }
        node._word = true;
    }

    public bool Contains(string word)
    {
        var node = this;
        foreach (var c in word)
        {
            if (!node._children.TryGetValue(c, out var child)) return false;
            node = child;
        }
        return node._word;
    }
}
''', r'''Insert("code"); Contains("code") => true; Contains("cod") => false'''),
    ("hard", "algorithms", r'''
public static Dictionary<string, int> Dijkstra(
    Dictionary<string, Dictionary<string, int>> graph,
    string start)
{
    var distances = new Dictionary<string, int> { [start] = 0 };
    var queue = new PriorityQueue<string, int>();
    queue.Enqueue(start, 0);

    while (queue.TryDequeue(out var node, out var cost))
    {
        if (cost > distances.GetValueOrDefault(node, int.MaxValue)) continue;
        if (!graph.TryGetValue(node, out var edges)) continue;

        foreach (var (next, weight) in edges)
        {
            var candidate = cost + weight;
            if (candidate < distances.GetValueOrDefault(next, int.MaxValue))
            {
                distances[next] = candidate;
                queue.Enqueue(next, candidate);
            }
        }
    }
    return distances;
}
''', r'''Dijkstra(graph, "a") => {a: 0, b: 1, c: 3}'''),
    ("hard", "algorithms", r'''
public static int Levenshtein(string a, string b)
{
    var previous = Enumerable.Range(0, b.Length + 1).ToArray();
    for (var i = 1; i <= a.Length; i++)
    {
        var current = new int[b.Length + 1];
        current[0] = i;
        for (var j = 1; j <= b.Length; j++)
        {
            var cost = a[i - 1] == b[j - 1] ? 0 : 1;
            current[j] = Math.Min(
                Math.Min(previous[j] + 1, current[j - 1] + 1),
                previous[j - 1] + cost);
        }
        previous = current;
    }
    return previous[b.Length];
}
''', r'''Levenshtein("kitten", "sitting") => 3'''),
    ("hard", "algorithms", r'''
public static void QuickSort(int[] a, int lo, int hi)
{
    if (lo >= hi) return;

    var pivot = a[(lo + hi) / 2];
    var i = lo;
    var j = hi;
    while (i <= j)
    {
        while (a[i] < pivot) i++;
        while (a[j] > pivot) j--;
        if (i <= j)
        {
            (a[i], a[j]) = (a[j], a[i]);
            i++;
            j--;
        }
    }
    QuickSort(a, lo, j);
    QuickSort(a, i, hi);
}
''', r'''[3, 6, 1, 8, 2] => [1, 2, 3, 6, 8]'''),
    ("hard", "async", r'''
public static async IAsyncEnumerable<T[]> BatchedAsync<T>(
    IAsyncEnumerable<T> source,
    int size,
    [EnumeratorCancellation] CancellationToken token = default)
{
    var batch = new List<T>(size);
    await foreach (var item in source.WithCancellation(token))
    {
        batch.Add(item);
        if (batch.Count >= size)
        {
            yield return batch.ToArray();
            batch.Clear();
        }
    }
    if (batch.Count > 0)
    {
        yield return batch.ToArray();
    }
}
''', r'''await foreach (var group in BatchedAsync(stream, 2)) => 2, 2, 1'''),
    ("hard", "async", r'''
public sealed class AsyncLock : IDisposable
{
    private readonly SemaphoreSlim _gate = new(1, 1);

    public async Task<IDisposable> AcquireAsync(CancellationToken token = default)
    {
        await _gate.WaitAsync(token);
        return new Releaser(_gate);
    }

    public void Dispose() => _gate.Dispose();

    private sealed class Releaser : IDisposable
    {
        private readonly SemaphoreSlim _gate;

        public Releaser(SemaphoreSlim gate) => _gate = gate;

        public void Dispose() => _gate.Release();
    }
}
''', r'''using (await guard.AcquireAsync()) { ... } => one holder at a time'''),
    ("hard", "async", r'''
public static async Task ProduceConsumeAsync(int producers, int consumers)
{
    var channel = Channel.CreateBounded<int>(64);

    var writers = Enumerable.Range(0, producers).Select(async id =>
    {
        for (var i = 0; i < 100; i++)
        {
            await channel.Writer.WriteAsync(id * 100 + i);
        }
    });

    var readers = Enumerable.Range(0, consumers).Select(async _ =>
    {
        await foreach (var item in channel.Reader.ReadAllAsync())
        {
            Handle(item);
        }
    });

    await Task.WhenAll(writers);
    channel.Writer.Complete();
    await Task.WhenAll(readers);
}
''', r'''ProduceConsumeAsync(2, 4) => 200 items handled, then completion'''),
    ("hard", "oop", r'''
public sealed class Mediator
{
    private readonly Dictionary<Type, List<Func<object, Task>>> _handlers = new();

    public void Register<TMessage>(Func<TMessage, Task> handler)
    {
        if (!_handlers.TryGetValue(typeof(TMessage), out var list))
        {
            list = new List<Func<object, Task>>();
            _handlers[typeof(TMessage)] = list;
        }
        list.Add(message => handler((TMessage)message));
    }

    public async Task PublishAsync<TMessage>(TMessage message)
        where TMessage : notnull
    {
        if (!_handlers.TryGetValue(typeof(TMessage), out var list)) return;
        foreach (var handler in list)
        {
            await handler(message);
        }
    }
}
''', r'''Register<RaceFinished>(OnFinish); await PublishAsync(evt)'''),
    ("hard", "oop", r'''
public readonly struct Meters : IEquatable<Meters>, IComparable<Meters>
{
    public Meters(double value) => Value = value;

    public double Value { get; }

    public static Meters operator +(Meters a, Meters b) => new(a.Value + b.Value);

    public bool Equals(Meters other) => Value.Equals(other.Value);

    public int CompareTo(Meters other) => Value.CompareTo(other.Value);

    public override string ToString() => $"{Value:0.0}m";
}
''', r'''new Meters(1.5) + new Meters(2) => 3.5m'''),
    ("hard", "functional", r'''
public static Func<T, TResult> Compose<T, TMiddle, TResult>(
    Func<T, TMiddle> first,
    Func<TMiddle, TResult> second)
{
    return value => second(first(value));
}

public static Func<T1, Func<T2, TResult>> Curry<T1, T2, TResult>(
    Func<T1, T2, TResult> fn)
{
    return a => b => fn(a, b);
}
''', r'''Curry<int, int, int>((a, b) => a + b)(1)(2) => 3'''),
    ("hard", "functional", r'''
public static IEnumerable<T> Traverse<T>(T root, Func<T, IEnumerable<T>> children)
{
    var stack = new Stack<T>();
    stack.Push(root);
    while (stack.Count > 0)
    {
        var node = stack.Pop();
        yield return node;
        foreach (var child in children(node).Reverse())
        {
            stack.Push(child);
        }
    }
}
''', r'''Traverse(root, n => n.Children) => depth-first order'''),
    ("hard", "errors", r'''
public readonly record struct Result<T>
{
    private Result(T? value, string? error)
    {
        Value = value;
        Error = error;
    }

    public T? Value { get; }
    public string? Error { get; }
    public bool IsOk => Error is null;

    public static Result<T> Ok(T value) => new(value, null);
    public static Result<T> Fail(string error) => new(default, error);

    public Result<TNext> Map<TNext>(Func<T, TNext> fn) =>
        IsOk ? Result<TNext>.Ok(fn(Value!)) : Result<TNext>.Fail(Error!);
}
''', r'''Result<int>.Fail("nope").Map(n => n * 2).Error => nope'''),
    ("hard", "data", r'''
public static async Task<int> TransferAsync(
    DbConnection connection,
    int from,
    int to,
    decimal amount)
{
    await using var tx = await connection.BeginTransactionAsync();
    try
    {
        var debited = await connection.ExecuteAsync(
            "UPDATE accounts SET balance = balance - @amount " +
            "WHERE id = @from AND balance >= @amount",
            new { amount, from }, tx);

        if (debited == 0)
        {
            throw new InvalidOperationException("insufficient funds");
        }

        await connection.ExecuteAsync(
            "UPDATE accounts SET balance = balance + @amount WHERE id = @to",
            new { amount, to }, tx);

        await tx.CommitAsync();
        return debited;
    }
    catch
    {
        await tx.RollbackAsync();
        throw;
    }
}
''', r'''await TransferAsync(conn, 1, 2, 500m) => 1, or rolled back'''),
    ("hard", "web", r'''
public sealed class RateLimitMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ConcurrentDictionary<string, int> _hits = new();

    public RateLimitMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        var key = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var count = _hits.AddOrUpdate(key, 1, (_, value) => value + 1);
        if (count > 100)
        {
            context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
            return;
        }
        await _next(context);
    }
}
''', r'''the 101st request from one address => 429 Too Many Requests'''),
    ("hard", "strings", r'''
public static List<(string Word, int Count)> TopWords(string text, int limit)
{
    return Regex.Matches(text.ToLowerInvariant(), @"[a-z0-9']+")
        .Select(match => match.Value)
        .GroupBy(word => word)
        .Select(group => (Word: group.Key, Count: group.Count()))
        .OrderByDescending(pair => pair.Count)
        .ThenBy(pair => pair.Word)
        .Take(limit)
        .ToList();
}
''', r'''TopWords("the cat the hat the end", 2) => [(the, 3), (cat, 1)]'''),
    ("hard", "math", r'''
public static double[,] Multiply(double[,] a, double[,] b)
{
    var rows = a.GetLength(0);
    var inner = b.GetLength(0);
    var cols = b.GetLength(1);
    var out_ = new double[rows, cols];

    for (var i = 0; i < rows; i++)
    {
        for (var k = 0; k < inner; k++)
        {
            var value = a[i, k];
            if (value == 0) continue;
            for (var j = 0; j < cols; j++)
            {
                out_[i, j] += value * b[k, j];
            }
        }
    }
    return out_;
}
''', r'''[[1, 2]] x [[3], [4]] => [[11]]'''),
    ("hard", "oop", r'''
public sealed class ObjectPool<T> where T : class
{
    private readonly ConcurrentBag<T> _idle = new();
    private readonly Func<T> _factory;

    public ObjectPool(Func<T> factory) => _factory = factory;

    public T Rent() => _idle.TryTake(out var item) ? item : _factory();

    public void Return(T item) => _idle.Add(item);
}
''', r'''Rent() => new; Return(it); Rent() => the same instance'''),
    ("hard", "data-structures", r'''
public sealed class Graph<T> where T : notnull
{
    private readonly Dictionary<T, HashSet<T>> _edges = new();

    public void Link(T from, T to)
    {
        if (!_edges.TryGetValue(from, out var set))
        {
            set = new HashSet<T>();
            _edges[from] = set;
        }
        set.Add(to);
    }

    public HashSet<T> Reachable(T start)
    {
        var seen = new HashSet<T> { start };
        var stack = new Stack<T>();
        stack.Push(start);
        while (stack.Count > 0)
        {
            foreach (var next in _edges.GetValueOrDefault(stack.Pop(), new HashSet<T>()))
            {
                if (seen.Add(next)) stack.Push(next);
            }
        }
        return seen;
    }
}
''', r'''Link(a, b); Link(b, c); Reachable("a") => {a, b, c}'''),
    ("hard", "functional", r'''
public static IEnumerable<TResult> SelectManyIndexed<T, TResult>(
    this IEnumerable<T> source,
    Func<T, int, IEnumerable<TResult>> selector)
{
    var index = 0;
    foreach (var item in source)
    {
        foreach (var result in selector(item, index))
        {
            yield return result;
        }
        index++;
    }
}
''', r'''rows.SelectManyIndexed((r, i) => r.Cells) => flattened with positions'''),
]
