# BigQuery → GitHub Actions with reconciliation

Trigger a deployment workflow for newly approved rows, then run a slower
reconciliation sweep to re-dispatch recent deployments that never completed.

## Setup

The project selects the `dev` profile. Configure it in
`~/.drt/profiles.yml`:

```yaml
dev:
  type: bigquery
  project: your_gcp_project_id
  dataset: operations
  method: application_default
```

Authenticate with BigQuery and provide a GitHub token with `actions: write`
access to the destination repository:

```bash
gcloud auth application-default login
export GITHUB_TOKEN="your-token"
```

The destination workflow's `workflow_dispatch` trigger must declare the
`deployment_id`, `environment`, `version`, and `triggered_by` inputs used by
these syncs.

## How the pair works

- `trigger_deploy` is the fast incremental path. Its watermark prevents the
  same approval from being selected on every run.
- `reconcile_missing_deploys` is a full sync. Its anti-join compares approved
  deployments with completed deployments and selects only the missing rows.

The GitHub Actions workflow must write a row to `completed_deployments` only
after the deployment finishes. It must also use `deployment_id` as an
idempotency key because the incremental and reconciliation syncs can dispatch
the same deployment at the same time.

Replace the project, dataset, and table names in
`reconcile_missing_deploys.yml` with your own BigQuery relations.

## Schedule

Run the incremental path frequently:

```bash
drt run --select trigger_deploy
```

Run the reconciliation path separately on a slower schedule, such as daily:

```bash
drt run --select reconcile_missing_deploys
```

Keep the seven-day lookback or choose another bounded window that matches how
long a missing deployment should remain eligible for recovery.

See [Reconciliation syncs](../../docs/guides/reconciliation-syncs.md) for the
requirements and operational trade-offs of this pattern.
