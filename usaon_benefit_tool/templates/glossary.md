# BENEFIT Tool Glossary

## General Terms

**Assessment**: A collection of information from one or more respondents, which describes how objects relate to one another and assesses strengths and gaps throughout the system through a structured rating process.

**Object**: Reusable descriptions of observing systems, data products, applications, and societal benefit areas. This reusability drives consistency across assessments to support analysis and also eases data entry for Respondents over time.

**Respondents**: A person who can add information (objects, assessments) to the BENEFIT tool. Respondents are experts and should provide ratings and descriptions within their field of expertise.

## Object Library

A list of available objects for use in assessments. The goal of the object library is to have reusable descriptions of observing systems, data products, applications, and societal benefit areas. This reusability drives consistency across assessments to support analysis and also eases data entry for Respondents over time.

**Object library**: The collection of available objects for use in assessments. Respondents may add new objects to the registry.

### Object Type

Type of Object - Observing System, Data Product, Application, Societal Benefit Area.

**Observing system** - A system or human in the environment or at a distance (e.g. remote sensing) that senses environmental conditions and records them for use by others, including through oral transmission.

**Data product** - A data product, or other intermediate object, is a product, service, process, or outcome derived from direct observations, models, or other types of knowledge synthesis. It has the potential to be used by a variety of users but is generally not as accessible to non-experts. This field can also include intermediate steps, such as data transmission systems.

**Application** - a key product, service, or outcome that directly supports societal benefit areas. It often informs non-experts or experts in other domains. Applications serve as the focal point for an assessment.

**Societal Benefit Area** - areas of impact for broad benefit as delineated by a societal benefit framework. These are often further described by sub-areas, key objectives, or other more specific descriptions. The BENEFIT tool can accommodate multiple societal benefit frameworks, but does not allow for ad hoc descriptions of societal benefit. There is a separate structure to register Societal Benefit Area objects.

> **Note**: Ongoing efforts are being made to align this data structure with best practices and partner organization structures (e.g. Polar Observing Assets working group, Arctic Data Center, Federated Search crew) with the goal to be able to import or sync items in the registry from an external source.

> **Note**: To simplify the database construction, we are pursuing a tiered development process. A simplified version of the object fields are described below and included in the current version of the BENEFIT tool. Future efforts will increase the complexity and utility of the objects and object library.

## Object Fields for Observing Systems, Data Products, and Applications

This is the structure to describe Observing System, Data Product, or Application objects. Most fields are optional but encouraged.

**Title**: Full name of the object. In the case where the full name is brief, this may be the same as the short name.

**Short Name**: Acronym or a short name of the object, which is displayed in the diagram to save space.

**Description**: Short summary of the object, including geographic or thematic scope.

**Organization**: The entity/entities responsible for the operation of the observing system, data product, or application. Preferably in the format [Full name] [acronym], e.g. National Snow and Ice Data Center (NSIDC).

**Funder**: The entity/entities responsible for funding the observing system, data product, or application. Preferably in the format [Full name] [acronym], e.g. National Science Foundation (NSF).

**Funding Country/Countries**: The countries contributing to funding an object.

**Website**: The URL to access more information about the referenced object and/or to access data directly. Can include more than one URL, separated by a comma.

**Contact Information**: An email address, web form link, or phone number for people to contact if they have questions about the object.

**Persistent Identifier**: A standard way to refer back to the object's source, usually a DOI.

**Hypothetical**: A yes/no toggle. A hypothetical object is one that does not exist or is envisioned as significantly different than the current version. This type of object allows for hypothetical future state assessments, in which respondents envision a change in the system (e.g., a new observing system, improved data transmission, or loss of a key asset) and can assess the potential impact on Societal Benefit Areas. In most cases, this field will not be checked as most objects and assessments focus on the current state.

## Object Fields for Societal Benefit Areas

This is the structure to describe Societal Benefit Area objects. Most fields are optional but encouraged.

**Title**: Full name of the societal benefit area.

**Short Name**: Acronym or a short name of the object, which is displayed in the diagram to save space.

**Description**: Short summary of the object, including a brief description of the sub-areas included in this Societal Benefit Area.

**Framework Name**: The framework that describes this Societal Benefit Area.

**Framework URL**: The link to access the framework that describes this Societal Benefit Area.

## Assessments

A collection of information from one or more respondents, which describes how objects relate to one another and assesses strengths and gaps throughout the system through a structured rating process.

### Assessment Fields

Fields that describe each assessment.

**ID #**: Computer-generated identifier

**Title**: Unique name of survey

**Created by**: Computer-generated field linking an assessment to the user who created the assessment.

**Description**: Narrative description of the assessment, including the focus, key scoping decisions, and who completed the assessment.

### Link Fields

Assessments contain a series of links. The rating for each link answers three questions:
- How important is a particular input object to its related output object?
- How well does it perform in supporting that output?
- What gaps are impacting performance?

The answers to these questions are reflected in the assessment diagram by the thickness and color of the link connecting two survey objects. For instance, imagine a satellite (observing system) that is very important to a sea ice data product but performs poorly because of persistent Arctic cloud cover and high latency (gaps). Those would be linked by a thick (high criticality) yellow (low performance) line. These concepts are further described below.

Most fields are optional but encouraged.

**Link**: Defines which survey objects are connected.

> **Note**: Ratings are applied to that link, which means that all ratings are applied to a specific context. An object can have a high criticality or performance in one context and a low criticality or performance in another.

**Criticality rating**: 1-10 rating of the criticality of an input to an output, e.g., criticality of an observing system to a data product. This answers the question: On a scale of 1-10, how much would the loss of this input impact the performance of your data product or application (see [rating rubrics](/user-support/rating-rubric)).

**Criticality rationale**: Text description answering the question: What accounts for this criticality rating? If there is a close equivalent product, why do you prefer this one?

**Performance rating**: 0-100 rating of the performance of the subject. Answers the question: What is your satisfaction with this input? (see [rating rubrics](/user-support/rating-rubric)).

**Performance rationale**: Text description answering the question: What accounts for this performance rating? Include any journal articles, statements, or contextual observations that might help us to understand your rating.

**Gaps**: Text description answering the question: If the rating is less than "ideal," what improvements are needed?

**Variable or Attribute**: If an observing system or data product contains multiple observable properties or variables, this allows a respondent to specify which field they used. (optional)

## Users

**User** - anyone who has an account in the BENEFIT tool, which can be created via a Google login.

### User Fields

**Name** - user's first and last name.

**Role** - defines a user's role and level of access within the tool.

- **Admin** - A user with the ability to create new assessments, change other user roles, and delete objects.
- **Respondent** - A person who can add information (objects, assessments) to the BENEFIT tool. Respondents are experts and should provide ratings and descriptions within their field of expertise.
- **Analyst** - The default role for new users. Analysts can view data within the BENEFIT tool, but cannot edit it.

**Email** - user's email address.

**ORCID iD** - user's ORCID iD, which is a free, unique, persistent identifier (PID) for individuals to use as they engage in research, scholarship, and innovation activities.

**Affiliation** - user's affiliation, could be institutional or regional.

## Future Fields

There are many improvements planned for the BENEFIT tool. This section provides definitions of a select number of high-priority improvements.

**Private** - An assessment that is only viewable by a select number of respondents and analysts. This capability is not yet in place.

**Cohort rating** - Recognizing that self-assessment has limitations, especially for assessing connections to broad societal benefit areas, US AON aims to implement a cohort rating process. This would be a group of 10-20 people who would assess connections to a few specific Societal Benefit Areas, to provide a view of the societal benefits of many applications.

**Status**: Work-In-Progress, Published, Closed, or Archived. In the absence of this capability, the status is generally included in the title of the assessment.

**Tags**: This will be a user-defined field within assessments or objects designed to create additional flexibility in how diagrams are constructed, constrained, and viewed, for example, allowing for a regionally- or thematically-focused analysis.

**Designated respondents**: List of respondents with edit-access for a particular assessment. Not yet implemented.
