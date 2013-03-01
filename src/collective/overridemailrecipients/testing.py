from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.testusermailpatch


OPSB_CONTENT = PloneWithPackageLayer(
    zcml_package=collective.testusermailpatch,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.testusermailpatch:testing',
    name="OPSB_CONTENT")

OPSB_CONTENT_INTEGRATION = IntegrationTesting(
    bases=(OPSB_CONTENT, ),
    name="OPSB_CONTENT_INTEGRATION")

OPSB_CONTENT_FUNCTIONAL = FunctionalTesting(
    bases=(OPSB_CONTENT, ),
    name="OPSB_CONTENT_FUNCTIONAL")
