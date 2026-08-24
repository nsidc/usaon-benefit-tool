from typing import Final

# NOTE: element 0 is the default value. Keep that in mind when altering the list.
ASSESSMENT_STATUSES: Final[dict[str, str]] = {
    'work in progress': 'The assessment is not done yet',
    'published': 'The assessment is complete and visible to the public',
    'private': 'Complete but not available for viewing publicly',
    'archived': 'data saved but not available for viewing. Admins can still review.',
}
