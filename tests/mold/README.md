# Mold policy fixtures

Run `python3 -m unittest discover -s tests -p 'test_mold*.py'` from the repository root.
`cases.json` contains positive and negative CSS/JS fixtures. The runner creates an
isolated temporary component, uses the production config and checker, and asserts
individual check statuses plus profile routing.

Coverage: UI raw/alias/shared values; alias chains and cycles; shared-name local
overrides; raw and token fallbacks; calc provenance; Lab geometry versus required
color/time/shadow/easing; UI spacing/type failures and Lab warnings; negated tokens and safe-area `env()`; configured primitives; delay;
font shorthand; JS failure promotion; slug/explicit prefix ownership; Carousel
Ring's shared danger ring; URL/comment exclusions; and declaration priority.

The checker considers all definitions of a local variable in the inspected source
and linked dependencies. If any possible definition is invalid, it reports it.
This is conservative source analysis, not a full CSS cascade simulation. It does
not certify runtime CSS validity, browser behavior, JS AST correctness or a11y.
