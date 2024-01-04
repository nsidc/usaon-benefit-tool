---
title: "Use a standard format for decision records"
date: "2024-01-04"
author: "Hazel Shapiro"
status: "Proposed"
---

## Context

In beginning this decision record, having a common format for each entry would be helpful. @hazelshapiro 
did some research and proposed Nygard's format. 


## Decision

Use the template described by Michael Nygard's 2011 blog post
[Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
This format includes:

- Title: short noun phrases
- Context: This section describes the forces at play. These forces are probably in tension and should be
called out as such. The language in this section is value-neutral. It is simply describing facts.
- Decision: This section describes our response to these forces. It is stated in full sentences, with an active voice.
- Status: A decision may be "proposed" if the project stakeholders haven't agreed with it yet, or "accepted"
once it is agreed. If a later ADR changes or reverses a decision, it may be marked as "deprecated" or
"superseded" with a reference to its replacement.
- Consequences: This section describes the resulting context, after applying the decision. All consequences
should be listed here, not just the "positive" ones. A particular decision may have positive, negative, and
neutral consequences, but all of them affect the team and project in the future.
- Consent: A non-exhaustive list of who consents to the decision.

_Above is copied or summarized from the original blog post._


## Consequences

* All future decision record entries will follow the agreed-upon format.
* Decision records will be more thorough.
* Decision records will be more readable.
* Decision records will take longer to author.


## Consent

* Matt Fisher
* Hazel Shapiro
