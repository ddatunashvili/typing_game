"""Ruby snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Two-space indentation, as
rubocop wants it.
"""
LANGUAGE = "ruby"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
def add(a, b)
  a + b
end
''', r'''irb> add(2, 3)
=> 5'''),
    ("very-easy", "math", r'''
def even?(n)
  n.even?
end
''', r'''irb> even?(10)
=> true'''),
    ("very-easy", "math", r'''
def square(n)
  n * n
end
''', r'''irb> square(7)
=> 49'''),
    ("very-easy", "math", r'''
def clamp(n, low, high)
  n.clamp(low, high)
end
''', r'''irb> clamp(42, 0, 10)
=> 10'''),
    ("very-easy", "strings", r'''
def shout(text)
  "#{text.upcase}!"
end
''', r'''irb> shout("hello")
=> "HELLO!"'''),
    ("very-easy", "strings", r'''
def reverse(text)
  text.reverse
end
''', r'''irb> reverse("ruby")
=> "ybur"'''),
    ("very-easy", "strings", r'''
def blank?(value)
  value.nil? || value.to_s.strip.empty?
end
''', r'''irb> blank?("   ")
=> true'''),
    ("very-easy", "strings", r'''
def initials(first, last)
  "#{first[0]}#{last[0]}"
end
''', r'''irb> initials("Ada", "Lovelace")
=> "AL"'''),
    ("very-easy", "algorithms", r'''
def total(numbers)
  numbers.sum
end
''', r'''irb> total([1, 2, 3, 4])
=> 10'''),
    ("very-easy", "algorithms", r'''
def count_up(n)
  (1..n).each { |i| puts i }
end
''', r'''irb> count_up(3)
1
2
3'''),
    ("very-easy", "algorithms", r'''
def largest(numbers)
  numbers.max
end
''', r'''irb> largest([3, 9, 4])
=> 9'''),
    ("very-easy", "functional", r'''
def doubled(numbers)
  numbers.map { |n| n * 2 }
end
''', r'''irb> doubled([1, 2, 3])
=> [2, 4, 6]'''),
    ("very-easy", "functional", r'''
def evens(numbers)
  numbers.select(&:even?)
end
''', r'''irb> evens([1, 2, 3, 4])
=> [2, 4]'''),
    ("very-easy", "data-structures", r'''
def names
  %w[ada grace linus]
end
''', r'''irb> names
=> ["ada", "grace", "linus"]'''),
    ("very-easy", "data-structures", r'''
def scores
  { ada: 98, grace: 104 }
end
''', r'''irb> scores
=> {:ada=>98, :grace=>104}'''),
    ("very-easy", "oop", r'''
class Dog
  def initialize(name)
    @name = name
  end

  def speak
    "#{@name} says woof"
  end
end
''', r'''irb> Dog.new("Rex").speak
=> "Rex says woof"'''),
    ("very-easy", "oop", r'''
Point = Struct.new(:x, :y) do
  def manhattan
    x.abs + y.abs
  end
end
''', r'''irb> Point.new(3, -4).manhattan
=> 7'''),
    ("very-easy", "errors", r'''
def safe_int(text, fallback = 0)
  Integer(text)
rescue ArgumentError, TypeError
  fallback
end
''', r'''irb> safe_int("oops")
=> 0'''),
    ("very-easy", "math", r'''
def average(numbers)
  return 0.0 if numbers.empty?

  numbers.sum.to_f / numbers.size
end
''', r'''irb> average([2, 4, 6])
=> 4.0'''),
    ("very-easy", "strings", r'''
def greet(name)
  "hello #{name}"
end
''', r'''irb> greet("world")
=> "hello world"'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
def fizzbuzz(n)
  (1..n).each do |i|
    if (i % 15).zero?
      puts "FizzBuzz"
    elsif (i % 3).zero?
      puts "Fizz"
    elsif (i % 5).zero?
      puts "Buzz"
    else
      puts i
    end
  end
end
''', r'''irb> fizzbuzz(5)
1
2
Fizz
4
Buzz'''),
    ("easy", "algorithms", r'''
def fib(n)
  a = 0
  b = 1
  n.times { a, b = b, a + b }
  a
end
''', r'''irb> (0..6).map { |i| fib(i) }
=> [0, 1, 1, 2, 3, 5, 8]'''),
    ("easy", "algorithms", r'''
def factorial(n)
  return 1 if n <= 1

  n * factorial(n - 1)
end
''', r'''irb> factorial(6)
=> 720'''),
    ("easy", "strings", r'''
def titleize(text)
  text.split.map(&:capitalize).join(" ")
end
''', r'''irb> titleize("hello wide world")
=> "Hello Wide World"'''),
    ("easy", "strings", r'''
def palindrome?(text)
  clean = text.downcase.gsub(/[^a-z0-9]/, "")
  clean == clean.reverse
end
''', r'''irb> palindrome?("A man, a plan, a canal: Panama")
=> true'''),
    ("easy", "strings", r'''
def anagram?(a, b)
  a.downcase.chars.sort == b.downcase.chars.sort
end
''', r'''irb> anagram?("listen", "silent")
=> true'''),
    ("easy", "strings", r'''
def slugify(text)
  text.downcase.strip.gsub(/[^a-z0-9]+/, "-").gsub(/\A-+|-+\z/, "")
end
''', r'''irb> slugify("  Hello, World!  ")
=> "hello-world"'''),
    ("easy", "strings", r'''
def truncate(text, max = 20)
  return text if text.length <= max

  "#{text[0, max - 1]}…"
end
''', r'''irb> truncate("a very long sentence", 10)
=> "a very lo…"'''),
    ("easy", "data-structures", r'''
def word_count(text)
  text.downcase.split.tally
end
''', r'''irb> word_count("the cat the hat")
=> {"the"=>2, "cat"=>1, "hat"=>1}'''),
    ("easy", "data-structures", r'''
def chunk(items, size)
  items.each_slice(size).to_a
end

def unique(items)
  items.uniq
end
''', r'''irb> chunk([1, 2, 3, 4, 5], 2)
=> [[1, 2], [3, 4], [5]]'''),
    ("easy", "data-structures", r'''
def group_by_length(words)
  words.group_by(&:length)
end
''', r'''irb> group_by_length(%w[a bb cc])
=> {1=>["a"], 2=>["bb", "cc"]}'''),
    ("easy", "math", r'''
def primes_below(limit)
  (2...limit).select do |n|
    (2..Integer.sqrt(n)).none? { |d| (n % d).zero? }
  end
end
''', r'''irb> primes_below(20)
=> [2, 3, 5, 7, 11, 13, 17, 19]'''),
    ("easy", "math", r'''
def gcd(a, b)
  b.zero? ? a.abs : gcd(b, a % b)
end
''', r'''irb> gcd(48, 18)
=> 6'''),
    ("easy", "functional", r'''
def group_by_status(orders)
  orders.each_with_object({}) do |order, acc|
    (acc[order.status] ||= []) << order.id
  end
end
''', r'''irb> group_by_status(orders)
=> {"paid"=>[1, 3], "open"=>[2]}'''),
    ("easy", "functional", r'''
def sum_of_squares(numbers)
  numbers.sum { |n| n * n }
end
''', r'''irb> sum_of_squares([1, 2, 3])
=> 14'''),
    ("easy", "oop", r'''
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
''', r'''irb> Inventory.new([{ price: 3, qty: 2 }]).total
=> 6'''),
    ("easy", "oop", r'''
class Counter
  def initialize
    @count = 0
  end

  attr_reader :count

  def bump(by = 1)
    @count += by
  end
end
''', r'''irb> c = Counter.new; c.bump(3)
=> 3'''),
    ("easy", "errors", r'''
def divide(a, b)
  raise ArgumentError, "cannot divide by zero" if b.zero?

  a / b
end
''', r'''irb> divide(1, 0)
ArgumentError: cannot divide by zero'''),
    ("easy", "data", r'''
def read_lines(path)
  File.readlines(path, chomp: true).reject(&:empty?)
end
''', r'''irb> read_lines("names.txt")
=> ["ada", "grace", "linus"]'''),
    ("easy", "web", r'''
def build_url(base, params)
  return base if params.empty?

  "#{base}?#{URI.encode_www_form(params)}"
end
''', r'''irb> build_url("/search", q: "code race")
=> "/search?q=code+race"'''),

    ("easy", "math", r"""
def sum_to(n)
  (1..n).sum
end
""", r"""irb> sum_to(10)
=> 55"""),
    ("easy", "data-structures", r"""
def most_common(items)
  items.tally.max_by { |_item, count| count }&.first
end
""", r"""irb> most_common(%w[a b a])
=> "a\""""),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
def binary_search(items, target)
  low = 0
  high = items.size - 1
  while low <= high
    mid = (low + high) / 2
    return mid if items[mid] == target

    if items[mid] < target
      low = mid + 1
    else
      high = mid - 1
    end
  end
  -1
end
''', r'''irb> binary_search([1, 3, 5, 7, 9], 7)
=> 3'''),
    ("medium", "algorithms", r'''
def two_sum(numbers, target)
  seen = {}
  numbers.each_with_index do |n, i|
    partner = seen[target - n]
    return [partner, i] if partner

    seen[n] = i
  end
  nil
end
''', r'''irb> two_sum([2, 7, 11, 15], 9)
=> [0, 1]'''),
    ("medium", "algorithms", r'''
def max_subarray(numbers)
  best = current = numbers.first
  numbers.drop(1).each do |n|
    current = [n, current + n].max
    best = [best, current].max
  end
  best
end
''', r'''irb> max_subarray([-2, 1, -3, 4, -1, 2, 1])
=> 6'''),
    ("medium", "algorithms", r'''
def merge_sorted(left, right)
  out = []
  until left.empty? || right.empty?
    out << (left.first <= right.first ? left.shift : right.shift)
  end
  out + left + right
end
''', r'''irb> merge_sorted([1, 4], [2, 3, 5])
=> [1, 2, 3, 4, 5]'''),
    ("medium", "data-structures", r'''
class Stack
  def initialize
    @items = []
  end

  def push(item)
    @items.push(item)
    self
  end

  def pop
    raise "the stack is empty" if @items.empty?

    @items.pop
  end

  def peek
    @items.last
  end
end
''', r'''irb> Stack.new.push(1).push(2).pop
=> 2'''),
    ("medium", "data-structures", r'''
class Queue
  def initialize
    @items = []
  end

  def enqueue(item)
    @items.push(item)
  end

  def dequeue
    @items.shift
  end

  def size
    @items.size
  end
end
''', r'''irb> q = Queue.new; q.enqueue("a"); q.dequeue
=> "a"'''),
    ("medium", "data-structures", r'''
Node = Struct.new(:value, :next_node) do
  def to_a
    out = []
    cursor = self
    while cursor
      out << cursor.value
      cursor = cursor.next_node
    end
    out
  end
end
''', r'''irb> Node.new(1, Node.new(2, nil)).to_a
=> [1, 2]'''),
    ("medium", "oop", r'''
class Money
  include Comparable

  attr_reader :cents

  def initialize(cents)
    @cents = cents
  end

  def <=>(other)
    cents <=> other.cents
  end

  def +(other)
    Money.new(cents + other.cents)
  end

  def to_s
    format("$%.2f", cents / 100.0)
  end
end
''', r'''irb> (Money.new(150) + Money.new(50)).to_s
=> "$2.00"'''),
    ("medium", "oop", r'''
class Shape
  def area
    raise NotImplementedError, "#{self.class} must implement area"
  end

  def describe
    format("area %.2f", area)
  end
end

class Rect < Shape
  def initialize(width, height)
    @width = width
    @height = height
  end

  def area
    @width * @height
  end
end
''', r'''irb> Rect.new(3, 4).describe
=> "area 12.00"'''),
    ("medium", "functional", r'''
def pipeline(*stages)
  lambda do |value|
    stages.reduce(value) { |acc, stage| stage.call(acc) }
  end
end
''', r'''irb> pipeline(:strip.to_proc, :upcase.to_proc).call("  hi  ")
=> "HI"'''),
    ("medium", "functional", r'''
def memoize(&block)
  cache = {}
  lambda do |key|
    cache.fetch(key) { cache[key] = block.call(key) }
  end
end
''', r'''irb> square = memoize { |n| n * n }; square.call(9)
=> 81'''),
    ("medium", "functional", r'''
def partition_by(items)
  items.partition { |item| yield(item) }
end

def index_by(items)
  items.to_h { |item| [yield(item), item] }
end
''', r'''irb> index_by(races) { |r| r.id }
=> {1=>#<Race>, 2=>#<Race>}'''),
    ("medium", "errors", r'''
class ValidationError < StandardError
  attr_reader :field

  def initialize(field, message)
    @field = field
    super("#{field}: #{message}")
  end
end

def require_fields(payload, *fields)
  fields.each do |field|
    raise ValidationError.new(field, "is required") if payload[field].to_s.empty?
  end
  payload
end
''', r'''irb> require_fields({ name: "ada" }, :name, :email)
ValidationError: email: is required'''),
    ("medium", "errors", r'''
def with_retry(attempts: 3, wait: 0.2)
  tries = 0
  begin
    tries += 1
    yield
  rescue StandardError
    raise if tries >= attempts

    sleep(wait * (2**(tries - 1)))
    retry
  end
end
''', r'''irb> with_retry { flaky_call }
RuntimeError: boom     # after 3 attempts'''),
    ("medium", "web", r'''
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
''', r'''PATCH /orders/1 => 200 OK, or 422 with errors'''),
    ("medium", "web", r'''
def fetch_json(url, timeout: 5)
  uri = URI(url)
  response = Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https",
                             read_timeout: timeout) do |http|
    http.get(uri.request_uri, "accept" => "application/json")
  end
  raise "HTTP #{response.code}" unless response.is_a?(Net::HTTPSuccess)

  JSON.parse(response.body)
end
''', r'''irb> fetch_json("https://api.example.com/me")
=> {"name"=>"ada"}'''),
    ("medium", "data", r'''
def top_by_language(limit = 5)
  Race
    .group(:language)
    .order(Arel.sql("MAX(wpm) DESC"))
    .limit(limit)
    .maximum(:wpm)
end
''', r'''irb> top_by_language(2)
=> {"python"=>118, "rust"=>104}'''),
    ("medium", "data", r'''
def write_csv(path, rows)
  CSV.open(path, "w") do |csv|
    csv << rows.first.keys
    rows.each { |row| csv << row.values }
  end
end
''', r'''irb> write_csv("out.csv", [{ name: "ada", wpm: 98 }])
# out.csv: name,wpm / ada,98'''),
    ("medium", "math", r'''
def percentile(values, p)
  sorted = values.sort
  index = (sorted.size - 1) * (p / 100.0)
  low = index.floor
  high = index.ceil
  return sorted[low].to_f if low == high

  sorted[low] + (sorted[high] - sorted[low]) * (index - low)
end
''', r'''irb> percentile([10, 20, 30, 40], 50)
=> 25.0'''),
    ("medium", "strings", r'''
def template(text, values)
  text.gsub(/\{(\w+)\}/) do
    key = Regexp.last_match(1).to_sym
    values.key?(key) ? values[key].to_s : Regexp.last_match(0)
  end
end
''', r'''irb> template("hi {name}", name: "ada")
=> "hi ada"'''),

    # --------------------------------------------------------------------- hard
    ("hard", "oop", r'''
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
''', r'''irb> Race.track(:wpm); race.wpm_changed?
=> false'''),
    ("hard", "oop", r'''
class Settings
  def initialize(values = {})
    @values = values
  end

  def method_missing(name, *args)
    key = name.to_s.delete_suffix("=").to_sym
    if name.to_s.end_with?("=")
      @values[key] = args.first
    elsif @values.key?(key)
      @values[key]
    else
      super
    end
  end

  def respond_to_missing?(name, include_private = false)
    @values.key?(name.to_s.delete_suffix("=").to_sym) || super
  end
end
''', r'''irb> s = Settings.new(port: 25_616); s.port
=> 25616'''),
    ("hard", "oop", r'''
class Pipeline
  def initialize
    @steps = []
  end

  def use(&block)
    @steps << block
    self
  end

  def call(input)
    @steps.reverse.reduce(->(value) { value }) do |next_step, step|
      ->(value) { step.call(value, next_step) }
    end.call(input)
  end
end
''', r'''irb> Pipeline.new.use { |v, n| n.call(v * 2) }.call(5)
=> 10'''),
    ("hard", "functional", r'''
def curry_all(callable)
  callable.curry
end

def compose(*functions)
  functions.reduce { |f, g| ->(value) { g.call(f.call(value)) } }
end
''', r'''irb> compose(->(n) { n + 1 }, ->(n) { n * 2 }).call(3)
=> 8'''),
    ("hard", "functional", r'''
def lazy_primes
  Enumerator.new do |yielder|
    n = 2
    loop do
      yielder << n if (2..Integer.sqrt(n)).none? { |d| (n % d).zero? }
      n += 1
    end
  end.lazy
end
''', r'''irb> lazy_primes.first(5)
=> [2, 3, 5, 7, 11]'''),
    ("hard", "functional", r'''
def transduce(items, *transforms)
  transforms.reduce(items.lazy) do |acc, transform|
    kind, block = transform
    kind == :map ? acc.map(&block) : acc.select(&block)
  end.to_a
end
''', r'''irb> transduce([1, 2, 3, 4], [:select, :even?.to_proc], [:map, ->(n) { n * 10 }])
=> [20, 40]'''),
    ("hard", "data-structures", r'''
class LruCache
  def initialize(capacity = 128)
    @capacity = capacity
    @items = {}
  end

  def get(key)
    return nil unless @items.key?(key)

    value = @items.delete(key)
    @items[key] = value
  end

  def put(key, value)
    @items.delete(key)
    @items[key] = value
    @items.delete(@items.keys.first) if @items.size > @capacity
    value
  end
end
''', r'''irb> c = LruCache.new(2) # put a, b, c => a evicted'''),
    ("hard", "data-structures", r'''
class Trie
  def initialize
    @children = {}
    @word = false
  end

  def insert(text)
    node = self
    text.each_char { |char| node = node.child(char) }
    node.mark_word
  end

  def include?(text)
    node = self
    text.each_char do |char|
      node = node.children[char]
      return false if node.nil?
    end
    node.word?
  end

  protected

  attr_reader :children

  def child(char)
    @children[char] ||= Trie.new
  end

  def mark_word
    @word = true
  end

  def word?
    @word
  end
end
''', r'''irb> t = Trie.new; t.insert("code"); t.include?("cod")
=> false'''),
    ("hard", "data-structures", r'''
class MinHeap
  def initialize
    @items = []
  end

  def push(value)
    @items << value
    index = @items.size - 1
    while index.positive?
      parent = (index - 1) / 2
      break if @items[parent] <= @items[index]

      @items[parent], @items[index] = @items[index], @items[parent]
      index = parent
    end
    self
  end

  def peek
    @items.first
  end
end
''', r'''irb> MinHeap.new.push(5).push(2).push(8).peek
=> 2'''),
    ("hard", "algorithms", r'''
def levenshtein(a, b)
  previous = (0..b.length).to_a
  a.each_char.with_index(1) do |ca, i|
    current = [i]
    b.each_char.with_index(1) do |cb, j|
      current[j] = [
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + (ca == cb ? 0 : 1)
      ].min
    end
    previous = current
  end
  previous.last
end
''', r'''irb> levenshtein("kitten", "sitting")
=> 3'''),
    ("hard", "algorithms", r'''
def dijkstra(graph, start)
  distances = { start => 0 }
  queue = [[0, start]]
  until queue.empty?
    queue.sort_by!(&:first)
    cost, node = queue.shift
    next if cost > distances.fetch(node, Float::INFINITY)

    graph.fetch(node, {}).each do |neighbour, weight|
      candidate = cost + weight
      next unless candidate < distances.fetch(neighbour, Float::INFINITY)

      distances[neighbour] = candidate
      queue << [candidate, neighbour]
    end
  end
  distances
end
''', r'''irb> dijkstra({ "a" => { "b" => 1 }, "b" => { "c" => 2 } }, "a")
=> {"a"=>0, "b"=>1, "c"=>3}'''),
    ("hard", "algorithms", r'''
def quicksort(items)
  return items if items.size < 2

  pivot, *rest = items
  left, right = rest.partition { |n| n < pivot }
  quicksort(left) + [pivot] + quicksort(right)
end
''', r'''irb> quicksort([3, 6, 1, 2])
=> [1, 2, 3, 6]'''),
    ("hard", "async", r'''
def parallel_map(items, threads: 4, &block)
  queue = Queue.new
  items.each_with_index { |item, i| queue << [i, item] }
  results = Array.new(items.size)

  workers = Array.new(threads) do
    Thread.new do
      while (job = queue.pop(true) rescue nil)
        index, item = job
        results[index] = block.call(item)
      end
    end
  end
  workers.each(&:join)
  results
end
''', r'''irb> parallel_map([1, 2, 3]) { |n| n * n }
=> [1, 4, 9]'''),
    ("hard", "async", r'''
class RateLimiter
  def initialize(per_second)
    @interval = 1.0 / per_second
    @last = Time.now - @interval
    @lock = Mutex.new
  end

  def throttle
    @lock.synchronize do
      wait = @interval - (Time.now - @last)
      sleep(wait) if wait.positive?
      @last = Time.now
    end
    yield
  end
end
''', r'''irb> limiter.throttle { call_api }
# at most N calls per second'''),
    ("hard", "async", r'''
def with_timeout(seconds, fallback: nil)
  Timeout.timeout(seconds) { yield }
rescue Timeout::Error
  fallback
end
''', r'''irb> with_timeout(0.1, fallback: "gave up") { sleep 5 }
=> "gave up"'''),
    ("hard", "errors", r'''
class Result
  def self.ok(value) = new(value: value)
  def self.err(error) = new(error: error)

  def initialize(value: nil, error: nil)
    @value = value
    @error = error
  end

  def ok? = @error.nil?

  def then
    return self unless ok?

    Result.ok(yield(@value))
  rescue StandardError => e
    Result.err(e)
  end

  def value_or(fallback) = ok? ? @value : fallback
end
''', r'''irb> Result.ok(2).then { |n| n * 3 }.value_or(0)
=> 6'''),
    ("hard", "data", r'''
def import_races(path)
  ActiveRecord::Base.transaction do
    CSV.foreach(path, headers: true).each_slice(500) do |batch|
      Race.insert_all(batch.map { |row| row.to_h.slice("wpm", "language") })
    end
  end
end
''', r'''irb> import_races("races.csv")
# one transaction, inserted 500 at a time'''),
    ("hard", "web", r'''
class Middleware
  def initialize(app)
    @app = app
  end

  def call(env)
    started = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    status, headers, body = @app.call(env)
    elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - started
    headers["x-runtime"] = format("%.3f", elapsed)
    [status, headers, body]
  end
end
''', r'''GET /  =>  x-runtime: 0.002'''),
    ("hard", "strings", r'''
def top_words(text, limit)
  text
    .downcase
    .scan(/[a-z0-9']+/)
    .tally
    .sort_by { |word, count| [-count, word] }
    .first(limit)
end
''', r'''irb> top_words("the cat the hat the end", 2)
=> [["the", 3], ["cat", 1]]'''),
    ("hard", "math", r'''
def matrix_multiply(a, b)
  rows = a.size
  inner = b.size
  cols = b.first.size
  out = Array.new(rows) { Array.new(cols, 0) }

  rows.times do |i|
    inner.times do |k|
      value = a[i][k]
      next if value.zero?

      cols.times { |j| out[i][j] += value * b[k][j] }
    end
  end
  out
end
''', r'''irb> matrix_multiply([[1, 2]], [[3], [4]])
=> [[11]]'''),
]
