"""Go snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Indentation is tabs, as
gofmt writes it.
"""
LANGUAGE = "go"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
func Add(a int, b int) int {
	return a + b
}
''', r'''Add(2, 3) = 5'''),
    ("very-easy", "math", r'''
func IsEven(n int) bool {
	return n%2 == 0
}
''', r'''IsEven(10) = true'''),
    ("very-easy", "strings", r'''
func Shout(text string) string {
	return strings.ToUpper(text) + "!"
}
''', r'''Shout("hello") = HELLO!'''),
    ("very-easy", "strings", r'''
func Reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}
''', r'''Reverse("golang") = gnalog'''),
    ("very-easy", "math", r'''
func Clamp(n, low, high int) int {
	if n < low {
		return low
	}
	if n > high {
		return high
	}
	return n
}
''', r'''Clamp(42, 0, 10) = 10'''),
    ("very-easy", "algorithms", r'''
func Sum(nums []int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}
''', r'''Sum([]int{1, 2, 3, 4}) = 10'''),
    ("very-easy", "algorithms", r'''
func Largest(nums []int) int {
	best := nums[0]
	for _, n := range nums {
		if n > best {
			best = n
		}
	}
	return best
}
''', r'''Largest([]int{3, 9, 4}) = 9'''),
    ("very-easy", "algorithms", r'''
func CountUp(n int) {
	for i := 1; i <= n; i++ {
		fmt.Println(i)
	}
}
''', r'''CountUp(3)
1
2
3'''),
    ("very-easy", "strings", r'''
func Greet(name string) string {
	return fmt.Sprintf("hello %s", name)
}
''', r'''Greet("world") = hello world'''),
    ("very-easy", "strings", r'''
func IsBlank(text string) bool {
	return strings.TrimSpace(text) == ""
}
''', r'''IsBlank("   ") = true'''),
    ("very-easy", "data-structures", r'''
func Names() []string {
	return []string{"ada", "grace", "linus"}
}
''', r'''Names() = [ada grace linus]'''),
    ("very-easy", "data-structures", r'''
func Scores() map[string]int {
	return map[string]int{
		"ada":   98,
		"grace": 104,
	}
}
''', r'''Scores() = map[ada:98 grace:104]'''),
    ("very-easy", "oop", r'''
type Dog struct {
	Name string
}

func (d Dog) Speak() string {
	return d.Name + " says woof"
}
''', r'''Dog{Name: "Rex"}.Speak() = Rex says woof'''),
    ("very-easy", "oop", r'''
type Point struct {
	X, Y int
}

func (p Point) String() string {
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}
''', r'''Point{3, 4} = (3, 4)'''),
    ("very-easy", "errors", r'''
func SafeAtoi(text string, fallback int) int {
	value, err := strconv.Atoi(text)
	if err != nil {
		return fallback
	}
	return value
}
''', r'''SafeAtoi("oops", 0) = 0'''),
    ("very-easy", "math", r'''
func Average(nums []int) float64 {
	if len(nums) == 0 {
		return 0
	}
	return float64(Sum(nums)) / float64(len(nums))
}
''', r'''Average([]int{2, 4, 6}) = 4'''),
    ("very-easy", "functional", r'''
func Doubled(nums []int) []int {
	out := make([]int, 0, len(nums))
	for _, n := range nums {
		out = append(out, n*2)
	}
	return out
}
''', r'''Doubled([]int{1, 2, 3}) = [2 4 6]'''),
    ("very-easy", "functional", r'''
func Evens(nums []int) []int {
	var out []int
	for _, n := range nums {
		if n%2 == 0 {
			out = append(out, n)
		}
	}
	return out
}
''', r'''Evens([]int{1, 2, 3, 4}) = [2 4]'''),
    ("very-easy", "data-structures", r'''
func FirstOr(nums []int, fallback int) int {
	if len(nums) == 0 {
		return fallback
	}
	return nums[0]
}
''', r'''FirstOr(nil, -1) = -1'''),
    ("very-easy", "async", r'''
func Later(d time.Duration, fn func()) {
	go func() {
		time.Sleep(d)
		fn()
	}()
}
''', r'''Later(200*time.Millisecond, ping)
ping'''),

    ("very-easy", "math", r'''
func Square(n int) int {
	return n * n
}
''', r'''Square(7) = 49'''),
    ("very-easy", "strings", r'''
func Initials(first, last string) string {
	return first[:1] + last[:1]
}
''', r'''Initials("Ada", "Lovelace") = AL'''),
    ("very-easy", "data-structures", r'''
func Last(nums []int) (int, bool) {
	if len(nums) == 0 {
		return 0, false
	}
	return nums[len(nums)-1], true
}
''', r'''Last([]int{1, 2, 3}) = 3 true'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
func FizzBuzz(n int) {
	for i := 1; i <= n; i++ {
		switch {
		case i%15 == 0:
			fmt.Println("FizzBuzz")
		case i%3 == 0:
			fmt.Println("Fizz")
		case i%5 == 0:
			fmt.Println("Buzz")
		default:
			fmt.Println(i)
		}
	}
}
''', r'''FizzBuzz(5)
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
func Fib(n int) int {
	a, b := 0, 1
	for i := 0; i < n; i++ {
		a, b = b, a+b
	}
	return a
}
''', r'''Fib(10) = 55'''),
    ("easy", "algorithms", r'''
func Factorial(n int) int {
	if n <= 1 {
		return 1
	}
	return n * Factorial(n-1)
}
''', r'''Factorial(6) = 720'''),
    ("easy", "strings", r'''
func IsPalindrome(text string) bool {
	var clean []rune
	for _, r := range strings.ToLower(text) {
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			clean = append(clean, r)
		}
	}
	for i, j := 0, len(clean)-1; i < j; i, j = i+1, j-1 {
		if clean[i] != clean[j] {
			return false
		}
	}
	return true
}
''', r'''IsPalindrome("A man, a plan, a canal: Panama") = true'''),
    ("easy", "strings", r'''
func TitleCase(text string) string {
	words := strings.Fields(text)
	for i, word := range words {
		words[i] = strings.ToUpper(word[:1]) + strings.ToLower(word[1:])
	}
	return strings.Join(words, " ")
}
''', r'''TitleCase("hello wide world") = Hello Wide World'''),
    ("easy", "strings", r'''
func WordCount(text string) map[string]int {
	counts := make(map[string]int)
	for _, word := range strings.Fields(strings.ToLower(text)) {
		counts[word]++
	}
	return counts
}
''', r'''WordCount("the cat the hat") = map[cat:1 hat:1 the:2]'''),
    ("easy", "data-structures", r'''
func Unique(items []string) []string {
	seen := make(map[string]struct{}, len(items))
	var out []string
	for _, item := range items {
		if _, ok := seen[item]; ok {
			continue
		}
		seen[item] = struct{}{}
		out = append(out, item)
	}
	return out
}
''', r'''Unique([a b a c]) = [a b c]'''),
    ("easy", "data-structures", r'''
func Chunk(items []int, size int) [][]int {
	var out [][]int
	for i := 0; i < len(items); i += size {
		end := i + size
		if end > len(items) {
			end = len(items)
		}
		out = append(out, items[i:end])
	}
	return out
}
''', r'''Chunk([]int{1, 2, 3, 4, 5}, 2) = [[1 2] [3 4] [5]]'''),
    ("easy", "data-structures", r'''
func Keys(m map[string]int) []string {
	out := make([]string, 0, len(m))
	for key := range m {
		out = append(out, key)
	}
	sort.Strings(out)
	return out
}
''', r'''Keys(map[b:2 a:1]) = [a b]'''),
    ("easy", "math", r'''
func IsPrime(n int) bool {
	if n < 2 {
		return false
	}
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return false
		}
	}
	return true
}
''', r'''IsPrime(97) = true'''),
    ("easy", "math", r'''
func Gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	if a < 0 {
		return -a
	}
	return a
}
''', r'''Gcd(48, 18) = 6'''),
    ("easy", "errors", r'''
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
''', r'''LoadConfig("missing.json")
read missing.json: no such file or directory'''),
    ("easy", "errors", r'''
var ErrNotFound = errors.New("not found")

func Find(rows map[string]string, key string) (string, error) {
	value, ok := rows[key]
	if !ok {
		return "", fmt.Errorf("key %q: %w", key, ErrNotFound)
	}
	return value, nil
}
''', r'''Find(nil, "a") => key "a": not found'''),
    ("easy", "oop", r'''
type Counter struct {
	count int
}

func (c *Counter) Bump(by int) int {
	c.count += by
	return c.count
}

func (c *Counter) Value() int {
	return c.count
}
''', r'''(&Counter{}).Bump(3) = 3'''),
    ("easy", "oop", r'''
type Shape interface {
	Area() float64
}

type Rect struct {
	W, H float64
}

func (r Rect) Area() float64 {
	return r.W * r.H
}
''', r'''Rect{3, 4}.Area() = 12'''),
    ("easy", "web", r'''
func handler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		http.Error(w, "missing id", http.StatusBadRequest)
		return
	}
	fmt.Fprintf(w, "looking up %s", id)
}
''', r'''GET /?id=7 => looking up 7'''),
    ("easy", "web", r'''
func BuildURL(base string, params map[string]string) string {
	values := url.Values{}
	for key, value := range params {
		values.Set(key, value)
	}
	return base + "?" + values.Encode()
}
''', r'''BuildURL("/search", map[q:code]) = /search?q=code'''),
    ("easy", "async", r'''
func FanOut(inputs []int, work func(int) int) []int {
	out := make([]int, len(inputs))
	var wg sync.WaitGroup
	for i, value := range inputs {
		wg.Add(1)
		go func(i, value int) {
			defer wg.Done()
			out[i] = work(value)
		}(i, value)
	}
	wg.Wait()
	return out
}
''', r'''FanOut([1 2 3], square) = [1 4 9]'''),
    ("easy", "data", r'''
func WriteCSV(path string, rows [][]string) error {
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()
	return writer.WriteAll(rows)
}
''', r'''WriteCSV("out.csv", rows) => out.csv written'''),
    ("easy", "functional", r'''
func Map[T, R any](items []T, fn func(T) R) []R {
	out := make([]R, 0, len(items))
	for _, item := range items {
		out = append(out, fn(item))
	}
	return out
}
''', r'''Map([]int{1, 2}, double) = [2 4]'''),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
func BinarySearch(items []int, target int) int {
	low, high := 0, len(items)-1
	for low <= high {
		mid := (low + high) / 2
		switch {
		case items[mid] == target:
			return mid
		case items[mid] < target:
			low = mid + 1
		default:
			high = mid - 1
		}
	}
	return -1
}
''', r'''BinarySearch([]int{1, 3, 5, 7, 9}, 7) = 3'''),
    ("medium", "algorithms", r'''
func TwoSum(nums []int, target int) (int, int, bool) {
	seen := make(map[int]int, len(nums))
	for i, n := range nums {
		if j, ok := seen[target-n]; ok {
			return j, i, true
		}
		seen[n] = i
	}
	return 0, 0, false
}
''', r'''TwoSum([]int{2, 7, 11, 15}, 9) = 0 1 true'''),
    ("medium", "algorithms", r'''
func MaxSubarray(nums []int) int {
	best, current := nums[0], nums[0]
	for _, n := range nums[1:] {
		current = max(n, current+n)
		best = max(best, current)
	}
	return best
}
''', r'''MaxSubarray([]int{-2, 1, -3, 4, -1, 2, 1}) = 6'''),
    ("medium", "algorithms", r'''
func MergeSorted(left, right []int) []int {
	out := make([]int, 0, len(left)+len(right))
	i, j := 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			out = append(out, left[i])
			i++
		} else {
			out = append(out, right[j])
			j++
		}
	}
	out = append(out, left[i:]...)
	return append(out, right[j:]...)
}
''', r'''MergeSorted([1 4], [2 3 5]) = [1 2 3 4 5]'''),
    ("medium", "data-structures", r'''
type Store struct {
	mu    sync.RWMutex
	items map[string][]byte
}

func (s *Store) Get(key string) ([]byte, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	value, ok := s.items[key]
	return value, ok
}

func (s *Store) Put(key string, value []byte) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.items == nil {
		s.items = make(map[string][]byte)
	}
	s.items[key] = value
}
''', r'''Put("a", data); Get("a") => data, true'''),
    ("medium", "data-structures", r'''
type Stack[T any] struct {
	items []T
}

func (s *Stack[T]) Push(item T) {
	s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
	var zero T
	if len(s.items) == 0 {
		return zero, false
	}
	item := s.items[len(s.items)-1]
	s.items = s.items[:len(s.items)-1]
	return item, true
}
''', r'''Push(1); Push(2); Pop() = 2 true'''),
    ("medium", "data-structures", r'''
type Node struct {
	Value int
	Next  *Node
}

func (n *Node) Slice() []int {
	var out []int
	for cursor := n; cursor != nil; cursor = cursor.Next {
		out = append(out, cursor.Value)
	}
	return out
}
''', r'''1 -> 2 -> 3 => [1 2 3]'''),
    ("medium", "async", r'''
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
''', r'''Workers(jobs, 4) => every job handled by one of four workers'''),
    ("medium", "async", r'''
func WithTimeout(parent context.Context, d time.Duration, work func(context.Context) error) error {
	ctx, cancel := context.WithTimeout(parent, d)
	defer cancel()

	done := make(chan error, 1)
	go func() {
		done <- work(ctx)
	}()

	select {
	case err := <-done:
		return err
	case <-ctx.Done():
		return ctx.Err()
	}
}
''', r'''WithTimeout(ctx, 100*time.Millisecond, slow)
context deadline exceeded'''),
    ("medium", "async", r'''
func Debounce(d time.Duration, fn func()) func() {
	var timer *time.Timer
	var mu sync.Mutex
	return func() {
		mu.Lock()
		defer mu.Unlock()
		if timer != nil {
			timer.Stop()
		}
		timer = time.AfterFunc(d, fn)
	}
}
''', r'''call(); call(); call()
// fn runs once, after the last call'''),
    ("medium", "oop", r'''
type Logger interface {
	Printf(format string, args ...any)
}

type Service struct {
	log   Logger
	store *Store
}

func NewService(log Logger, store *Store) *Service {
	return &Service{log: log, store: store}
}

func (s *Service) Save(key string, value []byte) {
	s.store.Put(key, value)
	s.log.Printf("saved %s (%d bytes)", key, len(value))
}
''', r'''Save("a", data)
saved a (4 bytes)'''),
    ("medium", "errors", r'''
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
	return e.Field + ": " + e.Message
}

func Require(payload map[string]string, fields ...string) error {
	for _, field := range fields {
		if payload[field] == "" {
			return &ValidationError{Field: field, Message: "is required"}
		}
	}
	return nil
}
''', r'''Require(map[name:ada], "name", "email")
email: is required'''),
    ("medium", "data", r'''
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
''', r'''ListActive(ctx) => [{1 ada} {2 grace}]'''),
    ("medium", "web", r'''
func JSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("content-type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(payload); err != nil {
		log.Printf("encode: %v", err)
	}
}
''', r'''JSON(w, 200, map[string]int{"wpm": 98})
{"wpm":98}'''),
    ("medium", "web", r'''
func Logging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("%s %s took %s", r.Method, r.URL.Path, time.Since(start))
	})
}
''', r'''GET /api/me
GET /api/me took 1.2ms'''),
    ("medium", "functional", r'''
func Filter[T any](items []T, keep func(T) bool) []T {
	var out []T
	for _, item := range items {
		if keep(item) {
			out = append(out, item)
		}
	}
	return out
}

func Reduce[T, A any](items []T, initial A, fn func(A, T) A) A {
	acc := initial
	for _, item := range items {
		acc = fn(acc, item)
	}
	return acc
}
''', r'''Reduce([]int{1, 2, 3}, 0, add) = 6'''),
    ("medium", "functional", r'''
func GroupBy[T any, K comparable](items []T, key func(T) K) map[K][]T {
	out := make(map[K][]T)
	for _, item := range items {
		k := key(item)
		out[k] = append(out[k], item)
	}
	return out
}
''', r'''GroupBy([]int{1, 2, 3, 4}, parity) = map[even:[2 4] odd:[1 3]]'''),
    ("medium", "strings", r'''
func Slugify(text string) string {
	var b strings.Builder
	lastDash := true
	for _, r := range strings.ToLower(text) {
		switch {
		case unicode.IsLetter(r) || unicode.IsDigit(r):
			b.WriteRune(r)
			lastDash = false
		case !lastDash:
			b.WriteRune('-')
			lastDash = true
		}
	}
	return strings.Trim(b.String(), "-")
}
''', r'''Slugify("  Hello, World!  ") = hello-world'''),
    ("medium", "math", r'''
func Percentile(values []float64, p float64) float64 {
	sorted := append([]float64(nil), values...)
	sort.Float64s(sorted)
	index := float64(len(sorted)-1) * p / 100
	low := int(math.Floor(index))
	high := int(math.Ceil(index))
	if low == high {
		return sorted[low]
	}
	return sorted[low] + (sorted[high]-sorted[low])*(index-float64(low))
}
''', r'''Percentile([10 20 30 40], 50) = 25'''),
    ("medium", "oop", r'''
type Option func(*Server)

func WithPort(port int) Option {
	return func(s *Server) { s.port = port }
}

func WithTimeout(d time.Duration) Option {
	return func(s *Server) { s.timeout = d }
}

func NewServer(opts ...Option) *Server {
	s := &Server{port: 8000, timeout: 30 * time.Second}
	for _, opt := range opts {
		opt(s)
	}
	return s
}
''', r'''NewServer(WithPort(25616)) => &Server{port: 25616}'''),

    # --------------------------------------------------------------------- hard
    ("hard", "async", r'''
func Pipeline(ctx context.Context, in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for value := range in {
			select {
			case out <- value * value:
			case <-ctx.Done():
				return
			}
		}
	}()
	return out
}
''', r'''1 2 3 => 1 4 9  (cancels with the context)'''),
    ("hard", "async", r'''
func Race(ctx context.Context, urls []string) (string, error) {
	type result struct {
		body string
		err  error
	}
	results := make(chan result, len(urls))
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	for _, url := range urls {
		go func(url string) {
			body, err := Get(ctx, url)
			results <- result{body: body, err: err}
		}(url)
	}

	var last error
	for range urls {
		r := <-results
		if r.err == nil {
			return r.body, nil
		}
		last = r.err
	}
	return "", last
}
''', r'''Race(ctx, mirrors) => body from whichever mirror answered first'''),
    ("hard", "async", r'''
type Limiter struct {
	tokens chan struct{}
}

func NewLimiter(n int) *Limiter {
	l := &Limiter{tokens: make(chan struct{}, n)}
	for i := 0; i < n; i++ {
		l.tokens <- struct{}{}
	}
	return l
}

func (l *Limiter) Do(ctx context.Context, work func()) error {
	select {
	case <-l.tokens:
		defer func() { l.tokens <- struct{}{} }()
		work()
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}
''', r'''NewLimiter(4) => at most four concurrent calls'''),
    ("hard", "async", r'''
func Broadcast[T any](in <-chan T, n int) []<-chan T {
	outs := make([]chan T, n)
	readers := make([]<-chan T, n)
	for i := range outs {
		outs[i] = make(chan T)
		readers[i] = outs[i]
	}
	go func() {
		defer func() {
			for _, out := range outs {
				close(out)
			}
		}()
		for value := range in {
			for _, out := range outs {
				out <- value
			}
		}
	}()
	return readers
}
''', r'''Broadcast(events, 3) => every listener sees every event'''),
    ("hard", "data-structures", r'''
type LRU[K comparable, V any] struct {
	capacity int
	order    *list.List
	index    map[K]*list.Element
}

type entry[K comparable, V any] struct {
	key   K
	value V
}

func (c *LRU[K, V]) Get(key K) (V, bool) {
	var zero V
	element, ok := c.index[key]
	if !ok {
		return zero, false
	}
	c.order.MoveToFront(element)
	return element.Value.(*entry[K, V]).value, true
}
''', r'''Get("a") on a hit moves "a" to the front'''),
    ("hard", "data-structures", r'''
type Trie struct {
	children map[rune]*Trie
	word     bool
}

func NewTrie() *Trie {
	return &Trie{children: map[rune]*Trie{}}
}

func (t *Trie) Insert(text string) {
	node := t
	for _, r := range text {
		child, ok := node.children[r]
		if !ok {
			child = NewTrie()
			node.children[r] = child
		}
		node = child
	}
	node.word = true
}

func (t *Trie) Contains(text string) bool {
	node := t
	for _, r := range text {
		child, ok := node.children[r]
		if !ok {
			return false
		}
		node = child
	}
	return node.word
}
''', r'''Insert("code"); Contains("code") = true; Contains("cod") = false'''),
    ("hard", "algorithms", r'''
func Dijkstra(graph map[string]map[string]int, start string) map[string]int {
	distances := map[string]int{start: 0}
	visited := map[string]bool{}
	for len(visited) < len(graph) {
		node, best := "", math.MaxInt
		for candidate, cost := range distances {
			if !visited[candidate] && cost < best {
				node, best = candidate, cost
			}
		}
		if node == "" {
			break
		}
		visited[node] = true
		for next, weight := range graph[node] {
			if candidate := best + weight; candidate < valueOr(distances, next, math.MaxInt) {
				distances[next] = candidate
			}
		}
	}
	return distances
}
''', r'''Dijkstra({a:{b:1}, b:{c:2}}, "a") = map[a:0 b:1 c:3]'''),
    ("hard", "algorithms", r'''
func Levenshtein(a, b string) int {
	previous := make([]int, len(b)+1)
	for j := range previous {
		previous[j] = j
	}
	for i := 1; i <= len(a); i++ {
		current := make([]int, len(b)+1)
		current[0] = i
		for j := 1; j <= len(b); j++ {
			cost := 1
			if a[i-1] == b[j-1] {
				cost = 0
			}
			current[j] = min(previous[j]+1, min(current[j-1]+1, previous[j-1]+cost))
		}
		previous = current
	}
	return previous[len(b)]
}
''', r'''Levenshtein("kitten", "sitting") = 3'''),
    ("hard", "algorithms", r'''
func Quicksort(a []int) {
	if len(a) < 2 {
		return
	}
	pivot := a[len(a)/2]
	left, right := 0, len(a)-1
	for left <= right {
		for a[left] < pivot {
			left++
		}
		for a[right] > pivot {
			right--
		}
		if left <= right {
			a[left], a[right] = a[right], a[left]
			left++
			right--
		}
	}
	Quicksort(a[:right+1])
	Quicksort(a[left:])
}
''', r'''[3 6 1 8 2] => [1 2 3 6 8]'''),
    ("hard", "oop", r'''
type Middleware func(http.Handler) http.Handler

func Chain(handler http.Handler, middleware ...Middleware) http.Handler {
	for i := len(middleware) - 1; i >= 0; i-- {
		handler = middleware[i](handler)
	}
	return handler
}

func Recoverer(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("panic: %v", err)
				http.Error(w, "internal error", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}
''', r'''Chain(mux, Recoverer, Logging) => panics become 500s, not crashes'''),
    ("hard", "errors", r'''
type MultiError struct {
	errs []error
}

func (m *MultiError) Add(err error) {
	if err != nil {
		m.errs = append(m.errs, err)
	}
}

func (m *MultiError) Err() error {
	if len(m.errs) == 0 {
		return nil
	}
	return m
}

func (m *MultiError) Error() string {
	parts := make([]string, 0, len(m.errs))
	for _, err := range m.errs {
		parts = append(parts, err.Error())
	}
	return fmt.Sprintf("%d errors: %s", len(m.errs), strings.Join(parts, "; "))
}
''', r'''2 errors: read failed; parse failed'''),
    ("hard", "errors", r'''
func Retry(ctx context.Context, attempts int, work func() error) error {
	var last error
	for i := 0; i < attempts; i++ {
		if err := work(); err == nil {
			return nil
		} else {
			last = err
		}
		select {
		case <-time.After(time.Duration(1<<i) * 100 * time.Millisecond):
		case <-ctx.Done():
			return errors.Join(last, ctx.Err())
		}
	}
	return fmt.Errorf("after %d attempts: %w", attempts, last)
}
''', r'''Retry(ctx, 3, flaky)
after 3 attempts: connection refused'''),
    ("hard", "functional", r'''
func Memoize[K comparable, V any](fn func(K) V) func(K) V {
	var mu sync.Mutex
	cache := map[K]V{}
	return func(key K) V {
		mu.Lock()
		defer mu.Unlock()
		if value, ok := cache[key]; ok {
			return value
		}
		value := fn(key)
		cache[key] = value
		return value
	}
}
''', r'''square := Memoize(slowSquare); square(9); square(9) = 81'''),
    ("hard", "functional", r'''
func SortBy[T any](items []T, less func(a, b T) bool) {
	sort.Slice(items, func(i, j int) bool {
		return less(items[i], items[j])
	})
}

func MaxBy[T any, N int | float64](items []T, score func(T) N) (T, bool) {
	var best T
	if len(items) == 0 {
		return best, false
	}
	best = items[0]
	for _, item := range items[1:] {
		if score(item) > score(best) {
			best = item
		}
	}
	return best, true
}
''', r'''MaxBy(races, wpm) => the fastest race, true'''),
    ("hard", "data", r'''
func Transfer(ctx context.Context, db *sql.DB, from, to int64, amount int64) error {
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	if _, err := tx.ExecContext(ctx,
		`UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?`,
		amount, from, amount); err != nil {
		return fmt.Errorf("debit: %w", err)
	}
	if _, err := tx.ExecContext(ctx,
		`UPDATE accounts SET balance = balance + ? WHERE id = ?`,
		amount, to); err != nil {
		return fmt.Errorf("credit: %w", err)
	}
	return tx.Commit()
}
''', r'''Transfer(ctx, db, 1, 2, 500) => committed, or rolled back on error'''),
    ("hard", "web", r'''
func Serve(ctx context.Context, addr string, handler http.Handler) error {
	server := &http.Server{
		Addr:              addr,
		Handler:           handler,
		ReadHeaderTimeout: 10 * time.Second,
	}
	go func() {
		<-ctx.Done()
		shutdown, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()
		_ = server.Shutdown(shutdown)
	}()
	if err := server.ListenAndServe(); !errors.Is(err, http.ErrServerClosed) {
		return err
	}
	return nil
}
''', r'''Serve(ctx, ":25616", mux) => drains connections on cancel'''),
    ("hard", "strings", r'''
func TopWords(text string, limit int) []string {
	counts := map[string]int{}
	for _, word := range strings.FieldsFunc(strings.ToLower(text), func(r rune) bool {
		return !unicode.IsLetter(r) && !unicode.IsDigit(r)
	}) {
		counts[word]++
	}
	words := make([]string, 0, len(counts))
	for word := range counts {
		words = append(words, word)
	}
	sort.Slice(words, func(i, j int) bool {
		if counts[words[i]] != counts[words[j]] {
			return counts[words[i]] > counts[words[j]]
		}
		return words[i] < words[j]
	})
	if len(words) > limit {
		words = words[:limit]
	}
	return words
}
''', r'''TopWords("the cat the hat the end", 2) = [the cat]'''),
    ("hard", "math", r'''
func Multiply(a, b [][]float64) [][]float64 {
	rows, inner, cols := len(a), len(b), len(b[0])
	out := make([][]float64, rows)
	for i := range out {
		out[i] = make([]float64, cols)
	}
	for i := 0; i < rows; i++ {
		for k := 0; k < inner; k++ {
			value := a[i][k]
			if value == 0 {
				continue
			}
			for j := 0; j < cols; j++ {
				out[i][j] += value * b[k][j]
			}
		}
	}
	return out
}
''', r'''[[1 2]] x [[3] [4]] = [[11]]'''),
    ("hard", "oop", r'''
type Event struct {
	Name    string
	Payload any
}

type Bus struct {
	mu       sync.RWMutex
	handlers map[string][]func(Event)
}

func (b *Bus) On(name string, fn func(Event)) {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.handlers == nil {
		b.handlers = map[string][]func(Event){}
	}
	b.handlers[name] = append(b.handlers[name], fn)
}

func (b *Bus) Emit(event Event) {
	b.mu.RLock()
	defer b.mu.RUnlock()
	for _, fn := range b.handlers[event.Name] {
		fn(event)
	}
}
''', r'''On("tick", print); Emit(Event{Name: "tick"})
{tick <nil>}'''),
    ("hard", "data-structures", r'''
type RingBuffer[T any] struct {
	items []T
	head  int
	size  int
}

func NewRing[T any](capacity int) *RingBuffer[T] {
	return &RingBuffer[T]{items: make([]T, capacity)}
}

func (r *RingBuffer[T]) Add(item T) {
	r.items[(r.head+r.size)%len(r.items)] = item
	if r.size == len(r.items) {
		r.head = (r.head + 1) % len(r.items)
	} else {
		r.size++
	}
}
''', r'''NewRing[int](3); Add 1..4 => oldest value dropped'''),
]
