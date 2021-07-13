# from .forms import UserForms
# from .model import UserTestCase
# from .newsletter import NewsletterLogic
# from .views import UserViews
from .helper_functions import HelperFunctionsTestCase
from .mail import UsersMailTestCase
from .model import ProfileTestCase

# __all__ = ["UserForms", "UserTestCase", "UserViews", "NewsletterLogic"]
__all__ = ["HelperFunctionsTestCase", "UsersMailTestCase", "ProfileTestCase"]
