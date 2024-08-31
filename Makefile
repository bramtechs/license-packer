README.md: license-packer.py README.base.md
	cat README.base.md > README.md
	python3 ./license-packer.py --help >> README.md
	echo \`\`\` >> README.md

.PHONY: teset
test:
	python3 license-packer.py ~/dev/vortex2 out.html --default-ignore --ignore parser projects --warn-gpl
