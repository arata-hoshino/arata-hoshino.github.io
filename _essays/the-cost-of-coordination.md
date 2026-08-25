---
title: "The Cost of Coordination"
number: "II"
order: 2
date: 2026-02-08
summary: "Why splitting a system into services makes some problems easier and one problem permanently harder."
---

Every distributed system is an attempt to buy independence. Separate deploys, separate
failure domains, separate teams. The bill arrives in a single currency: coordination.

## Independence is the product, not the architecture

The reason to split a service out is almost never technical. It is that two groups of people
want to change two things on different schedules without asking each other for permission.
When that is true, a service boundary is worth its cost. When it is not true — when every
feature still requires three teams and one release train — you have paid for distribution and
received none of the independence.

The test is simple and unkind: *can this service ship a change to production without a
coordinated change anywhere else?* If the answer is no, more often than not, the boundary is
in the wrong place.

## What coordination costs

Once a call crosses a process boundary, four things that used to be free stop being free.

**Atomicity.** A function call either happened or it didn't. A network call has a third
outcome: it might have happened. Every remote mutation needs an idempotency key or a
reconciliation process, and most systems discover this after their first duplicate charge.

**Ordering.** Within a process, statements run in order. Across services, two events emitted a
millisecond apart may arrive in either order, or one may not arrive for six hours because a
consumer was down. Code that assumes ordering will be correct in staging and wrong in
production.

**Schema.** A shared struct is enforced by the compiler. A shared JSON payload is enforced by
hope, a wiki page, and eventually an incident. Contract tests convert the hope into something
mechanical, which is why they are the highest-value test in a distributed codebase.

**Debuggability.** A stack trace crosses function boundaries automatically. Nothing crosses
service boundaries automatically. If you split a system before you have distributed tracing,
you have chosen to debug by correlation of timestamps, which is to say by guessing.

## The gradient that actually works

Boundaries are cheapest to move before they exist. The pattern that consistently survives
contact with reality:

1. Build the module inside the monolith, with its own package, its own tables, and no
   cross-imports into the rest of the code.
2. Enforce the boundary in CI — a lint rule that fails a build is worth more than a design
   document.
3. Let it run that way for a while. Boundaries that are wrong will start to hurt in months,
   not weeks.
4. Extract only when independence is genuinely needed, and only the modules that earned it.

Steps one through three are cheap and reversible. Step four is neither.

> Distribution is not a level you unlock by growing. It is a tradeoff you accept when the
> alternative — everyone editing the same thing at once — has become more expensive.

## The failure mode nobody names

The most common outcome of a premature split is not an outage. It is a slow decline in the
rate at which anyone can change anything. Every feature grows a coordination tax: a meeting, a
version bump, a deploy ordering constraint. Velocity drops smoothly enough that no single
decision looks like the cause.

That is the real cost, and it does not show up on any dashboard you own.
