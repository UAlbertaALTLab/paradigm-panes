"""
Handles paradigm generation.
"""

from manager import (
    ParadigmManager,
    ParadigmManagerWithExplicitSizes,
)
from hfst_optimized_lookup import TransducerFile

import settings

# MAYBE ?
FST_DIR = settings.BASE_DIR / "resources" / "fst"
SHARED_RES_DIR = settings.BASE_DIR / "res"

def default_paradigm_manager() -> ParadigmManager:
    """
    Returns the ParadigmManager instance that loads layouts and FST from the res
    (resource) directory for the crk/eng language pair (itwêwina).

    Affected by:
      - MORPHODICT_PARADIGM_SIZE_ORDER
    """

    # TODO combine into 1 dir, since not operating on 5 different resources
    # Shared res dir
    layout_dir = SHARED_RES_DIR / "layouts"

    # site specific resources directory
    site_specific_layout_dir = settings.BASE_DIR / "resources" / "layouts"
    if site_specific_layout_dir.exists():
        layout_dir = site_specific_layout_dir

    generator = strict_generator()

    if hasattr(settings, "MORPHODICT_PARADIGM_SIZES"):
        return ParadigmManagerWithExplicitSizes(
            layout_dir,
            generator,
            ordered_sizes=settings.MORPHODICT_PARADIGM_SIZES,
        )
    else:
        return ParadigmManager(layout_dir, generator)

def strict_generator():
    return TransducerFile(FST_DIR / settings.STRICT_GENERATOR_FST_FILENAME)
