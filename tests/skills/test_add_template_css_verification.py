"""rolesherpa-add-template/SKILL.md Step 1 explicitly accepts a source
that is "HTML plus a CSS file", but its Step 4 mandatory test-render
never passed --css to `render pdf` - so a template with external CSS
could pass the mandatory verification gate without its real styling
ever being applied.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ADD_TEMPLATE = REPO_ROOT / ".agents" / "skills" / "rolesherpa-add-template" / "SKILL.md"


def test_step_4_render_command_can_pass_css():
    text = ADD_TEMPLATE.read_text()
    step4_start = text.index("Step 4")
    step4_text = text[step4_start:step4_start + 1200]
    assert "--css" in step4_text
