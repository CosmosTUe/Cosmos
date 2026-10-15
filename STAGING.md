# Using staging

Staging is a copy of the Cosmos website and Common Room for trying changes before they go live: https://staging.cosmostue.nl and https://staging.commonroom.nl. It runs the same setup as production (Ubuntu 24.04, Python 3.12) with an anonymised copy of prod data.

## Getting in

- Currently, there is only one login to the staging site, subject to change soon, ask Anas for it.
- On the sites, log in with the test accounts `staging-admin@student.tue.nl` (admin) and `staging-member@student.tue.nl` (regular member). Anas has these too, we will expand it at some point.

## How changes get there

1. Open your pull request into `staging` (not `master`). This will run our CI/CD pipeline.
2. When it's merged, it's deployed to staging automatically (about 5 minutes). If the staging server is off, the deploy boots it up automatically.
3. Check your change on staging.
4. If it all looks good, it will be bundled into the next release PR to `master`.

## Good to know

- Emails are never sent from staging. They all get sent to an email sink that can be accessed through logs, though we are working on a way to see this without SSH'ing into the server.
- The server switches itself off after 2 hours without deploys, and every night at 23:00 (UTC). Any deployment restarts the timer. If you need to launch staging again for some reason, re-run the latest "Staging Deployment Workflow" in the Actions tab.
- Don't put real personal data on staging, and don't use your real passwords there.
- The data can be refreshed with a new anonymised copy of production if needed, ask Anas for this.
