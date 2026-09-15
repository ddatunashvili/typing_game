"""TypeScript snippet pack: 20 per level, leaning on the type system.

Entries are (level, topic, code, expected_output). The output is a short demo
transcript for the simulated run panel - nothing is executed.
"""
LANGUAGE = "typescript"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
export function add(a: number, b: number): number {
  return a + b;
}
''', r'''> add(2, 3)
5'''),
    ("very-easy", "math", r'''
export const isEven = (n: number): boolean => n % 2 === 0;
''', r'''> isEven(10)
true'''),
    ("very-easy", "strings", r'''
export function shout(text: string): string {
  return text.toUpperCase() + "!";
}
''', r'''> shout("hello")
'HELLO!' '''),
    ("very-easy", "strings", r'''
export const reverse = (text: string): string =>
  text.split("").reverse().join("");
''', r'''> reverse("typescript")
'tpircsepyt' '''),
    ("very-easy", "oop", r'''
interface User {
  id: number;
  name: string;
}

export function label(user: User): string {
  return `#${user.id} ${user.name}`;
}
''', r'''> label({ id: 1, name: "ada" })
'#1 ada' '''),
    ("very-easy", "oop", r'''
type Status = "waiting" | "racing" | "finished";

export function isDone(status: Status): boolean {
  return status === "finished";
}
''', r'''> isDone("racing")
false'''),
    ("very-easy", "math", r'''
export const clamp = (n: number, min: number, max: number): number =>
  Math.min(Math.max(n, min), max);
''', r'''> clamp(42, 0, 10)
10'''),
    ("very-easy", "functional", r'''
export const doubled = (numbers: number[]): number[] =>
  numbers.map((n) => n * 2);
''', r'''> doubled([1, 2, 3])
[ 2, 4, 6 ]'''),
    ("very-easy", "functional", r'''
export const sum = (numbers: number[]): number =>
  numbers.reduce((a, b) => a + b, 0);
''', r'''> sum([1, 2, 3, 4])
10'''),
    ("very-easy", "data-structures", r'''
export function firstOrNull<T>(items: T[]): T | null {
  return items.length ? items[0] : null;
}
''', r'''> firstOrNull<number>([])
null'''),
    ("very-easy", "data-structures", r'''
export const last = <T>(items: T[]): T | undefined => items[items.length - 1];
''', r'''> last([1, 2, 3])
3'''),
    ("very-easy", "errors", r'''
export function safeInt(text: string, fallback = 0): number {
  const value = Number.parseInt(text, 10);
  return Number.isNaN(value) ? fallback : value;
}
''', r'''> safeInt("oops")
0'''),
    ("very-easy", "oop", r'''
export class Dog {
  constructor(public readonly name: string) {}

  speak(): string {
    return `${this.name} says woof`;
  }
}
''', r'''> new Dog("Rex").speak()
'Rex says woof' '''),
    ("very-easy", "strings", r'''
export const isBlank = (text: string): boolean => text.trim().length === 0;
''', r'''> isBlank("   ")
true'''),
    ("very-easy", "algorithms", r'''
export function largest(numbers: number[]): number {
  let best = numbers[0];
  for (const n of numbers) {
    if (n > best) best = n;
  }
  return best;
}
''', r'''> largest([3, 9, 4])
9'''),
    ("very-easy", "async", r'''
export const later = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));
''', r'''> await later(200);
// resolves after 200ms'''),
    ("very-easy", "math", r'''
export function round(value: number, places = 2): number {
  const factor = 10 ** places;
  return Math.round(value * factor) / factor;
}
''', r'''> round(3.14159)
3.14'''),
    ("very-easy", "data-structures", r'''
export const merge = <A extends object, B extends object>(a: A, b: B): A & B => ({
  ...a,
  ...b,
});
''', r'''> merge({ a: 1 }, { b: 2 })
{ a: 1, b: 2 }'''),
    ("very-easy", "web", r'''
export function buildUrl(base: string, params: Record<string, string>): string {
  return base + "?" + new URLSearchParams(params).toString();
}
''', r'''> buildUrl("/search", { q: "code" })
'/search?q=code' '''),
    ("very-easy", "strings", r'''
export function initials(first: string, last: string): string {
  return (first[0] ?? "") + (last[0] ?? "");
}
''', r'''> initials("Ada", "Lovelace")
'AL' '''),

    # --------------------------------------------------------------------- easy
    ("easy", "oop", r'''
interface User {
  id: number;
  name: string;
  roles: string[];
}

export function isAdmin(user: User): boolean {
  return user.roles.includes("admin");
}

export const byName = (a: User, b: User): number =>
  a.name.localeCompare(b.name);
''', r'''> isAdmin({ id: 1, name: "ada", roles: ["admin"] })
true'''),
    ("easy", "oop", r'''
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

export function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rect":
      return shape.width * shape.height;
  }
}
''', r'''> area({ kind: "rect", width: 3, height: 4 })
12'''),
    ("easy", "algorithms", r'''
export function fib(n: number): number {
  let a = 0;
  let b = 1;
  for (let i = 0; i < n; i++) {
    [a, b] = [b, a + b];
  }
  return a;
}
''', r'''> [0, 1, 2, 3, 4, 5, 6].map(fib)
[ 0, 1, 1, 2, 3, 5, 8 ]'''),
    ("easy", "algorithms", r'''
export function fizzbuzz(n: number): string[] {
  const out: string[] = [];
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) out.push("FizzBuzz");
    else if (i % 3 === 0) out.push("Fizz");
    else if (i % 5 === 0) out.push("Buzz");
    else out.push(String(i));
  }
  return out;
}
''', r'''> fizzbuzz(5)
[ '1', '2', 'Fizz', '4', 'Buzz' ]'''),
    ("easy", "strings", r'''
export function isPalindrome(text: string): boolean {
  const clean = text.toLowerCase().replace(/[^a-z0-9]/g, "");
  return clean === [...clean].reverse().join("");
}
''', r'''> isPalindrome("A man, a plan, a canal: Panama")
true'''),
    ("easy", "strings", r'''
export function titleCase(text: string): string {
  return text
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}
''', r'''> titleCase("hello wide world")
'Hello Wide World' '''),
    ("easy", "data-structures", r'''
export function unique<T>(items: T[]): T[] {
  return [...new Set(items)];
}

export function chunk<T>(items: T[], size: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < items.length; i += size) out.push(items.slice(i, i + size));
  return out;
}
''', r'''> chunk(unique([1, 1, 2, 3, 4]), 2)
[ [ 1, 2 ], [ 3, 4 ] ]'''),
    ("easy", "data-structures", r'''
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
''', r'''> new Registry<number>().set("a", 1).get("a")
1'''),
    ("easy", "functional", r'''
export function partition<T>(rows: T[], keep: (row: T) => boolean): [T[], T[]] {
  const yes: T[] = [];
  const no: T[] = [];
  for (const row of rows) (keep(row) ? yes : no).push(row);
  return [yes, no];
}
''', r'''> partition([1, 2, 3, 4], (n) => n % 2 === 0)
[ [ 2, 4 ], [ 1, 3 ] ]'''),
    ("easy", "functional", r'''
export function pluck<T, K extends keyof T>(rows: T[], key: K): T[K][] {
  return rows.map((row) => row[key]);
}
''', r'''> pluck([{ id: 1 }, { id: 2 }], "id")
[ 1, 2 ]'''),
    ("easy", "errors", r'''
type Result<T> = { ok: true; value: T } | { ok: false; error: string };

export async function safe<T>(fn: () => Promise<T>): Promise<Result<T>> {
  try {
    return { ok: true, value: await fn() };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}
''', r'''> await safe(async () => 1)
{ ok: true, value: 1 }'''),
    ("easy", "errors", r'''
export class ValidationError extends Error {
  constructor(public readonly field: string, message: string) {
    super(`${field}: ${message}`);
    this.name = "ValidationError";
  }
}
''', r'''> new ValidationError("email", "is required").message
'email: is required' '''),
    ("easy", "math", r'''
export function isPrime(n: number): boolean {
  if (n < 2) return false;
  for (let d = 2; d * d <= n; d++) {
    if (n % d === 0) return false;
  }
  return true;
}
''', r'''> [2, 3, 4, 5].filter(isPrime)
[ 2, 3, 5 ]'''),
    ("easy", "math", r'''
export function average(numbers: readonly number[]): number {
  return numbers.length ? numbers.reduce((a, b) => a + b, 0) / numbers.length : 0;
}
''', r'''> average([2, 4, 6])
4'''),
    ("easy", "async", r'''
export async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url, { headers: { accept: "application/json" } });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return (await res.json()) as T;
}
''', r'''> await getJson<{ name: string }>("/api/me")
{ name: 'ada' }'''),
    ("easy", "web", r'''
export interface Paged<T> {
  items: T[];
  page: number;
  total: number;
}

export function pageOf<T>(items: T[], page = 1, per = 10): Paged<T> {
  const start = (page - 1) * per;
  return { items: items.slice(start, start + per), page, total: items.length };
}
''', r'''> pageOf([1, 2, 3, 4, 5], 2, 2)
{ items: [ 3, 4 ], page: 2, total: 5 }'''),
    ("easy", "oop", r'''
export class Counter {
  #count = 0;

  bump(by = 1): number {
    this.#count += by;
    return this.#count;
  }

  get value(): number {
    return this.#count;
  }
}
''', r'''> const c = new Counter();
> c.bump(3)
3'''),
    ("easy", "data", r'''
export interface Race {
  id: number;
  wpm: number;
}

export function bestWpm(races: Race[]): number {
  return races.reduce((best, race) => Math.max(best, race.wpm), 0);
}
''', r'''> bestWpm([{ id: 1, wpm: 88 }, { id: 2, wpm: 104 }])
104'''),
    ("easy", "ui", r'''
export function onClick(selector: string, handler: (el: HTMLElement) => void): void {
  document.querySelectorAll<HTMLElement>(selector).forEach((el) => {
    el.addEventListener("click", () => handler(el));
  });
}
''', r'''> onClick(".card", (el) => el.classList.add("picked"))
// each card toggles .picked when clicked'''),
    ("easy", "strings", r'''
export function truncate(text: string, max = 20): string {
  return text.length <= max ? text : `${text.slice(0, max - 1)}…`;
}
''', r'''> truncate("a very long sentence", 10)
'a very lo…' '''),

    # ------------------------------------------------------------------- medium
    ("medium", "oop", r'''
export type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

export function patch<T extends object>(base: T, changes: DeepPartial<T>): T {
  return { ...base, ...(changes as T) };
}
''', r'''> patch({ a: 1, b: 2 }, { b: 9 })
{ a: 1, b: 9 }'''),
    ("medium", "oop", r'''
export type Keys<T, V> = {
  [K in keyof T]-?: T[K] extends V ? K : never;
}[keyof T];

export function numericKeys<T extends object>(row: T): Keys<T, number>[] {
  return Object.keys(row).filter(
    (key) => typeof (row as Record<string, unknown>)[key] === "number"
  ) as Keys<T, number>[];
}
''', r'''> numericKeys({ id: 1, name: "ada", wpm: 98 })
[ 'id', 'wpm' ]'''),
    ("medium", "oop", r'''
export abstract class Repository<T extends { id: number }> {
  protected rows = new Map<number, T>();

  abstract validate(row: T): void;

  save(row: T): T {
    this.validate(row);
    this.rows.set(row.id, row);
    return row;
  }

  find(id: number): T | undefined {
    return this.rows.get(id);
  }
}
''', r'''> class Users extends Repository<User> { validate() {} }
> new Users().save({ id: 1, name: "ada" }).name
'ada' '''),
    ("medium", "functional", r'''
export function memoize<A extends unknown[], R>(fn: (...args: A) => R) {
  const cache = new Map<string, R>();
  return (...args: A): R => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) cache.set(key, fn(...args));
    return cache.get(key) as R;
  };
}
''', r'''> const square = memoize((n: number) => n * n);
> square(9); square(9);
81'''),
    ("medium", "functional", r'''
export function debounce<A extends unknown[]>(
  fn: (...args: A) => void,
  wait = 250
): (...args: A) => void {
  let timer: ReturnType<typeof setTimeout> | null = null;
  return (...args: A) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}
''', r'''> const log = debounce(() => console.log("fired"), 200);
> log(); log();
fired'''),
    ("medium", "functional", r'''
export function groupBy<T, K extends string>(
  items: T[],
  key: (item: T) => K
): Record<K, T[]> {
  return items.reduce((acc, item) => {
    const bucket = key(item);
    (acc[bucket] ??= []).push(item);
    return acc;
  }, {} as Record<K, T[]>);
}
''', r'''> groupBy([1, 2, 3], (n) => (n % 2 ? "odd" : "even"))
{ odd: [ 1, 3 ], even: [ 2 ] }'''),
    ("medium", "algorithms", r'''
export function binarySearch(items: readonly number[], target: number): number {
  let low = 0;
  let high = items.length - 1;
  while (low <= high) {
    const mid = (low + high) >> 1;
    if (items[mid] === target) return mid;
    if (items[mid] < target) low = mid + 1;
    else high = mid - 1;
  }
  return -1;
}
''', r'''> binarySearch([1, 3, 5, 7], 5)
2'''),
    ("medium", "algorithms", r'''
export function twoSum(numbers: number[], target: number): [number, number] | null {
  const seen = new Map<number, number>();
  for (let i = 0; i < numbers.length; i++) {
    const partner = seen.get(target - numbers[i]);
    if (partner !== undefined) return [partner, i];
    seen.set(numbers[i], i);
  }
  return null;
}
''', r'''> twoSum([2, 7, 11], 9)
[ 0, 1 ]'''),
    ("medium", "data-structures", r'''
export class Stack<T> {
  private items: T[] = [];

  push(item: T): this {
    this.items.push(item);
    return this;
  }

  pop(): T {
    const value = this.items.pop();
    if (value === undefined) throw new Error("stack is empty");
    return value;
  }

  peek(): T | undefined {
    return this.items.at(-1);
  }
}
''', r'''> new Stack<number>().push(1).push(2).pop()
2'''),
    ("medium", "data-structures", r'''
export class Queue<T> {
  private items: T[] = [];
  private head = 0;

  enqueue(item: T): void {
    this.items.push(item);
  }

  dequeue(): T | undefined {
    if (this.head >= this.items.length) return undefined;
    const value = this.items[this.head];
    this.head += 1;
    return value;
  }

  get length(): number {
    return this.items.length - this.head;
  }
}
''', r'''> const q = new Queue<string>();
> q.enqueue("a"); q.dequeue();
'a' '''),
    ("medium", "async", r'''
export async function retry<T>(
  fn: () => Promise<T>,
  times = 3,
  delay = 200
): Promise<T> {
  let last: unknown;
  for (let attempt = 0; attempt < times; attempt++) {
    try {
      return await fn();
    } catch (err) {
      last = err;
      await new Promise((r) => setTimeout(r, delay * 2 ** attempt));
    }
  }
  throw last;
}
''', r'''> await retry(() => getJson("/flaky"))
Error: 500 Internal Server Error'''),
    ("medium", "async", r'''
export async function withTimeout<T>(
  promise: Promise<T>,
  ms: number,
  fallback: T
): Promise<T> {
  let timer: ReturnType<typeof setTimeout>;
  const guard = new Promise<T>((resolve) => {
    timer = setTimeout(() => resolve(fallback), ms);
  });
  try {
    return await Promise.race([promise, guard]);
  } finally {
    clearTimeout(timer!);
  }
}
''', r'''> await withTimeout(slow(), 100, "gave up")
'gave up' '''),
    ("medium", "errors", r'''
export class HttpError extends Error {
  constructor(
    public readonly status: number,
    public readonly body?: unknown
  ) {
    super(`HTTP ${status}`);
    this.name = "HttpError";
  }

  get retryable(): boolean {
    return this.status >= 500 || this.status === 429;
  }
}
''', r'''> new HttpError(503).retryable
true'''),
    ("medium", "web", r'''
export interface Handler {
  (request: Request): Promise<Response>;
}

export function withCors(handler: Handler): Handler {
  return async (request) => {
    const response = await handler(request);
    response.headers.set("access-control-allow-origin", "*");
    return response;
  };
}
''', r'''> await withCors(handler)(new Request("/api"))
Response { status: 200 }'''),
    ("medium", "data", r'''
export function upsert<T extends { id: number }>(rows: T[], row: T): T[] {
  const index = rows.findIndex((item) => item.id === row.id);
  if (index === -1) return [...rows, row];
  return rows.map((item, i) => (i === index ? { ...item, ...row } : item));
}
''', r'''> upsert([{ id: 1, n: "a" }], { id: 1, n: "b" })
[ { id: 1, n: 'b' } ]'''),
    ("medium", "strings", r'''
export function template(text: string, values: Record<string, unknown>): string {
  return text.replace(/\{(\w+)\}/g, (match, key: string) =>
    key in values ? String(values[key]) : match
  );
}
''', r'''> template("hi {name}", { name: "ada" })
'hi ada' '''),
    ("medium", "ui", r'''
export function useLocalStorage<T>(key: string, fallback: T): [() => T, (v: T) => void] {
  const read = (): T => {
    try {
      const raw = localStorage.getItem(key);
      return raw ? (JSON.parse(raw) as T) : fallback;
    } catch {
      return fallback;
    }
  };
  const write = (value: T): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      /* private mode: ignore */
    }
  };
  return [read, write];
}
''', r'''> const [read, write] = useLocalStorage("theme", "dark");
> write("light"); read();
'light' '''),
    ("medium", "math", r'''
export function percentile(values: readonly number[], p: number): number {
  const sorted = [...values].sort((a, b) => a - b);
  const index = (sorted.length - 1) * (p / 100);
  const low = Math.floor(index);
  const high = Math.ceil(index);
  if (low === high) return sorted[low];
  return sorted[low] + (sorted[high] - sorted[low]) * (index - low);
}
''', r'''> percentile([10, 20, 30, 40], 50)
25'''),
    ("medium", "oop", r'''
export class Builder<T extends object> {
  private draft: Partial<T> = {};

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.draft[key] = value;
    return this;
  }

  build(): T {
    return this.draft as T;
  }
}
''', r'''> new Builder<User>().set("id", 1).set("name", "ada").build()
{ id: 1, name: 'ada' }'''),
    ("medium", "functional", r'''
export const pipe =
  <T>(...fns: Array<(value: T) => T>) =>
  (value: T): T =>
    fns.reduce((acc, fn) => fn(acc), value);
''', r'''> pipe<string>((s) => s.trim(), (s) => s.toUpperCase())("  hi  ")
'HI' '''),

    # --------------------------------------------------------------------- hard
    ("hard", "oop", r'''
export type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

export type Paths<T> = T extends object
  ? {
      [K in keyof T & string]: T[K] extends object ? K | `${K}.${Paths<T[K]>}` : K;
    }[keyof T & string]
  : never;
''', r'''> type P = Paths<{ db: { host: string } }>
'db' | 'db.host' '''),
    ("hard", "oop", r'''
export type Mutable<T> = { -readonly [K in keyof T]: T[K] };

export type RequireAtLeastOne<T, K extends keyof T = keyof T> = Omit<T, K> &
  { [P in K]-?: Required<Pick<T, P>> & Partial<Omit<T, P>> }[K];

export function fetchBy(
  query: RequireAtLeastOne<{ id: number; email: string }>
): string {
  return "id" in query ? `id=${query.id}` : `email=${query.email}`;
}
''', r'''> fetchBy({ email: "ada@example.com" })
'email=ada@example.com'
> fetchBy({})
error TS2345: Argument of type '{}' is not assignable'''),
    ("hard", "oop", r'''
export function assertNever(value: never): never {
  throw new Error(`unhandled case: ${JSON.stringify(value)}`);
}

type Event =
  | { type: "start"; at: number }
  | { type: "finish"; wpm: number };

export function describe(event: Event): string {
  switch (event.type) {
    case "start":
      return `started at ${event.at}`;
    case "finish":
      return `finished at ${event.wpm} wpm`;
    default:
      return assertNever(event);
  }
}
''', r'''> describe({ type: "finish", wpm: 98 })
'finished at 98 wpm' '''),
    ("hard", "oop", r'''
export function typedEmitter<Events extends Record<string, unknown[]>>() {
  const handlers = new Map<keyof Events, Set<(...args: never[]) => void>>();
  return {
    on<K extends keyof Events>(event: K, fn: (...args: Events[K]) => void) {
      if (!handlers.has(event)) handlers.set(event, new Set());
      handlers.get(event)!.add(fn as (...args: never[]) => void);
    },
    emit<K extends keyof Events>(event: K, ...args: Events[K]) {
      for (const fn of handlers.get(event) ?? []) {
        (fn as (...a: Events[K]) => void)(...args);
      }
    },
  };
}
''', r'''> const bus = typedEmitter<{ tick: [number] }>();
> bus.on("tick", (n) => console.log(n)); bus.emit("tick", 1);
1'''),
    ("hard", "errors", r'''
export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export function tryAll<T>(tasks: Array<() => T>): Result<T[]> {
  const values: T[] = [];
  for (const task of tasks) {
    try {
      values.push(task());
    } catch (err) {
      return { ok: false, error: err instanceof Error ? err : new Error(String(err)) };
    }
  }
  return { ok: true, value: values };
}
''', r'''> tryAll([() => 1, () => { throw new Error("nope"); }])
{ ok: false, error: Error: nope }'''),
    ("hard", "functional", r'''
type Curried<A extends unknown[], R> = A extends [infer H, ...infer T]
  ? (arg: H) => Curried<T, R>
  : R;

export function curry<A extends unknown[], R>(fn: (...args: A) => R): Curried<A, R> {
  const collect = (...args: unknown[]): unknown =>
    args.length >= fn.length ? fn(...(args as A)) : (next: unknown) => collect(...args, next);
  return collect as Curried<A, R>;
}
''', r'''> curry((a: number, b: number) => a + b)(1)(2)
3'''),
    ("hard", "functional", r'''
export function lens<T, K extends keyof T>(key: K) {
  return {
    get: (source: T): T[K] => source[key],
    set: (source: T, value: T[K]): T => ({ ...source, [key]: value }),
  };
}
''', r'''> const name = lens<User, "name">("name");
> name.set({ id: 1, name: "ada" }, "grace").name
'grace' '''),
    ("hard", "async", r'''
export async function pool<T>(
  tasks: Array<() => Promise<T>>,
  limit = 4
): Promise<T[]> {
  const results: T[] = [];
  const running = new Set<Promise<void>>();
  for (const task of tasks) {
    const job = task().then((value) => {
      results.push(value);
      running.delete(job);
    });
    running.add(job);
    if (running.size >= limit) await Promise.race(running);
  }
  await Promise.all(running);
  return results;
}
''', r'''> await pool(urls.map((u) => () => getJson(u)), 3)
[ {...}, {...}, {...} ]'''),
    ("hard", "async", r'''
export async function* batched<T>(
  source: AsyncIterable<T>,
  size: number
): AsyncGenerator<T[]> {
  let batch: T[] = [];
  for await (const item of source) {
    batch.push(item);
    if (batch.length >= size) {
      yield batch;
      batch = [];
    }
  }
  if (batch.length) yield batch;
}
''', r'''> for await (const group of batched(stream, 2)) console.log(group.length);
2
2
1'''),
    ("hard", "async", r'''
export class AsyncQueue<T> {
  private items: T[] = [];
  private waiting: Array<(value: T) => void> = [];

  push(item: T): void {
    const next = this.waiting.shift();
    if (next) next(item);
    else this.items.push(item);
  }

  pull(): Promise<T> {
    const item = this.items.shift();
    if (item !== undefined) return Promise.resolve(item);
    return new Promise((resolve) => this.waiting.push(resolve));
  }
}
''', r'''> const q = new AsyncQueue<number>();
> q.push(1); await q.pull();
1'''),
    ("hard", "data-structures", r'''
export class LruCache<K, V> {
  private items = new Map<K, V>();

  constructor(private readonly capacity = 128) {}

  get(key: K): V | undefined {
    if (!this.items.has(key)) return undefined;
    const value = this.items.get(key) as V;
    this.items.delete(key);
    this.items.set(key, value);
    return value;
  }

  set(key: K, value: V): void {
    this.items.delete(key);
    this.items.set(key, value);
    if (this.items.size > this.capacity) {
      this.items.delete(this.items.keys().next().value as K);
    }
  }
}
''', r'''> const c = new LruCache<string, number>(2);
> c.set("a", 1); c.set("b", 2); c.get("a"); c.set("c", 3);
> c.get("b")
undefined'''),
    ("hard", "data-structures", r'''
export class Graph<T> {
  private edges = new Map<T, Set<T>>();

  link(from: T, to: T): void {
    if (!this.edges.has(from)) this.edges.set(from, new Set());
    this.edges.get(from)!.add(to);
  }

  reachable(start: T): Set<T> {
    const seen = new Set<T>([start]);
    const stack: T[] = [start];
    while (stack.length) {
      for (const next of this.edges.get(stack.pop() as T) ?? []) {
        if (!seen.has(next)) {
          seen.add(next);
          stack.push(next);
        }
      }
    }
    return seen;
  }
}
''', r'''> const g = new Graph<string>();
> g.link("a", "b"); g.link("b", "c"); [...g.reachable("a")]
[ 'a', 'b', 'c' ]'''),
    ("hard", "algorithms", r'''
export function levenshtein(a: string, b: string): number {
  let previous = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const current = [i];
    for (let j = 1; j <= b.length; j++) {
      current[j] = Math.min(
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      );
    }
    previous = current;
  }
  return previous[b.length];
}
''', r'''> levenshtein("kitten", "sitting")
3'''),
    ("hard", "algorithms", r'''
export function topologicalSort(graph: Record<string, string[]>): string[] {
  const seen = new Set<string>();
  const order: string[] = [];
  const visit = (node: string, path: Set<string>): void => {
    if (path.has(node)) throw new Error(`cycle at ${node}`);
    if (seen.has(node)) return;
    path.add(node);
    for (const next of graph[node] ?? []) visit(next, path);
    path.delete(node);
    seen.add(node);
    order.push(node);
  };
  for (const node of Object.keys(graph)) visit(node, new Set());
  return order;
}
''', r'''> topologicalSort({ app: ["db"], db: [] })
[ 'db', 'app' ]'''),
    ("hard", "web", r'''
export function createClient(base: string, token?: string) {
  const request = async <T>(path: string, init: RequestInit = {}): Promise<T> => {
    const res = await fetch(base + path, {
      ...init,
      headers: {
        "content-type": "application/json",
        ...(token ? { authorization: `Bearer ${token}` } : {}),
        ...init.headers,
      },
    });
    if (!res.ok) throw new HttpError(res.status, await res.text());
    return (await res.json()) as T;
  };
  return {
    get: <T>(path: string) => request<T>(path),
    post: <T>(path: string, body: unknown) =>
      request<T>(path, { method: "POST", body: JSON.stringify(body) }),
  };
}
''', r'''> const api = createClient("/api", "tok");
> await api.get<User>("/me")
{ id: 1, name: 'ada' }'''),
    ("hard", "data", r'''
export interface Column<T> {
  key: keyof T & string;
  label: string;
  format?: (value: T[keyof T]) => string;
}

export function toTable<T extends object>(rows: T[], columns: Column<T>[]): string {
  const header = columns.map((c) => c.label).join(" | ");
  const body = rows.map((row) =>
    columns
      .map((c) => (c.format ? c.format(row[c.key]) : String(row[c.key])))
      .join(" | ")
  );
  return [header, ...body].join("\n");
}
''', r'''> toTable([{ name: "ada", wpm: 98 }], [{ key: "name", label: "Who" }])
Who
ada'''),
    ("hard", "ui", r'''
export function createSignal<T>(initial: T) {
  let value = initial;
  const subscribers = new Set<(next: T) => void>();
  return {
    get: (): T => value,
    set: (next: T): void => {
      if (Object.is(next, value)) return;
      value = next;
      subscribers.forEach((fn) => fn(value));
    },
    subscribe: (fn: (next: T) => void): (() => void) => {
      subscribers.add(fn);
      return () => subscribers.delete(fn);
    },
  };
}
''', r'''> const wpm = createSignal(0);
> wpm.subscribe((n) => console.log("wpm", n)); wpm.set(98);
wpm 98'''),
    ("hard", "strings", r'''
export function tokenize(source: string): Array<{ type: string; value: string }> {
  const patterns: Array<[string, RegExp]> = [
    ["number", /^\d+(\.\d+)?/],
    ["ident", /^[A-Za-z_]\w*/],
    ["op", /^[+\-*/()=]/],
    ["space", /^\s+/],
  ];
  const out: Array<{ type: string; value: string }> = [];
  let rest = source;
  while (rest) {
    const hit = patterns.find(([, re]) => re.test(rest));
    if (!hit) throw new SyntaxError(`unexpected ${rest[0]}`);
    const [type, re] = hit;
    const [match] = re.exec(rest) as RegExpExecArray;
    if (type !== "space") out.push({ type, value: match });
    rest = rest.slice(match.length);
  }
  return out;
}
''', r'''> tokenize("x = 1 + 2").map((t) => t.type)
[ 'ident', 'op', 'number', 'op', 'number' ]'''),
    ("hard", "math", r'''
export function matrixMultiply(a: number[][], b: number[][]): number[][] {
  return a.map((row) =>
    b[0].map((_, j) => row.reduce((sum, value, k) => sum + value * b[k][j], 0))
  );
}
''', r'''> matrixMultiply([[1, 2]], [[3], [4]])
[ [ 11 ] ]'''),
    ("hard", "functional", r'''
export function immer<T extends object>(base: T, recipe: (draft: T) => void): T {
  const changes: Record<string, unknown> = {};
  const draft = new Proxy(base, {
    get: (target, key) => (key in changes ? changes[key as string] : Reflect.get(target, key)),
    set: (_, key, value) => {
      changes[key as string] = value;
      return true;
    },
  }) as T;
  recipe(draft);
  return { ...base, ...(changes as Partial<T>) };
}
''', r'''> immer({ wpm: 0, acc: 100 }, (d) => { d.wpm = 98; })
{ wpm: 98, acc: 100 }'''),
]
