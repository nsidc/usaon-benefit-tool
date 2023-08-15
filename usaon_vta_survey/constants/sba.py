# TODO: Consider using a type compatible with SQLAlchemy models
SocietalBenefitKeyObjective = str
SocietalBenefitSubArea = list[SocietalBenefitKeyObjective]
SocietalBenefitArea = dict[str, SocietalBenefitSubArea]
IaoaSbaFramework = dict[str, SocietalBenefitArea]

# International Arctic Observations Assessment Framework
#     https://www.arcticobserving.org/images/pdf/misc/STPI-SAON-International-Arctic-Observations-Framework-Report-2017.pdf
IAOA_SBA_FRAMEWORK: IaoaSbaFramework = {
    'Disaster Preparedness': {
        'Disaster Mitigation': [
            'Apply common indices and indicators to inform'
            ' disaster mitigation activities',
            'Develop educationtrainingand compliance procedures'
            ' for disaster mitigation',
            'Ensure access to disaster-relevant environmental intelligence',
            'Inform infrastructure design standards for disaster mitigation',
        ],
        'Disaster Protection and Prevention': [
            'Apply common indices and indicators to assess'
            ' state of disaster preparedness',
            'Conduct risk assessments to inform disaster preparedness activities',
            'Deploy emergency responder personnel and equipment in an optimal'
            ' manner prior to a disaster',
            'Develop and execute plans and procedures for disaster prevention',
            'Improve emergency preparedness for human-made hazards',
            'Improve emergency preparedness for natural hazards',
        ],
        'Disaster Recovery': [
            'Conduct damage assessments to inform disaster recovery',
            'Improve future disaster preparedness activies',
            'Inform social, economic, and cultural post-disaster recovery',
            'Support disaster aid planning and deployment',
        ],
        'Disaster Response': [
            'Conduct disaster response operations in a timely and'
            ' cost-effective manner',
            'Conduct search and rescue operations in a safe and effective manner',
            'Deploy emergency responder personnel and equipment in an optimal'
            ' manner during and after a disaster',
            'Ensure domain awareness for disaster response',
        ],
        'Hazard Identification and Disaster Prediction': [
            'Develop and maintain analytical capabilities for hazard'
            ' identification and disaster prediction',
            'Ensure domain awareness for identification and prediction'
            ' of all hazards',
            'Improve understanding of Earth systems to inform hazard'
            ' identification and disaster prediction',
        ],
    },
    # TODO: Populate societal benefit sub-areas and their key objectives
    'Environmental Quality': {
        'Drivers of Environmental Impacts': [
            'Improve ability to identify environmental impact thresholds'
            ' and predict their consequences',
            'Improve understanding of climate as a driver of changing'
            ' environmental quality',
            'Manage regional and local human activities in the Arctic'
            ' to mitigate environmental impact',
            'Reduce the source of transboundary and local pullutants' ' in the Arctic',
        ],
        'Environmental Impacts': [
            'Adapt to and mitigate the impacts of climate change on'
            ' ecosystems and human health',
            'Improve understanding of the impacts of climate change'
            ' on ecosystems and human health',
            'Manage the environmental impacts of increased human'
            ' activities in the Arctic',
            'Mitigate the impacts of pollutants on ecosystems and human health',
            'Understand the impacts of pollutants on the energy balance and'
            ' the effects on the cryosphere',
        ],
        'Quality of Ecosystem Functions': [
            'Ensure the availability of freshwater suitable for human use'
            ' and ecosystem function',
            'Improve the understanding and function of habitats in the Arctic',
            'Improve understanding of the value proposition of ecosystem'
            ' sevices in the Arctic',
            'Maintain ecosystem quality, diversity, and extent to ensure the'
            ' delivery of ecosystem functions and services',
        ],
    },
    'Food Security': {
        'Accesible Available and Sustainable Food': [
            'Enhance resilience to changes in Arctic climate and ecosystems'
            ' that affect access to food',
            'Ensure continued access to and viability of hunting, fishing,'
            ' and gathering activ ities in the Arctic',
            'Improve stewardship of fisheries and animal stocks in an'
            ' environmentally sustainable manner',
            'Improve understanding of land use on sustainable stewardship'
            ' of food resources',
            'Improve understanding of the energy demands associated with'
            ' the Arctic food supply chain',
            'Improve understanding of the impacts of climate change on hunting'
            ' and fishing in the Arctic',
            'Improve understanding of the impacts of climate change on the Arctic'
            ' food supply chain',
            'Understand and coordinate institutional arrangements affecting the'
            ' availability, accessibility, and sustainability of food',
        ],
        'Exchange of Food': [
            'Ensure continued operation of transportatoin and shipping activities'
            ' for food exhange',
            'Improve understanding of formal and informal exchange networks to'
            ' assess the use of food beyond its currency value',
            'Understanding and coordinate food exchange regulations and activities'
            ' to mitigate resource scarcity and overabundance',
        ],
        'Safe Food': [
            'Ensure food supplies do not exceed minimum pollutant thresholds',
            'Ensure the safety and storage of food supplies under changing'
            ' environmental conditions',
            'Improve the quality of and access to information about the'
            ' availability and safety of food',
            'Improve understanding of the nutritional quality of food in the Arctic',
            'Improve understanding of the nutritional requirements of Arctic'
            ' populations',
            'Understand and coordinate institutional arrangements affecting food'
            ' safety',
        ],
    },
    'Fundamental Understanding of Arctic Systems': {
        'Linkages, Interactions, and Feedback among Arctic Subsystems': [
            'Improve ability to scale projections, models, and information'
            ' related to components of the Arctic system',
            'Improve systems-level understanding by identifying predictability'
            ' limits for the Arctic system',
            'Improve Understanding of processes, variables, and rates of change'
            ' in components of the Arctic system, including the cryosphere',
        ],
        'Linkages, Interactions and Feedback between Arctic Subsystems'
        ' and Global Systems': [
            'Improve understanding of anthropogenic influences on Arctic change',
            'Improve understanding of Arctic amplification of global warming',
            'Improve understanding of the impacts of biologic drivers on the'
            ' Arctic system',
            'Improve understanding of the impacts of socioeconomic drivers on'
            ' the Arctic system',
            'Improve understanding of the relationship between Arctic and global'
            ' atmospheric and oceanic processes',
        ],
    },
    'Human Health': {
        'Mental Health': [
            'Improve understanding of mental health determinants of Arctic residents',
            'Improve understanding of the risks and benefits of climatic and'
            ' environmental changes on community, household, and individual mental'
            ' health',
            'Mitigate the impacts of climatic and environmental changes on community,'
            ' household, and individual mental health',
            'Promote community, household, and individual mental health through'
            ' adaptation to climatic and environmental changes',
        ],
        'Physical Health': [
            'Improve understanding of physical health determinants of Arctic residents',
            'Improve understanding of the risks and benefits of climatic and'
            ' environmental changes on community, household, and individual'
            ' physical health',
            'Mitigate the impacts of climatic and environmental changes on'
            ' community, household, and individual physical health',
            'Promote community, household, and inidivdual physical health'
            ' through adaptation to climatic and environmental changes',
        ],
        'Public Health': [
            'Ensure access to health care and health promotion services',
            'Improves acces to clean water and sanitation infastructure',
            'Improve early warning systems for impending public health emergencies',
            'Improve synthesis of health- and environmental health-related'
            ' knowledge across Arctic cultures',
            'Improve understanding of epidemiology and health behaviors'
            ' in the Arctic to inform public health policies and strategies',
            'Improve understanding of influences of climatic and environmental'
            ' changes on emerging infectious diseases in the Arctic',
            'Reduce presence of foodborne pathogens and contaminants in Arctic food'
            ' supplies',
        ],
    },
    'Infrastructure and Operations': {
        'Planning of Infrastructure': [
            'Ensure safe and secure infrastructure design',
            'Improve understanding of the impacts of infrastructure on the'
            ' environment, human systems, and society',
            'Support infrastructure design siting',
        ],
        'Development of Infrastructure': [
            'Ensure compliance with infrastructure codes and'
            ' environmental regulations',
            'Inform and support construction and quality assurance'
            ' and control activities',
        ],
        'Operations and Maintenance of Infrastructure': [
            'Ensure safe and secure infrastructure operations',
            'Improve understanding of environmental effects on'
            ' infrastructure operations',
            'Maintain awareness and provide predictive capabilities'
            ' to support safe operation of infrastructure',
            'Maintain operational awareness of infrastructure systems',
            'Support economic optimization of operations',
        ],
        'Decommissioning of Infrastructure': [
            'Dispose of infrastructure materials or assets that cannot be re-utilized',
            'Identify opportunities for re-utilization of infrastructure system assets',
            'Improve understanding of long-term impacts of decommissioned'
            ' infrastructure systems on Arctic communities and the environment',
            'Inform decisions regarding re-utilization and disposition'
            ' of infrastructure systems',
        ],
    },
    'Marine and Coastal Ecosystems and Processes': {
        'Marine and Coastal Ecosystem Biodiversity': [
            'Identify and preserve culturally important marine and coastal areas',
            'Identify and preserve ecologically sensitive marine and coastal'
            ' areas for biodiversity',
            'Identify and understand the diversity of Arctic biota throughout'
            ' their ranges',
            'Manage and preserve Arctic biota throughout their ranges',
            'Promote resilience and sustainability of Arctic biodiversity'
            ' in marine and coastal ecosystems',
        ],
        'Marine and Coastal Ecosystem Changes': [
            'Improve understanding of impacts of environmental change on'
            ' Arctic marine and coastal ecosystems',
            'Improve understanding of ecological and evolutionary responses'
            ' of marine and coastal organisms to changes in the Arctic',
            'Inform human adaptation to ecosystem changes',
            'Manage disturbances to marine and coastal ecosystems',
        ],
        'Marine and Coastal Living Resources': [
            'Characterize and assess the status and trends of Arctic'
            ' and migratory living resources',
            'Manage Arctic and migratory living resources in a sustainable manner',
            'Sustain marine bioprospecting in the Arctic',
        ],
        'Marine and Coastal Processes': [
            'Asses the impact of changing hydrologic and cryospheric'
            ' conditions on marine and coastal ecosystems',
            'Improve decision making for responses to changes in'
            ' marine and coastal conditions',
            'Improve understanding of physical oceanography, ocean'
            ' biogeochemistry, and their interactions',
        ],
    },
    'Natural Resources': {},
    'Resilient Communities': {},
    'Sociocultural Services': {},
    'Terrestrial and Freshwater Ecosystems and Processes': {},
    'Weather and Climate': {},
}
