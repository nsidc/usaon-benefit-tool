## NOTES:
- we started imagining a model with the different node types unified within one main table
- relationships are now `links` also in a unified table
- starting to think more about `node` table as a library of node objects (data products, applications, etc)
- TODO: how do we handle societal benefit areas, other node types are more uniform. Should we represent each of the 12 major SBAs as nodes in the node library with special fields that link those nodes to sba sub areas (or another way).
- NOTE: some needed tables were deleted to make this process easier visually in mermaid (should we add them back?)
- NOTE: Survey became Assessment
```mermaid
erDiagram

%% Dynamic operational data:
assessment {
    uuid id PK
    %% seq version PK

    str title
    str description

    string assignee FK

    array tags

    string created_by FK
    datetime created
    datetime updated
}


assessment_node {
    int id PK "SK"
    int assessment_id FK
    int node_id FK

}

link {
    int source_assessment_node_id PK "FK"
    int target_assessment_node_id PK "FK"

    %% TODO identify which rating
    int rating
}

%% AKA node library
node {
    int id PK
    
    enum type
    str short_name
    str full_name
    str organization
    str funder
    str funding_country
    str website
    str description
    str contact_information
    str persistent_identifier
    str tags
    boolean hypothetical
    str version

}



%% Static reference data:
node_type {
    string id PK "name"
}
societal_benefit_area {
    string id PK "name"
}
societal_benefit_subarea {
    string id PK "name"
    string societal_benefit_area_id FK
}
societal_benefit_key_objective {
    string id PK "name"
    string societal_benefit_subarea_id FK
}


%% Relationships

assessment_node ||--|{ link: "points from"
assessment_node ||--|{ link: "points to"

node ||--|{ assessment_node: ""
assessment ||--|{ assessment_node: ""

node }o--|| node_type: ""




societal_benefit_area ||--|{ societal_benefit_subarea: ""
societal_benefit_subarea ||--|{ societal_benefit_key_objective: ""
```
