---
title: "Failure Is a Design Parameter"
number: "IIIa"
order: 3
date: 2026-03-02
summary: "Reliability is not the absence of failure. It is the presence of a plan for it."
---

There is a version of reliability engineering that consists of trying harder. Better testing,
more careful reviews, stricter deploys. It helps, and it has a ceiling, and the ceiling is
lower than most teams expect — because at sufficient scale the failure is not in your code at
all. A disk fails. A certificate expires. A dependency you have never heard of publishes a
bad version at 3 a.m.

The alternative is to treat failure as an input to the design rather than a defect in it.

## Every dependency needs a stated behavior on failure

For each thing your service calls, there is an answer to "what happens when this is down."
The answer is either written into the code or discovered during an incident. Only three
answers are legitimate:

- **Fail closed.** The request errors. Correct for payments, authorization, anything where a
  wrong answer is worse than no answer.
- **Fail open.** The request proceeds without the dependency. Correct for recommendations,
  analytics, non-blocking enrichment.
- **Degrade.** The request proceeds with a cached, stale, or default value, and says so.

The bug is not choosing wrong. The bug is not choosing — which in practice means a 30-second
timeout, an exhausted thread pool, and an outage that spreads to services that did not depend
on the broken thing at all.

## Timeouts are a budget, not a number

A timeout copied from another service is a coincidence, not a decision. Timeouts should
descend from the caller's budget: if the request has 500 ms and three sequential calls, no
single call may be given 5 seconds, no matter what the client library defaults to.

Two rules keep this honest:

- **Every timeout is shorter than its caller's.** Otherwise the caller gives up first and the
  work continues, unread, consuming capacity.
- **Retries have a budget too.** Three retries on three layers is twenty-seven requests. Retry
  storms are a self-inflicted denial of service, and they arrive precisely when the system is
  least able to absorb them.

## Backpressure beats buffering

The instinct when a consumer is slow is to add a queue. Sometimes that is right — a queue
absorbs a burst. But an unbounded queue does not absorb anything; it converts a fast failure
into a slow one, and hides the signal that would have told you to shed load.

> A bounded queue that rejects is a working system under stress. An unbounded queue that grows
> is a broken system that has not admitted it yet.

Load shedding feels like giving up. It is the opposite: serving 80% of requests correctly is
strictly better than serving 100% of them badly, and it is the only outcome that leaves you
capacity to recover.

## Practice the recovery, not the failure

Most teams that run failure drills test whether the system survives. The more valuable
question is whether the *humans* can get it back. Can you find the runbook? Does the on-call
have the permissions? Does the rollback actually roll back, including the schema change?

Reliability is measured in time-to-recovery far more than in time-between-failures, and only
one of those two is under your control on any given Tuesday.
