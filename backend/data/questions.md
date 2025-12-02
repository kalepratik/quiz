# dbt Certification Questions

# Question 1
**Topic:** DAG Execution  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG scenario defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run the following command:
`dbt build --select B_customer_dim`

**Question:**
What will happen?

**Options:**
A. seed_customers → A_stg_customers → S_customers → B_customer_dim → tests
B. seed_customers → B_customer_dim → tests
C. A_stg_customers → S_customers → B_customer_dim → tests
D. Only B_customer_dim runs

**Correct Answer:** A

**Explanation:**  
When selecting a specific model dbt builds the entire upstream dependency chain including seeds models and snapshots then runs tests on the selected model.

---

# Question 2
**Topic:** Incremental Models  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG with incremental models. You run the following command:
`dbt build --full-refresh`

**Question:**
What will happen?

**Options:**
A. All models are rebuilt from scratch
B. Only incremental models are forced to rebuild from scratch
C. Only snapshots are rebuilt
D. Only seeds are reloaded

**Correct Answer:** B

**Explanation:**  
The --full-refresh flag only forces incremental models to rebuild from scratch; seeds snapshots and regular models run normally.

---

# Question 3
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG scenario defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

You run `dbt build --select state:modified+ --state prod_artifacts/ --defer`. If only `A_stg_customers` changed.

**Question:**
Which models will run?

**Options:**
A. Only A_stg_customers runs
B. A_stg_customers → S_customers → B_customer_dim run
C. A_stg_customers and B_customer_dim run
D. Only B_customer_dim runs

**Correct Answer:** B

**Explanation:**  
With state:modified+ and defer the modified model and all its downstream dependencies run while upstream models use production versions.

---

# Question 4
**Topic:** Dependencies  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG scenario defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

If `S_customers` fails during `dbt build`, what happens to `B_customer_dim`?

**Question:**
What happens to B_customer_dim?

**Options:**
A. B_customer_dim runs normally
B. B_customer_dim is skipped
C. B_customer_dim runs with production data
D. B_customer_dim runs with empty data

**Correct Answer:** B

**Explanation:**  
When a dependency fails dbt stops building nodes that depend on it so B_customer_dim won't run if S_customers fails.

---

# Question 5
**Topic:** Snapshots  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG with snapshots. You run the following command:
`dbt build --full-refresh`

**Question:**
What will happen?

**Options:**
A. Snapshots are forced to rebuild from scratch
B. Snapshots ignore --full-refresh and run normally
C. Snapshots are deleted and recreated
D. Snapshots are skipped entirely

**Correct Answer:** B

**Explanation:**  
Snapshots ignore --full-refresh and run normally comparing current data vs historical snapshot table.

---

# Question 6
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the primary purpose of the `--defer` flag in dbt?

**Options:**
A. To delay model execution
B. To use production models for references instead of building locally
C. To skip model dependencies
D. To run models in parallel

**Correct Answer:** B

**Explanation:**  
The --defer flag uses production models for references instead of building them locally useful for CI/CD scenarios.

---

# Question 7
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
What happens when you run `dbt build --fail-fast` and a model fails?

**Options:**
A. dbt continues with other models
B. dbt aborts immediately on first failure
C. dbt retries the failed model
D. dbt skips the failed model

**Correct Answer:** B

**Explanation:**  
The --fail-fast flag stops execution immediately when the first failure occurs providing quick feedback.

---

# Question 8
**Topic:** State Management  
**Difficulty:** 2 (Medium)

**Scenario:**
What is the purpose of the `--state` flag in dbt?

**Options:**
A. To specify the target environment
B. To specify which state artifacts to use for comparison
C. To specify the database state
D. To specify the model state

**Correct Answer:** B

**Explanation:**  
The --state flag specifies which state artifacts to use for comparison enabling features like state:modified+ selectors.

---

# Question 9
**Topic:** Snapshots  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG scenario defined as:

```
+---------------+   +------------------+   +-------------+   +------------------+
| seed_customers | ->| A_stg_customers  | ->| S_customers | ->| B_customer_dim   |
+---------------+   +------------------+   +-------------+   +------------------+
```

If `S_customers` is a snapshot, what happens when `A_stg_customers` changes?

**Options:**
A. S_customers detects changes and updates history
B. S_customers ignores changes
C. S_customers fails
D. S_customers is deleted

**Correct Answer:** A

**Explanation:**  
When a snapshot's source model changes the snapshot detects differences and updates its historical tracking accordingly.

---

# Question 10
**Topic:** Testing  
**Difficulty:** 1 (Easy)

**Scenario:**
What is the execution order for tests in `dbt build`?

**Options:**
A. Tests run before models
B. Tests run after their target models exist
C. Tests run in parallel with models
D. Tests run randomly

**Correct Answer:** B

**Explanation:**  
Tests run after their target models exist ensuring that the models they test have been built successfully.

---

# Question 11
**Topic:** Data Quality  
**Difficulty:** 4 (Critical)

**Scenario:**
You have a DAG scenario defined as:

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

**Correct Answer:** B

**Explanation:**  
When data quality issues cause foreign key violations in upstream models, the most critical action is to stop the deployment and fix the data quality issues in stg_payments. This prevents downstream models from inheriting corrupted data and maintains data integrity across the entire DAG.

---

# Question 12
**Topic:** Model Contracts  
**Difficulty:** 4 (Critical)

**Scenario:**
Your dbt project uses cross-project references with model contracts. During a deployment you discover that a referenced model has breaking schema changes.

**Question:**
What is the MOST critical action?

**Options:**
A. Deploy immediately to fix the issue
B. Check model contract violations and coordinate with the upstream team
C. Ignore the changes and continue deployment
D. Rollback to the previous version

**Correct Answer:** B

**Explanation:**  
When model contracts are violated the most critical action is to check violations and coordinate with the upstream team to ensure compatibility.

---

# Question 13
**Topic:** Incremental Models  
**Difficulty:** 4 (Critical)

**Scenario:**
You have incremental models with complex business logic that process millions of records daily. During a routine deployment you discover that the incremental logic has a bug causing data duplication.

**Question:**
What is the MOST critical action?

**Options:**
A. Continue with the deployment
B. Stop the deployment and investigate the data impact
C. Delete all incremental data and start fresh
D. Ignore the duplication

**Correct Answer:** B

**Explanation:**  
When incremental logic bugs cause data duplication the most critical action is to stop deployment and investigate the data impact before proceeding.

---

# Question 14
**Topic:** CI/CD  
**Difficulty:** 4 (Critical)

**Scenario:**
Your dbt project uses `--defer` in CI/CD with production state artifacts. During a deployment you discover that the production state artifacts are corrupted or missing.

**Question:**
What is the MOST critical action?

**Options:**
A. Continue with the deployment
B. Stop deployment and rebuild state artifacts
C. Use development state artifacts instead
D. Ignore the defer flag

**Correct Answer:** B

**Explanation:**  
When production state artifacts are corrupted the most critical action is to stop deployment and rebuild state artifacts to ensure reliable testing.

---

# Question 15
**Topic:** DAG Execution  
**Difficulty:** 1 (Easy)

**Scenario:**
What is the execution order when running plain `dbt build`?

**Options:**
A. Seeds → Models → Snapshots → Tests
B. Seeds → Models and Snapshots mixed → Tests
C. Models → Seeds → Snapshots → Tests
D. Tests → Models → Seeds → Snapshots

**Correct Answer:** B

**Explanation:**  
The standard execution order is: seeds first then models and snapshots mixed based on dependencies then tests last.

---

# Question 16
**Topic:** Model Configuration
**Difficulty:** 1 (Easy)

**Scenario:**
You are creating a model that is reused by multiple downstream models but you don't want it to create a table in the database.

**Question:**
Which materialization should you choose?

**Options:**
A. Table
B. View
C. Ephemeral
D. Incremental

**Correct Answer:** C

**Explanation:**
Ephemeral models are not created in the database; instead, they are inlined into downstream queries, reducing unnecessary tables.

---

# Question 17
**Topic:** Macros and Jinja
**Difficulty:** 1 (Easy)

**Scenario:**
You want to reuse a SQL snippet across multiple models.

**Question:**
Which dbt feature allows you to achieve this?

**Options:**
A. Hooks
B. Variables
C. Macros
D. Seeds

**Correct Answer:** C

**Explanation:**
Macros allow you to define reusable SQL or Jinja logic that can be used across multiple models.

---

# Question 18
**Topic:** Testing
**Difficulty:** 1 (Easy)

**Scenario:**
You want to check that the column `id` in your model is unique.

**Question:**
Which generic test would you apply?

**Options:**
A. `not_null`
B. `unique`
C. `accepted_values`
D. `relationships`

**Correct Answer:** B

**Explanation:**
The `unique` generic test ensures all values in the column are distinct.

---

# Question 19
**Topic:** Documentation
**Difficulty:** 1 (Easy)

**Scenario:**
You are writing documentation directly inside a model file.

**Question:**
Which dbt block allows you to embed documentation?

**Options:**
A. `{{ doc() }}`
B. `{{ var() }}`
C. `{{ config() }}`
D. `{{ source() }}`

**Correct Answer:** A

**Explanation:**
The `doc()` block lets you embed and reference documentation for models, sources, and columns.

---

# Question 20
**Topic:** Variables
**Difficulty:** 1 (Easy)

**Scenario:**
You want to pull an environment variable for database password.

**Question:**
Which Jinja function is used?

**Options:**
A. `var()`
B. `env_var()`
C. `target`
D. `config()`

**Correct Answer:** B

**Explanation:**
The `env_var()` function is used to access environment variables in dbt.

---

# Question 21
**Topic:** Hooks
**Difficulty:** 2 (Medium)

**Scenario:**
You want to grant SELECT permissions to a role whenever a model is created.

**Question:**
Which hook should you use?

**Options:**
A. `on-run-start`
B. `post-hook`
C. `pre-hook`
D. `on-run-end`

**Correct Answer:** B

**Explanation:**
`post-hook` runs after a model is built, making it ideal for applying grants.

---

# Question 22
**Topic:** Profiles
**Difficulty:** 2 (Medium)

**Scenario:**
You need different connection settings for development and production environments.

**Question:**
Which profile section handles this configuration?

**Options:**
A. `outputs`
B. `vars`
C. `packages`
D. `seeds`

**Correct Answer:** A

**Explanation:**
The `outputs` section of `profiles.yml` defines connection settings for different targets.

---

# Question 23
**Topic:** Packages
**Difficulty:** 2 (Medium)

**Scenario:**
You want to reuse dbt-utils macros in your project.

**Question:**
Where should you declare this dependency?

**Options:**
A. `profiles.yml`
B. `packages.yml`
C. `dbt_project.yml`
D. `models/schema.yml`

**Correct Answer:** B

**Explanation:**
External dependencies like dbt-utils are declared in `packages.yml`.

---

# Question 24
**Topic:** Seeds
**Difficulty:** 2 (Medium)

**Scenario:**
You need to load static reference data stored in CSV files.

**Question:**
Which dbt command is used?

**Options:**
A. `dbt docs generate`
B. `dbt run`
C. `dbt seed`
D. `dbt test`

**Correct Answer:** C

**Explanation:**
`dbt seed` loads CSVs defined in the `seeds` directory into the database.

---

# Question 25
**Topic:** Snapshots
**Difficulty:** 2 (Medium)

**Scenario:**
You want to track historical changes in a slowly changing dimension table.

**Question:**
Which snapshot strategy should you use to detect changes in multiple columns?

**Options:**
A. `timestamp`
B. `check`
C. `unique_key`
D. `incremental`

**Correct Answer:** B

**Explanation:**
The `check` strategy compares selected columns to detect changes across multiple fields.

---

# Question 26
**Topic:** Sources
**Difficulty:** 2 (Medium)

**Scenario:**
You want to ensure a source table was refreshed within the last 24 hours.

**Question:**
Which configuration do you use?

**Options:**
A. `freshness`
B. `check_cols`
C. `unique_key`
D. `loaded_at_field`

**Correct Answer:** A

**Explanation:**
Source freshness tests allow you to validate that data is up to date.

---

# Question 27
**Topic:** Exposures
**Difficulty:** 2 (Medium)

**Scenario:**
You want to document a dashboard in dbt that depends on certain models.

**Question:**
Which dbt feature is used?

**Options:**
A. Snapshots
B. Exposures
C. Metrics
D. Sources

**Correct Answer:** B

**Explanation:**
Exposures document downstream dependencies such as dashboards or reports.

---

# Question 28
**Topic:** Metrics
**Difficulty:** 2 (Medium)

**Scenario:**
You define a metric with `time_grains: [day, week, month]`.

**Question:**
What does this configuration allow?

**Options:**
A. Limits metric usage to only daily queries
B. Aggregates the metric at multiple time granularities
C. Forces snapshots at each grain
D. Ensures uniqueness in metrics

**Correct Answer:** B

**Explanation:**
`time_grains` defines the time granularities at which a metric can be queried.

---

# Question 29
**Topic:** Semantic Layer
**Difficulty:** 3 (Difficult)

**Scenario:**
You are defining dimensions and entities for metrics in dbt.

**Question:**
Where are these typically defined?

**Options:**
A. `schema.yml`
B. `metrics.yml`
C. `semantic.yml`
D. `sources.yml`

**Correct Answer:** C

**Explanation:**
Semantic Layer definitions for entities, dimensions, and metrics are stored in `semantic.yml`.

---

# Question 30
**Topic:** Audit
**Difficulty:** 3 (Difficult)

**Scenario:**
You want to compare row counts between staging and production tables.

**Question:**
Which dbt utility can you use?

**Options:**
A. `dbt seed`
B. `audit_helper`
C. `dbt snapshot`
D. `dbt docs generate`

**Correct Answer:** B

**Explanation:**
`audit_helper` provides macros for comparing row counts and values across tables for auditing.

---

# Question 31
**Topic:** Performance
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a large fact table updated daily with billions of rows.

**Question:**
What's the best strategy to optimize dbt incremental loads?

**Options:**
A. Rebuild the full table each time
B. Use an incremental filter column like `updated_at`
C. Convert to a view for lighter queries
D. Use ephemeral materialization

**Correct Answer:** B

**Explanation:**
Using incremental loads with a filter column processes only new or updated rows, saving resources.

---

# Question 32
**Topic:** Security
**Difficulty:** 3 (Difficult)

**Scenario:**
You want to enforce row-level security in dbt models.

**Question:**
How can this be implemented?

**Options:**
A. Use `config(materialized='ephemeral')`
B. Apply SQL filters with user-based conditions in models
C. Add `unique` test in schema.yml
D. Use snapshots

**Correct Answer:** B

**Explanation:**
Row-level security can be enforced using SQL filters referencing user context or access controls.

---

# Question 33
**Topic:** Version Control
**Difficulty:** 3 (Difficult)

**Scenario:**
Your team is collaborating on dbt models via GitHub.

**Question:**
What is the best practice for adding new features?

**Options:**
A. Push directly to main branch
B. Create a feature branch, then open a pull request
C. Edit models directly in production
D. Commit to packages.yml

**Correct Answer:** B

**Explanation:**
Feature branches and pull requests allow safe collaboration and code review.

---

# Question 34
**Topic:** Deployment
**Difficulty:** 4 (Critical)

**Scenario:**
You need to promote a tested dbt project from staging to production while minimizing downtime.

**Question:**
What's the best approach?

**Options:**
A. Run `dbt run` directly in production
B. Use environment-specific targets and CI/CD pipelines
C. Manually copy models to production schema
D. Switch all configs to ephemeral

**Correct Answer:** B

**Explanation:**
CI/CD with environment-specific targets ensures safe, repeatable, and automated deployments.

---

# Question 35
**Topic:** Monitoring
**Difficulty:** 4 (Critical)

**Scenario:**
Your dbt runs must trigger alerts when tests fail in production.

**Question:**
Which approach is most effective?

**Options:**
A. Ignore failures until the next run
B. Use logging and integrate with alerting tools (e.g., Slack, Airflow)
C. Re-run failed models silently
D. Remove tests to prevent failures

**Correct Answer:** B

**Explanation:**
Integrating dbt logs and test results with monitoring/alerting tools provides timely visibility into failures.

---

