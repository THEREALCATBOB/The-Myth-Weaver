import random

TEXT_VARIANTS = {

    # =========================================================
    # SYSTEM / META
    # =========================================================

    "start_message": [
        "The world exhales as you open your eyes.",
        "You wake to the sound of distant wind and unseen wings.",
        "A quiet breath of the wild greets your first step.",
        "The land has been waiting for someone to wander it again.",
        "You arrive in a world that feels half-remembered, half-dreamed.",
        "Somewhere, something ancient stirs as you begin.",
        "Your story does not start here—but this is where you remember it.",
        "The horizon leans in, as if curious about you.",
        "A faint tremor runs through the ground, welcoming or warning.",
        "The silence feels expectant, like a held breath.",
        "You step into a world that has not forgotten how to feel.",
        "The wilds shift, acknowledging your arrival.",
        "A soft breeze brushes past, carrying the scent of possibility.",
        "You sense the world watching, patient and old.",
        "Something unseen whispers: *Begin.*",
    ],

    "quit": [
        "You turn away from the wilds—for now.",
        "The world grows quiet as your footsteps fade.",
        "You leave the land to its own stories.",
        "The wind carries away the last trace of your presence.",
        "You step out of the tale, but it keeps moving without you.",
        "The horizon closes its eyes as you depart.",
        "The silence settles back into place.",
        "The world exhales, returning to its slow dreaming.",
        "You retreat from the wilds, but they remember you.",
        "Your absence echoes softly across the land.",
    ],

    "error_generic": [
        "Something feels off, like a page missing from a story.",
        "The world hesitates, unsure what you meant.",
        "A strange silence answers you.",
        "Nothing responds. Perhaps try again.",
        "The wilds tilt their head, confused.",
    ],

    "misc_acknowledge": [
        "The world shifts slightly.",
        "A faint breeze answers.",
        "Something unseen stirs.",
        "The land listens.",
        "A quiet moment passes.",
    ],


    # =========================================================
    # WORLD / ROOM DESCRIPTION
    # =========================================================

    "room_title": [
        "{name}",
        "— {name} —",
        "{name}, where the air feels different.",
        "{name}, a place that remembers old footsteps.",
        "{name}, carved into the wilds.",
        "{name}, quiet but not empty.",
        "{name}, where stories linger.",
        "{name}, wrapped in the breath of the land.",
    ],

    "enter_room": [
        "You step into {name}.",
        "You cross an unseen threshold and arrive at {name}.",
        "Your path leads you into {name}.",
        "The world shifts as you enter {name}.",
        "You find yourself standing in {name}.",
        "A subtle change in the air marks your arrival at {name}.",
        "Your footsteps echo softly as you enter {name}.",
        "The land opens before you: {name}.",
        "A quiet tension greets you in {name}.",
        "You feel eyes—real or imagined—watching as you enter {name}.",
    ],

    "biome_effect": [
        "The {biome} presses in on you, testing your endurance.",
        "You feel the {biome} working against you in subtle ways.",
        "The {biome} is not kind to the unprepared.",
        "Every step in this {biome} seems to cost a little more strength.",
        "The {biome} whispers warnings you can’t quite decipher.",
        "The {biome} feels heavier here, as if aware of you.",
        "A quiet pressure settles over you in the {biome}.",
        "The {biome} watches, patient and old.",
    ],

    "warning": [
        "A quiet unease settles in your chest.",
        "Something feels wrong, just out of sight.",
        "Your instincts whisper that you should be careful.",
        "The air feels heavier, as if watching you.",
        "A faint tension prickles at the back of your neck.",
        "You sense movement where there should be none.",
        "The world holds its breath.",
        "A subtle dread coils in your stomach.",
        "The silence feels too deliberate.",
        "You feel the weight of unseen eyes.",
    ],


    # =========================================================
    # REST / RECOVERY
    # =========================================================

    "rest": [
        "You find a moment of stillness and let your body relax.",
        "You settle in, letting time blur as you rest.",
        "You close your eyes and let the world fade for a while.",
        "You take shelter in the moment, letting fatigue slip away.",
        "You breathe deeply, grounding yourself in the quiet.",
        "You allow your muscles to loosen, tension melting away.",
        "You rest, letting the world drift to the edges of your awareness.",
        "You pause, letting exhaustion ebb slowly.",
        "You sink into a brief, welcome calm.",
        "You let your guard down—just for a moment.",
    ],

    "rest_recover": [
        "You feel your strength returning.",
        "Your muscles ache less than before.",
        "Your thoughts sharpen as exhaustion loosens its grip.",
        "You rise feeling a little more whole.",
        "A renewed steadiness settles into your limbs.",
        "Your breath feels easier, your steps lighter.",
        "A quiet resilience returns to your body.",
        "You feel steadier, more anchored.",
        "Your fatigue fades like mist in sunlight.",
        "You stand, restored enough to continue.",
    ],


    # =========================================================
    # WORLD AMBIENCE (SUBTLE FLAVOR)
    # =========================================================

    "world_ambience": [
        "A distant sound echoes across the land.",
        "The wind shifts, carrying a faint scent you can’t place.",
        "Something rustles far away, then goes still.",
        "The air hums with quiet life.",
        "A soft breeze brushes past your cheek.",
        "The ground vibrates with a subtle, rhythmic pulse.",
        "A shadow moves at the edge of your vision.",
        "The silence deepens, rich and layered.",
        "A faint tremor runs beneath your feet.",
        "The world feels watchful, but not hostile.",
        "A bird calls once, then falls silent.",
        "Leaves whisper secrets you can’t quite hear.",
        "The horizon flickers with distant movement.",
        "A strange calm settles over the area.",
        "You feel the land breathing around you.",
        "A soft crackle of energy tingles in the air.",
        "Something unseen shifts its attention.",
        "The wilds murmur in a language older than memory.",
        "A faint metallic scent lingers in the breeze.",
        "The world feels poised, as if waiting.",
    ],
    # =========================================================
    # BIOME FLAVOR — FOREST
    # =========================================================

    "biome_forest": [
        "The forest hums with quiet, watchful life.",
        "Branches knit together overhead, turning the sky into a rumor.",
        "Every rustle in the undergrowth feels like a held breath.",
        "The scent of moss and bark clings to the air.",
        "A distant bird call echoes, sharp and lonely.",
        "The forest floor muffles your steps like it’s listening.",
        "Sunlight filters through leaves in trembling shards.",
        "Shadows move where nothing should be moving.",
        "The trees stand like ancient guardians, patient and stern.",
        "A soft crackle of twigs hints at unseen company.",
        "The forest feels alive in a way that isn’t entirely comforting.",
        "A breeze stirs the canopy, whispering secrets overhead.",
        "The air tastes green, damp, and old.",
        "Something scurries out of sight before you can look.",
        "The forest watches, but does not judge.",
    ],


    # =========================================================
    # BIOME FLAVOR — PLAINS
    # =========================================================

    "biome_plains": [
        "The plains roll out like an endless, breathing sea.",
        "Wind races across the grass, whispering secrets you can’t quite catch.",
        "The sky feels impossibly wide above the open land.",
        "Distant shapes move like ghosts along the horizon.",
        "The grass sways in long, rhythmic waves.",
        "A hawk circles overhead, silent and precise.",
        "The plains stretch so far they feel unreal.",
        "Your footsteps vanish into the vastness.",
        "The wind carries scents from miles away.",
        "The land feels open, honest, and a little lonely.",
        "A distant rumble hints at herds on the move.",
        "The horizon shimmers with heat and possibility.",
        "The plains breathe with slow, steady patience.",
        "You feel small beneath the endless sky.",
        "The world feels wider here than anywhere else.",
    ],


    # =========================================================
    # BIOME FLAVOR — SWAMP
    # =========================================================

    "biome_swamp": [
        "The swamp clings to your boots and your thoughts.",
        "The air is thick, heavy, and full of unseen things.",
        "Water and mud blur the line between ground and depth.",
        "Every step feels like an intrusion into something ancient.",
        "A chorus of insects rises and falls like a fever dream.",
        "The swamp smells of rot, life, and secrets.",
        "Shadows ripple across the water’s surface.",
        "Something bubbles beneath the murk, then goes still.",
        "The air hums with a low, unsettling vibration.",
        "The swamp feels alive in a way that watches you back.",
        "Mist coils around twisted roots like pale fingers.",
        "The ground squelches with every reluctant step.",
        "You hear movement, but the water hides everything.",
        "The swamp breathes in slow, wet sighs.",
        "A strange heaviness settles over your shoulders.",
    ],


    # =========================================================
    # BIOME FLAVOR — MOUNTAIN
    # =========================================================

    "biome_mountain": [
        "The mountains loom like sleeping giants around you.",
        "Cold air bites at your lungs with every breath.",
        "Stone and sky meet in jagged, unforgiving lines.",
        "The wind howls between the rocks like a living thing.",
        "Loose gravel shifts underfoot with quiet menace.",
        "The air is thin, sharp, and honest.",
        "Echoes bounce strangely between the cliffs.",
        "The mountains feel ancient, indifferent, and immense.",
        "A distant rumble hints at shifting stone.",
        "Your breath fogs in the cold, brittle air.",
        "The climb feels like a test the mountain set for you.",
        "Shadows stretch long across the ridges.",
        "The world feels sharper at this altitude.",
        "A lone bird cries somewhere far above.",
        "The mountain watches without blinking.",
    ],


    # =========================================================
    # BIOME FLAVOR — DESERT
    # =========================================================

    "biome_desert": [
        "The desert stretches out in shimmering waves of heat.",
        "Sand shifts underfoot, erasing your tracks as you walk.",
        "The sun presses down like a weight on your shoulders.",
        "The horizon wavers, uncertain and distant.",
        "A dry wind scrapes across the dunes.",
        "The desert feels empty, but never dead.",
        "Heat radiates from the ground in shimmering curtains.",
        "Your throat feels dry just looking at the landscape.",
        "The silence is vast enough to swallow thoughts.",
        "A lone dune crests like a frozen wave.",
        "The desert tests your resolve with every step.",
        "Shadows are short, sharp, and unforgiving.",
        "The air tastes of dust and sun-baked stone.",
        "The desert hides its secrets beneath endless sand.",
        "You feel exposed beneath the blazing sky.",
    ],


    # =========================================================
    # BIOME FLAVOR — TUNDRA (NEW)
    # =========================================================

    "biome_tundra": [
        "The tundra stretches out in a frozen, endless hush.",
        "Cold air stings your skin like tiny needles.",
        "Snow crunches beneath your feet with brittle finality.",
        "The wind sweeps across the land in long, mournful sighs.",
        "The tundra feels empty, but not uninhabited.",
        "Frost clings to every surface like a stubborn memory.",
        "The horizon is a pale, unbroken line.",
        "Your breath hangs in the air, refusing to leave.",
        "The cold feels alive, testing your resolve.",
        "A distant crack echoes across the ice.",
        "The tundra watches with quiet, frozen patience.",
        "Shadows stretch long across the snow.",
        "The world feels fragile beneath the frost.",
        "A faint glimmer hints at buried ice.",
        "The tundra whispers in the language of winter.",
    ],


    # =========================================================
    # BIOME FLAVOR — JUNGLE (NEW)
    # =========================================================

    "biome_jungle": [
        "The jungle presses in from all sides, vibrant and alive.",
        "Humidity clings to your skin like a second layer.",
        "Every sound is loud, sharp, and startlingly close.",
        "Vines twist overhead like living ropes.",
        "The air smells of earth, fruit, and hidden danger.",
        "Leaves drip with moisture, even without rain.",
        "The jungle hums with relentless, pulsing life.",
        "Shadows move with unsettling frequency.",
        "The canopy filters sunlight into shifting green patterns.",
        "Something calls out in the distance—once, then again.",
        "The jungle feels wild, hungry, and curious.",
        "Your footsteps vanish beneath the noise of life.",
        "The air vibrates with insect wings.",
        "A sudden rustle makes your heart jump.",
        "The jungle watches with bright, unblinking eyes.",
    ],


    # =========================================================
    # BIOME FLAVOR — VOLCANIC (NEW)
    # =========================================================

    "biome_volcanic": [
        "The ground radiates heat from deep beneath the surface.",
        "Ash drifts through the air like dark snow.",
        "The scent of sulfur stings your nose.",
        "Rocks glow faintly with trapped fire.",
        "The land trembles with distant, volcanic murmurs.",
        "Heat shimmers distort the landscape.",
        "Cracks in the earth pulse with molten light.",
        "The air tastes metallic and sharp.",
        "A low rumble vibrates through your bones.",
        "The volcanic terrain feels unstable, alive, and dangerous.",
        "Smoke coils upward in thin, ghostly trails.",
        "The ground feels warm even through your boots.",
        "A sudden hiss of steam escapes nearby fissures.",
        "The world here feels forged, not grown.",
        "The volcanic land watches with fiery indifference.",
    ],


    # =========================================================
    # BIOME FLAVOR — RUINS (NEW)
    # =========================================================

    "biome_ruins": [
        "Broken stone structures rise like the bones of forgotten giants.",
        "The ruins whisper of stories long buried.",
        "Shattered walls cast jagged shadows.",
        "The air feels thick with old memories.",
        "Vines crawl over crumbling stone.",
        "Every step echoes through abandoned halls.",
        "The ruins feel haunted—not by ghosts, but by time.",
        "Dust motes drift through shafts of pale light.",
        "A faint metallic scent lingers in the air.",
        "The silence feels reverent, like a temple long forgotten.",
        "Something ancient stirs beneath the rubble.",
        "The ruins watch with hollow, empty windows.",
        "A broken statue gazes at you with eroded eyes.",
        "The ground is uneven with collapsed stone.",
        "The ruins feel patient, waiting for someone to remember them.",
    ],


    # =========================================================
    # BIOME FLAVOR — COAST (NEW)
    # =========================================================

    "biome_coast": [
        "Waves crash rhythmically against the shore.",
        "Salt hangs in the air, sharp and refreshing.",
        "Seabirds cry overhead, circling lazily.",
        "The horizon stretches endlessly across the water.",
        "Foam hisses as waves retreat over wet sand.",
        "The wind carries the scent of distant storms.",
        "The sea glitters with shifting silver light.",
        "Your footsteps leave temporary marks in the sand.",
        "The coast feels open, wild, and restless.",
        "A distant ship silhouette drifts along the horizon.",
        "The tide pulls at the shore with steady insistence.",
        "The air tastes of salt and possibility.",
        "The sea murmurs in a language older than land.",
        "A cold spray of water brushes your face.",
        "The coast watches with a restless, wandering gaze.",
    ],


    # =========================================================
    # BIOME FLAVOR — DEEP FOREST (NEW)
    # =========================================================

    "biome_deep_forest": [
        "The deep forest swallows light whole.",
        "The air feels thick, ancient, and reverent.",
        "Roots twist like sleeping serpents beneath your feet.",
        "The silence is heavy, layered, and alive.",
        "Moss blankets everything in muted green.",
        "The trees tower impossibly high, older than memory.",
        "Shadows cling to the ground like living things.",
        "The deep forest feels sacred—and dangerous.",
        "A faint glow pulses between the trees.",
        "Your footsteps sound too loud in the stillness.",
        "The forest breathes in slow, deliberate rhythms.",
        "Something watches from the dark, patient and curious.",
        "The air tastes of earth, age, and quiet power.",
        "The deep forest holds secrets it will not share.",
        "You feel small beneath the ancient canopy.",
    ],


    # =========================================================
    # BIOME FLAVOR — CRYSTAL CAVERNS (NEW)
    # =========================================================

    "biome_crystal_caverns": [
        "Crystals jut from the walls, glowing with soft inner light.",
        "The air hums with faint, musical vibrations.",
        "Shards of light scatter across the cavern floor.",
        "Your footsteps echo with crystalline clarity.",
        "The caverns feel alive with quiet resonance.",
        "Colors shift subtly across the crystal surfaces.",
        "A faint chime rings out when you brush past a formation.",
        "The air tastes metallic and strangely sweet.",
        "Shadows fracture into prismatic shapes.",
        "The caverns glow like a dream half-remembered.",
        "A soft pulse of light travels through the walls.",
        "The crystals seem to watch with faceted eyes.",
        "The cavern feels sacred, humming with hidden energy.",
        "Your reflection stares back from a dozen angles.",
        "The air vibrates with quiet, ancient music.",
    ],


    # =========================================================
    # BIOME FLAVOR — CORRUPTED LANDS (NEW)
    # =========================================================

    "biome_corrupted_lands": [
        "The ground twists in unnatural patterns.",
        "The air tastes wrong—metallic, sharp, unsettling.",
        "Shadows move independently of their sources.",
        "The land pulses with sickly, shifting colors.",
        "A faint hum vibrates through your bones.",
        "The corrupted soil cracks beneath your feet.",
        "The world feels warped, bent by unseen forces.",
        "A low whisper echoes from nowhere and everywhere.",
        "The sky flickers with unnatural hues.",
        "The corrupted land watches with hungry intent.",
        "Your vision blurs at the edges, just for a moment.",
        "The air feels thick, heavy, and hostile.",
        "Something writhes beneath the surface.",
        "The land feels wounded—and angry.",
        "A quiet dread settles deep in your chest.",
    ],
    # =========================================================
    # WEATHER — CLEAR
    # =========================================================

    "weather_clear": [
        "The sky is clear, and the light feels sharp and honest.",
        "A calm, open sky watches over everything.",
        "The air is still, carrying only distant sounds.",
        "Sunlight spills across the land in warm, steady waves.",
        "A gentle breeze stirs, barely enough to move the grass.",
        "The world feels open and unguarded beneath the clear sky.",
        "Shadows fall clean and defined across the ground.",
        "The clarity of the air makes every detail feel sharper.",
        "The sky stretches endlessly, unmarred by cloud or storm.",
        "A quiet peace settles over the land under the clear sky.",
        "The sunlight feels almost gentle today.",
        "The horizon glows with soft, golden warmth.",
        "The world feels honest beneath the open sky.",
        "A faint shimmer of heat rises from the ground.",
        "The clear sky feels like a promise of calm.",
    ],


    # =========================================================
    # WEATHER — RAIN
    # =========================================================

    "weather_rain": [
        "Rain patters against the earth in a steady rhythm.",
        "Droplets bead on your gear and drip from your hair.",
        "The world smells of wet stone and fresh soil.",
        "A soft drizzle mutes the landscape.",
        "The rain falls in thin, silver threads.",
        "Puddles ripple with each falling drop.",
        "The air feels cool and clean beneath the rain.",
        "A gentle rain softens the edges of the world.",
        "The steady patter of rain is almost comforting.",
        "Mist rises where the rain meets warm ground.",
        "The rain blurs distant shapes into watercolor smudges.",
        "Your footsteps splash softly in the growing puddles.",
        "The rain whispers against leaves overhead.",
        "A faint chill settles into your clothes.",
        "The world feels quieter beneath the rain’s steady song.",
    ],


    # =========================================================
    # WEATHER — STORM
    # =========================================================

    "weather_storm": [
        "Thunder growls somewhere above, too close to ignore.",
        "Lightning splits the sky, turning shadows into stark shapes.",
        "The storm presses in, loud and insistent.",
        "Wind lashes at you with wild, unpredictable force.",
        "The sky churns with dark, roiling clouds.",
        "Rain slams against the ground in chaotic bursts.",
        "The storm feels alive, restless, and hungry.",
        "Thunder cracks like the world is tearing open.",
        "The wind howls with a voice that isn’t entirely natural.",
        "Lightning flickers across the sky in jagged veins.",
        "The storm’s fury rattles your bones.",
        "The air vibrates with electric tension.",
        "The storm roars, drowning out all other sound.",
        "A violent gust nearly knocks you off balance.",
        "The storm feels like a test of your resolve.",
    ],


    # =========================================================
    # WEATHER — FOG
    # =========================================================

    "weather_fog": [
        "Fog curls around your legs, hiding the ground.",
        "Shapes blur and soften, distance becoming a guess.",
        "The world feels smaller, wrapped in pale mist.",
        "Your breath mingles with the fog in faint wisps.",
        "The fog muffles sound, turning everything hushed.",
        "Shadows drift like ghosts through the mist.",
        "The fog clings to your clothes in cold tendrils.",
        "Visibility shrinks to a narrow, uncertain bubble.",
        "The fog feels thick enough to touch.",
        "Your footsteps sound strangely distant.",
        "The world fades to soft grays and muted outlines.",
        "The fog moves like a living thing, slow and deliberate.",
        "A chill seeps through the mist into your bones.",
        "The fog hides more than it reveals.",
        "The silence feels heavier inside the fog.",
    ],


    # =========================================================
    # WEATHER — SNOW
    # =========================================================

    "weather_snow": [
        "Snow drifts down in slow, deliberate silence.",
        "Your breath hangs in the air, a ghost that won’t leave.",
        "The world is muted, wrapped in a cold, white hush.",
        "Snow crunches beneath your feet with crisp finality.",
        "A thin layer of frost clings to everything.",
        "The air feels sharp, clean, and unforgiving.",
        "Snowflakes swirl in lazy spirals around you.",
        "The cold sinks into your bones with quiet persistence.",
        "The landscape glows with pale, icy light.",
        "Your footsteps leave a clear trail behind you.",
        "The snow absorbs sound, leaving the world strangely still.",
        "A faint shimmer dances across the frozen ground.",
        "The cold air stings your cheeks.",
        "Snow gathers on your shoulders like soft, cold dust.",
        "The world feels fragile beneath the falling snow.",
    ],


    # =========================================================
    # WEATHER — HEATWAVE (NEW)
    # =========================================================

    "weather_heatwave": [
        "The air shimmers with oppressive heat.",
        "Every breath feels thick and heavy.",
        "Sweat beads instantly on your skin.",
        "The sun blazes overhead like a merciless eye.",
        "Heat radiates from the ground in shimmering waves.",
        "Your vision wavers at the edges from the heat.",
        "The world feels slow, sluggish, and overheated.",
        "A dry, scorching wind brushes past you.",
        "The heat presses against you like a physical weight.",
        "Your clothes cling uncomfortably to your skin.",
        "The air tastes hot and metallic.",
        "The heatwave turns the horizon into a wavering mirage.",
        "Your heartbeat feels louder in the oppressive heat.",
        "The world seems to melt into soft, blurry shapes.",
        "The heatwave tests your endurance with every step.",
    ],


    # =========================================================
    # WEATHER — SANDSTORM (NEW)
    # =========================================================

    "weather_sandstorm": [
        "Sand whips through the air in stinging sheets.",
        "The wind howls, carrying grit that scratches your skin.",
        "Visibility drops to almost nothing in the swirling sand.",
        "The sandstorm roars like a living beast.",
        "Grains of sand rattle against your gear.",
        "The air becomes a choking haze of dust.",
        "Your eyes water as sand stings your face.",
        "The storm buries tracks as fast as they’re made.",
        "The sandstorm feels wild, chaotic, and relentless.",
        "Wind-driven sand scrapes across exposed skin.",
        "The world disappears behind a curtain of swirling grit.",
        "The storm’s roar drowns out all other sound.",
        "Sand grinds between your teeth with every breath.",
        "The storm pushes against you with brutal force.",
        "The sandstorm feels like the desert’s wrath made manifest.",
    ],


    # =========================================================
    # WEATHER — BLIZZARD (NEW)
    # =========================================================

    "weather_blizzard": [
        "Snow whips through the air in violent, swirling gusts.",
        "The blizzard howls like a furious spirit.",
        "Cold bites at your skin with savage intensity.",
        "Visibility shrinks to a few desperate feet.",
        "The wind tears at your clothes and balance.",
        "Snow stings your face like a barrage of needles.",
        "The world becomes a white, roaring void.",
        "Your footsteps vanish instantly beneath fresh snow.",
        "The blizzard feels merciless and unending.",
        "The cold sinks deep, numbing your fingers.",
        "The storm’s roar drowns out your thoughts.",
        "Snow swirls in chaotic, blinding patterns.",
        "Your breath freezes almost as soon as it leaves you.",
        "The blizzard presses in from all sides.",
        "The world feels swallowed by winter’s fury.",
    ],


    # =========================================================
    # WEATHER — MIST (NEW)
    # =========================================================

    "weather_mist": [
        "A thin mist drifts across the ground like a wandering spirit.",
        "The mist curls around your ankles in pale ribbons.",
        "The world feels soft, blurred, and dreamlike.",
        "Your footsteps stir the mist into swirling patterns.",
        "The mist clings to your clothes in cool tendrils.",
        "Shadows stretch strangely through the pale haze.",
        "The mist muffles sound into gentle whispers.",
        "A faint chill lingers in the damp air.",
        "The mist moves with slow, deliberate grace.",
        "Your breath merges with the drifting haze.",
        "The world feels distant behind the mist’s veil.",
        "Light scatters softly through the pale fog.",
        "The mist hides small movements at the edge of sight.",
        "A quiet stillness settles over the land.",
        "The mist feels almost thoughtful as it drifts.",
    ],


    # =========================================================
    # WEATHER — MAGIC STORM (NEW)
    # =========================================================

    "weather_magicstorm": [
        "The sky crackles with unnatural energy.",
        "Lightning arcs in colors no storm should hold.",
        "The air hums with raw, unstable power.",
        "Shimmering sparks drift through the storm clouds.",
        "The storm pulses like a living heartbeat.",
        "Magic twists the wind into strange, spiraling currents.",
        "The ground vibrates with arcane resonance.",
        "Bolts of energy strike with eerie precision.",
        "The storm glows faintly with shifting hues.",
        "Your skin tingles with charged air.",
        "The magic storm feels unpredictable and alive.",
        "Whispers echo faintly through the crackling air.",
        "The sky flickers with impossible colors.",
        "The storm’s energy dances across your vision.",
        "The world feels thinner beneath the storm’s power.",
    ],


    # =========================================================
    # WEATHER — ACID RAIN (NEW)
    # =========================================================

    "weather_acid_rain": [
        "Raindrops sizzle faintly as they hit the ground.",
        "The air smells sharp, acrid, and dangerous.",
        "Acid rain hisses against your gear.",
        "The droplets leave faint scorch marks where they fall.",
        "A toxic mist rises from the wet ground.",
        "The rain burns slightly where it touches exposed skin.",
        "The world feels hostile beneath the acidic downpour.",
        "The air tastes metallic and bitter.",
        "The rain eats away at leaves and stone alike.",
        "A faint smoke rises where the rain lands.",
        "The acid rain falls in slow, heavy drops.",
        "Your gear creaks under the corrosive assault.",
        "The storm feels poisonous, unnatural, and angry.",
        "The rain leaves faint trails of steam behind.",
        "The world hisses beneath the acidic fall.",
    ],


    # =========================================================
    # WEATHER — ECLIPSE (NEW)
    # =========================================================

    "weather_eclipse": [
        "The light dims as the sun slips behind the moon.",
        "Shadows stretch unnaturally long across the land.",
        "The world holds its breath beneath the eclipse.",
        "A strange hush settles over everything.",
        "The sky darkens into an eerie twilight.",
        "Animals fall silent as the light fades.",
        "The air feels charged with quiet tension.",
        "The eclipse casts the world in muted, uncanny hues.",
        "Your heartbeat sounds louder in the dim light.",
        "The land feels suspended between moments.",
        "The eclipse paints the world in strange, cold colors.",
        "A faint chill spreads through the dimming air.",
        "The world feels paused, waiting for something.",
        "The eclipse turns familiar shapes unfamiliar.",
        "The silence deepens into something almost sacred.",
    ],


    # =========================================================
    # WEATHER — BLOOD MOON (NEW)
    # =========================================================

    "weather_blood_moon": [
        "The moon rises red, casting the world in eerie crimson.",
        "Shadows deepen into dark, unsettling shapes.",
        "The air feels thick with quiet dread.",
        "The blood moon stains the land in ominous light.",
        "A faint metallic scent lingers in the air.",
        "The world feels tense beneath the crimson glow.",
        "Your pulse quickens for reasons you can’t explain.",
        "The blood moon watches with cold, unblinking eyes.",
        "The land feels restless under the red sky.",
        "A strange stillness settles over everything.",
        "The moon’s glow twists familiar shapes into something uncanny.",
        "The blood moon casts long, trembling shadows.",
        "The air hums with faint, unsettling energy.",
        "The world feels thinner beneath the red light.",
        "Something ancient stirs beneath the blood moon.",
    ],
    # =========================================================
    # ANIMAL — SEEN (NON-HOSTILE INTRO)
    # =========================================================

    "animal_seen": [
        "You spot a {animal} nearby.",
        "A {animal} watches you from a short distance.",
        "You notice a {animal} moving through the area.",
        "A {animal} pauses, noticing your presence.",
        "The {animal} lifts its head, ears twitching.",
        "A quiet rustle reveals a {animal} observing you.",
        "The {animal} stands still, waiting to see what you’ll do.",
        "A {animal} emerges from behind the brush.",
        "The {animal} glances your way, curious but cautious.",
        "You catch sight of a {animal} slipping between shadows.",
        "A {animal} freezes mid-step when it notices you.",
        "The {animal} sniffs the air, testing your scent.",
        "A {animal} watches you with unreadable eyes.",
        "The {animal} shifts its weight, unsure of your intentions.",
        "You lock eyes with a {animal} for a brief, quiet moment.",
    ],


    # =========================================================
    # ANIMAL — HOSTILE INTRO
    # =========================================================

    "animal_hostile": [
        "The {animal} bristles with hostility, ready to attack.",
        "The {animal} lunges toward you, eyes blazing.",
        "The {animal} decides you are a threat.",
        "The {animal} charges, leaving no room for negotiation.",
        "A fierce snarl erupts from the {animal} as it advances.",
        "The {animal} lowers its stance, preparing to strike.",
        "A guttural growl rolls from the {animal}'s throat.",
        "The {animal} bares its teeth and rushes forward.",
        "The {animal} moves with sudden, violent intent.",
        "The {animal} snaps at the air, daring you to move.",
        "A flash of aggression sparks in the {animal}'s eyes.",
        "The {animal} circles you with predatory focus.",
        "The {animal} lunges without hesitation.",
        "The {animal} snarls, claiming the ground beneath it.",
        "The {animal} charges with reckless fury.",
    ],


    # =========================================================
    # ANIMAL — FEEDING REACTIONS
    # =========================================================

    "feed_react": [
        "The {animal} sniffs at your offering, then eats cautiously.",
        "The {animal} edges closer, accepting the food with wary eyes.",
        "The {animal} hesitates, then takes the food from your hand.",
        "The {animal} seems calmer after eating what you offer.",
        "The {animal} nudges your hand gently before eating.",
        "The {animal} devours the food quickly, hunger overriding fear.",
        "The {animal} takes the food and steps back, watching you.",
        "The {animal} eats slowly, never breaking eye contact.",
        "The {animal} sniffs the food twice before accepting it.",
        "The {animal} relaxes slightly as it eats.",
        "The {animal} licks your hand briefly before retreating.",
        "The {animal} takes the food with surprising gentleness.",
        "The {animal} eats, tail flicking with cautious interest.",
        "The {animal} accepts the offering with a soft grunt.",
        "The {animal} lowers its guard just a little as it eats.",
    ],


    # =========================================================
    # ANIMAL — TAME FAIL
    # =========================================================

    "tame_fail": [
        "The {animal} keeps its distance, not ready to trust you.",
        "The {animal} watches you warily, muscles tense.",
        "The {animal} flinches away from your touch.",
        "The {animal} is not ready to accept you yet.",
        "The {animal} steps back, distrust clear in its eyes.",
        "The {animal} snorts and turns away.",
        "The {animal} shakes its head, refusing your approach.",
        "The {animal} growls softly, warning you off.",
        "The {animal} refuses to come closer.",
        "The {animal} backs away, uncertain and guarded.",
        "The {animal} lowers its ears, uncomfortable with your presence.",
        "The {animal} huffs and avoids your gaze.",
        "The {animal} circles away from you, keeping space.",
        "The {animal} stiffens, unwilling to trust.",
        "The {animal} steps aside, uninterested in bonding.",
    ],


    # =========================================================
    # ANIMAL — TAME SUCCESS
    # =========================================================

    "tame_success": [
        "The {animal} steps closer, eyes softening with trust.",
        "You feel a quiet bond settle between you and the {animal}.",
        "The {animal} relaxes, accepting you as one of its own.",
        "The {animal} now trusts you completely.",
        "The {animal} nudges your hand affectionately.",
        "The {animal} lowers its head in gentle acceptance.",
        "The {animal} lets out a soft, contented sound.",
        "The {animal} leans into your touch.",
        "The {animal} stands beside you, calm and trusting.",
        "The {animal} follows you with quiet confidence.",
        "The {animal} accepts you without hesitation.",
        "The {animal} bows its head in a gesture of trust.",
        "The {animal} settles beside you, peaceful and loyal.",
        "The {animal} gazes at you with newfound warmth.",
        "The {animal} chooses you, simple as that.",
    ],


    # =========================================================
    # ANIMAL — PERSONALITY REACTIONS
    # =========================================================

    "animal_react_timid": [
        "The {animal} shrinks back, eyes wide and wary.",
        "The {animal} flutters with nervous energy, ready to bolt.",
        "The {animal} watches you from a safe distance, trembling slightly.",
        "The {animal} steps back, unsure of your intentions.",
        "The {animal} lowers its head, avoiding your gaze.",
        "The {animal} tenses, prepared to flee.",
        "The {animal} shivers with quiet fear.",
        "The {animal} edges away, uncertain and fragile.",
        "The {animal} keeps its body low, ready to run.",
        "The {animal} flicks its ears nervously.",
    ],

    "animal_react_aggressive": [
        "The {animal} lowers its stance, teeth bared.",
        "A low growl rumbles from the {animal}'s throat.",
        "The {animal} glares at you, every muscle coiled to strike.",
        "The {animal} snaps at the air, warning you.",
        "The {animal} paws at the ground aggressively.",
        "The {animal} snarls, daring you to move.",
        "The {animal} lashes its tail with irritation.",
        "The {animal} lunges forward a few inches.",
        "The {animal} bares its fangs in open hostility.",
        "The {animal} huffs sharply, ready to attack.",
    ],

    "animal_react_curious": [
        "The {animal} tilts its head, studying you with bright eyes.",
        "The {animal} edges closer, sniffing the air around you.",
        "The {animal} circles you slowly, trying to understand.",
        "The {animal} watches you with open curiosity.",
        "The {animal} steps closer, intrigued.",
        "The {animal} sniffs your hand cautiously.",
        "The {animal} flicks its ears with interest.",
        "The {animal} examines your movements closely.",
        "The {animal} seems fascinated by your presence.",
        "The {animal} leans forward, curious and unafraid.",
    ],

    "animal_react_territorial": [
        "The {animal} plants itself firmly, as if drawing a line in the ground.",
        "The {animal} paces in front of you, guarding its space.",
        "The {animal} makes it very clear you are in its domain.",
        "The {animal} snorts, asserting dominance.",
        "The {animal} stomps the ground in warning.",
        "The {animal} blocks your path with a firm stance.",
        "The {animal} watches you with territorial intensity.",
        "The {animal} bristles, unwilling to yield ground.",
        "The {animal} growls protectively at its surroundings.",
        "The {animal} stands tall, claiming the area.",
    ],


    # =========================================================
    # ANIMAL — FLEEING
    # =========================================================

    "animal_flee": [
        "The {animal} bolts away in a burst of panic.",
        "The {animal} flees, vanishing into the wilds.",
        "The {animal} darts off before you can react.",
        "The {animal} runs, fear overpowering curiosity.",
        "The {animal} disappears between the trees.",
        "The {animal} sprints away, kicking up dust.",
        "The {animal} escapes with surprising speed.",
        "The {animal} retreats into the shadows.",
        "The {animal} bounds away, unwilling to risk staying.",
        "The {animal} flees with a startled cry.",
    ],


    # =========================================================
    # ANIMAL — IDLE BEHAVIOR
    # =========================================================

    "animal_idle": [
        "The {animal} sniffs the ground absentmindedly.",
        "The {animal} scratches behind its ear.",
        "The {animal} flicks its tail lazily.",
        "The {animal} looks around with mild interest.",
        "The {animal} shakes dust from its coat.",
        "The {animal} paws at the dirt idly.",
        "The {animal} lets out a soft grunt.",
        "The {animal} stretches its limbs slowly.",
        "The {animal} blinks at you, unbothered.",
        "The {animal} grazes quietly.",
    ],


    # =========================================================
    # LEGENDARY ANIMAL REACTIONS
    # =========================================================

    "animal_react_legendary": [
        "The air trembles as the {animal} acknowledges you.",
        "The {animal}'s gaze pierces through you like ancient judgment.",
        "A low, resonant growl shakes the ground beneath the {animal}.",
        "The {animal} radiates a presence older than memory.",
        "The {animal} watches you with impossible intelligence.",
        "The ground hums with power around the {animal}.",
        "The {animal}'s breath fogs the air with unnatural heat.",
        "The {animal} stands tall, a living myth made flesh.",
        "The {animal}'s eyes glow with quiet, terrifying awareness.",
        "The world seems to bend around the {animal}'s presence.",
    ],
    # =========================================================
    # LEGENDARY BEAST — INTRO
    # =========================================================

    "legendary_intro": [
        "The ground trembles as the {animal} emerges from the wild.",
        "A hush falls over the land as the {animal} appears.",
        "You feel the weight of an ancient presence: the {animal}.",
        "The air crackles with power as the {animal} steps into view.",
        "The world seems to dim around the {animal}'s arrival.",
        "A deep vibration rolls through the earth as the {animal} approaches.",
        "The {animal} emerges like a living myth, impossible to ignore.",
        "A cold shiver crawls up your spine as the {animal} appears.",
        "The land bends subtly around the {animal}'s presence.",
        "The {animal} steps forward, each movement heavy with meaning.",
        "A distant rumble heralds the arrival of the {animal}.",
        "The {animal}'s silhouette dominates the horizon.",
        "The air grows still, waiting for the {animal} to act.",
        "A primal instinct warns you: this is no ordinary creature.",
        "The {animal} arrives with the quiet certainty of a natural disaster.",
    ],


    # =========================================================
    # LEGENDARY BEAST — ROARS / AURA
    # =========================================================

    "legendary_roar": [
        "The {animal} unleashes a roar that shakes the very air.",
        "A thunderous bellow erupts from the {animal}, rattling your bones.",
        "The {animal}'s roar echoes across the land like a storm breaking.",
        "A deep, resonant cry rolls from the {animal}, ancient and powerful.",
        "The {animal} roars, and the world seems to flinch.",
        "A shockwave of sound bursts from the {animal}'s throat.",
        "The {animal}'s roar vibrates through the ground beneath you.",
        "A primal scream tears from the {animal}, raw and terrifying.",
        "The {animal} bellows, and the sky seems to darken.",
        "A roar erupts from the {animal}, filled with ancient fury.",
        "The {animal}'s voice shakes loose dust from nearby stones.",
        "A low, rumbling growl rolls outward like distant thunder.",
        "The {animal} roars, and your instincts scream to flee.",
        "A chilling howl rises from the {animal}, echoing for miles.",
        "The {animal}'s roar feels like a warning from the world itself.",
    ],


    # =========================================================
    # LEGENDARY BEAST — PHASE CHANGE (BOSS PHASES)
    # =========================================================

    "legendary_phase_change": [
        "The {animal} rises again, stronger than before.",
        "A surge of power erupts from the {animal}, shaking the ground.",
        "The {animal}'s wounds glow with fierce, renewed energy.",
        "The {animal} roars, entering a new, terrifying phase.",
        "A violent pulse of energy bursts from the {animal}.",
        "The {animal}'s eyes ignite with renewed fury.",
        "The air distorts around the {animal} as its power grows.",
        "The {animal} steadies itself, refusing to fall.",
        "A second wind fills the {animal}, wild and unstoppable.",
        "The {animal} snarls, its strength rising sharply.",
        "The {animal}'s aura flares, scorching the air.",
        "The ground cracks beneath the {animal}'s renewed force.",
        "The {animal} shakes off dust and blood, unbroken.",
        "A chilling calm settles over the {animal}—the storm before the storm.",
        "The {animal} enters a new phase, more dangerous than ever.",
    ],


    # =========================================================
    # LEGENDARY BEAST — ENVIRONMENTAL EFFECTS
    # =========================================================

    "legendary_environment": [
        "The air warps around the {animal}, shimmering with heat.",
        "Shadows twist unnaturally near the {animal}.",
        "The ground cracks beneath the {animal}'s weight.",
        "A faint glow radiates from the {animal}'s body.",
        "The wind shifts direction, drawn toward the {animal}.",
        "The world seems to tilt slightly around the {animal}.",
        "A low hum vibrates through the air near the {animal}.",
        "The temperature drops sharply as the {animal} approaches.",
        "The earth pulses with energy beneath the {animal}.",
        "A faint tremor ripples outward from the {animal}.",
        "The sky darkens subtly above the {animal}.",
        "The air tastes metallic near the {animal}.",
        "A strange pressure builds around the {animal}.",
        "The land seems to recoil from the {animal}'s presence.",
        "A faint aura flickers around the {animal}, alive and dangerous.",
    ],


    # =========================================================
    # LEGENDARY BEAST — DEATH / DEFEAT
    # =========================================================

    "legendary_death": [
        "The {animal} collapses with earth-shaking finality.",
        "A final roar escapes the {animal}, fading into silence.",
        "The {animal} falls, its mythic presence unraveling.",
        "A deep tremor rolls through the ground as the {animal} dies.",
        "The {animal} exhales one last time, the world softening around it.",
        "The {animal}'s body slumps, its power fading like a dying star.",
        "A heavy silence follows the {animal}'s fall.",
        "The {animal} crashes to the ground, shaking the land.",
        "The world seems to sigh as the {animal} finally falls.",
        "The {animal} lets out a low, fading rumble before going still.",
        "The {animal}'s aura flickers, then vanishes entirely.",
        "The ground settles as the {animal}'s presence fades.",
        "The {animal} collapses, its legend ending in dust.",
        "A strange calm washes over the land as the {animal} dies.",
        "The {animal} falls, and the world feels a little emptier.",
    ],
    # =========================================================
    # ENEMY — APPEARANCE / INTRO
    # =========================================================

    "enemy_appears": [
        "A {enemy} emerges from the {biome}.",
        "From the {biome}, a {enemy} steps into view.",
        "You sense danger just before a {enemy} appears.",
        "The {biome} parts to reveal a {enemy} watching you.",
        "A {enemy} approaches with hostile intent.",
        "The {enemy} spots you and moves in quickly.",
        "A {enemy} blocks your path, eyes sharp and focused.",
        "The {enemy} steps forward, sizing you up.",
        "A {enemy} bursts from cover, ready to fight.",
        "The {enemy} appears with a low, threatening growl.",
        "A {enemy} emerges, clearly spoiling for a fight.",
        "The {enemy} approaches with deliberate menace.",
        "A {enemy} stands before you, daring you to act.",
        "The {enemy} arrives, tension thick in the air.",
        "A {enemy} confronts you, leaving no room to retreat.",
    ],


    # =========================================================
    # ENEMY — TAUNTS
    # =========================================================

    "enemy_taunt": [
        "The {enemy} snarls, challenging you.",
        "The {enemy} laughs harshly, mocking your stance.",
        "The {enemy} gestures for you to come closer.",
        "The {enemy} smirks with cruel confidence.",
        "The {enemy} taps its weapon impatiently.",
        "The {enemy} circles you, looking for weakness.",
        "The {enemy} spits at your feet.",
        "The {enemy} cracks its knuckles with intent.",
        "The {enemy} growls something you don’t understand—but the tone is clear.",
        "The {enemy} grins, eager for blood.",
        "The {enemy} slams its weapon against the ground.",
        "The {enemy} narrows its eyes, unimpressed.",
        "The {enemy} lets out a mocking bark of laughter.",
        "The {enemy} points at you, then at the ground, as if claiming your future corpse.",
        "The {enemy} tilts its head, daring you to make the first move.",
    ],


    # =========================================================
    # ENEMY — FLEEING
    # =========================================================

    "enemy_flee": [
        "The {enemy} turns and bolts, abandoning the fight.",
        "The {enemy} flees into the {biome}, unwilling to continue.",
        "The {enemy} retreats with a frustrated snarl.",
        "The {enemy} escapes before you can react.",
        "The {enemy} runs, fear overpowering its aggression.",
        "The {enemy} limps away, desperate to survive.",
        "The {enemy} vanishes into the terrain.",
        "The {enemy} breaks off the fight and disappears.",
        "The {enemy} flees, leaving the battle unfinished.",
        "The {enemy} scrambles away in panic.",
    ],


    # =========================================================
    # ENEMY — CALLING REINFORCEMENTS
    # =========================================================

    "enemy_call_reinforcements": [
        "The {enemy} lets out a sharp cry for help.",
        "The {enemy} signals to something unseen.",
        "A piercing shout from the {enemy} echoes across the area.",
        "The {enemy} calls for reinforcements with a desperate roar.",
        "The {enemy} slams its weapon against the ground, summoning allies.",
        "The {enemy} whistles sharply—too sharply to be natural.",
        "The {enemy} raises its voice, calling others to join the fight.",
        "The {enemy} howls, and the sound carries far.",
        "The {enemy} gestures urgently toward the shadows.",
        "The {enemy} shouts a command you don’t understand.",
        "The {enemy} roars, and distant footsteps answer.",
        "The {enemy} calls out, and the air shifts with incoming danger.",
        "The {enemy} summons backup with a guttural cry.",
        "The {enemy} slams its fist into its chest, rallying allies.",
        "The {enemy} bellows, and something stirs nearby.",
    ],


    # =========================================================
    # ENEMY — IDLE BEHAVIOR
    # =========================================================

    "enemy_idle": [
        "The {enemy} shifts its weight, watching you closely.",
        "The {enemy} cracks its neck with a sharp pop.",
        "The {enemy} taps its foot impatiently.",
        "The {enemy} adjusts its stance, ready for anything.",
        "The {enemy} wipes sweat from its brow.",
        "The {enemy} mutters something under its breath.",
        "The {enemy} rolls its shoulders, loosening up.",
        "The {enemy} glances around, checking its surroundings.",
        "The {enemy} grinds its teeth softly.",
        "The {enemy} flexes its fingers, preparing to strike.",
        "The {enemy} sniffs the air, wary.",
        "The {enemy} narrows its eyes, studying you.",
        "The {enemy} shifts its grip on its weapon.",
        "The {enemy} breathes heavily, adrenaline rising.",
        "The {enemy} paces a short line, restless.",
    ],
    # =========================================================
    # EVENT — TREASURE
    # =========================================================

    "event_treasure": [
        "You notice something half-buried and gleaming nearby.",
        "A glint of metal catches your eye among the debris.",
        "You stumble upon a stash of forgotten valuables.",
        "Someone once hid something here—and never came back for it.",
        "A faint shimmer reveals a concealed cache.",
        "You spot a chest wedged between stones.",
        "A loose plank reveals something hidden beneath.",
        "You uncover a bundle wrapped in old cloth.",
        "A cracked crate lies abandoned, its contents spilling out.",
        "You find a pouch tucked beneath a fallen branch.",
        "A faint metallic clink draws your attention.",
        "You brush aside dirt to reveal something valuable.",
        "A hidden compartment reveals its secrets.",
        "You discover a stash left behind by a hurried traveler.",
        "A forgotten treasure waits quietly for a new owner.",
    ],


    # =========================================================
    # EVENT — SHRINE
    # =========================================================

    "event_shrine": [
        "A small shrine stands here, worn but not forgotten.",
        "You find a shrine, its offerings long since faded.",
        "Symbols of old faith are carved into stone nearby.",
        "The air around the shrine feels strangely still.",
        "A faint warmth radiates from the shrine’s center.",
        "The shrine hums with quiet, ancient energy.",
        "Candles—long extinguished—still hold the scent of incense.",
        "A carved idol watches with serene, unreadable eyes.",
        "The shrine feels like a place where wishes once gathered.",
        "A soft glow lingers around the shrine’s base.",
        "The air tastes faintly of old prayers.",
        "The shrine stands untouched by time’s decay.",
        "A gentle breeze stirs as you approach the shrine.",
        "The shrine feels peaceful, but not empty.",
        "You sense a presence listening, patient and distant.",
    ],


    # =========================================================
    # EVENT — CAMPFIRE
    # =========================================================

    "event_campfire": [
        "The remains of a campfire still smell faintly of smoke.",
        "You find a campfire site—recent, but abandoned.",
        "Ash and charred wood mark where someone once rested.",
        "A circle of stones and embers suggests a safe place to pause.",
        "The firepit is cold, but the memory of warmth lingers.",
        "Someone left in a hurry; the ashes are still warm.",
        "A few burnt scraps hint at a meal once cooked here.",
        "The campfire feels like a brief refuge from the wild.",
        "You sense the quiet comfort of those who rested here before.",
        "The firepit sits like a small island of civilization.",
        "A faint trail of smoke rises from a dying ember.",
        "The campfire’s glow has faded, but not forgotten.",
        "You find footprints circling the firepit.",
        "The campfire feels like a story interrupted.",
        "A gentle calm settles around the abandoned fire.",
    ],


    # =========================================================
    # EVENT — MINIBOSS LAIR
    # =========================================================

    "event_miniboss": [
        "The air thickens with tension—something powerful is nearby.",
        "You feel eyes on you, heavy and unblinking.",
        "This place feels like a lair, not a simple room.",
        "You sense a presence here that will not let you pass easily.",
        "The ground bears marks of violent struggle.",
        "A low growl echoes from deeper within.",
        "The air tastes metallic, like blood and anticipation.",
        "Shadows cling unnaturally to the corners.",
        "You feel a pressure in your chest, primal and instinctive.",
        "The silence here is too deliberate.",
        "A faint vibration hums beneath your feet.",
        "The walls seem to lean inward, expectant.",
        "You sense something waiting, patient and deadly.",
        "The atmosphere feels thick enough to cut.",
        "A cold dread settles over the area.",
    ],


    # =========================================================
    # EVENT — RUINS (NEW)
    # =========================================================

    "event_ruins": [
        "You step into a chamber half-swallowed by time.",
        "Broken pillars lie scattered like fallen giants.",
        "Ancient carvings stare back with eroded faces.",
        "A collapsed archway hints at forgotten grandeur.",
        "Dust swirls in the faint light filtering through cracks.",
        "The ruins feel haunted—not by spirits, but by memory.",
        "A shattered mural tells a story you can’t fully read.",
        "Loose stones shift beneath your feet.",
        "A faint echo lingers in the hollow space.",
        "The ruins feel like a place that remembers too much.",
        "A broken statue watches with empty eyes.",
        "The air tastes of dust and old secrets.",
        "A faint draft whispers through the broken walls.",
        "The ruins feel patient, waiting to be understood.",
        "You sense history pressing in from all sides.",
    ],


    # =========================================================
    # EVENT — PORTAL (NEW)
    # =========================================================

    "event_portal": [
        "A faint shimmer distorts the air before you.",
        "A swirling rift pulses with quiet energy.",
        "The fabric of reality seems thin here.",
        "A soft hum vibrates from a glowing tear in space.",
        "Colors shift unnaturally within the portal’s surface.",
        "The portal flickers like a heartbeat.",
        "A strange wind blows from the rift, carrying unfamiliar scents.",
        "The portal warps the air around it in subtle waves.",
        "A low resonance echoes from the shimmering gateway.",
        "The portal feels like an invitation—and a warning.",
        "You sense countless places on the other side.",
        "The portal’s glow reflects in your eyes.",
        "A faint whisper drifts from the rift.",
        "The portal pulses, as if aware of your presence.",
        "The air around the portal feels charged and alive.",
    ],


    # =========================================================
    # EVENT — OMEN (NEW)
    # =========================================================

    "event_omen": [
        "A sudden chill crawls up your spine.",
        "The wind shifts direction without warning.",
        "A distant cry echoes, too distorted to identify.",
        "The shadows lengthen unnaturally for a moment.",
        "A faint metallic taste fills your mouth.",
        "The world seems to pause, just for a heartbeat.",
        "A strange pressure builds behind your eyes.",
        "The air grows heavy with unspoken meaning.",
        "A flicker of movement appears at the edge of vision.",
        "Your instincts whisper that something is coming.",
        "A soft ringing fills your ears, then fades.",
        "The ground vibrates with a subtle, rhythmic pulse.",
        "A sudden stillness grips the land.",
        "The sky darkens for a moment, then clears.",
        "You feel watched by something far away.",
    ],


    # =========================================================
    # EVENT — ANOMALY (NEW, MILD CHAOS)
    # =========================================================

    "event_anomaly": [
        "The air ripples as if reality hiccups.",
        "A faint glow flickers beneath the ground.",
        "You feel a momentary weightlessness.",
        "The world blurs for a heartbeat, then snaps back.",
        "A soft chime rings from nowhere in particular.",
        "Your shadow twitches a moment out of sync.",
        "A warm breeze brushes past, though the air is still.",
        "The ground hums beneath your feet.",
        "Colors shift slightly, then return to normal.",
        "You feel like you stepped through a thought not your own.",
        "A faint afterimage lingers in your vision.",
        "The world feels misaligned for a breath.",
        "A soft pulse of light travels across the ground.",
        "Your heartbeat stutters, then steadies.",
        "Something unseen brushes past your awareness.",
    ],
    # =========================================================
    # COMBAT — PLAYER TURN
    # =========================================================

    "combat_player_turn": [
        "You steady yourself and prepare to act.",
        "Your muscles tense as you seize the initiative.",
        "You move first, instincts sharp and focused.",
        "You take a decisive step forward.",
        "You ready your next move with practiced precision.",
        "You feel the moment shift in your favor.",
        "You strike before the enemy can react.",
        "You advance, determination burning in your chest.",
        "You act swiftly, refusing to hesitate.",
        "You seize the opening and prepare your attack.",
        "You tighten your grip, ready to strike.",
        "You move with purpose, eyes locked on your foe.",
        "You take control of the fight.",
        "You push forward, refusing to yield.",
        "You act with sharp, deliberate intent.",
    ],


    # =========================================================
    # COMBAT — ENEMY TURN
    # =========================================================

    "combat_enemy_turn": [
        "The {enemy} moves with sudden aggression.",
        "The {enemy} seizes the moment and attacks.",
        "The {enemy} lunges forward, taking the initiative.",
        "The {enemy} advances with hostile intent.",
        "The {enemy} strikes with fierce determination.",
        "The {enemy} makes its move, swift and brutal.",
        "The {enemy} attacks without hesitation.",
        "The {enemy} presses the assault.",
        "The {enemy} charges, eyes burning with fury.",
        "The {enemy} lashes out with violent precision.",
        "The {enemy} moves first, catching you off guard.",
        "The {enemy} closes the distance in an instant.",
        "The {enemy} attacks with reckless abandon.",
        "The {enemy} surges forward, refusing to relent.",
        "The {enemy} takes advantage of the opening.",
    ],


    # =========================================================
    # COMBAT — PLAYER CHOICE / HESITATION
    # =========================================================

    "combat_player_choice": [
        "You weigh your options in a heartbeat.",
        "You shift your stance, considering your next move.",
        "You look for an opening, mind racing.",
        "You hesitate for a moment, then commit.",
        "You adjust your grip, preparing for what comes next.",
        "You breathe deeply, steadying your nerves.",
        "You choose your next action with care.",
        "You focus, letting instinct guide you.",
        "You search for a weakness in the enemy’s stance.",
        "You prepare to strike—or defend.",
    ],

    "combat_player_hesitate": [
        "You falter, just for a moment.",
        "Your confidence wavers, slowing your reaction.",
        "You hesitate, and the world narrows around you.",
        "Doubt flickers through your mind.",
        "You freeze, caught between choices.",
        "Your grip tightens, unsure.",
        "You lose a precious second to uncertainty.",
        "Your breath catches as hesitation grips you.",
        "You pause, heart pounding.",
        "Your instincts clash, leaving you momentarily still.",
    ],


    # =========================================================
    # COMBAT — DEFEND / BLOCK
    # =========================================================

    "combat_player_defend": [
        "You raise your guard just in time.",
        "You brace yourself, absorbing the impact.",
        "You deflect the blow with practiced precision.",
        "You shield yourself from the worst of the attack.",
        "You block the strike, feet sliding back slightly.",
        "You parry the incoming blow with sharp reflexes.",
        "You twist aside, minimizing the damage.",
        "You brace your stance and hold firm.",
        "You intercept the attack with your weapon.",
        "You deflect the strike, sparks flying.",
    ],


    # =========================================================
    # COMBAT — COMPANION ASSIST
    # =========================================================

    "combat_companion_attack": [
        "Your companion leaps in, striking the {enemy} with fierce loyalty.",
        "Your ally darts forward, landing a clean hit.",
        "Your companion attacks, creating an opening.",
        "Your ally distracts the {enemy} with a swift strike.",
        "Your companion lunges, teeth bared.",
        "Your ally slams into the {enemy}, staggering it.",
        "Your companion snaps at the {enemy}, forcing it back.",
        "Your ally charges, landing a decisive blow.",
        "Your companion attacks with surprising ferocity.",
        "Your ally moves in perfect sync with you.",
    ],


    # =========================================================
    # COMBAT — PLAYER DAMAGE (NORMAL)
    # =========================================================

    "combat_player_damage": [
        "You strike the {enemy}, landing a solid hit.",
        "Your attack connects with sharp impact.",
        "You slash across the {enemy}'s guard.",
        "Your blow lands cleanly.",
        "You drive your weapon into the {enemy}'s defenses.",
        "You hit the {enemy}, forcing it back.",
        "Your strike draws a pained snarl.",
        "You land a decisive blow.",
        "Your attack cuts through the {enemy}'s stance.",
        "You strike with controlled force.",
        "Your weapon bites into the {enemy}'s flesh.",
        "You land a heavy hit, staggering your foe.",
        "Your attack leaves a clear mark.",
        "You strike with precision and intent.",
        "Your blow forces the {enemy} to recoil.",
    ],


    # =========================================================
    # COMBAT — ENEMY DAMAGE (NORMAL)
    # =========================================================

    "combat_enemy_damage": [
        "The {enemy} strikes you with brutal force.",
        "Pain flares as the {enemy}'s attack lands.",
        "The {enemy} hits you hard, knocking you off balance.",
        "The {enemy}'s blow connects with sharp impact.",
        "You feel the sting of the {enemy}'s strike.",
        "The {enemy} slashes across your guard.",
        "The {enemy} lands a heavy hit.",
        "The {enemy}'s attack forces you back.",
        "You stagger under the {enemy}'s blow.",
        "The {enemy} strikes with vicious precision.",
        "The {enemy}'s attack leaves you reeling.",
        "You grit your teeth as the {enemy} hits you.",
        "The {enemy} lands a punishing blow.",
        "The {enemy}'s strike sends a jolt of pain through you.",
        "The {enemy} attacks with relentless force.",
    ],


    # =========================================================
    # COMBAT — SPECIAL ATTACKS
    # =========================================================

    "combat_player_special": [
        "You unleash a powerful strike, catching the {enemy} off guard.",
        "Your weapon arcs with force as you deliver a devastating blow.",
        "You channel your strength into a single, crushing attack.",
        "You strike with precision, exploiting a perfect opening.",
        "Your special attack lands with explosive impact.",
        "You unleash a fierce combination of blows.",
        "Your attack cuts through the {enemy}'s defenses.",
        "You strike with overwhelming force.",
        "Your special move sends the {enemy} stumbling.",
        "You deliver a blow that shakes the battlefield.",
    ],


    # =========================================================
    # COMBAT — MAGIC ATTACKS
    # =========================================================

    "combat_magic_hit": [
        "Your spell bursts against the {enemy} in a flash of energy.",
        "Arcane force slams into the {enemy}.",
        "Your magic crackles through the air, striking true.",
        "A surge of power erupts from your hands.",
        "Your spell hits with shimmering impact.",
        "The {enemy} recoils from the magical blast.",
        "Your magic arcs across the battlefield.",
        "A burst of light engulfs the {enemy}.",
        "Your spell lands with precise force.",
        "Energy ripples outward as your magic connects.",
    ],

    "combat_magic_crit": [
        "Your spell detonates with overwhelming power.",
        "A brilliant flash engulfs the {enemy}, tearing through its defenses.",
        "Your magic erupts in a devastating surge.",
        "The spell hits with catastrophic force.",
        "Arcane energy explodes outward, overwhelming the {enemy}.",
        "Your spell crackles with amplified intensity.",
        "A violent burst of magic tears into the {enemy}.",
        "Your spell lands with impossible precision.",
        "The air vibrates as your magic overwhelms the {enemy}.",
        "Your spell ignites into a critical blast.",
    ],


    # =========================================================
    # COMBAT — ENEMY HEAVY ATTACKS
    # =========================================================

    "combat_enemy_heavy": [
        "The {enemy} unleashes a crushing blow.",
        "A heavy strike from the {enemy} sends you reeling.",
        "The {enemy} attacks with brutal, overwhelming force.",
        "A devastating hit slams into you.",
        "The {enemy}'s heavy attack nearly knocks you off your feet.",
        "The {enemy} swings with terrifying strength.",
        "A powerful blow crashes into your guard.",
        "The {enemy} strikes with bone-rattling impact.",
        "You stagger under the force of the {enemy}'s attack.",
        "The {enemy} delivers a punishing heavy strike.",
    ],
    # =========================================================
    # COMBAT — PLAYER DODGE / BLOCK
    # =========================================================

    "combat_player_dodge": [
        "You slip aside just in time.",
        "You dodge the attack with sharp reflexes.",
        "You twist away from the incoming strike.",
        "You evade the blow by a hair’s breadth.",
        "You duck under the {enemy}'s attack.",
        "You sidestep the strike with practiced ease.",
        "You leap back, avoiding the hit.",
        "You pivot away from danger.",
        "You evade the attack with fluid motion.",
        "You narrowly avoid the {enemy}'s blow.",
    ],

    "combat_player_block": [
        "You block the attack with a firm stance.",
        "Your guard absorbs the impact.",
        "You intercept the blow with your weapon.",
        "You brace yourself and block the strike.",
        "You deflect the attack with controlled force.",
        "Your shield takes the brunt of the hit.",
        "You parry the incoming strike.",
        "You hold your ground and block the blow.",
        "Your guard holds strong.",
        "You meet the attack head-on and stop it cold.",
    ],


    # =========================================================
    # COMBAT — ENEMY DODGE / BLOCK
    # =========================================================

    "combat_enemy_dodge": [
        "The {enemy} slips aside, avoiding your strike.",
        "The {enemy} dodges with surprising agility.",
        "Your attack misses as the {enemy} twists away.",
        "The {enemy} leaps back, evading your blow.",
        "The {enemy} sidesteps your strike.",
        "The {enemy} ducks under your attack.",
        "The {enemy} evades with sharp reflexes.",
        "Your blow cuts through empty air.",
        "The {enemy} pivots away from your strike.",
        "The {enemy} avoids your attack with ease.",
    ],

    "combat_enemy_block": [
        "The {enemy} blocks your attack with a firm stance.",
        "Your strike glances off the {enemy}'s guard.",
        "The {enemy} intercepts your blow.",
        "Your attack is stopped cold by the {enemy}'s defense.",
        "The {enemy} parries your strike.",
        "Your weapon clashes against the {enemy}'s guard.",
        "The {enemy} deflects your attack.",
        "Your blow is absorbed by the {enemy}'s defense.",
        "The {enemy} braces and blocks your strike.",
        "Your attack fails to break through the {enemy}'s guard.",
    ],


    # =========================================================
    # COMBAT — CRITICAL HITS
    # =========================================================

    "combat_crit_player": [
        "Your strike lands with devastating precision.",
        "A perfect hit tears through the {enemy}'s defenses.",
        "Your attack finds a critical opening.",
        "You deliver a blow that shakes the {enemy}.",
        "Your strike hits with overwhelming force.",
        "You land a critical hit, staggering your foe.",
        "Your weapon bites deep with brutal accuracy.",
        "A flawless strike sends the {enemy} reeling.",
        "Your attack lands with catastrophic impact.",
        "You unleash a critical blow.",
    ],

    "combat_crit_enemy": [
        "The {enemy} lands a devastating critical hit.",
        "Pain explodes through you as the {enemy} strikes true.",
        "The {enemy}'s attack finds a perfect opening.",
        "A critical blow sends you stumbling.",
        "The {enemy} hits with overwhelming force.",
        "A brutal strike tears through your defenses.",
        "The {enemy} lands a catastrophic hit.",
        "You reel from the {enemy}'s critical attack.",
        "The {enemy}'s strike hits with terrifying precision.",
        "A critical blow nearly knocks you off your feet.",
    ],


    # =========================================================
    # STATUS EFFECTS — BLEED / POISON / BURN / STUN
    # =========================================================

    "combat_status_bleed": [
        "Blood drips steadily from your wound.",
        "A sharp pain pulses with every heartbeat.",
        "You feel warm blood running down your side.",
        "Your vision blurs slightly from the bleeding.",
        "You grit your teeth as the wound worsens.",
        "Blood loss weakens your stance.",
        "You feel your strength slipping away.",
        "Your wound throbs with painful intensity.",
        "You struggle to stay steady as you bleed.",
        "The bleeding refuses to slow.",
    ],

    "combat_status_poison": [
        "A sickly numbness spreads through your veins.",
        "Your limbs feel heavy and unresponsive.",
        "A bitter taste fills your mouth.",
        "Your vision swims as the poison takes hold.",
        "A cold sweat breaks across your skin.",
        "Your heartbeat stutters irregularly.",
        "You feel the poison burning through your body.",
        "Your breath grows shallow and strained.",
        "A wave of nausea hits you hard.",
        "The poison weakens you with every passing moment.",
    ],

    "combat_status_burn": [
        "Flames lick at your skin, searing painfully.",
        "Heat scorches your flesh with every movement.",
        "You feel the burn spreading across your body.",
        "Your skin blisters under the intense heat.",
        "A wave of fiery pain surges through you.",
        "The burning sensation intensifies with each breath.",
        "You wince as flames cling stubbornly.",
        "Your body trembles from the heat.",
        "The fire refuses to die down.",
        "You feel the burn deep in your muscles.",
    ],

    "combat_status_stun": [
        "Your thoughts scatter as the world tilts.",
        "You struggle to regain focus.",
        "Your limbs refuse to respond.",
        "A ringing fills your ears, drowning out everything else.",
        "You stagger, unable to act.",
        "Your vision flickers as you fight to stay upright.",
        "You feel frozen, trapped in your own body.",
        "Your senses blur into a dull haze.",
        "You can’t move—your body won’t obey.",
        "The stun leaves you momentarily helpless.",
    ],


    # =========================================================
    # COMBAT — OUTCOMES
    # =========================================================

    "combat_victory": [
        "The {enemy} collapses, defeated.",
        "You stand victorious over the fallen {enemy}.",
        "The battle ends with your triumph.",
        "You exhale, adrenaline fading as the {enemy} falls.",
        "The {enemy} lies still—you have won.",
        "Your final strike ends the fight.",
        "The {enemy} crumples under your last blow.",
        "You emerge from the battle victorious.",
        "The fight ends in your favor.",
        "You steady yourself, victorious but exhausted.",
    ],

    "combat_defeat": [
        "Your strength fails, and darkness closes in.",
        "You collapse, unable to continue the fight.",
        "The {enemy} stands over you as your vision fades.",
        "Pain overwhelms you as you fall.",
        "Your body gives out, the battle lost.",
        "You sink to the ground, defeated.",
        "The world tilts as you lose consciousness.",
        "You fall, the {enemy} victorious.",
        "Your legs buckle beneath you.",
        "The fight slips from your grasp as you collapse.",
    ],
        # ---------------------------------------------------------
    # DIALOGUE SYSTEM (CINEMATIC)
    # ---------------------------------------------------------

    "dialogue_start": [
        "{npc} pauses, studying you with guarded curiosity.",
        "{npc} turns toward you, their expression unreadable.",
        "{npc} acknowledges your presence with a slow nod."
    ],

    "dialogue_personality_curious": [
        "{npc} leans in slightly, eager to hear what you have to say.",
        "A spark of interest flickers in {npc}'s eyes."
    ],

    "dialogue_personality_serious": [
        "{npc} stands firm, posture rigid, voice low and controlled.",
        "There is a stern weight behind {npc}'s gaze."
    ],

    "dialogue_personality_friendly": [
        "{npc} offers a warm smile, easing the tension in the air.",
        "{npc} seems genuinely pleased to speak with you."
    ],

    "dialogue_personality_hostile": [
        "{npc}'s jaw tightens. They clearly don't trust you.",
        "A cold glare from {npc} warns you to tread carefully."
    ],

    "dialogue_intro_generic": [
        "The stranger eyes you cautiously. 'What brings you here?'",
        "'You don't look like you're from around here,' {npc} mutters."
    ],

    "dialogue_neutral_reply": [
        "'Hmph. Not many wanderers these days,' {npc} says.",
        "{npc} crosses their arms. 'These roads have grown quiet.'"
    ],

    "dialogue_friendly_reply": [
        "{npc} relaxes slightly. 'Good to hear. These lands can be harsh.'",
        "'A kind soul is rare out here,' {npc} admits."
    ],

    "dialogue_hostile_reply": [
        "{npc}'s eyes narrow. 'Watch your tone.'",
        "'Careful now,' {npc} warns, voice sharp."
    ],

    "dialogue_ask_name": [
        "'Name's not important,' {npc} says. 'But trouble is everywhere.'",
        "'Call me what you like. Just stay alert,' {npc} replies."
    ],

    "dialogue_offer_help": [
        "'Help? Maybe… I might have something for you,' {npc} says quietly.",
        "{npc} hesitates. 'If you're serious, I could use a hand.'"
    ],

    "dialogue_unlock_quest": [
        "{npc} nods slowly. 'Alright… I do have a task for you.'",
        "'If you're willing, there's something that needs doing,' {npc} says."
    ],

    "dialogue_give_quest": [
        "'Good. I knew I could trust you,' {npc} says with relief.",
        "{npc} hands you a small token. 'This marks the beginning.'"
    ],

    "dialogue_end": [
        "The conversation fades, and {npc} steps back.",
        "{npc} gives a final nod before turning away."
    ],

    "dialogue_choice_prompt": [
        "How do you respond?",
        "Your reply?"
    ],

    # ---------------------------------------------------------
    # CHOICE TEXT
    # ---------------------------------------------------------

    "choice_pass_through": ["Just passing through."],
    "choice_no_harm": ["I mean no harm."],
    "choice_none_business": ["None of your business."],
    "choice_who_are_you": ["Who are you?"],
    "choice_goodbye": ["Goodbye."],
    "choice_offer_help": ["Need any help?"],
    "choice_safe_travels": ["Safe travels."],
    "choice_sorry": ["Sorry… rough day."],
    "choice_back_off": ["Back off."],
    "choice_help": ["Do you need help?"],
    "choice_tell_more": ["Tell me more."],
    "choice_not_interested": ["Not interested."],
    "choice_accept": ["I'll take it."],
    "choice_later": ["Maybe later."],
    "choice_return_soon": ["I'll return soon."],

    # ---------------------------------------------------------
    # RUMORS / MICRO-STORIES
    # ---------------------------------------------------------

    "rumor_beast": [
        "'They say a beast roams the old paths… huge, silent, hungry.'",
        "'Something's been stalking travelers at dusk. Big. Fast.'"
    ],

    "rumor_ruins": [
        "'Old ruins lie east of here. Some say they shift at night.'",
        "'Stone halls buried in the earth… and voices beneath them.'"
    ],

    "rumor_shrine": [
        "'A forgotten shrine lies nearby. Strange lights at dusk.'",
        "'People leave offerings there. Some vanish afterward.'"
    ],

    "rumor_weather": [
        "'Storms have been unnatural lately. Like the sky is angry.'",
        "'Fog rolls in without warning. Thick enough to swallow sound.'"
    ],

    "rumor_wanderer": [
        "'A wanderer passed through—said they were being followed.'",
        "'Someone's been asking about you. Can't say who.'"
    ],

    # ---------------------------------------------------------
    # THREAT / TRADE / LEAVE
    # ---------------------------------------------------------

    "dialogue_trade_unavailable": [
        "'Trade? Not today,' {npc} says, shaking their head.",
        "'I've nothing to barter right now,' {npc} replies."
    ],

    "dialogue_threaten": [
        "You step forward, voice low and dangerous.",
        "Your tone sharpens as you confront {npc}."
    ],

    "dialogue_threaten_backdown": [
        "{npc} flinches. 'Alright, alright… no trouble.'",
        "'Easy! I don't want a fight,' {npc} stammers."
    ],

    "dialogue_threaten_hostile": [
        "{npc}'s expression hardens. 'Big mistake.'",
        "'If it's a fight you want…' {npc} growls."
    ],

    "dialogue_leave": [
        "{npc} nods and steps aside.",
        "You turn away, ending the exchange."
    ],
"dialogue_intro_storyteller": [
    "The storyteller's eyes sparkle with old tales.",
    "They carry the weight of many forgotten stories.",
    "A soft smile forms — they seem eager to share a tale."
],

"dialogue_intro_bandit": [
    "The bandit sizes you up with a predatory grin.",
    "A dangerous glint flashes in their eyes.",
    "They rest a hand on their weapon, watching you closely."
],

"dialogue_intro_guardian": [
    "The shrine guardian stands firm, unmoving.",
    "Their presence radiates discipline and purpose.",
    "They watch you with calm, unwavering focus."
],

"dialogue_intro_emissary": [
    "The emissary bears the colors of their faction proudly.",
    "Their posture is formal, diplomatic.",
    "They greet you with measured respect."
],

"dialogue_intro_questgiver": [
    "They look troubled, as if burdened by a task.",
    "Their eyes plead for help.",
    "They seem relieved to see another traveler."
],

"dialogue_intro_friendly": [
    "They greet you with a warm smile.",
    "Their expression brightens at your arrival.",
    "They seem genuinely happy to see you."
],

"dialogue_intro_hostile": [
    "They glare at you with open hostility.",
    "Their stance is tense and aggressive.",
    "They look ready to start a fight."
],

"dialogue_intro_generic": [
    "You don't look like you're from around here,",
    "They glance at you with mild curiosity.",
    "They acknowledge you with a nod."
]

    
    
    
    
    # =========================================================
    # END OF TEXT VARIANTS
    # =========================================================
}


# =============================================================
# RANDOM TEXT FUNCTION (rt)
# =============================================================

def rt(key: str, **kwargs) -> str:
    """
    Returns a random cinematic text line for the given key.
    Automatically formats placeholders like {enemy}, {animal}, {biome}, etc.
    Falls back gracefully if a key is missing or empty.
    """

    # Key missing entirely
    if key not in TEXT_VARIANTS:
        return f"[Missing text: {key}]"

    variants = TEXT_VARIANTS.get(key, [])

    # Key exists but has no lines
    if not variants:
        return f"[Empty text list: {key}]"

    # Choose a random line
    line = random.choice(variants)

    # Format placeholders safely
    try:
        return line.format(**kwargs)
    except KeyError:
        # If a placeholder is missing, return the raw line
        return line
