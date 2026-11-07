"""Names for the existing hand-drawn icons, in grid order (non-empty cells only)."""
ARROWS = """arrow-up-narrow arrow-down-narrow arrow-right-narrow arrow-left-narrow arrow-up arrow-down arrow-right arrow-left chevron-up chevron-down
chevron-right chevron-left chevron-up-small chevron-down-small chevron-right-small chevron-left-small arrow-up-circle arrow-down-circle arrow-right-circle arrow-left-circle
chevron-up-circle chevron-down-circle chevron-right-circle chevron-left-circle arrow-up-square arrow-down-square arrow-right-square arrow-left-square chevron-up-square chevron-down-square
chevron-right-square chevron-left-square triangle-up triangle-down triangle-right triangle-left chevrons-right chevrons-left chevrons-down chevrons-up
arrows-horizontal arrows-vertical corner-up-right corner-up-left undo reply-all arrows-exchange move minimize maximize
expand-diagonal navigation rotate-cw refresh download upload shuffle
log-in log-out""".split()

UI = """plus-circle x-circle minus-circle info-circle alert-circle help-circle check-circle check-circle-alt circle power
plus-square x-square minus-square info-square alert-square help-square check-square check-square-alt square transform
alert-triangle triangle ban play stop record pause
x plus minus check menu sliders-horizontal sliders-vertical more-horizontal more-vertical
share-square share share-nodes pencil redo-square external-square external-link trash lock unlock
toggle-on toggle-off thumbs-up thumbs-down droplet tag tags ruler edit-square percent-square
sort-alpha-up sort-alpha-up-reverse sort-numeric-up sort-numeric-up-reverse sort-amount-up sort-amount-down search zoom-in zoom-out search-location
sort-alpha-down sort-alpha-down-reverse sort-numeric-down sort-numeric-down-reverse sort-lines-up sort-lines-down search-dollar send clipboard-copy paperclip
list list-ordered list-checks hourglass fingerprint flag filter door-open door-closed bookmark
message-square messages""".split()

assert len(ARROWS) == 59 and len(UI) == 88, (len(ARROWS), len(UI))
