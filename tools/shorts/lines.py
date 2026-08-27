"""
The spoken lines, written to sound natural first. Timing is fitted to the speech afterwards,
never the other way round. Contractions, full units ("percent", "dollars"), and real commas
all matter: stripping them to save a tenth of a second is what makes TTS gabble.
"""

V1 = [
    "Twenty five percent off twice is not fifty percent off.",
    "The coupon comes off the sale price, not the tag.",
    "An eighty dollar sweater. Sixteen squares, five dollars each.",
    "The sale takes a quarter off. Twenty dollars gone, sixty left.",
    "The coupon takes a quarter of sixty. That's fifteen, not twenty.",
    "So you pay forty five. Same percent, but a smaller chunk.",
    "And look, that's only one square past half.",
    "You paid seventy five percent, of seventy five percent.",
    "That's forty three point seven five percent off. Not fifty.",
    "Keep stacking coupons, and the price never hits zero.",
]

V2 = [
    "One eighteen inch pizza is more pizza than two twelve inch pizzas.",
    "Pizza is sold by the diameter, the distance straight across.",
    "But area is not proportional to the diameter.",
    "Proportional would mean that doubling one doubles the other.",
    "Area does not do that. Double the width and you get four times the pizza.",
    "Area is proportional to the radius squared, and the radius is half the diameter.",
    "So nine inches for the big one, and six for the small ones.",
    "The formula is pie r squared, so the big one is eighty one pie.",
    "Each small one is thirty six pie, and two of them only make seventy two.",
    "Pour them both in, and it still does not fill.",
    "Nine pie is left over, which is exactly one ninth of the big pizza.",
    "The width grew by half, but area squares that, so you get two point two five times as much.",
]

V3 = [
    "One, two, four, eight, sixteen.",
    "Say the next number out loud.",
    "You said thirty two.",
    "It's thirty one.",
    "These numbers count regions inside a circle.",
    "Put dots on the edge, and join every pair.",
    "One dot, one region. Two dots, two.",
    "Three dots, four. Four dots, eight. Five dots, sixteen.",
    "Now six dots. That's fifteen chords.",
    "Count the pieces.",
    "You get thirty one, not thirty two.",
    "Here's why.",
    "Start with one region. Every chord adds one.",
    "And every crossing adds one more.",
    "One plus fifteen plus fifteen is thirty one.",
    "Five terms is not a proof.",
]


# --- 4. average speed. 210 miles each way makes both legs whole hours.
V4 = [
    "You drive out at thirty miles an hour, and come back at seventy.",
    "Your average speed is not fifty.",
    "Say the trip is two hundred and ten miles each way.",
    "At thirty, the drive out takes seven hours.",
    "At seventy, the drive back takes only three.",
    "So you spent seven hours going slow, and three going fast.",
    "That's four hundred and twenty miles, in ten hours.",
    "Forty two miles an hour.",
    "The slow half eats more of your time, so it pulls harder on the average.",
]

# --- 5. 0.999... = 1
V5 = [
    "Zero point nine repeating is not almost one.",
    "It is one. Same number, two spellings.",
    "Here's the proof. Let x be zero point nine repeating.",
    "Then ten x is nine point nine repeating.",
    "Subtract x from both sides. The tails cancel exactly.",
    "Nine x equals nine. So x equals one.",
    "If these were different numbers, something would sit between them.",
    "Name it. You can't.",
    "There is no gap, so there are not two numbers.",
]

# --- 6. PEMDAS
V6 = [
    "Forty eight, divided by two, times three.",
    "If you said eight, PEMDAS lied to you.",
    "You were taught six letters, so you assumed six steps.",
    "But multiply and divide are not two ranks. They are one.",
    "Dividing by two is multiplying by a half. Same operation.",
    "So you work left to right. Forty eight over two is twenty four.",
    "Twenty four times three is seventy two.",
    "Add and subtract behave the same way.",
    "It is four levels, not six.",
]



# --- 7. an exponent outside a bracket hits every factor inside. (2x)^3 = 8x^3, not 2x^3.
V7 = [
    "Two x, all cubed. Most people write two x cubed.",
    "That is wrong. The cube lands on the two as well.",
    "Two x cubed means two x, times two x, times two x.",
    "Three twos multiply to eight. Three x's make x cubed.",
    "So the answer is eight x cubed.",
    "Check it. Put x equal to five.",
    "Two times five is ten, and ten cubed is a thousand.",
    "But two times five cubed is only two hundred and fifty.",
    "Four times too small, because the two never got cubed.",
]

# --- 8. squares end only in 0,1,4,5,6,9
V8 = [
    "No square number has ever ended in seven.",
    "And none ever will.",
    "The last digit of a square depends only on the last digit you started with.",
    "So there are just ten cases to check.",
    "Zero, one, four, nine, six, five, six, nine, four, one.",
    "That is every ending a square can have.",
    "Zero, one, four, five, six, and nine.",
    "Two, three, seven and eight never show up.",
    "Ten cases, and you have covered every number there is.",
]

# --- 9. down 20 then up 20 lands at 96, not 100
V9 = [
    "Down twenty percent, then up twenty percent.",
    "You do not end up where you started.",
    "Start at one hundred. Twenty percent off leaves eighty.",
    "Now add twenty percent of eighty.",
    "That is sixteen, not twenty.",
    "You land on ninety six.",
    "Four percent down.",
    "The rise was smaller because it grew from a smaller number.",
    "Swap the order and you still get ninety six.",
]

# --- 10. undoing a 20% cut takes a 25% raise, since 0.8 x 1.25 = 1 exactly
V10 = [
    "A twenty percent pay cut takes a twenty five percent raise to undo.",
    "Not twenty.",
    "Say you earn fifty thousand.",
    "A twenty percent cut takes ten thousand off. You are on forty.",
    "A twenty percent raise on forty gives you eight thousand back.",
    "That is forty eight, not fifty.",
    "To get back you need ten thousand on top of forty.",
    "And ten out of forty is twenty five percent.",
    "The cut and the raise are measured against different numbers.",
]

V11 = [
    "A test for a disease is ninety seven percent accurate.",
    "You test positive. What are the odds you actually have it?",
    "Almost everyone says ninety seven percent. It's about three.",
    "The catch is that the disease is rare. One person in a thousand.",
    "So line up a hundred thousand people.",
    "A hundred of them have it, and ninety seven of those test positive.",
    "The other ninety nine thousand nine hundred are healthy, but the test is wrong three percent of the time. Nearly three thousand of them test positive too.",
    "Everyone with a positive result steps forward. Three thousand and ninety four people.",
    "Only ninety seven are actually sick. That is three point one percent.",
    "A test can be accurate and still be mostly false alarms, when the thing it hunts for is rare.",
]

SETS = {"v1": V1, "v2": V2, "v3": V3, "v4": V4, "v5": V5, "v6": V6,
        "v7": V7, "v8": V8, "v9": V9, "v10": V10, "v11": V11}
