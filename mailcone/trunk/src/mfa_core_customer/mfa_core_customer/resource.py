from fanstatic import Library, Resource
from js.jquery import jquery

library = Library('mfa_core_customer', 'static')

popupJs = Resource(library, 'popup.js', depends=[jquery])
popupCss = Resource(library, 'popup.css')