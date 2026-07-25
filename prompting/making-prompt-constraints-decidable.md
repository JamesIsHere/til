# Making prompt constraints decidable

Prompts need constraints, and numbers are the best kind. When there is no
natural number, use a stopping rule, a reference artifact, a cut after
ranking, or a tier name. The real dividing line is not numeric vs.
non-numeric — it is decidable vs. vibes: could a third party check whether
the output complied?

## The test

"Concise" fails the test. Two readers can disagree about whether an answer
was concise, and neither is wrong. "Main page" passes it without containing
a digit: either the output fits on the main page or it does not.

When a number does not exist naturally, these substitutes still pass:

- A stopping rule — "stop when the test suite is green"
- A reference artifact — "match the layout of the existing report"
- A cut after ranking — "rank everything, keep what survives the cut"
- A tier name — a named level from a shared scale

## Priorities are orderings, and orderings are decidable

The priority-level habit ports directly. Priority is an ordering, and an
ordering is decidable: "if this fights with the deadline, the deadline
wins." A third party can check who won.
