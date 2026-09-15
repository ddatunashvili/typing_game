"""PHP snippet pack: 20 per level, modern PHP 8 style.

Entries are (level, topic, code, expected_output).
"""
LANGUAGE = "php"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
<?php

function add(int $a, int $b): int
{
    return $a + $b;
}
''', r'''php > echo add(2, 3);
5'''),
    ("very-easy", "math", r'''
<?php

function isEven(int $n): bool
{
    return $n % 2 === 0;
}
''', r'''php > var_dump(isEven(10));
bool(true)'''),
    ("very-easy", "math", r'''
<?php

function square(int $n): int
{
    return $n * $n;
}
''', r'''php > echo square(7);
49'''),
    ("very-easy", "math", r'''
<?php

function clampTo(int $n, int $low, int $high): int
{
    return max($low, min($n, $high));
}
''', r'''php > echo clampTo(42, 0, 10);
10'''),
    ("very-easy", "strings", r'''
<?php

function shout(string $text): string
{
    return strtoupper($text) . '!';
}
''', r'''php > echo shout("hello");
HELLO!'''),
    ("very-easy", "strings", r'''
<?php

function greet(string $name): string
{
    return "hello {$name}";
}
''', r'''php > echo greet("world");
hello world'''),
    ("very-easy", "strings", r'''
<?php

function reverseText(string $text): string
{
    return strrev($text);
}
''', r'''php > echo reverseText("php");
php'''),
    ("very-easy", "strings", r'''
<?php

function isBlank(?string $text): bool
{
    return trim((string) $text) === '';
}
''', r'''php > var_dump(isBlank("   "));
bool(true)'''),
    ("very-easy", "algorithms", r'''
<?php

function sumAll(array $numbers): int
{
    $total = 0;
    foreach ($numbers as $n) {
        $total += $n;
    }
    return $total;
}
''', r'''php > echo sumAll([1, 2, 3, 4]);
10'''),
    ("very-easy", "algorithms", r'''
<?php

function countUp(int $n): void
{
    for ($i = 1; $i <= $n; $i++) {
        echo $i, PHP_EOL;
    }
}
''', r'''php > countUp(3);
1
2
3'''),
    ("very-easy", "algorithms", r'''
<?php

function largest(array $numbers): int
{
    return max($numbers);
}
''', r'''php > echo largest([3, 9, 4]);
9'''),
    ("very-easy", "functional", r'''
<?php

function doubled(array $numbers): array
{
    return array_map(static fn (int $n): int => $n * 2, $numbers);
}
''', r'''php > print_r(doubled([1, 2, 3]));
Array([0] => 2 [1] => 4 [2] => 6)'''),
    ("very-easy", "functional", r'''
<?php

function evens(array $numbers): array
{
    return array_values(array_filter($numbers, static fn (int $n): bool => $n % 2 === 0));
}
''', r'''php > print_r(evens([1, 2, 3, 4]));
Array([0] => 2 [1] => 4)'''),
    ("very-easy", "data-structures", r'''
<?php

function names(): array
{
    return ['ada', 'grace', 'linus'];
}
''', r'''php > print_r(names());
Array([0] => ada [1] => grace [2] => linus)'''),
    ("very-easy", "data-structures", r'''
<?php

function scores(): array
{
    return [
        'ada' => 98,
        'grace' => 104,
    ];
}
''', r'''php > print_r(scores());
Array([ada] => 98 [grace] => 104)'''),
    ("very-easy", "oop", r'''
<?php

class Dog
{
    public function __construct(private string $name)
    {
    }

    public function speak(): string
    {
        return "{$this->name} says woof";
    }
}
''', r'''php > echo (new Dog("Rex"))->speak();
Rex says woof'''),
    ("very-easy", "oop", r'''
<?php

final class Point
{
    public function __construct(
        public readonly int $x,
        public readonly int $y,
    ) {
    }

    public function manhattan(): int
    {
        return abs($this->x) + abs($this->y);
    }
}
''', r'''php > echo (new Point(3, -4))->manhattan();
7'''),
    ("very-easy", "errors", r'''
<?php

function safeInt(string $text, int $fallback = 0): int
{
    return is_numeric($text) ? (int) $text : $fallback;
}
''', r'''php > echo safeInt("oops");
0'''),
    ("very-easy", "math", r'''
<?php

function average(array $numbers): float
{
    if ($numbers === []) {
        return 0.0;
    }
    return array_sum($numbers) / count($numbers);
}
''', r'''php > echo average([2, 4, 6]);
4'''),
    ("very-easy", "strings", r'''
<?php

function initials(string $first, string $last): string
{
    return $first[0] . $last[0];
}
''', r'''php > echo initials("Ada", "Lovelace");
AL'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
<?php

function fizzbuzz(int $n): void
{
    for ($i = 1; $i <= $n; $i++) {
        if ($i % 15 === 0) {
            echo 'FizzBuzz', PHP_EOL;
        } elseif ($i % 3 === 0) {
            echo 'Fizz', PHP_EOL;
        } elseif ($i % 5 === 0) {
            echo 'Buzz', PHP_EOL;
        } else {
            echo $i, PHP_EOL;
        }
    }
}
''', r'''php > fizzbuzz(5);
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
<?php

function fib(int $n): int
{
    [$a, $b] = [0, 1];
    for ($i = 0; $i < $n; $i++) {
        [$a, $b] = [$b, $a + $b];
    }
    return $a;
}
''', r'''php > echo fib(10);
55'''),
    ("easy", "algorithms", r'''
<?php

function factorial(int $n): int
{
    return $n <= 1 ? 1 : $n * factorial($n - 1);
}
''', r'''php > echo factorial(6);
720'''),
    ("easy", "strings", r'''
<?php

function slugify(string $text): string
{
    $text = strtolower(trim($text));
    $text = preg_replace('/[^a-z0-9]+/', '-', $text);
    return trim($text, '-');
}
''', r'''php > echo slugify("  Hello, World!  ");
hello-world'''),
    ("easy", "strings", r'''
<?php

function isPalindrome(string $text): bool
{
    $clean = preg_replace('/[^a-z0-9]/', '', strtolower($text));
    return $clean === strrev($clean);
}
''', r'''php > var_dump(isPalindrome("A man, a plan, a canal: Panama"));
bool(true)'''),
    ("easy", "strings", r'''
<?php

function titleCase(string $text): string
{
    return ucwords(strtolower($text));
}
''', r'''php > echo titleCase("hello wide world");
Hello Wide World'''),
    ("easy", "strings", r'''
<?php

function truncate(string $text, int $max = 20): string
{
    if (mb_strlen($text) <= $max) {
        return $text;
    }
    return mb_substr($text, 0, $max - 1) . '…';
}
''', r'''php > echo truncate("a very long sentence", 10);
a very lo…'''),
    ("easy", "data-structures", r'''
<?php

function wordCount(string $text): array
{
    $counts = [];
    foreach (preg_split('/\s+/', strtolower(trim($text))) as $word) {
        if ($word === '') {
            continue;
        }
        $counts[$word] = ($counts[$word] ?? 0) + 1;
    }
    return $counts;
}
''', r'''php > print_r(wordCount("the cat the"));
Array([the] => 2 [cat] => 1)'''),
    ("easy", "data-structures", r'''
<?php

function chunkList(array $items, int $size): array
{
    return array_chunk($items, $size);
}

function uniqueList(array $items): array
{
    return array_values(array_unique($items));
}
''', r'''php > print_r(chunkList([1, 2, 3, 4, 5], 2));
Array([0] => Array([0] => 1 [1] => 2) ...)'''),
    ("easy", "data-structures", r'''
<?php

function groupByLength(array $words): array
{
    $groups = [];
    foreach ($words as $word) {
        $groups[strlen($word)][] = $word;
    }
    return $groups;
}
''', r'''php > print_r(groupByLength(["a", "bb", "cc"]));
Array([1] => Array([0] => a) [2] => Array([0] => bb [1] => cc))'''),
    ("easy", "math", r'''
<?php

function isPrime(int $n): bool
{
    if ($n < 2) {
        return false;
    }
    for ($d = 2; $d * $d <= $n; $d++) {
        if ($n % $d === 0) {
            return false;
        }
    }
    return true;
}
''', r'''php > var_dump(isPrime(97));
bool(true)'''),
    ("easy", "math", r'''
<?php

function gcd(int $a, int $b): int
{
    while ($b !== 0) {
        [$a, $b] = [$b, $a % $b];
    }
    return abs($a);
}
''', r'''php > echo gcd(48, 18);
6'''),
    ("easy", "oop", r'''
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
''', r'''php > $total = (new Money(100))->plus(new Money(50));'''),
    ("easy", "oop", r'''
<?php

class Counter
{
    private int $count = 0;

    public function bump(int $by = 1): int
    {
        $this->count += $by;
        return $this->count;
    }

    public function value(): int
    {
        return $this->count;
    }
}
''', r'''php > echo (new Counter())->bump(3);
3'''),
    ("easy", "errors", r'''
<?php

function divide(float $a, float $b): float
{
    if ($b === 0.0) {
        throw new InvalidArgumentException('cannot divide by zero');
    }
    return $a / $b;
}
''', r'''php > divide(1, 0);
InvalidArgumentException: cannot divide by zero'''),
    ("easy", "data", r'''
<?php

function findUser(PDO $db, int $id): ?array
{
    $stmt = $db->prepare('SELECT id, name, email FROM users WHERE id = :id');
    $stmt->execute(['id' => $id]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    return $row === false ? null : $row;
}
''', r'''php > print_r(findUser($db, 1));
Array([id] => 1 [name] => ada [email] => ada@example.com)'''),
    ("easy", "data", r'''
<?php

function readLines(string $path): array
{
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    return $lines === false ? [] : $lines;
}
''', r'''php > print_r(readLines("names.txt"));
Array([0] => ada [1] => grace)'''),
    ("easy", "web", r'''
<?php

function buildUrl(string $base, array $params): string
{
    return $params === [] ? $base : $base . '?' . http_build_query($params);
}
''', r'''php > echo buildUrl("/search", ["q" => "code race"]);
/search?q=code+race'''),
    ("easy", "web", r'''
<?php

function jsonResponse(mixed $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json');
    echo json_encode($payload, JSON_THROW_ON_ERROR);
}
''', r'''php > jsonResponse(["wpm" => 98]);
{"wpm":98}'''),
    ("easy", "functional", r'''
<?php

function sumOfSquares(array $numbers): int
{
    return array_reduce(
        $numbers,
        static fn (int $acc, int $n): int => $acc + $n * $n,
        0
    );
}
''', r'''php > echo sumOfSquares([1, 2, 3]);
14'''),

    ("easy", "math", r"""
<?php

function sumTo(int $n): int
{
    return intdiv($n * ($n + 1), 2);
}
""", r"""php > echo sumTo(10);
55"""),
    ("easy", "data-structures", r"""
<?php

function mostCommon(array $items): ?string
{
    if ($items === []) {
        return null;
    }
    $counts = array_count_values($items);
    arsort($counts);
    return (string) array_key_first($counts);
}
""", r"""php > echo mostCommon(["a", "b", "a"]);
a"""),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
<?php

function binarySearch(array $items, int $target): int
{
    $low = 0;
    $high = count($items) - 1;
    while ($low <= $high) {
        $mid = intdiv($low + $high, 2);
        if ($items[$mid] === $target) {
            return $mid;
        }
        if ($items[$mid] < $target) {
            $low = $mid + 1;
        } else {
            $high = $mid - 1;
        }
    }
    return -1;
}
''', r'''php > echo binarySearch([1, 3, 5, 7, 9], 7);
3'''),
    ("medium", "algorithms", r'''
<?php

function twoSum(array $numbers, int $target): ?array
{
    $seen = [];
    foreach ($numbers as $i => $n) {
        if (isset($seen[$target - $n])) {
            return [$seen[$target - $n], $i];
        }
        $seen[$n] = $i;
    }
    return null;
}
''', r'''php > print_r(twoSum([2, 7, 11, 15], 9));
Array([0] => 0 [1] => 1)'''),
    ("medium", "algorithms", r'''
<?php

function maxSubarray(array $numbers): int
{
    $best = $numbers[0];
    $current = $numbers[0];
    for ($i = 1; $i < count($numbers); $i++) {
        $current = max($numbers[$i], $current + $numbers[$i]);
        $best = max($best, $current);
    }
    return $best;
}
''', r'''php > echo maxSubarray([-2, 1, -3, 4, -1, 2, 1]);
6'''),
    ("medium", "data-structures", r'''
<?php

final class Stack implements Countable
{
    /** @var list<mixed> */
    private array $items = [];

    public function push(mixed $item): void
    {
        $this->items[] = $item;
    }

    public function pop(): mixed
    {
        if ($this->items === []) {
            throw new UnderflowException('the stack is empty');
        }
        return array_pop($this->items);
    }

    public function count(): int
    {
        return count($this->items);
    }
}
''', r'''php > $s = new Stack(); $s->push(1); $s->push(2); echo $s->pop();
2'''),
    ("medium", "data-structures", r'''
<?php

final class Collection implements Countable, IteratorAggregate
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

    public function getIterator(): ArrayIterator
    {
        return new ArrayIterator($this->items);
    }

    public function count(): int
    {
        return count($this->items);
    }
}
''', r'''php > count((new Collection([1, 2, 3]))->filter(fn ($n) => $n > 1));
2'''),
    ("medium", "oop", r'''
<?php

interface Shape
{
    public function area(): float;
}

final class Rect implements Shape
{
    public function __construct(
        private readonly float $width,
        private readonly float $height,
    ) {
    }

    public function area(): float
    {
        return $this->width * $this->height;
    }
}
''', r'''php > echo (new Rect(3, 4))->area();
12'''),
    ("medium", "oop", r'''
<?php

enum Status: string
{
    case Waiting = 'waiting';
    case Racing = 'racing';
    case Finished = 'finished';

    public function isOver(): bool
    {
        return $this === self::Finished;
    }
}
''', r'''php > var_dump(Status::from('finished')->isOver());
bool(true)'''),
    ("medium", "oop", r'''
<?php

trait Timestamps
{
    private ?DateTimeImmutable $createdAt = null;

    public function touch(): void
    {
        $this->createdAt ??= new DateTimeImmutable();
    }

    public function createdAt(): ?DateTimeImmutable
    {
        return $this->createdAt;
    }
}
''', r'''php > $race->touch(); echo $race->createdAt()->format('Y-m-d');
2026-09-16'''),
    ("medium", "errors", r'''
<?php

final class ValidationException extends RuntimeException
{
    public function __construct(
        public readonly string $field,
        string $message,
    ) {
        parent::__construct("{$field}: {$message}");
    }
}

function require_fields(array $payload, string ...$fields): array
{
    foreach ($fields as $field) {
        if (($payload[$field] ?? '') === '') {
            throw new ValidationException($field, 'is required');
        }
    }
    return $payload;
}
''', r'''php > require_fields(["name" => "ada"], "name", "email");
ValidationException: email: is required'''),
    ("medium", "errors", r'''
<?php

function retry(callable $work, int $attempts = 3): mixed
{
    $last = null;
    for ($i = 0; $i < $attempts; $i++) {
        try {
            return $work();
        } catch (Throwable $e) {
            $last = $e;
            usleep(200_000 * (2 ** $i));
        }
    }
    throw new RuntimeException("failed after {$attempts} attempts", 0, $last);
}
''', r'''php > retry($flaky);
RuntimeException: failed after 3 attempts'''),
    ("medium", "data", r'''
<?php

function insertRaces(PDO $db, array $races): int
{
    $db->beginTransaction();
    try {
        $stmt = $db->prepare('INSERT INTO races (wpm, language) VALUES (:wpm, :language)');
        foreach ($races as $race) {
            $stmt->execute(['wpm' => $race['wpm'], 'language' => $race['language']]);
        }
        $db->commit();
        return count($races);
    } catch (Throwable $e) {
        $db->rollBack();
        throw $e;
    }
}
''', r'''php > echo insertRaces($db, $races);
500'''),
    ("medium", "data", r'''
<?php

function topByLanguage(PDO $db, int $limit = 5): array
{
    $sql = 'SELECT language, MAX(wpm) AS best FROM races '
        . 'GROUP BY language ORDER BY best DESC LIMIT :limit';
    $stmt = $db->prepare($sql);
    $stmt->bindValue('limit', $limit, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}
''', r'''php > print_r(topByLanguage($db, 2));
Array([0] => Array([language] => python [best] => 118))'''),
    ("medium", "web", r'''
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
''', r'''php > dispatch($routes, "GET", "/races/7");
Response(200)'''),
    ("medium", "web", r'''
<?php

function readJsonBody(): array
{
    $raw = file_get_contents('php://input');
    if ($raw === false || $raw === '') {
        return [];
    }
    try {
        return json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        return [];
    }
}
''', r'''php > print_r(readJsonBody());
Array([wpm] => 98)'''),
    ("medium", "functional", r'''
<?php

function pipe(callable ...$stages): callable
{
    return static function (mixed $value) use ($stages): mixed {
        foreach ($stages as $stage) {
            $value = $stage($value);
        }
        return $value;
    };
}
''', r'''php > echo pipe('trim', 'strtoupper')("  hi  ");
HI'''),
    ("medium", "functional", r'''
<?php

function groupBy(array $items, callable $key): array
{
    $out = [];
    foreach ($items as $item) {
        $out[$key($item)][] = $item;
    }
    return $out;
}
''', r'''php > print_r(groupBy([1, 2, 3, 4], fn ($n) => $n % 2 ? 'odd' : 'even'));
Array([odd] => Array([0] => 1 [1] => 3) [even] => ...)'''),
    ("medium", "strings", r'''
<?php

function template(string $text, array $values): string
{
    return preg_replace_callback(
        '/\{(\w+)\}/',
        static fn (array $m): string => (string) ($values[$m[1]] ?? $m[0]),
        $text
    );
}
''', r'''php > echo template("hi {name}", ["name" => "ada"]);
hi ada'''),
    ("medium", "math", r'''
<?php

function percentile(array $values, float $p): float
{
    sort($values);
    $index = (count($values) - 1) * $p / 100;
    $low = (int) floor($index);
    $high = (int) ceil($index);
    if ($low === $high) {
        return (float) $values[$low];
    }
    return $values[$low] + ($values[$high] - $values[$low]) * ($index - $low);
}
''', r'''php > echo percentile([10, 20, 30, 40], 50);
25'''),
    ("medium", "data-structures", r'''
<?php

function flatten(array $nested): array
{
    $out = [];
    array_walk_recursive($nested, static function (mixed $item) use (&$out): void {
        $out[] = $item;
    });
    return $out;
}
''', r'''php > print_r(flatten([1, [2, [3, 4]]]));
Array([0] => 1 [1] => 2 [2] => 3 [3] => 4)'''),
    ("medium", "async", r'''
<?php

function parallelCurl(array $urls): array
{
    $multi = curl_multi_init();
    $handles = [];
    foreach ($urls as $key => $url) {
        $handle = curl_init($url);
        curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
        curl_multi_add_handle($multi, $handle);
        $handles[$key] = $handle;
    }

    do {
        curl_multi_exec($multi, $running);
        curl_multi_select($multi);
    } while ($running > 0);

    $out = [];
    foreach ($handles as $key => $handle) {
        $out[$key] = curl_multi_getcontent($handle);
        curl_multi_remove_handle($multi, $handle);
    }
    curl_multi_close($multi);
    return $out;
}
''', r'''php > print_r(parallelCurl($urls));
// every body fetched concurrently'''),

    # --------------------------------------------------------------------- hard
    ("hard", "data-structures", r'''
<?php

final class LruCache
{
    private array $items = [];

    public function __construct(private readonly int $capacity = 128)
    {
    }

    public function get(string $key): mixed
    {
        if (!array_key_exists($key, $this->items)) {
            return null;
        }
        $value = $this->items[$key];
        unset($this->items[$key]);
        $this->items[$key] = $value;
        return $value;
    }

    public function put(string $key, mixed $value): void
    {
        unset($this->items[$key]);
        $this->items[$key] = $value;
        if (count($this->items) > $this->capacity) {
            array_shift($this->items);
        }
    }
}
''', r'''php > $c = new LruCache(2); // put a, b, c => a evicted'''),
    ("hard", "data-structures", r'''
<?php

final class Trie
{
    /** @var array<string, Trie> */
    private array $children = [];
    private bool $word = false;

    public function insert(string $text): void
    {
        $node = $this;
        foreach (str_split($text) as $char) {
            $node->children[$char] ??= new self();
            $node = $node->children[$char];
        }
        $node->word = true;
    }

    public function contains(string $text): bool
    {
        $node = $this;
        foreach (str_split($text) as $char) {
            if (!isset($node->children[$char])) {
                return false;
            }
            $node = $node->children[$char];
        }
        return $node->word;
    }
}
''', r'''php > $t->insert("code"); var_dump($t->contains("cod"));
bool(false)'''),
    ("hard", "data-structures", r'''
<?php

function buildTree(array $rows, ?int $parent = null): array
{
    $out = [];
    foreach ($rows as $row) {
        if (($row['parent_id'] ?? null) !== $parent) {
            continue;
        }
        $children = buildTree($rows, $row['id']);
        if ($children !== []) {
            $row['children'] = $children;
        }
        $out[] = $row;
    }
    return $out;
}
''', r'''php > print_r(buildTree($rows));
// nested children under each parent'''),
    ("hard", "algorithms", r'''
<?php

function levenshtein_distance(string $a, string $b): int
{
    $previous = range(0, strlen($b));
    for ($i = 1; $i <= strlen($a); $i++) {
        $current = [$i];
        for ($j = 1; $j <= strlen($b); $j++) {
            $cost = $a[$i - 1] === $b[$j - 1] ? 0 : 1;
            $current[$j] = min(
                $previous[$j] + 1,
                $current[$j - 1] + 1,
                $previous[$j - 1] + $cost
            );
        }
        $previous = $current;
    }
    return $previous[strlen($b)];
}
''', r'''php > echo levenshtein_distance("kitten", "sitting");
3'''),
    ("hard", "algorithms", r'''
<?php

function dijkstra(array $graph, string $start): array
{
    $distances = [$start => 0];
    $queue = new SplPriorityQueue();
    $queue->insert($start, 0);

    while (!$queue->isEmpty()) {
        $node = $queue->extract();
        foreach ($graph[$node] ?? [] as $next => $weight) {
            $candidate = $distances[$node] + $weight;
            if ($candidate < ($distances[$next] ?? PHP_INT_MAX)) {
                $distances[$next] = $candidate;
                $queue->insert($next, -$candidate);
            }
        }
    }
    return $distances;
}
''', r'''php > print_r(dijkstra($graph, "a"));
Array([a] => 0 [b] => 1 [c] => 3)'''),
    ("hard", "algorithms", r'''
<?php

function quicksort(array $items): array
{
    if (count($items) < 2) {
        return $items;
    }
    $pivot = array_shift($items);
    $left = array_filter($items, static fn ($n) => $n < $pivot);
    $right = array_filter($items, static fn ($n) => $n >= $pivot);
    return [...quicksort(array_values($left)), $pivot, ...quicksort(array_values($right))];
}
''', r'''php > print_r(quicksort([3, 6, 1, 2]));
Array([0] => 1 [1] => 2 [2] => 3 [3] => 6)'''),
    ("hard", "oop", r'''
<?php

final class Container
{
    /** @var array<string, callable> */
    private array $factories = [];
    private array $instances = [];

    public function bind(string $id, callable $factory): void
    {
        $this->factories[$id] = $factory;
    }

    public function get(string $id): mixed
    {
        if (array_key_exists($id, $this->instances)) {
            return $this->instances[$id];
        }
        if (!isset($this->factories[$id])) {
            throw new RuntimeException("nothing bound for {$id}");
        }
        return $this->instances[$id] = ($this->factories[$id])($this);
    }
}
''', r'''php > $c->bind(PDO::class, fn () => new PDO($dsn)); $c->get(PDO::class);'''),
    ("hard", "oop", r'''
<?php

final class EventBus
{
    /** @var array<string, list<callable>> */
    private array $listeners = [];

    public function on(string $event, callable $listener): Closure
    {
        $this->listeners[$event][] = $listener;
        $index = array_key_last($this->listeners[$event]);

        return function () use ($event, $index): void {
            unset($this->listeners[$event][$index]);
        };
    }

    public function emit(string $event, mixed $payload = null): void
    {
        foreach ($this->listeners[$event] ?? [] as $listener) {
            $listener($payload);
        }
    }
}
''', r'''php > $off = $bus->on("tick", fn ($n) => print($n)); $bus->emit("tick", 1);
1'''),
    ("hard", "oop", r'''
<?php

abstract class Model implements JsonSerializable
{
    protected array $attributes = [];

    public function __get(string $key): mixed
    {
        return $this->attributes[$key] ?? null;
    }

    public function __set(string $key, mixed $value): void
    {
        $this->attributes[$key] = $value;
    }

    public function __isset(string $key): bool
    {
        return isset($this->attributes[$key]);
    }

    public function jsonSerialize(): array
    {
        return $this->attributes;
    }
}
''', r'''php > $m->wpm = 98; echo json_encode($m);
{"wpm":98}'''),
    ("hard", "functional", r'''
<?php

function curry(callable $fn, int $arity): callable
{
    $collect = static function (array $args) use (&$collect, $fn, $arity): mixed {
        if (count($args) >= $arity) {
            return $fn(...$args);
        }
        return static fn (mixed ...$rest): mixed => $collect([...$args, ...$rest]);
    };
    return static fn (mixed ...$args): mixed => $collect($args);
}
''', r'''php > $add = curry(fn ($a, $b, $c) => $a + $b + $c, 3); echo $add(1)(2)(3);
6'''),
    ("hard", "functional", r'''
<?php

function lazyMap(iterable $source, callable $fn): Generator
{
    foreach ($source as $key => $value) {
        yield $key => $fn($value);
    }
}

function take(iterable $source, int $count): array
{
    $out = [];
    foreach ($source as $value) {
        if (count($out) >= $count) {
            break;
        }
        $out[] = $value;
    }
    return $out;
}
''', r'''php > print_r(take(lazyMap(range(1, 1000), fn ($n) => $n * $n), 3));
Array([0] => 1 [1] => 4 [2] => 9)'''),
    ("hard", "functional", r'''
<?php

function memoize(callable $fn): callable
{
    $cache = [];
    return static function (mixed ...$args) use ($fn, &$cache): mixed {
        $key = serialize($args);
        if (!array_key_exists($key, $cache)) {
            $cache[$key] = $fn(...$args);
        }
        return $cache[$key];
    };
}
''', r'''php > $square = memoize(fn ($n) => $n * $n); echo $square(9);
81'''),
    ("hard", "errors", r'''
<?php

set_error_handler(static function (int $severity, string $message, string $file, int $line): bool {
    if (!(error_reporting() & $severity)) {
        return false;
    }
    throw new ErrorException($message, 0, $severity, $file, $line);
});

set_exception_handler(static function (Throwable $e): void {
    error_log(sprintf('[%s] %s', $e::class, $e->getMessage()));
    http_response_code(500);
});
''', r'''a notice now becomes an ErrorException you can catch'''),
    ("hard", "data", r'''
<?php

function streamCsv(string $path, callable $onRow): int
{
    $handle = fopen($path, 'rb');
    if ($handle === false) {
        throw new RuntimeException("cannot open {$path}");
    }
    try {
        $header = fgetcsv($handle);
        $count = 0;
        while (($row = fgetcsv($handle)) !== false) {
            $onRow(array_combine($header, $row));
            $count++;
        }
        return $count;
    } finally {
        fclose($handle);
    }
}
''', r'''php > echo streamCsv("races.csv", $save);
50000'''),
    ("hard", "web", r'''
<?php

function middleware(array $stack, callable $handler): callable
{
    return array_reduce(
        array_reverse($stack),
        static fn (callable $next, callable $layer): callable =>
            static fn (Request $request): Response => $layer($request, $next),
        $handler
    );
}
''', r'''php > $app = middleware([$cors, $auth], $controller);'''),
    ("hard", "web", r'''
<?php

function rateLimit(string $key, int $max, int $seconds): bool
{
    $file = sys_get_temp_dir() . '/rl_' . md5($key);
    $hits = [];
    if (is_file($file)) {
        $hits = json_decode((string) file_get_contents($file), true) ?: [];
    }
    $now = time();
    $hits = array_values(array_filter($hits, static fn (int $t): bool => $t > $now - $seconds));
    if (count($hits) >= $max) {
        return false;
    }
    $hits[] = $now;
    file_put_contents($file, json_encode($hits), LOCK_EX);
    return true;
}
''', r'''php > var_dump(rateLimit("ip:1.2.3.4", 100, 60));
bool(true)'''),
    ("hard", "strings", r'''
<?php

function topWords(string $text, int $limit): array
{
    preg_match_all('/[a-z0-9\']+/', strtolower($text), $matches);
    $counts = array_count_values($matches[0]);
    arsort($counts);
    return array_slice($counts, 0, $limit, true);
}
''', r'''php > print_r(topWords("the cat the hat the end", 2));
Array([the] => 3 [cat] => 1)'''),
    ("hard", "math", r'''
<?php

function matrixMultiply(array $a, array $b): array
{
    $rows = count($a);
    $inner = count($b);
    $cols = count($b[0]);
    $out = array_fill(0, $rows, array_fill(0, $cols, 0));

    for ($i = 0; $i < $rows; $i++) {
        for ($k = 0; $k < $inner; $k++) {
            $value = $a[$i][$k];
            if ($value === 0) {
                continue;
            }
            for ($j = 0; $j < $cols; $j++) {
                $out[$i][$j] += $value * $b[$k][$j];
            }
        }
    }
    return $out;
}
''', r'''php > print_r(matrixMultiply([[1, 2]], [[3], [4]]));
Array([0] => Array([0] => 11))'''),
    ("hard", "async", r'''
<?php

function withLock(string $name, callable $work): mixed
{
    $file = sys_get_temp_dir() . '/lock_' . md5($name);
    $handle = fopen($file, 'c');
    if ($handle === false) {
        throw new RuntimeException("cannot open lock {$name}");
    }
    try {
        if (!flock($handle, LOCK_EX)) {
            throw new RuntimeException("cannot lock {$name}");
        }
        return $work();
    } finally {
        flock($handle, LOCK_UN);
        fclose($handle);
    }
}
''', r'''php > withLock("cron:nightly", $job);
// only one process runs the job'''),
    ("hard", "data-structures", r'''
<?php

final class RingBuffer implements IteratorAggregate
{
    private array $items;
    private int $head = 0;
    private int $size = 0;

    public function __construct(private readonly int $capacity)
    {
        $this->items = array_fill(0, $capacity, null);
    }

    public function add(mixed $item): void
    {
        $this->items[($this->head + $this->size) % $this->capacity] = $item;
        if ($this->size === $this->capacity) {
            $this->head = ($this->head + 1) % $this->capacity;
        } else {
            $this->size++;
        }
    }

    public function getIterator(): Generator
    {
        for ($i = 0; $i < $this->size; $i++) {
            yield $this->items[($this->head + $i) % $this->capacity];
        }
    }
}
''', r'''php > $r = new RingBuffer(3); // add 1..4 => oldest dropped'''),
]
