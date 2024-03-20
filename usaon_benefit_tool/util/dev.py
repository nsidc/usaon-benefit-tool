from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.models.tables import User

# This user will be used when login is disabled. It will be inserted if login is
# disabled at init time.
DEV_USER = User(
    id=0,
    email="dev_user@example.com",
    name="Dev User",
    orcid="junk",
    role_id=RoleName.ADMIN,
)
TEST_USER = User(
    email="test_user@example.com",
    name="Test User",
    orcid="junk",
    role_id=RoleName.ADMIN,
)
