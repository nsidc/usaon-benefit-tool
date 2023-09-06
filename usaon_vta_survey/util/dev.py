from usaon_vta_survey.models.tables import User

# This user will be used when login is disabled. It will be inserted if login is
# disabled at init time.
DEV_USER = User(
    id=0,
    email="test_user@example.com",
    name="Test User",
    orcid="junk",
    role_id="admin",
)
