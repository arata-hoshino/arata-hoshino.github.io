---
title: "The Observability Budget"
number: "IIIb"
order: 4
date: 2026-03-27
summary: "You cannot log everything. Deciding what not to record is the whole discipline."
---

Observability has an economics problem that its vendors would prefer you discover slowly.
Every signal has a cost — storage, ingest, index, and the attention of the person reading it —
and the marginal value of the ten-thousandth log line is not merely small. It is often
negative, because it buries the one that mattered.

## Three signals, three jobs

The standard triad is usually presented as a menu. It is closer to a division of labor.

**Metrics** answer *is something wrong?* They are cheap, aggregate, and low-cardinality. They
should be the only thing that pages you.

**Traces** answer *where is it wrong?* They are per-request and expensive, which is why they
should be sampled — but sampled intelligently. Head sampling at 1% will miss every error you
care about. Tail sampling that keeps all errors and slow requests plus a small baseline gives
you a hundredth of the volume with nearly all the signal.

**Logs** answer *what exactly happened?* They are the most expensive per unit of insight and
the most tempting to over-produce. A log line earns its place if you can name the question it
answers.

## The cardinality trap

The fastest way to make a metrics bill unpayable is to attach a user ID to a label. Each
distinct combination of label values is a separate time series; add one unbounded dimension and
the count is no longer bounded by anything.

The rule that scales: **metrics carry dimensions you would group by; traces carry identifiers
you would search for.** `status_code`, `region`, and `endpoint` belong on a metric.
`user_id`, `request_id`, and `order_id` belong on a span.

## Structure at the source

The difference between

```
[ERROR] failed to charge user 8812 after 3 attempts: gateway timeout
```

and

```json
{"level":"error","event":"charge_failed","user_id":8812,
 "attempts":3,"cause":"gateway_timeout","trace_id":"a3f9..."}
```

is not tidiness. It is whether the answer to "how many charge failures were gateway timeouts
last Tuesday" takes four seconds or four hours. Parse at write time, once, or parse at read
time, forever.

## Alerts are a promise about human attention

Every alert is a claim that a person should stop what they are doing. Judged that way, most
alert catalogues are dishonest. Two tests worth applying to each one:

1. **Is it actionable?** If the response is "watch it," it is a dashboard, not an alert.
2. **Is it symptom-based?** Alert on the thing users feel — error rate, latency, queue age —
   not on the cause. Cause-based alerts fire for causes that turn out to be harmless and stay
   silent for the ones you did not anticipate.

A page that fires and requires no action trains the on-call to ignore the next one. Alert
fatigue is not a personal failing; it is the predictable output of a system that cries wolf.

> The goal is not to see everything. It is to be told the one thing that changes what you do
> next.
