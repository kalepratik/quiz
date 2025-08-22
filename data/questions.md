# dbt Certification Questions

# Question 1
**Topic:** DAG Execution  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+   +---------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   | ->| tests   |
+---------------+   +------------------+   +-------------+   +------------------+   +---------+
```

You run the following command:
`dbt build --select B_customer_dim`

**Question:**
What will happen?

**Options:**
A. seed_customers → A_stg_customers → S_customers → B_customer_dim → tests
B. seed_customers → B_customer_dim → tests
C. A_stg_customers → S_customers → B_customer_dim → tests
D. seed_customers → A_stg_customers → B_customer_dim → tests
E. Only B_customer_dim runs

**Correct Answer:** A

**Explanation:**  
When selecting a specific model dbt builds the entire upstream dependency chain including seeds
models and snapshots then runs tests on the selected model.

---

# Question 2
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --full-refresh`

**Question:**
What will happen?

**Options:**
A. All models are rebuilt from scratch
B. Only incremental models are forced to rebuild from scratch
C. Only snapshots are rebuilt
D. Only seeds are reloaded
E. Only tests are rerun

**Correct Answer:** B

**Explanation:**  
The --full-refresh flag only forces incremental models to rebuild from scratch; seeds snapshots and
regular models run normally.

---

# Question 3
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run `dbt build --select state:modified+ --state prod_artifacts/ --defer`. If only `A_stg_customers` changed, what runs?

**Question:**
What will happen?

**Options:**
A. Only A_stg_customers runs
B. A_stg_customers → S_customers → B_customer_dim run
C. A_stg_customers and B_customer_dim run
D. Only B_customer_dim runs
E. Nothing runs

**Correct Answer:** B

**Explanation:**  
With state:modified+ and defer the modified model and all its downstream dependencies run while
upstream models use production versions.

---

# Question 4
**Topic:** CI/CD  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:
```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select state:modified+ --state prod_artifacts/ --defer`

If only `B_customer_dim` changed, what happens?

**Question:**
What will happen?

**Options:**
A. Only `B_customer_dim` runs
B. `A_stg_customers` → `S_customers` → `B_customer_dim` run
C. All models run
D. Only tests run
E. Nothing runs

**Correct Answer:** A

**Explanation:**  
When only a downstream model changes and `--defer` is used, upstream models resolve to production versions and only the changed model builds.

---

# Question 5
**Topic:** Dependencies  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

If `S_customers` fails during `dbt build`, what happens to `B_customer_dim`?

**Question:**
What will happen?

**Options:**
A. B_customer_dim runs normally
B. B_customer_dim is skipped
C. B_customer_dim runs with production data
D. B_customer_dim runs with empty data
E. B_customer_dim is deleted

**Correct Answer:** B

**Explanation:**  
When a dependency fails dbt stops building nodes that depend on it so B_customer_dim won't run if
S_customers fails.

---

# Question 6
**Topic:** Snapshots  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:
`dbt build --full-refresh`

You run the following command:
`snapshots`

**Question:**
What will happen?

**Options:**
A. Snapshots are forced to rebuild from scratch
B. Snapshots ignore --full-refresh and run normally
C. Snapshots are deleted and recreated
D. Snapshots are skipped entirely
E. Snapshots run in parallel

**Correct Answer:** B

**Explanation:**  
Snapshots ignore --full-refresh and run normally comparing current data vs historical snapshot
table.

---

# Question 7
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
In a DAG with incremental models what does --full-refresh do?

**Question:**
What will happen?

**Options:**
A. Forces all models to rebuild from scratch
B. Forces only incremental models to rebuild from scratch
C. Forces only seeds to reload
D. Forces only tests to rerun
E. Forces only snapshots to rebuild

**Correct Answer:** B

**Explanation:**  
The --full-refresh flag specifically forces incremental models to rebuild from scratch ignoring
their incremental logic.

---

# Question 8
**Topic:** DAG Execution  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have a DAG with multiple models and snapshots. When you run plain dbt build what is
the execution order?

**Question:**
What will happen?

**Options:**
A. Seeds → Models → Snapshots → Tests
B. Seeds → Models and Snapshots mixed → Tests
C. Seeds → Snapshots → Models → Tests
D. Models → Snapshots → Seeds → Tests
E. Random order

**Correct Answer:** B

**Explanation:**  
Seeds run first then models and snapshots are mixed based on dependencies not by type then tests run
last.

---

# Question 9
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the primary purpose of the --defer flag in dbt?

**Question:**
What will happen?

**Options:**
A. To delay model execution
B. To use production models for references instead of building locally
C. To skip model dependencies
D. To run models in parallel
E. To stop execution

**Correct Answer:** B

**Explanation:**  
The --defer flag uses production models for references instead of building them locally useful for
CI/CD scenarios.

---

# Question 10
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select B_customer_dim --defer --state prod_artifacts/`

**Question:**
What will happen?

**Options:**
A. Only B_customer_dim runs using prod versions of dependencies
B. All models run locally
C. Only seeds run
D. Only tests run
E. Nothing runs

**Correct Answer:** A

**Explanation:**  
With --select and --defer only the selected model runs using production versions of its
dependencies.

---

# Question 11
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens when you run dbt build --fail-fast and a model fails?

**Question:**
What will happen?

**Options:**
A. dbt continues with other models
B. dbt aborts immediately on first failure
C. dbt retries the failed model
D. dbt skips the failed model
E. dbt uses production version

**Correct Answer:** B

**Explanation:**  
The --fail-fast flag stops execution immediately when the first failure occurs providing quick
feedback.

---

# Question 12
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have a DAG with incremental models. When you run dbt build --full-refresh what happens
to the incremental logic?

**Question:**
What will happen?

**Options:**
A. Incremental logic is ignored and models rebuild completely
B. Incremental logic is enhanced
C. Incremental logic runs normally
D. Incremental logic is disabled permanently
E. Incremental logic is optimized

**Correct Answer:** A

**Explanation:**  
The --full-refresh flag forces incremental models to ignore their incremental logic and rebuild
completely from scratch.

---

# Question 13
**Topic:** DAG Execution  
**Difficulty:** 1 (Easy)

**Scenario:**
What is the execution order when running plain dbt build?

**Question:**
What will happen?

**Options:**
A. Seeds → Models → Snapshots → Tests
B. Seeds → Models and Snapshots mixed → Tests
C. Models → Seeds → Snapshots → Tests
D. Tests → Models → Seeds → Snapshots
E. Random order

**Correct Answer:** B

**Explanation:**  
The standard execution order is: seeds first then models and snapshots mixed based on dependencies
then tests last.

---

# Question 14
**Topic:** Dependencies  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

If `A_stg_customers` fails, what happens to downstream models?

**Question:**
What will happen?

**Options:**
A. S_customers and B_customer_dim run normally
B. S_customers and B_customer_dim are skipped
C. S_customers runs but B_customer_dim is skipped
D. Only B_customer_dim runs
E. All models run

**Correct Answer:** B

**Explanation:**  
When a model fails all its downstream dependencies are skipped because they cannot be built without
the failed dependency.

---

# Question 15
**Topic:** State Management  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the purpose of the --state flag in dbt?

**Question:**
What will happen?

**Options:**
A. To specify the target environment
B. To specify which state artifacts to use for comparison
C. To specify the database state
D. To specify the model state
E. To specify the test state

**Correct Answer:** B

**Explanation:**  
The --state flag specifies which state artifacts to use for comparison enabling features like
state:modified+ selectors.

---

# Question 16
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have incremental models in your DAG. What happens when you run dbt build
--full-refresh?

**Question:**
What will happen?

**Options:**
A. All models rebuild from scratch
B. Only incremental models rebuild from scratch
C. Only regular models rebuild
D. Only snapshots rebuild
E. Only seeds reload

**Correct Answer:** B

**Explanation:**  
The --full-refresh flag specifically targets incremental models forcing them to rebuild completely
while other resource types run normally.

---

# Question 17
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
What is the difference between --state and --defer flags?

**Question:**
What will happen?

**Options:**
A. They are the same thing
B. --state specifies which state to use --defer uses production
C. --defer specifies which state to use --state uses production
D. They cannot be used together
E. They are deprecated

**Correct Answer:** B

**Explanation:**  
--state specifies which state artifacts to use for comparison while --defer uses production models
for references.

---

# Question 18
**Topic:** CI/CD  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select state:modified+ --defer`

**Question:**
What will happen?

**Options:**
A. Only B_customer_dim runs
B. A_stg_customers → S_customers → B_customer_dim run
C. All models run
D. Only tests run
E. Nothing runs

**Correct Answer:** A

**Explanation:**  
When only a downstream model is modified and defer is used upstream models use production versions
and only the changed model builds.

---

# Question 19
**Topic:** Snapshots  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens to snapshot history when you run dbt build --full-refresh?

**Question:**
What will happen?

**Options:**
A. Snapshot history is wiped
B. Snapshot history is preserved and snapshots re-evaluate changes
C. Snapshot history is backed up
D. Snapshot history is ignored
E. Snapshot history is deleted

**Correct Answer:** B

**Explanation:**  
Snapshots ignore --full-refresh and preserve their history only re-evaluating changes in the source
data.

---

# Question 20
**Topic:** DAG Execution  
**Difficulty:** 1 (Easy)

**Scenario:**
Scenario: You have a complex DAG with multiple dependencies. When you run dbt build without
selectors what determines the execution order?

**Question:**
What will happen?

**Options:**
A. Random order
B. Alphabetical order
C. File modification time
D. Dependency relationships
E. File size

**Correct Answer:** D

**Explanation:**  
The execution order is determined by dependency relationships ensuring that dependencies are built
before the models that depend on them.

---

# Question 21
**Topic:** State Management  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the purpose of the state:modified+ selector?

**Question:**
What will happen?

**Options:**
A. To select only modified resources
B. To select modified resources and all downstream dependencies
C. To select only new resources
D. To select all resources
E. To select only deleted resources

**Correct Answer:** B

**Explanation:**  
The state:modified+ selector includes modified resources and all their downstream dependencies
ensuring the entire affected subgraph is rebuilt.

---

# Question 22
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select B_customer_dim --defer`

**Question:**
What will happen?

**Options:**
A. A_stg_customers runs locally
B. A_stg_customers uses production version
C. A_stg_customers is skipped
D. A_stg_customers runs in parallel
E. A_stg_customers is deleted

**Correct Answer:** B

**Explanation:**  
With --defer and --select upstream dependencies like A_stg_customers use production versions instead
of building locally.

---

# Question 23
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens when you run dbt build --fail-fast and multiple models could fail?

**Question:**
What will happen?

**Options:**
A. dbt stops on the first failure
B. dbt continues and reports all failures
C. dbt retries failed models
D. dbt skips failed models
E. dbt uses production versions

**Correct Answer:** A

**Explanation:**  
The --fail-fast flag stops execution immediately on the first failure providing quick feedback but
potentially missing other issues.

---

# Question 24
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have incremental models with unique_key and on_schema_change configuration. What
happens when you run dbt build --full-refresh?

**Question:**
What will happen?

**Options:**
A. The incremental logic is ignored and models rebuild completely
B. The incremental logic is enhanced with full refresh
C. The incremental logic runs normally
D. The incremental logic is optimized
E. The incremental logic is disabled

**Correct Answer:** A

**Explanation:**  
The --full-refresh flag forces incremental models to ignore their incremental logic including
unique_key and on_schema_change configurations.

---

# Question 25
**Topic:** Testing  
**Difficulty:** 1 (Easy)

**Scenario:**
What is the execution order for tests in dbt build?

**Question:**
What will happen?

**Options:**
A. Tests run before models
B. Tests run after their target models exist
C. Tests run in parallel with models
D. Tests run randomly
E. Tests run only if models succeed

**Correct Answer:** B

**Explanation:**  
Tests run after their target models exist ensuring that the models they test have been built
successfully.

---

# Question 26
**Topic:** Snapshots  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

If `S_customers` is a snapshot, what happens when `A_stg_customers` changes?

**Question:**
What will happen?

**Options:**
A. S_customers detects changes and updates history
B. S_customers ignores changes
C. S_customers fails
D. S_customers is deleted
E. S_customers runs in parallel

**Correct Answer:** A

**Explanation:**  
When a snapshot's source model changes the snapshot detects differences and updates its historical
tracking accordingly.

---

# Question 27
**Topic:** CI/CD  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the purpose of the --defer flag in CI/CD scenarios?

**Question:**
What will happen?

**Options:**
A. To speed up execution
B. To use production models for references instead of building locally
C. To skip model dependencies
D. To run models in parallel
E. To stop execution

**Correct Answer:** B

**Explanation:**  
In CI/CD the --defer flag uses production models for references instead of building them locally
saving time and resources.

---

# Question 28
**Topic:** DAG Execution  
**Difficulty:** 1 (Easy)

**Scenario:**
Scenario: You have a DAG with multiple seeds models and snapshots. When you run dbt build what runs
first?

**Question:**
What will happen?

**Options:**
A. Models run first
B. Seeds run first
C. Snapshots run first
D. Tests run first
E. Random order

**Correct Answer:** B

**Explanation:**  
Seeds always run first in dbt build regardless of the DAG structure or dependencies.

---

# Question 29
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens to incremental models when you run dbt build --full-refresh?

**Question:**
What will happen?

**Options:**
A. They ignore incremental logic and rebuild completely
B. They use enhanced incremental logic
C. They run normally
D. They are skipped
E. They are deleted

**Correct Answer:** A

**Explanation:**  
The --full-refresh flag forces incremental models to ignore their incremental logic and rebuild
completely from scratch.

---

# Question 30
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select state:modified+ --defer --state prod_artifacts/`

**Question:**
What will happen?

**Options:**
A. Only A_stg_customers runs
B. A_stg_customers → S_customers → B_customer_dim run
C. All models run
D. Only tests run
E. Nothing runs

**Correct Answer:** B

**Explanation:**  
With state:modified+ the modified model and all its downstream dependencies run while upstream
models use production versions via defer.

---

# Question 31
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the difference between running dbt build and dbt build --full-refresh?

**Question:**
What will happen?

**Options:**
A. No difference
B. --full-refresh forces incremental models to rebuild completely
C. --full-refresh skips all models
D. --full-refresh only runs tests
E. --full-refresh only runs seeds

**Correct Answer:** B

**Explanation:**  
The --full-refresh flag specifically forces incremental models to rebuild completely while other
resource types run normally.

---

# Question 32
**Topic:** DAG Execution  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have a DAG with multiple models and snapshots. When you run dbt build without
selectors what determines the order of models and snapshots?

**Question:**
What will happen?

**Options:**
A. They run in alphabetical order
B. They run based on dependency relationships
C. They run in random order
D. They run based on file size
E. They run based on modification time

**Correct Answer:** B

**Explanation:**  
Models and snapshots run based on dependency relationships not by type ensuring dependencies are
built before dependent models.

---

# Question 33
**Topic:** CI/CD  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the purpose of the --defer flag in Slim CI?

**Question:**
What will happen?

**Options:**
A. To speed up CI execution
B. To use production models for references instead of building locally
C. To skip model dependencies
D. To run models in parallel
E. To stop execution

**Correct Answer:** B

**Explanation:**  
In Slim CI the --defer flag uses production models for references instead of building them locally
saving CI time and resources.

---

# Question 34
**Topic:** Snapshots  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

If `S_customers` is a snapshot, what happens when you run `dbt build --full-refresh`?

**Question:**
What will happen?

**Options:**
A. S_customers rebuilds completely
B. S_customers ignores --full-refresh and runs normally
C. S_customers is skipped
D. S_customers runs in parallel
E. S_customers is deleted

**Correct Answer:** B

**Explanation:**  
Snapshots ignore the --full-refresh flag and run normally comparing current data vs historical
snapshot table.

---

# Question 35
**Topic:** State Management  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens when you run dbt build --select state:modified+ --defer and no models are modified?

**Question:**
What will happen?

**Options:**
A. Nothing runs
B. All models run
C. Only seeds run
D. Only tests run
E. Only snapshots run

**Correct Answer:** A

**Explanation:**  
When no models are modified the state:modified+ selector returns an empty set so nothing runs.

---

# Question 36
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have incremental models with on_schema_change configuration. What happens when you run
dbt build --full-refresh?

**Question:**
What will happen?

**Options:**
A. The on_schema_change logic is ignored and models rebuild completely
B. The on_schema_change logic is enhanced
C. The on_schema_change logic runs normally
D. The on_schema_change logic is optimized
E. The on_schema_change logic is disabled

**Correct Answer:** A

**Explanation:**  
The --full-refresh flag forces incremental models to ignore all incremental logic including
on_schema_change and rebuild completely.

---

# Question 37
**Topic:** DAG Execution  
**Difficulty:** 1 (Easy)

**Scenario:**
What is the execution order for seeds in dbt build?

**Question:**
What will happen?

**Options:**
A. Seeds run last
B. Seeds run first
C. Seeds run randomly
D. Seeds run in parallel
E. Seeds run based on file size

**Correct Answer:** B

**Explanation:**  
Seeds always run first in dbt build regardless of the DAG structure or dependencies.

---

# Question 38
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select B_customer_dim --defer`

**Question:**
What will happen?

**Options:**
A. S_customers runs locally
B. S_customers uses production version
C. S_customers is skipped
D. S_customers runs in parallel
E. S_customers is deleted

**Correct Answer:** B

**Explanation:**  
With --defer and --select upstream dependencies like S_customers use production versions instead of
building locally.

---

# Question 39
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens to incremental models when you run dbt build --full-refresh?

**Question:**
What will happen?

**Options:**
A. They ignore incremental logic and rebuild completely
B. They use enhanced incremental logic
C. They run normally
D. They are skipped
E. They are deleted

**Correct Answer:** A

**Explanation:**  
The --full-refresh flag forces incremental models to ignore their incremental logic and rebuild
completely from scratch.

---

# Question 40
**Topic:** DAG Execution  
**Difficulty:** 2 (Medium)

**Scenario:**
Scenario: You have a DAG with multiple models and snapshots. When you run dbt build what runs
between seeds and tests?

**Question:**
What will happen?

**Options:**
A. Models and snapshots mixed based on dependencies
B. Models first then snapshots
C. Snapshots first then models
D. Random order
E. Alphabetical order

**Correct Answer:** A

**Explanation:**  
Between seeds and tests models and snapshots run mixed based on dependency relationships not by
type.

---

# Question 41
**Topic:** Data Quality  
**Difficulty:** 4 (Critical)

**Scenario:**
You have a production DAG structured as follows:

```
+---------------+   +---------------+   +---------------+   +---------------+
| raw_orders    | ->| stg_orders    | ->| fct_orders    | ->| mart_revenue  |
+---------------+   +---------------+   +---------------+   +---------------+
                                            ^
                                            |
+---------------+   +---------------+       |
| raw_payments  | ->| stg_payments  | ------+
+---------------+   +---------------+
                        |
                        v
                    +---------------+
                    | fct_payments  |
                    +---------------+

+---------------+   +---------------+   +---------------+
| raw_customers | ->| stg_customers | ->| dim_customers |
+---------------+   +---------------+   +---------------+
```

The `stg_payments` model contains **data quality issues** that are causing **foreign key violations**.
The `fct_orders` model depends on both `stg_orders` and `stg_payments`.

**Question:**
What is the **most critical action** to take in this situation?

**Options:**
A. Continue with the deployment and fix the issues later
B. Stop the deployment and fix the data quality issues in stg_payments
C. Skip the fct_orders model and deploy the rest
D. Use the previous version of stg_payments
E. Deploy with warnings and monitor the issues

**Correct Answer:** B

**Explanation:**  
When data quality issues cause foreign key violations in upstream models, the most critical action is to stop the deployment and fix the data quality issues in stg_payments. This prevents downstream models from inheriting corrupted data and maintains data integrity across the entire DAG.

---

# Question 42
**Topic:** Production Recovery  
**Difficulty:** 4 (Critical)

**Scenario:**
Critical Scenario: You have a complex DAG with 50+ models and snapshots. During a production
deployment you encounter a critical failure in a core model that affects 30+ downstream models. What
is the MOST critical consideration for recovery?

**Question:**
What will happen?

**Options:**
A. Speed of execution
B. Data consistency and integrity
C. Cost optimization
D. Code simplicity
E. Resource usage

**Correct Answer:** B

**Explanation:**  
In production failures affecting many downstream models data consistency and integrity are the most
critical considerations for recovery.

---

# Question 43
**Topic:** Model Contracts  
**Difficulty:** 4 (Critical)

**Scenario:**
Critical Scenario: Your dbt project uses cross-project references with model contracts. During a
deployment you discover that a referenced model has breaking schema changes. What is the MOST
critical action?

**Question:**
What will happen?

**Options:**
A. Deploy immediately to fix the issue
B. Check model contract violations and coordinate with the upstream team
C. Ignore the changes and continue deployment
D. Rollback to the previous version
E. Delete the model contract

**Correct Answer:** B

**Explanation:**  
When model contracts are violated the most critical action is to check violations and coordinate
with the upstream team to ensure compatibility.

---

# Question 44
**Topic:** Incremental Models  
**Difficulty:** 4 (Critical)

**Scenario:**
Critical Scenario: You have incremental models with complex business logic that process millions of
records daily. During a routine deployment you discover that the incremental logic has a bug causing
data duplication. What is the MOST critical action?

**Question:**
What will happen?

**Options:**
A. Continue with the deployment
B. Stop the deployment and investigate the data impact
C. Delete all incremental data and start fresh
D. Ignore the duplication
E. Deploy a hotfix immediately

**Correct Answer:** B

**Explanation:**  
When incremental logic bugs cause data duplication the most critical action is to stop deployment
and investigate the data impact before proceeding.

---

# Question 45
**Topic:** CI/CD  
**Difficulty:** 4 (Critical)

**Scenario:**
Critical Scenario: Your dbt project uses --defer in CI/CD with production state artifacts. During a
deployment you discover that the production state artifacts are corrupted or missing. What is the
MOST critical action?

**Question:**
What will happen?

**Options:**
A. Continue with the deployment
B. Stop deployment and rebuild state artifacts
C. Use development state artifacts instead
D. Ignore the defer flag
E. Deploy without state comparison

**Correct Answer:** B

**Explanation:**  
When production state artifacts are corrupted the most critical action is to stop deployment and
rebuild state artifacts to ensure reliable testing.

---

