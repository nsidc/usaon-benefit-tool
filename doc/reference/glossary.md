# Glossary

* `Assessment`: A solicitation for input from a `respondent.`
* `Library`: The collection of all `assessements`.
* `Registry`: The collection of available `objects` for use in `responses`.
* `Analysis`: The process of viewing or analyzing 'assessments' (Sankey diagrams and underlying data) by an
  `Analyst` interacting with the `Library`. Surveys are searched by title, `tags`, and/or other survey object fields.

> :memo: We think it would be really cool for surveys to be "composed", e.g. a respondent
> fills out a survey for a single application and its upstreams. Then, another respondent
> fills out a survey focused on an SBA and its upstream applications. The data for the upstream
> applications in the second survey can come from the response to the first survey, enabling one
> large graph to be composed from multiple surveys.


## Response Object Registry

A list of available `response objects`. Drives consistency in naming across `assessments` to
support `analysis` and also to ease data entry for `Respondents`, over time.

`Respondents` may add new `objects` to the `registry`.

There is a generic `Registered Object` structure that applies to Applications,
Data Product, and Observing Systems.
`Application` - an instantiation of an `object` in a particular `assessment` where that
object connects directly to the `societal benefit areas`. This could also be referred to
as the focal point for an `assessment`.
There are a few additional fields that apply to `end product` `objects`, and that influence
the way those `objects` are displayed. These `end products` are also referred to as `applications`.

There is a separate structure to register `Societal Benefit Area objects`.

Ongoing efforts are being made to align this data structure with best practices and partner organization
structures (e.g. Polar Observing Assets working group, Arctic Data Center, Federated
Search crew) with the goal to be able to import or sync items in the registry
from an external source.

> :memo: To simplify the database construction, we are pursuing a tiered development process.
> A simplified version of the `object` fields are described below with steps for increasing
> the complexity and utility of the `objects` and `object library`.

### Version 1 Fields

* `Object Type`: Type of Object - `Observing System`, `Intermediate Product`, `End Product`.
   (_Multiplicity: 1..1; Format: Pick from list_)

  _NOTE_ This is the field currently under debate. What is the correct level of detail to be able to
  interpret the information and build diagrams, while still creating a streamlined and intuitive process?
  Working definitions below.

  * `End product` - a service, product, or outcome that directly supports societal benefit. It often informs
     non-experts or experts in other domains.
  * `Intermediate product` - An intermediate product, like a dataset, is a product, service, process, or outcome
     derived from direct observations, models, or other types of knowledge synthesis. It has the potential to be
     used by a variety of users but is generally not as accessible to non-experts
  * `Observing system` - A system or human in the environment or at a distance (e.g. remote sensing) that senses
     environmental conditions and records them for use by others, including through oral transmission.

* `Acronym/Short Name`: Acronym or a short name of the object, which would be displayed in the sankey diagram to save space.
   (_Multiplicity: 1..1; Format: Text_)
* `Full Name`: Full name of the object. In the case where the full name is brief, this may be the same as the `short name`.
   (_Multiplicity: 1..1; Format: Text_)
* `Website (about)`: The URL to access more information about the referenced object (_Multiplicity: 0..1; Format: URL_)
* `Website (data access)`: The URL to access data directly (_Multiplicity: 0..1; Format: URL_)
* `Description`: Short summary of the object, including geographic or thematic scope. (_Multiplicity: 1..1; Format: Text_)
* `Contact Information`: An email address, web form link, or phone number for people to contact if the have questions about the object.
   (_Multiplicity: 0..1; Format: Text_)
* `Persistent Identifier`: A standard way to refer back to the object's source, usually a DOI
   (_Multiplicity: 0..n; Format: Text_)


 _NOTE_ In most parts of the diagram, an `object`'s node color is defined by it's performance as an input
 to various outputs. For example, the color of an observing system is calculated as a weighted average
 of its performance score relative to the `intermediate products` it supports. In the instance of an
 `end product` which links directly to `societal benefit areas`, this logic does not apply because
 `end products` are often serving `societal benefit areas` outside of their main mission or scope. Instead,
 their node color is displayed based on an `performance rating` that connects to specific
 `performance criteria`. See details below.

`End product` objects also include:
* `Application Performance Criteria`: Text description of what the ideal performance of this data
  product looks like.
   (_Multiplicity: 1..1; Format: Text_)
* `Application Performance Rating`: 0-100 rating of the performance of the application compared to
   the `Application Performance Criteria` (0=No performance, 100 = perfect)
  (_Multiplicity: 1..1; Format: Number 0-100_)
* `Rationale`: Text description answering the question: What accounts for this
   performance rating?
* `Gaps`: If the rating is less than "ideal" what improvements are needed.

### Version 2 Fields - Links to organizations, agencies, and countries

  _NOTE_ This simply adds a few more fields to manage but not a significant amount of complexity.
  It will improve search and filter features for `analysts`.

* `Organization`: The entity/entities responsible for the operation of the observing system, data product, or application.
   Preferably in the format [Full name] [acronym], e.g. National Snow and Ice Data Center (NSIDC).
   (_Multiplicity: 1..n; Format: Text/List_)
   * _NOTE_: future enhancement would be to use [Type-ahead standard names](https://ror.readme.io/docs/create-ror-powered-typeaheads)
* `Funder`: The entity/entities responsible for funding the observing system, data product, or application. Preferably
   in the format [Full name] [acronym], e.g. National Snow and Ice Data Center (NSIDC). (_Multiplicity: 1..n; Format: Text/List_)
   * _NOTE_: future enhancement would be to use [Type-ahead standard names](https://ror.readme.io/docs/create-ror-powered-typeaheads)
* `Country/Countries`: The countries contributing to running or funding an object.
   (_Multiplicity: 1..n; Format: Pick from [ISO 3166](https://www.iso.org/iso-3166-country-codes.html) or similar_)

### Version 3 Fields - Tags

  _NOTE_ This simply adds tags, which will increase the complexity of data management and display functions.
  If implemented successfully, it will significantly improve search and filter features for `analysts`.

* `Tags`: Please add three or more tags to indicate thematic- or geographic- information about this object to
  aid in analysis and discovery. (_Multiplicity: 0..n; Format: Text_)
   * This is a user-defined field that admins can and will edit. It creates additional
     flexibility in the analysis, for example allowing for a regionally- or
     thematically-focused `analysis`.
   * For the early phase of this tool, the description above encourages users to include
     multiple tags, but the software does not require it.
   * These could also be split into pre-defined regional and topical fields
   * Could include more detail about `object type`



### Version 4 fields - Desired state assessments and versioned objects

  _NOTE_ We intend to do `current state` and `desired state` `analyses`. In a `desired state`
  `analysis`, the `real` field allows us to `desired state` (hypothetical) objects. For instance,
  the USGS stream gauge network if funding increased and there were X number of additional gauges.
  This allows us to trace the impact of changes on the entire network. Related to the survey `type`.

* `Real`: A boolean indicating that an object is real (not hypothetical). Maybe could be called `hypothetical`
  instead?
   (_Multiplicity: 1..1; Format: Boolean_)
* `Version`: Match the version identification system used by the observing system, data product, or
   application managers. This field allows the `analyses` to reflect change over time.
   (_Multiplicity: 0..n; Format: Text_)

## Rated Instance of an Object

The rating answers two questions - how important is a particular input `object` to it's
related output `object`? And how well does it perform in supporting that output? It is
reflected in the `analysis` by the thickness and color of the link connecting two `survey objects`.
For instance: Imagine a satellite (`observing system`) that is very important to a sea ice
`data product` but performs poorly because of persistent Arctic cloud cover and high
latency (`gaps`. Those would be linked by a thick (high `criticality`) red (low
`performance`) line.


```mermaid
flowchart LR
    A[Observing Systems]--> |supports| B[Intermediate Products]
    A --> |self| A
    B --> |supports| C(End Products)
    B --> B
    C --> C
    C --> |supports| D[Societal Benefit Areas]
```

Response objects exist both as a definition in the `registry` and an instantiation with
rating(s) and other fields associated with a `response`. The following specifications
pertain to rated instances, _not_ `registry` definitions.

* `Link`: Defines which `survey objects` are connected. The rating is applied to that `link`.
* `Criticality rating`: 0-10 rating of the criticality of an input to an output,
  e.g. criticality of an `observing system` to a `data product`. This answers the question:
  On a scale of 1-10, how much would the loss of this input impact the performance of your
  `data product` or `application` (1 - very little impact; 10 - complete loss of performance).
* `Criticality rationale`: Text description answering the question: What accounts for this
   criticality rating? If there is a close equivalent product, why do you prefer this one?
* `Performance rating`: 0-100 rating of the performance of the subject. Answers the question:
   What is your satisfaction with this input? (0=No performance, 100 = perfect)
* `Performance rationale`: Text description answering the question: What accounts for this
   performance rating? Include any journal articles, statements or contextual observations
   that might help us to understand your rating.
* `Gaps`: If the rating is less than "ideal" what improvements are needed.
* `Variable or Attribute`: If an `observing system` or `data product` contains many
  observable properties or variables, this allows a `respondent` to specify
  which field they used.
* `Rated by`: Link to the `respondent` who provided this rating.

The `node color` of an `observing system` or a `data product` is defined in this
document: https://docs.google.com/presentation/d/1RmEGcPkC3_9o3qeAndv0QvAcdZwFIHC-/edit#slide=id.g1e651286dde_0_54
The `node color` of an `end product` is rated separately based on the application performance
compared to the `application performance criteria`.

While only a  small number of respondents will provide responses on `Observing Systems` through
`Applications`, a larger number of respondents (up to ~20)  will evaluate the relationships between
`Applications` and `Societal Benefit Areas`. For now, we expect users to follow instructions, but
eventually, we may want to apply restrictions so that the right people can only fill out the right
parts.


## Surveys

* `ID`: Computer generated identifier
* `Title`: Unique name of survey
* `Description`: Narrative description of the survey topic
* `Tags`: This is a user-defined field that admins can and will edit. It creates additional flexibility in
  the analysis, for example allowing for a regionally- or thematically-focused `analysis`.
* `Respondents`: List of `respondents` with edit-access
* `Description`: Narrative description of the survey topic; may be displayed as a prompt
  to the user.
* `Status`: WIP, Published, Closed, Archived? Should we have dedicated date fields, e.g.
  `opened_date`, `published_date`, etc.
```mermaid
---
title: Survey state
---
flowchart LR
    new["New"]
    wip["In progress"]
    review["In review"]
    published["Published"]
    archived["Archived"]
    any["Any state"]

    new --> |response updated| wip
    wip --> |response completed| review
    review --> |admin rejects| wip
    review --> |admin approves| published
    published --> |admin unapproves| review

    any <--> |admin sets| archived
```
* `Private`: Can this survey be viewed by non-registered members? (Or should it be
  restricted to individuals?)

#### Fields not yet supported / need to discuss more:
* `Year`: Allows for repeated analyses to show change over time - (We currently have
`created_timestamp` field which can show when it was originally created. Year seems too wide?)
* `Type`: Surveys could be requesting information about the current state or desired
  state of `response objects`. For "desired state" surveys, we wouldn't be interested in
  `gaps`. (_TODO_: This concept needs to be refined in the future.)
* `Parent`: Another survey that this one is based on. (TODO: Do we want a version number?)

While most `surveys` will link observing systems, data products, applications, and societal benefit
areas, some may simply allow for a data manager to link the `data product` to `observing systems`
without any related `application`. Additionally, a group of up to ~20 `respondents` known as a
`societal benefit cohort` may provide ratings on how  1-3 specific `SBAs` relate to the
`application`.



## Responses

* `Respondents`: `Experts` who can contribute to `assessments`.
* `Tags`: Arbitrary strings for grouping surveys. For example: `river-watch`.
* `Version`: Surveys can be re-issued, with changes, as a new version. E.g. a new survey
  is created as version "1" (version may be represented to user as creation date).
  Later, the survey is copied to version "2", altered, and re-issued, possibly to a
  different `respondent`. We also copy the old response to the new version so the
  `respondent(s)` do not need to start from scratch.
* `Validated date`: Date when an admin marked this survey valid for inclusion in the
  `library`. (NOTE: If populated represents the status is _at least_ validated. Probably
  want to do all statuses this way.)
* `Status`: Draft, ready to validate, validated, ??? (_TODO_: Better to use date fields
  instead? e.g. a submitted response has `submitted_date` populated, a draft does not)



## Analysis

A visualization that is generated from the `library` of responses by an `Analyst`
selecting filters based on fields of `response objects`, such as `tags`. We envision
being able to blend `responses` around common Objects or Fields within those Objects, for
example: "show all `responses` tied to a given `data product`". Or "show all where `tags`
include 'rivers'", etc.

* `Name`: Unique
* `Description`
* `Analyst`
* Filter criteria or list of `responses` associated with the analysis. (_TODO_: If we
  don't want an analysis to change over time, we should probably link it to `responses`
  by ID. But if we _do_ want the analysis to be automatically updated as more
  `responses` are submitted with e.g. a specific `tag`, we should use filter criteria)


## User personas / roles

### Admin

A user who creates a `survey` and invites `experts` to respond, in addition to
validating `responses` and marking them valid/complete.

When creating a `survey`, the admin either creates or selects an `application` in the
registry to associate with the survey.

Can create `surveys` by creating new `versions` of old surveys.

Fields/relationships:

* `Name`
* `Email`
* `ORCID iD`
* `Surveys created`
* `Affiliation`
* `Biography`


### Respondent (field expert)

A user who is invited to register to provide a `response` to a `survey`. Admins will
assign Surveys to Experts. Experts can contribute to multiple Surveys; Surveys can have
many Experts.

Experts may add new `applications`, `data products`, and `observing systems` to the
`registry`, or may select existing `objects`.

Fields/relationships:

* `Name`
* `Email`
* `ORCiD` (optional? | validate format, e.g.: `0000-0003-3260-5445`)
* `Biography`
* `Affiliation` (should this be saved on a response-by-response basis? Affiliation may
  change between surveys)
* `Tags` of interest (areas of expertise, e.g. `river-watch`, `hydrology`)
* `Responses` submitted


### Analyst

These are people who are viewing the data. Not contributing to it in any way.
A user who registers to generate one or more `analysis`. Eventually, we’d like Analysts
to be able to save their Analyses, recreate them and update them. I’m not sure we need
or should track things like Orcid ID, Bio, Affiliation for Analysts, but we could give
them option. It would help with our analytics.

We might also need to support a Guest Analyst so someone could do visualizations without
registering. If we don’t want to create user accounts, then basically everyone would be
a Guest Analyst and they could just export .jpgs and JSON to recreate their analyses.

Fields/relationships:

* `Name`
* `ORCiD` (optional? | validate format, e.g.: `0000-0003-3260-5445`)
* `Biography`
* `Affiliation`
* `Tags` of interest (areas of expertise, e.g. `river-watch`)
* `Analyses` submitted


### SBA Rating Cohort

A group of `respondents` who provide `responses` to `surveys` focused on SBA ratings. A cohort
will generally be solicited to complete many `Societal Benefit surveys`, focusing on a
small number of `SBAs`, to provide a view of the societal benefits of many `applications`.

Fields/relationships:

* `Name`: Unique
* `Description`
* `Expert(s)`: Members of cohort


## Analysis views

Enable analysts to filter surveys by "views". We imagine a "River watch" view, a "Rivers"
view, a "Risk mitigation" view, "A sea ice index" view.

Admins would manage the views. E.g. create a new view, give it a name, and populate `tags`
for surveys that should display in that view.
