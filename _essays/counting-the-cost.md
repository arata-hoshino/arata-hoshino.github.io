---
title: "Counting the Cost: Where Latency Actually Comes From"
number: "I"
order: 1
date: 2026-01-14
summary: "Almost nobody's slow endpoint is slow for the reason they think. A method for finding out."
---

Ask an engineer why an endpoint takes 900 milliseconds and you will usually get a theory
before you get a measurement. The database is slow. The serializer is slow. The network is
slow. Theories are cheap; the useful move is to make the request account for itself.

## Start with a budget, not a profile

A profile tells you where time went in one run. A budget tells you where time is *allowed*
to go, and that turns a vague complaint into arithmetic. Write it down before you open a
flame graph:

| Stage | Budget | Observed |
| --- | --- | --- |
| TLS + routing | 15 ms | 12 ms |
| Auth lookup | 20 ms | 180 ms |
| Primary query | 60 ms | 55 ms |
| Fan-out to 3 services | 120 ms | 610 ms |
| Serialization | 25 ms | 30 ms |

The moment the table exists, the conversation stops being about opinions. Two rows are wrong,
and the other three are noise. Most performance work fails because it optimizes the rows that
were already inside budget.

## The three ways time disappears

In practice, latency at the service level has three sources, and they call for different
remedies.

1. **Work you actually asked for.** Real computation, real I/O. This is the honest kind, and
   it is optimized by doing less of it — narrower queries, smaller payloads, fewer round trips.
2. **Work you asked for by accident.** The N+1 query, the retry that fires on a 200, the cache
   that never gets a hit because the key includes a timestamp. This is the majority of it.
3. **Waiting.** Connection pool exhaustion, lock contention, a queue behind a slow consumer.
   Nothing is computing; everything is blocked. No amount of code optimization touches this.

Category three is the one that ruins postmortems, because the CPU graphs look calm while the
system is unusable.

> A system at 30% CPU and 100% queue depth is not underutilized. It is broken in a way your
> dashboard was not designed to show.

## Measure the tail, not the mean

The mean latency of a service tells you about a request that no user ever made. What people
experience is the tail: p95, p99, and the long, ugly p99.9 that shows up in support tickets.

The reason is compounding. If a page issues twenty backend calls and each has a 1% chance of
being slow, the chance that the *page* is slow is not 1% — it is about 18%. Tail latency at
one layer becomes median latency at the layer above. This is why fan-out architectures feel
worse than their component metrics suggest.

## What to do on Monday

- Instrument the boundaries, not the internals. Spans at every network call buy more insight
  than a profiler ever will.
- Record queue wait separately from service time. They are different problems with different
  fixes, and averaging them together hides both.
- Set an explicit budget per endpoint and alert on the budget, not on an absolute number.
- Re-measure after every fix. Roughly a third of performance "fixes" move time somewhere else.

Latency is not a mystery. It is a ledger that nobody bothered to keep.
