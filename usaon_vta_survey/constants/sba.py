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
        # TODO: Finish this SBA
    },
    # TODO: Populate societal benefit sub-areas and their key objectives
    'Environmental Quality': {},
    'Food Security': {},
    'Fundamental Understanding of Arctic Systems': {},
    'Human Health': {},
    'Infrastructure and Operations': {},
    'Marine and Coastal Ecosystems and Processes': {},
    'Natural Resources': {},
    'Resilient Communities': {},
    'Sociocultural Services': {},
    'Terrestrial and Freshwater Ecosystems and Processes': {},
    'Weather and Climate': {},
}
