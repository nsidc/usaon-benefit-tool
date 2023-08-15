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
    'Human Health': {},
    'Infrastructure and Operations': {},
    'Marine and Coastal Ecosystems and Processes': {},
    'Natural Resources': {},
    'Resilient Communities': {},
    'Sociocultural Services': {},
    'Terrestrial and Freshwater Ecosystems and Processes': {},
    'Weather and Climate': {},
}
