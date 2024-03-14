from typing import Final

# NOTE: element 0 is the default value. Keep that in mind when altering the list.
ASSESSMENT_STATUSES: Final[dict[str, str]] = {
    'work in progress': 'The assessment is not done yet',
    'published': 'The assessment is complete and visible to the public',
    'closed': 'TODO',
    'archived': 'TODO',
}
