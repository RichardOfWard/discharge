import os
from discharge.site import Site

site = Site(
    source_path=os.path.dirname(__file__),
    build_path=os.path.dirname(__file__) + '/_build',
)
