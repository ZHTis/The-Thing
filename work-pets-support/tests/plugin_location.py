"""Resolve the installed official plugin explicitly; never fall back to hatch-pet."""
import os
from pathlib import Path


def plugin_skill_dir():
    configured = os.environ.get('WORK_PETS_CREATE_SKILL_DIR')
    if configured:
        directory = Path(configured).expanduser().resolve()
    else:
        cache = Path.home() / '.codex/plugins/cache'
        matches = list(cache.glob('*/work-pets/*/skills/create-pet'))
        if len(matches) != 1:
            raise RuntimeError('Set WORK_PETS_CREATE_SKILL_DIR to the active official work-pets create-pet directory')
        directory = matches[0].resolve()
    required = ['SKILL.md', 'scripts/validate_atlas.py', 'scripts/assemble_extended_atlas.py', 'scripts/despill_chroma_edges.py',
                'scripts/validate_direction_blind_verdicts.py', 'scripts/measure_direction_continuity.py',
                'scripts/make_direction_blind_qa_sheet.py', 'scripts/combine_direction_blind_verdicts.py']
    missing = [name for name in required if not (directory / name).is_file()]
    if missing:
        raise RuntimeError('The selected work-pets installation is incomplete: ' + ', '.join(missing))
    return directory
