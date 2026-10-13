# DECISIONS.md

## 1. Indexes

**Created Indexes:**

- **`employees.emp_code` (unique)**: Ensures uniqueness for the business identifier and speeds up lookups in punch operations and analytics joins. Used in every attendance operation.

- **`employees.department + emp_code`**: Compound index for filtering employees by department (list endpoint) with emp_code for sort order. Also helps department analytics.

- **`employees.joined_on`**: Supports department summary filtering for headcount (R9: employees joined by end of period).

- **`attendance_logs.emp_code + date` (unique)**: Ensures one record per employee per day (prevents punch-in races). Primary lookup pattern for attendance operations.

- **`attendance_logs.date + emp_code`**: Supports date range queries in list endpoint and analytics, with emp_code as secondary sort.

- **`attendance_logs.status + date`**: Helps status filtering in list endpoint.

- **`attendance_logs.emp_code + date + status`**: Compound index covering the common filter pattern (employee + date range + status filter).

- **`attendance_logs.date + status`**: Supports monthly analytics filtering by date range and presence status.

**Considered and Rejected:**

- **Index on `late_minutes`**: Rejected because the leaderboard aggregates (sums) late minutes first, then sorts. An index on the raw field wouldn't help the aggregation, and the dataset size (100k docs) is manageable without it.

## 2. Punch-in Race

When two identical punch-in requests arrive simultaneously:

1. Both calculate the attendance date and create the same document structure with `emp_code` and `date`.
2. Both call `insert_one()` on the attendance collection.
3. The unique index on `(emp_code, date)` serializes the inserts at the database level.
4. The first insert succeeds and returns the document.
5. The second insert raises `DuplicateKeyError` exception.
6. My code catches this exception and returns HTTP 409 with a clear message.
7. Result: Exactly one 201 response, all others get 409 as required.

This relies on MongoDB's unique index enforcement rather than application-level locking, making it race-safe and performant.

## 3. Ties

My leaderboard uses MongoDB's `$rank` window function. For two employees tied at the cutoff:

- Both employees at rank N receive rank N in the output.
- The next employee receives rank N+2 (standard competition ranking: 1, 2, 2, 4).
- The `$match` filter `{"rank": {"$lte": limit}}` is applied after ranking, so both tied employees are included if their shared rank is ≤ limit.
- Within ties, rows are ordered by `emp_code` (ascending) as required.

Example: limit=2, three employees with [100, 90, 90] late minutes → all three returned with ranks [1, 2, 2].

## 4. Headcount

The department summary starts the aggregation pipeline from the `employees` collection (not attendance_logs):

1. `$match` filters employees by `joined_on <= end_date` (R9).
2. `$lookup` joins attendance records with `preserveNullAndEmptyArrays: true`, keeping employees with zero logs.
3. `$unwind` expands the attendance array but preserves null entries.
4. `$group` by department uses `$addToSet` on `emp_code` to count unique employees (headcount), regardless of log count.

This ensures an employee who joined but never punched in is still counted in headcount, while present_days, late_minutes, etc., correctly show zero.

## 5. One Thing to Change for 100x Data

**Sharding on `attendance_logs` by `(emp_code, date)`**:

At 10 million records, queries spanning many employees (department summary, trend) would bottleneck on a single server. Sharding by `(emp_code, date)` distributes data across shards while keeping each employee's records co-located for efficient monthly summaries. Range queries by date alone would scatter-gather, but the join from employees (which filters by department) would target relevant shards. I'd also add read replicas for analytics queries to offload the primary, and consider pre-aggregating monthly summaries into a separate collection updated incrementally to avoid recalculating from raw logs.
