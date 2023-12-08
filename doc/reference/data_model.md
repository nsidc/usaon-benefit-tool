```mermaid
erDiagram

%% Dynamic operational data:
survey {
    uuid id PK
    int response_id FK
    str title 
    str created_by FK
    datetime created_timestamp
    str notes "nullable"
}

user {
    string id PK "user identifier"
    string role FK
    string orcid "nullable"
    string biography
    string affiliation "?"
}

response {
    uuid id PK
    seq version PK

    string expert_user_id FK
    string application_object_id FK

    array tags

    string created_by FK
    datetime created
    datetime updated
}


response_observing_system {
    int response_id FK
    string id PK
    string object_id FK

    enum type
    string url
    string author_name
    string author_email
    string funding_country
    string funding_agency
    string references_citations
    string notes "nullable"
}

%% This name is confusing, but "observational" _is_ a type of observing system
response_observing_system_observational {
    int response_id PK
    string response_observing_system_id FK

    string platform
    string sensor
}

response_observing_system_research {
    int response_id PK
    string response_observing_system_id FK


    string intermediate_product
}

response_observing_system_data_product {
    int response_id PK
    string observing_system_id PK
    string data_product_id PK

    int observing_system_contribution_to_data_product_rating "0-100"
    int satisfaction_rating "0-100"
    string rationale "nullable"
    string needed_improvements "nullable"
}

response_data_product {
    int id PK
    int response_id FK
    
    str name
    int satisfaction_rating "0-100"
}

response_data_product_application {
    string response_data_product_id FK
    string response_application_id PK

    int data_product_contribution_to_application_rating "0-100"
    int satisfaction_rating "0-100"
    string rationale "nullable"
    string needed_improvements "nullable"
}

response_application {
    int id PK

    int response_id FK
    string name
}

response_application_societal_benefit_area {
    int response_application_id FK
    string response_societal_benefit_area_id FK

    int application_contribution_to_sociateal_benefit_area_rating "0-100"
}


response_object {
    string id PK "name"
    string type FK
    TODO TODO "more fields?"
}


analysis {
    string id PK "name"
    string analyst_user_id FK
    string description
}
analysis_response {
    string analysis_id PK
    string response_id PK
}


%% Static reference data:
response_object_type {
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
role {
    string id PK "name"
}



%% Relationships
survey }|--|| user: ""
user }|--|| role: ""

response }|--o{ survey: ""
response }o--|| user: ""
response }o--|| response_object: ""

response ||--o{ response_observing_system: ""
response ||--o{ response_data_product: ""
response ||--o{ response_application: ""
response ||--o{ response_application_societal_benefit_area: ""

response_observing_system }|--|| response_object: ""
response_observing_system ||--o| response_observing_system_observational: ""
response_observing_system ||--o| response_observing_system_research: ""

response_data_product }|--|| response_object: ""

response_application }|--|| response_object: ""


societal_benefit_area ||--|{ societal_benefit_subarea: ""
societal_benefit_subarea ||--|{ societal_benefit_key_objective: ""

response_application_societal_benefit_area ||--|| societal_benefit_area: ""

response_object }|--|| response_object_type: ""

analysis }|--|| user: ""

%% Associative relationships (i.e. relationships with data)
response_observing_system ||--|{ response_observing_system_data_product: ""
response_data_product ||--|{ response_observing_system_data_product: ""

response_data_product ||--|{ response_data_product_application: ""
response_application ||--|{ response_data_product_application: ""

response_application ||--|{ response_application_societal_benefit_area: ""

response }|--o{ analysis_response: ""
analysis }|--o{ analysis_response: ""
```
