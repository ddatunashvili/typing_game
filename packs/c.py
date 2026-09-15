"""C snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Four-space indentation, K&R
braces, no compiler-specific extensions.
"""
LANGUAGE = "c"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "math", r'''
int add(int a, int b) {
    return a + b;
}
''', r'''add(2, 3) = 5'''),
    ("very-easy", "math", r'''
int is_even(int n) {
    return n % 2 == 0;
}
''', r'''is_even(10) = 1'''),
    ("very-easy", "math", r'''
long square(long n) {
    return n * n;
}
''', r'''square(7) = 49'''),
    ("very-easy", "math", r'''
int max_of(int a, int b) {
    return a > b ? a : b;
}
''', r'''max_of(3, 9) = 9'''),
    ("very-easy", "strings", r'''
void hello(void) {
    printf("hello world");
}
''', r'''hello world'''),
    ("very-easy", "strings", r'''
size_t str_len(const char *s) {
    size_t n = 0;
    while (s[n]) {
        n++;
    }
    return n;
}
''', r'''str_len("hello") = 5'''),
    ("very-easy", "algorithms", r'''
int sum(const int *a, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += a[i];
    }
    return total;
}
''', r'''sum({1, 2, 3, 4}, 4) = 10'''),
    ("very-easy", "algorithms", r'''
int largest(const int *a, int n) {
    int best = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > best) {
            best = a[i];
        }
    }
    return best;
}
''', r'''largest({3, 9, 4}, 3) = 9'''),
    ("very-easy", "algorithms", r'''
void count_up(int n) {
    for (int i = 1; i <= n; i++) {
        printf("%d\n", i);
    }
}
''', r'''count_up(3)
1
2
3'''),
    ("very-easy", "algorithms", r'''
void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}
''', r'''a = 1, b = 2 -> a = 2, b = 1'''),
    ("very-easy", "math", r'''
int abs_of(int n) {
    return n < 0 ? -n : n;
}
''', r'''abs_of(-7) = 7'''),
    ("very-easy", "math", r'''
double average(const int *a, int n) {
    if (n == 0) {
        return 0.0;
    }
    return (double) sum(a, n) / n;
}
''', r'''average({2, 4, 6}, 3) = 4.000000'''),
    ("very-easy", "data-structures", r'''
void fill(int *a, int n, int value) {
    for (int i = 0; i < n; i++) {
        a[i] = value;
    }
}
''', r'''fill(a, 3, 7) -> {7, 7, 7}'''),
    ("very-easy", "data-structures", r'''
int contains(const int *a, int n, int needle) {
    for (int i = 0; i < n; i++) {
        if (a[i] == needle) {
            return 1;
        }
    }
    return 0;
}
''', r'''contains({1, 2, 3}, 3, 2) = 1'''),
    ("very-easy", "oop", r'''
struct Point {
    int x;
    int y;
};

int manhattan(struct Point p) {
    return abs_of(p.x) + abs_of(p.y);
}
''', r'''manhattan((struct Point){3, -4}) = 7'''),
    ("very-easy", "strings", r'''
void to_upper(char *s) {
    for (size_t i = 0; s[i]; i++) {
        s[i] = (char) toupper((unsigned char) s[i]);
    }
}
''', r'''"hello" -> "HELLO"'''),
    ("very-easy", "errors", r'''
int safe_div(int a, int b, int *out) {
    if (b == 0) {
        return -1;
    }
    *out = a / b;
    return 0;
}
''', r'''safe_div(1, 0, &r) = -1'''),
    ("very-easy", "strings", r'''
int is_blank(const char *s) {
    for (size_t i = 0; s[i]; i++) {
        if (!isspace((unsigned char) s[i])) {
            return 0;
        }
    }
    return 1;
}
''', r'''is_blank("   ") = 1'''),
    ("very-easy", "math", r'''
int clamp(int n, int low, int high) {
    if (n < low) {
        return low;
    }
    if (n > high) {
        return high;
    }
    return n;
}
''', r'''clamp(42, 0, 10) = 10'''),
    ("very-easy", "data-structures", r'''
void reverse_array(int *a, int n) {
    for (int i = 0, j = n - 1; i < j; i++, j--) {
        swap(&a[i], &a[j]);
    }
}
''', r'''{1, 2, 3} -> {3, 2, 1}'''),

    # --------------------------------------------------------------------- easy
    ("easy", "algorithms", r'''
void fizzbuzz(int n) {
    for (int i = 1; i <= n; i++) {
        if (i % 15 == 0) {
            printf("FizzBuzz\n");
        } else if (i % 3 == 0) {
            printf("Fizz\n");
        } else if (i % 5 == 0) {
            printf("Buzz\n");
        } else {
            printf("%d\n", i);
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
    for (int i = 0; i < n; i++) {
        long next = a + b;
        a = b;
        b = next;
    }
    return a;
}
''', r'''fib(10) = 55'''),
    ("easy", "algorithms", r'''
long factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
''', r'''factorial(6) = 720'''),
    ("easy", "math", r'''
int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a < 0 ? -a : a;
}
''', r'''gcd(48, 18) = 6'''),
    ("easy", "math", r'''
int is_prime(int n) {
    if (n < 2) {
        return 0;
    }
    for (int d = 2; (long) d * d <= n; d++) {
        if (n % d == 0) {
            return 0;
        }
    }
    return 1;
}
''', r'''is_prime(97) = 1'''),
    ("easy", "math", r'''
unsigned long power(unsigned long base, unsigned exp) {
    unsigned long out = 1;
    while (exp) {
        if (exp & 1u) {
            out *= base;
        }
        base *= base;
        exp >>= 1u;
    }
    return out;
}
''', r'''power(2, 10) = 1024'''),
    ("easy", "strings", r'''
int is_palindrome(const char *s) {
    size_t i = 0;
    size_t j = strlen(s);
    while (j > 0 && i < j) {
        j--;
        while (i < j && !isalnum((unsigned char) s[i])) i++;
        while (i < j && !isalnum((unsigned char) s[j])) j--;
        if (tolower((unsigned char) s[i]) != tolower((unsigned char) s[j])) {
            return 0;
        }
        i++;
    }
    return 1;
}
''', r'''is_palindrome("A man, a plan, a canal: Panama") = 1'''),
    ("easy", "strings", r'''
void str_reverse(char *s) {
    size_t n = strlen(s);
    for (size_t i = 0, j = n - 1; n > 0 && i < j; i++, j--) {
        char t = s[i];
        s[i] = s[j];
        s[j] = t;
    }
}
''', r'''"hello" -> "olleh"'''),
    ("easy", "strings", r'''
int count_char(const char *s, char needle) {
    int n = 0;
    for (size_t i = 0; s[i]; i++) {
        if (s[i] == needle) {
            n++;
        }
    }
    return n;
}
''', r'''count_char("banana", 'a') = 3'''),
    ("easy", "strings", r'''
char *str_dup(const char *s) {
    size_t n = strlen(s) + 1;
    char *copy = malloc(n);
    if (copy == NULL) {
        return NULL;
    }
    memcpy(copy, s, n);
    return copy;
}
''', r'''str_dup("hello") -> a new "hello" you must free()'''),
    ("easy", "data-structures", r'''
void bubble_sort(int *a, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                swap(&a[j], &a[j + 1]);
            }
        }
    }
}
''', r'''{5, 1, 4, 2} -> {1, 2, 4, 5}'''),
    ("easy", "data-structures", r'''
int index_of(const int *a, int n, int needle) {
    for (int i = 0; i < n; i++) {
        if (a[i] == needle) {
            return i;
        }
    }
    return -1;
}
''', r'''index_of({1, 2, 3}, 3, 3) = 2'''),
    ("easy", "data-structures", r'''
int *copy_array(const int *a, int n) {
    int *out = malloc(sizeof(int) * (size_t) n);
    if (out == NULL) {
        return NULL;
    }
    memcpy(out, a, sizeof(int) * (size_t) n);
    return out;
}
''', r'''copy_array(a, 3) -> a fresh array you must free()'''),
    ("easy", "errors", r'''
int read_int(const char *text, int *out) {
    char *end = NULL;
    long value = strtol(text, &end, 10);
    if (end == text || *end != '\0' || value > INT_MAX || value < INT_MIN) {
        return -1;
    }
    *out = (int) value;
    return 0;
}
''', r'''read_int("42x", &n) = -1'''),
    ("easy", "errors", r'''
FILE *open_or_die(const char *path, const char *mode) {
    FILE *fp = fopen(path, mode);
    if (fp == NULL) {
        fprintf(stderr, "cannot open %s: %s\n", path, strerror(errno));
        exit(EXIT_FAILURE);
    }
    return fp;
}
''', r'''open_or_die("missing.txt", "r")
cannot open missing.txt: No such file or directory'''),
    ("easy", "oop", r'''
struct Counter {
    int count;
};

int bump(struct Counter *c, int by) {
    c->count += by;
    return c->count;
}
''', r'''bump(&c, 3) = 3'''),
    ("easy", "devops", r'''
int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <name>\n", argv[0]);
        return 64;
    }
    printf("hello %s\n", argv[1]);
    return 0;
}
''', r'''./greet
usage: ./greet <name>'''),
    ("easy", "data", r'''
int count_lines(const char *path) {
    FILE *fp = fopen(path, "r");
    if (fp == NULL) {
        return -1;
    }
    int lines = 0;
    int c;
    while ((c = fgetc(fp)) != EOF) {
        if (c == '\n') {
            lines++;
        }
    }
    fclose(fp);
    return lines;
}
''', r'''count_lines("names.txt") = 3'''),
    ("easy", "math", r'''
void min_max(const int *a, int n, int *min, int *max) {
    *min = a[0];
    *max = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] < *min) *min = a[i];
        if (a[i] > *max) *max = a[i];
    }
}
''', r'''min_max({3, 9, 1}, 3, &lo, &hi) -> lo = 1, hi = 9'''),
    ("easy", "algorithms", r'''
int binary_search(const int *a, int n, int target) {
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (a[mid] == target) {
            return mid;
        }
        if (a[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}
''', r'''binary_search({1, 3, 5, 7}, 4, 5) = 2'''),

    # ------------------------------------------------------------------- medium
    ("medium", "algorithms", r'''
int *merge(int *a, int n, int *b, int m) {
    int *out = malloc(sizeof(int) * (n + m));
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        out[k++] = a[i] < b[j] ? a[i++] : b[j++];
    }
    while (i < n) out[k++] = a[i++];
    while (j < m) out[k++] = b[j++];
    return out;
}
''', r'''merge({1, 4}, 2, {2, 3, 5}, 3) = {1, 2, 3, 4, 5}'''),
    ("medium", "algorithms", r'''
void insertion_sort(int *a, int n) {
    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
''', r'''{5, 2, 4, 1} -> {1, 2, 4, 5}'''),
    ("medium", "algorithms", r'''
int max_subarray(const int *a, int n) {
    int best = a[0];
    int current = a[0];
    for (int i = 1; i < n; i++) {
        current = a[i] > current + a[i] ? a[i] : current + a[i];
        if (current > best) {
            best = current;
        }
    }
    return best;
}
''', r'''max_subarray({-2, 1, -3, 4, -1, 2, 1}, 7) = 6'''),
    ("medium", "data-structures", r'''
typedef struct Node {
    int value;
    struct Node *next;
} Node;

Node *push(Node *head, int value) {
    Node *node = malloc(sizeof(Node));
    if (node == NULL) {
        return head;
    }
    node->value = value;
    node->next = head;
    return node;
}
''', r'''push(push(NULL, 1), 2) -> 2 -> 1'''),
    ("medium", "data-structures", r'''
void list_free(Node *head) {
    while (head != NULL) {
        Node *next = head->next;
        free(head);
        head = next;
    }
}
''', r'''list_free(head) -> every node released'''),
    ("medium", "data-structures", r'''
Node *list_reverse(Node *head) {
    Node *previous = NULL;
    while (head != NULL) {
        Node *next = head->next;
        head->next = previous;
        previous = head;
        head = next;
    }
    return previous;
}
''', r'''1 -> 2 -> 3  becomes  3 -> 2 -> 1'''),
    ("medium", "data-structures", r'''
typedef struct {
    int *items;
    size_t len;
    size_t cap;
} Vec;

int vec_push(Vec *v, int value) {
    if (v->len == v->cap) {
        size_t cap = v->cap ? v->cap * 2 : 4;
        int *items = realloc(v->items, cap * sizeof(int));
        if (items == NULL) {
            return -1;
        }
        v->items = items;
        v->cap = cap;
    }
    v->items[v->len++] = value;
    return 0;
}
''', r'''vec_push grows the buffer when it is full'''),
    ("medium", "strings", r'''
char *str_join(const char **parts, int n, const char *sep) {
    size_t total = 1;
    for (int i = 0; i < n; i++) {
        total += strlen(parts[i]) + (i ? strlen(sep) : 0);
    }
    char *out = malloc(total);
    if (out == NULL) {
        return NULL;
    }
    out[0] = '\0';
    for (int i = 0; i < n; i++) {
        if (i) strcat(out, sep);
        strcat(out, parts[i]);
    }
    return out;
}
''', r'''str_join({"a", "b", "c"}, 3, ", ") = "a, b, c"'''),
    ("medium", "strings", r'''
int split(char *text, char sep, char **out, int max) {
    int n = 0;
    char *cursor = text;
    out[n++] = cursor;
    while (*cursor && n < max) {
        if (*cursor == sep) {
            *cursor = '\0';
            out[n++] = cursor + 1;
        }
        cursor++;
    }
    return n;
}
''', r'''split("a,b,c", ',', parts, 8) = 3'''),
    ("medium", "strings", r'''
void trim(char *s) {
    char *start = s;
    while (*start && isspace((unsigned char) *start)) start++;

    size_t len = strlen(start);
    while (len > 0 && isspace((unsigned char) start[len - 1])) len--;

    memmove(s, start, len);
    s[len] = '\0';
}
''', r'''"  hello  " -> "hello"'''),
    ("medium", "errors", r'''
int read_file(const char *path, char **out, size_t *len) {
    FILE *fp = fopen(path, "rb");
    if (fp == NULL) {
        return -1;
    }
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    rewind(fp);

    char *buf = malloc((size_t) size + 1);
    if (buf == NULL) {
        fclose(fp);
        return -1;
    }
    if (fread(buf, 1, (size_t) size, fp) != (size_t) size) {
        free(buf);
        fclose(fp);
        return -1;
    }
    buf[size] = '\0';
    fclose(fp);
    *out = buf;
    *len = (size_t) size;
    return 0;
}
''', r'''read_file("notes.txt", &text, &n) = 0'''),
    ("medium", "math", r'''
double mean(const double *a, int n) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        total += a[i];
    }
    return n ? total / n : 0.0;
}

double stddev(const double *a, int n) {
    double m = mean(a, n);
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += (a[i] - m) * (a[i] - m);
    }
    return n > 1 ? sqrt(sum / (n - 1)) : 0.0;
}
''', r'''stddev({2, 4, 4, 4, 5, 5, 7, 9}, 8) = 2.138090'''),
    ("medium", "math", r'''
int count_bits(unsigned long value) {
    int n = 0;
    while (value) {
        value &= value - 1;
        n++;
    }
    return n;
}
''', r'''count_bits(255) = 8'''),
    ("medium", "oop", r'''
typedef struct {
    void *state;
    int (*read)(void *state, char *buf, int n);
    void (*close)(void *state);
} Reader;

int read_all(Reader *r, char *buf, int n) {
    int total = 0;
    int got;
    while (total < n && (got = r->read(r->state, buf + total, n - total)) > 0) {
        total += got;
    }
    return total;
}
''', r'''read_all(&reader, buf, 1024) = bytes actually read'''),
    ("medium", "devops", r'''
int main(int argc, char **argv) {
    int verbose = 0;
    int opt;
    while ((opt = getopt(argc, argv, "v")) != -1) {
        switch (opt) {
        case 'v':
            verbose = 1;
            break;
        default:
            fprintf(stderr, "usage: %s [-v]\n", argv[0]);
            return 64;
        }
    }
    if (verbose) {
        printf("verbose mode\n");
    }
    return 0;
}
''', r'''./tool -v
verbose mode'''),
    ("medium", "data", r'''
int write_csv(const char *path, const char **names, const int *scores, int n) {
    FILE *fp = fopen(path, "w");
    if (fp == NULL) {
        return -1;
    }
    fprintf(fp, "name,score\n");
    for (int i = 0; i < n; i++) {
        fprintf(fp, "%s,%d\n", names[i], scores[i]);
    }
    return fclose(fp);
}
''', r'''write_csv("out.csv", names, scores, 2) = 0'''),
    ("medium", "algorithms", r'''
void rotate(int *a, int n, int by) {
    by = ((by % n) + n) % n;
    reverse_array(a, n);
    reverse_array(a, by);
    reverse_array(a + by, n - by);
}
''', r'''{1, 2, 3, 4, 5} rotate 2 -> {4, 5, 1, 2, 3}'''),
    ("medium", "functional", r'''
void for_each(int *a, int n, void (*fn)(int *)) {
    for (int i = 0; i < n; i++) {
        fn(&a[i]);
    }
}

int reduce(const int *a, int n, int initial, int (*fn)(int, int)) {
    int acc = initial;
    for (int i = 0; i < n; i++) {
        acc = fn(acc, a[i]);
    }
    return acc;
}
''', r'''reduce({1, 2, 3}, 3, 0, add) = 6'''),
    ("medium", "data-structures", r'''
typedef struct {
    int items[64];
    int top;
} Stack;

int stack_push(Stack *s, int value) {
    if (s->top >= 64) {
        return -1;
    }
    s->items[s->top++] = value;
    return 0;
}

int stack_pop(Stack *s, int *out) {
    if (s->top == 0) {
        return -1;
    }
    *out = s->items[--s->top];
    return 0;
}
''', r'''push 1, push 2, pop -> 2'''),

    ("medium", "algorithms", r"""
int partition_index(int *a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; j++) {
        if (a[j] <= pivot) {
            i++;
            swap(&a[i], &a[j]);
        }
    }
    swap(&a[i + 1], &a[hi]);
    return i + 1;
}
""", r"""partition_index(a, 0, 4) places the pivot and returns its index"""),
    ("medium", "strings", r"""
int starts_with(const char *text, const char *prefix) {
    while (*prefix) {
        if (*text++ != *prefix++) {
            return 0;
        }
    }
    return 1;
}
""", r"""starts_with("coderace", "code") = 1"""),

    # --------------------------------------------------------------------- hard
    ("hard", "algorithms", r'''
void quicksort(int *a, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = a[(lo + hi) / 2];
    int i = lo, j = hi;
    while (i <= j) {
        while (a[i] < pivot) i++;
        while (a[j] > pivot) j--;
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
''', r'''{3, 6, 1, 8, 2} -> {1, 2, 3, 6, 8}'''),
    ("hard", "algorithms", r'''
static void sift_down(int *a, int n, int root) {
    while (1) {
        int largest = root;
        int left = 2 * root + 1;
        int right = left + 1;
        if (left < n && a[left] > a[largest]) largest = left;
        if (right < n && a[right] > a[largest]) largest = right;
        if (largest == root) return;
        swap(&a[root], &a[largest]);
        root = largest;
    }
}

void heapsort(int *a, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) sift_down(a, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(&a[0], &a[i]);
        sift_down(a, i, 0);
    }
}
''', r'''{5, 3, 8, 1} -> {1, 3, 5, 8}'''),
    ("hard", "algorithms", r'''
int levenshtein(const char *a, const char *b) {
    size_t la = strlen(a), lb = strlen(b);
    int *previous = malloc((lb + 1) * sizeof(int));
    int *current = malloc((lb + 1) * sizeof(int));
    for (size_t j = 0; j <= lb; j++) previous[j] = (int) j;

    for (size_t i = 1; i <= la; i++) {
        current[0] = (int) i;
        for (size_t j = 1; j <= lb; j++) {
            int cost = a[i - 1] == b[j - 1] ? 0 : 1;
            int best = previous[j] + 1;
            if (current[j - 1] + 1 < best) best = current[j - 1] + 1;
            if (previous[j - 1] + cost < best) best = previous[j - 1] + cost;
            current[j] = best;
        }
        int *t = previous;
        previous = current;
        current = t;
    }
    int out = previous[lb];
    free(previous);
    free(current);
    return out;
}
''', r'''levenshtein("kitten", "sitting") = 3'''),
    ("hard", "data-structures", r'''
#define BUCKETS 256

typedef struct Entry {
    char *key;
    int value;
    struct Entry *next;
} Entry;

static unsigned long hash(const char *key) {
    unsigned long h = 5381;
    for (const unsigned char *p = (const unsigned char *) key; *p; p++) {
        h = ((h << 5) + h) + *p;
    }
    return h;
}

int map_put(Entry **table, const char *key, int value) {
    unsigned long index = hash(key) % BUCKETS;
    for (Entry *e = table[index]; e; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            e->value = value;
            return 0;
        }
    }
    Entry *entry = malloc(sizeof(Entry));
    if (entry == NULL) return -1;
    entry->key = str_dup(key);
    entry->value = value;
    entry->next = table[index];
    table[index] = entry;
    return 0;
}
''', r'''map_put(table, "wpm", 98) = 0'''),
    ("hard", "data-structures", r'''
typedef struct {
    int *items;
    size_t cap;
    size_t head;
    size_t len;
} Ring;

int ring_push(Ring *r, int value) {
    if (r->len == r->cap) {
        r->items[r->head] = value;
        r->head = (r->head + 1) % r->cap;
        return 1;
    }
    r->items[(r->head + r->len) % r->cap] = value;
    r->len++;
    return 0;
}
''', r'''pushing into a full ring returns 1 and drops the oldest value'''),
    ("hard", "data-structures", r'''
typedef struct TreeNode {
    int value;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

TreeNode *tree_insert(TreeNode *root, int value) {
    if (root == NULL) {
        TreeNode *node = calloc(1, sizeof(TreeNode));
        if (node) node->value = value;
        return node;
    }
    if (value < root->value) {
        root->left = tree_insert(root->left, value);
    } else if (value > root->value) {
        root->right = tree_insert(root->right, value);
    }
    return root;
}

void in_order(const TreeNode *node) {
    if (node == NULL) return;
    in_order(node->left);
    printf("%d ", node->value);
    in_order(node->right);
}
''', r'''insert 5, 3, 8 then in_order prints: 3 5 8'''),
    ("hard", "strings", r'''
char *replace_all(const char *text, const char *from, const char *to) {
    size_t from_len = strlen(from);
    if (from_len == 0) return str_dup(text);

    size_t count = 0;
    for (const char *p = text; (p = strstr(p, from)); p += from_len) count++;

    size_t out_len = strlen(text) + count * (strlen(to) - from_len) + 1;
    char *out = malloc(out_len);
    if (out == NULL) return NULL;

    char *cursor = out;
    while (1) {
        const char *hit = strstr(text, from);
        if (hit == NULL) {
            strcpy(cursor, text);
            return out;
        }
        size_t prefix = (size_t) (hit - text);
        memcpy(cursor, text, prefix);
        cursor += prefix;
        strcpy(cursor, to);
        cursor += strlen(to);
        text = hit + from_len;
    }
}
''', r'''replace_all("a-b-c", "-", "+") = "a+b+c"'''),
    ("hard", "strings", r'''
int wildcard_match(const char *pattern, const char *text) {
    const char *star = NULL;
    const char *mark = text;
    while (*text) {
        if (*pattern == '?' || *pattern == *text) {
            pattern++;
            text++;
        } else if (*pattern == '*') {
            star = pattern++;
            mark = text;
        } else if (star) {
            pattern = star + 1;
            text = ++mark;
        } else {
            return 0;
        }
    }
    while (*pattern == '*') pattern++;
    return *pattern == '\0';
}
''', r'''wildcard_match("a*c", "abbbc") = 1'''),
    ("hard", "math", r'''
void mat_multiply(const double *a, const double *b, double *out,
                  int rows, int inner, int cols) {
    for (int i = 0; i < rows * cols; i++) {
        out[i] = 0.0;
    }
    for (int i = 0; i < rows; i++) {
        for (int k = 0; k < inner; k++) {
            double value = a[i * inner + k];
            if (value == 0.0) continue;
            for (int j = 0; j < cols; j++) {
                out[i * cols + j] += value * b[k * cols + j];
            }
        }
    }
}
''', r'''[[1, 2]] x [[3], [4]] = [[11]]'''),
    ("hard", "math", r'''
unsigned long long mod_pow(unsigned long long base,
                           unsigned long long exp,
                           unsigned long long mod) {
    unsigned long long out = 1;
    base %= mod;
    while (exp) {
        if (exp & 1ull) {
            out = (out * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1ull;
    }
    return out;
}
''', r'''mod_pow(2, 10, 1000) = 24'''),
    ("hard", "errors", r'''
typedef enum {
    OK = 0,
    ERR_IO,
    ERR_PARSE,
    ERR_RANGE
} Status;

const char *status_text(Status status) {
    switch (status) {
    case OK:        return "ok";
    case ERR_IO:    return "io error";
    case ERR_PARSE: return "parse error";
    case ERR_RANGE: return "out of range";
    default:        return "unknown";
    }
}
''', r'''status_text(ERR_PARSE) = "parse error"'''),
    ("hard", "errors", r'''
int parse_port(const char *text, unsigned short *out) {
    errno = 0;
    char *end = NULL;
    long value = strtol(text, &end, 10);
    if (errno == ERANGE) {
        return ERR_RANGE;
    }
    if (end == text || *end != '\0') {
        return ERR_PARSE;
    }
    if (value < 1024 || value > 65535) {
        return ERR_RANGE;
    }
    *out = (unsigned short) value;
    return OK;
}
''', r'''parse_port("80", &p) = ERR_RANGE'''),
    ("hard", "devops", r'''
int run(const char *path, char *const argv[]) {
    pid_t pid = fork();
    if (pid < 0) {
        return -1;
    }
    if (pid == 0) {
        execv(path, argv);
        _exit(127);
    }
    int status = 0;
    if (waitpid(pid, &status, 0) < 0) {
        return -1;
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
}
''', r'''run("/bin/true", argv) = 0'''),
    ("hard", "devops", r'''
static volatile sig_atomic_t stopping = 0;

static void on_signal(int signum) {
    (void) signum;
    stopping = 1;
}

int serve(void) {
    struct sigaction action = {0};
    action.sa_handler = on_signal;
    sigaction(SIGINT, &action, NULL);
    sigaction(SIGTERM, &action, NULL);

    while (!stopping) {
        handle_one();
    }
    printf("shutting down\n");
    return 0;
}
''', r'''^C
shutting down'''),
    ("hard", "async", r'''
typedef struct {
    pthread_mutex_t lock;
    pthread_cond_t ready;
    int items[16];
    int count;
} Queue;

void queue_push(Queue *q, int value) {
    pthread_mutex_lock(&q->lock);
    while (q->count == 16) {
        pthread_cond_wait(&q->ready, &q->lock);
    }
    q->items[q->count++] = value;
    pthread_cond_signal(&q->ready);
    pthread_mutex_unlock(&q->lock);
}
''', r'''producers block while the queue is full'''),
    ("hard", "async", r'''
typedef struct {
    int start;
    int end;
    long total;
} Chunk;

static void *worker(void *arg) {
    Chunk *chunk = arg;
    chunk->total = 0;
    for (int i = chunk->start; i < chunk->end; i++) {
        chunk->total += i;
    }
    return NULL;
}

long parallel_sum(int n, int threads) {
    pthread_t ids[8];
    Chunk chunks[8];
    int step = n / threads;
    for (int t = 0; t < threads; t++) {
        chunks[t].start = t * step;
        chunks[t].end = (t == threads - 1) ? n : (t + 1) * step;
        pthread_create(&ids[t], NULL, worker, &chunks[t]);
    }
    long total = 0;
    for (int t = 0; t < threads; t++) {
        pthread_join(ids[t], NULL);
        total += chunks[t].total;
    }
    return total;
}
''', r'''parallel_sum(1000, 4) = 499500'''),
    ("hard", "data", r'''
int save_records(const char *path, const Record *records, size_t n) {
    FILE *fp = fopen(path, "wb");
    if (fp == NULL) {
        return -1;
    }
    unsigned long magic = 0x43524143ul;
    if (fwrite(&magic, sizeof(magic), 1, fp) != 1 ||
        fwrite(&n, sizeof(n), 1, fp) != 1 ||
        fwrite(records, sizeof(Record), n, fp) != n) {
        fclose(fp);
        return -1;
    }
    return fclose(fp);
}
''', r'''save_records("races.bin", records, 500) = 0'''),
    ("hard", "web", r'''
int listen_on(unsigned short port) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) {
        return -1;
    }
    int yes = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));

    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(port);

    if (bind(fd, (struct sockaddr *) &addr, sizeof(addr)) < 0 ||
        listen(fd, 64) < 0) {
        close(fd);
        return -1;
    }
    return fd;
}
''', r'''listen_on(25616) = 3   (a listening socket)'''),
    ("hard", "functional", r'''
typedef int (*Compare)(const void *, const void *);

static int by_int(const void *a, const void *b) {
    int left = *(const int *) a;
    int right = *(const int *) b;
    return (left > right) - (left < right);
}

void sort_ints(int *a, size_t n) {
    qsort(a, n, sizeof(int), (Compare) by_int);
}
''', r'''{5, 1, 4} -> {1, 4, 5}'''),
    ("hard", "oop", r'''
typedef struct Shape Shape;

typedef struct {
    double (*area)(const Shape *);
    void (*describe)(const Shape *);
} ShapeVTable;

struct Shape {
    const ShapeVTable *vtable;
};

double area_of(const Shape *shape) {
    return shape->vtable->area(shape);
}
''', r'''area_of((Shape *) &rect) = 12.000000'''),
]
