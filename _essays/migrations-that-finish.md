---
title: "Migrations That Finish"
number: "IV"
order: 5
date: 2026-05-11
summary: "The half-migrated system is the most expensive state a codebase can be in, and the easiest to reach."
---

Most large migrations do not fail. They stall — which is worse, because a failed migration
gets reverted and a stalled one gets a permanent home in the codebase. Two auth systems. Two
config formats. A new service that handles 60% of traffic while the old one handles the rest,
each with its own bugs, forever.

## The shape of a migration that lands

The pattern that reliably completes has four phases and one non-negotiable property: the
system is correct at every intermediate step.

1. **Dual write.** New code writes to both old and new. Reads still come from old. Nothing
   user-visible changes; if the new path is broken, you find out with no consequences.
2. **Backfill and verify.** Copy the history, then run a continuous comparison of old versus
   new on live reads. Log the mismatches. Do not proceed while the mismatch rate is
   interesting — and it will be, for reasons that are always more subtle than expected.
3. **Flip reads.** Behind a flag, per-tenant or per-percentage. This is the only step that can
   hurt a user, and it is the only step that is instantly reversible.
4. **Delete the old path.** Including the dual write, the comparison job, and the flag.

Phase four is the one that gets skipped, and skipping it is what turns a migration into a
permanent tax. It should be scheduled as work, with an owner and a date, at the same time as
phase one.

## Expand, migrate, contract

The same shape applies to schemas, and here it has a name. To rename a column without
downtime:

- **Expand.** Add the new column. Deploy code that writes both and reads the old.
- **Migrate.** Backfill. Deploy code that reads the new and still writes both.
- **Contract.** Deploy code that only touches the new. Then, and only then, drop the old.

Each step is independently deployable and independently revertible. The temptation is to
compress it into one deploy, because three deploys for a rename feels absurd. It is absurd
right up until the deploy that must be rolled back at 2 a.m., at which point it is the only
reason you can.

## Why they stall

Migrations stall for reasons that are organizational, not technical:

- **No owner after the interesting part.** Phases one through three are engineering. Phase
  four is chores, and chores do not get staffed.
- **The long tail of callers.** Ninety percent of traffic moves in a week; the last four
  callers are a batch job, an internal tool, a partner integration, and something nobody can
  identify. Finding them requires instrumentation on the old path — add it in phase one, or
  you will be grepping.
- **No deadline for the old system.** If the old path has no removal date, it has no removal.

> A migration is not done when the new thing works. It is done when the old thing is gone.

## The instrumentation that makes it finishable

One counter, added at the start, saves the entire endgame: increment a metric labeled by
caller every time the deprecated path is used. When it reaches zero and stays there for a
full business cycle, deletion is a five-minute task instead of an archaeology project.

That counter is the cheapest thing in this essay and the most reliably skipped.
