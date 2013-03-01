from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.overridemailrecipients

TEST_LAYER = PloneWithPackageLayer(
    zcml_package=collective.overridemailrecipients,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.overridemailrecipients:testing',
    name="TEST_LAYER")

TEST_LAYER_INTEGRATION = IntegrationTesting(
    bases=(TEST_LAYER, ),
    name="TEST_LAYER_INTEGRATION")

TEST_LAYER_FUNCTIONAL = FunctionalTesting(
    bases=(TEST_LAYER, ),
    name="TEST_LAYER_FUNCTIONAL")
