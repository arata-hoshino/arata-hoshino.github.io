---
title: "Writing It Down"
number: "V"
order: 6
date: 2026-06-30
summary: "The highest-leverage engineering artifact is usually a document, and almost nobody is rewarded for producing one."
---

The decisions that shape a system are made in an afternoon and lived with for years. Most of
them are never recorded. Two years later someone asks why the queue is configured that way,
and the honest answer — that a person who has since left had a good reason involving a
constraint that no longer exists — is unavailable.

## Record the decision, not the design

A design document describes what will be built. It is obsolete within a quarter. A decision
record describes *why one option was chosen over the others*, and it stays useful for as long
as the decision does.

The useful form is short enough that people actually write it:

- **Context.** What was true when this was decided. Constraints, deadlines, scale, team size.
- **Decision.** What was chosen, in one sentence.
- **Alternatives.** What else was considered, and the specific reason each was rejected.
- **Consequences.** What this makes easy, and what it makes hard.

The alternatives section carries most of the value. Without it, a future reader cannot tell
whether an option was rejected for good reason or never considered at all — and that
distinction determines whether it is safe to revisit.

## Write the constraints, because they expire

"We chose the single-region deployment because we had two months and no one on the team had
run a multi-region system before" is a genuinely useful sentence. It tells a future reader
exactly what would have to change for the decision to change.

Compare it to "we chose single-region for simplicity," which sounds more professional and
communicates nothing. Documents that hide their real reasoning read as more authoritative and
age far worse.

## Comments answer why; code answers what

The same rule scales down. A comment that restates the code is noise:

```python
# increment the counter
counter += 1
```

A comment that records the reasoning is durable:

```python
# Retry three times: the upstream provider's load balancer drops
# roughly one connection in a thousand during its rolling deploys.
# Four retries measurably increased tail latency without improving
# the success rate. See incident 2026-02-14.
```

The second one survives a refactor, because what it explains is not visible in any version of
the code.

## The postmortem is a decision record with a body count

Incident reviews follow the same logic, and they fail in the same way — by describing what
happened rather than why the decision that led to it was reasonable at the time. If the
writeup makes the people involved look careless, it is wrong. They were not careless; they
were operating with the information available, and the useful output is a change to what
information is available next time.

> A blameless postmortem is not a polite one. It is one that locates the cause in the system
> rather than in the person, because only the system can be changed.

## Why this is hard

Nobody has ever been promoted for a document that prevented an outage that consequently did
not happen. The incentives point at visible work, and writing is invisible by construction.

The counterweight is to make it cheap: a template, a directory in the repo, a norm that a
non-trivial pull request links to a decision record. Not a review board, not a process — just
a place where the reasoning goes, and the expectation that it goes there.

Everything on this site is an attempt to take that advice seriously.
