.PHONY: install-claude install-claude-project build-plugin package-desktop validate-skills

install-claude:
	python3 scripts/install_claude_skills.py --scope user --force

install-claude-project:
	python3 scripts/install_claude_skills.py --scope project --force

build-plugin:
	python3 scripts/build_claude_plugin.py

package-desktop:
	python3 scripts/package_claude_desktop.py

validate-skills:
	python3 scripts/validate_skills.py
