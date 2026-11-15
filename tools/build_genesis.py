import json, os

C = []  # chapters
def ch(n, title, summary, questions, refs):
    C.append({"n": n, "title": title, "summary": summary, "questions": questions, "crossRefs": refs})

ch(1, "God Creates the Heavens and the Earth",
   "God speaks creation into being over six days, bringing order and fullness out of what was \u201cwithout form and void.\u201d Days 1\u20133 form the realms (light, sky and seas, land), and days 4\u20136 fill them (lights, birds and fish, animals and people). Everything is declared \u201cgood,\u201d and humanity, made male and female in God\u2019s image, is blessed and given dominion over the earth.",
   ["What does the repeated phrase \u201cAnd God said\u2026 and it was so\u201d teach about God\u2019s power and authority?",
    "Notice the pattern of forming (days 1\u20133) and filling (days 4\u20136). What does this reveal about God\u2019s character?",
    "What does it mean to be made in the image of God (1:26\u201327), and how should it shape the way we treat every person?",
    "God called creation \u201cvery good\u201d (1:31). How does that affect your view of the physical world, work, and the body?"],
   ["John 1:1\u20133", "Psalm 33:6\u20139", "Hebrews 11:3", "Colossians 1:16"])
ch(2, "The Seventh Day and the Garden of Eden",
   "God rests on the seventh day and blesses it. The narrative then zooms in on the creation of man from the dust, the planting of the garden in Eden, the command not to eat from the tree of the knowledge of good and evil, and the creation of woman from the man\u2019s side. Marriage is established as a one-flesh union, and the first couple live unashamed.",
   ["Why do you think God \u201crested\u201d on the seventh day? What does it model for us?",
    "What does God\u2019s single prohibition (2:16\u201317) say about freedom, trust, and boundaries?",
    "How does 2:18\u201325 describe the purpose and nature of marriage?"],
   ["Exodus 20:8\u201311", "Matthew 19:4\u20136", "Ephesians 5:31\u201332", "Hebrews 4:9\u201310"])
ch(3, "The Fall",
   "The serpent questions God\u2019s word, and Eve and then Adam eat the forbidden fruit. Shame, fear, and blame immediately follow. God confronts them, pronounces curses on the serpent and the ground and consequences for the man and woman, yet also gives the first promise of a coming offspring who will crush the serpent (3:15). God clothes them with garments of skin and sends them out of Eden.",
   ["How does the serpent twist God\u2019s words (3:1\u20135)? Where do you hear similar lies today?",
    "Trace the chain of blame in 3:9\u201313. Why is it so hard to own our sin?",
    "Why is 3:15 often called the \u201cfirst gospel\u201d? Who is the promised offspring?",
    "Where do you see God\u2019s mercy mixed with judgment in this chapter?"],
   ["Romans 5:12\u201319", "1 Corinthians 15:21\u201322", "Romans 16:20", "Revelation 12:9"])
ch(4, "Cain and Abel",
   "Sin spreads to the next generation. God accepts Abel\u2019s offering but not Cain\u2019s, and Cain, warned that sin is \u201ccrouching at the door,\u201d murders his brother. God sentences Cain to wander but marks him for protection. Cain\u2019s line builds cities and culture but also grows violent (Lamech). Seth is born, and people begin to call upon the name of the LORD.",
   ["What does God\u2019s warning to Cain in 4:7 teach about temptation and personal responsibility?",
    "Why might God have accepted Abel\u2019s offering but not Cain\u2019s? (See Hebrews 11:4.)",
    "Compare Cain\u2019s line (4:17\u201324) with Seth\u2019s (4:25\u201326). What two paths are being contrasted?"],
   ["Hebrews 11:4", "1 John 3:11\u201312", "Hebrews 12:24", "Jude 11"])
ch(5, "From Adam to Noah",
   "A genealogy traces the line from Adam through Seth to Noah. Its repeated refrain \u201cand he died\u201d shows the reign of death after the fall. The exception is Enoch, who \u201cwalked with God, and he was not, for God took him.\u201d Lamech names his son Noah, hoping he will bring relief from the cursed ground.",
   ["What is the effect of the repeated phrase \u201cand he died\u201d?",
    "What does it mean that Enoch \u201cwalked with God\u201d (5:22\u201324)? What would that look like in your life?",
    "How does this genealogy keep the promise of 3:15 moving forward?"],
   ["Hebrews 11:5\u20136", "Jude 14\u201315", "Luke 3:36\u201338", "Romans 5:14"])
ch(6, "Wickedness and the Call of Noah",
   "Human wickedness grows so great that \u201cevery intention of the thoughts of his heart was only evil continually.\u201d The LORD is grieved and resolves to judge the earth, but Noah finds favor in His eyes. God tells Noah, a righteous man who walked with God, to build an ark and promises to establish His covenant with him.",
   ["How does 6:5\u20136 describe the depth of human sin and God\u2019s response to it?",
    "Noah \u201cfound favor\u201d (6:8) before he is described as righteous (6:9). Why is that order significant?",
    "Noah \u201cdid all that God commanded him\u201d (6:22). What does long-term obedience look like for you?"],
   ["Hebrews 11:7", "Matthew 24:37\u201339", "2 Peter 2:5", "1 Peter 3:20"])
ch(7, "The Flood",
   "Noah, his family, and the animals enter the ark, and the LORD shuts them in. For forty days the waters pour down and rise until even the mountains are covered. Every living thing on the land dies; only Noah and those with him in the ark survive.",
   ["What is the significance of the LORD Himself shutting the door of the ark (7:16)?",
    "How does the flood reverse the creation of Genesis 1?",
    "How is the ark a picture of salvation in Christ?"],
   ["1 Peter 3:20\u201321", "Luke 17:26\u201327", "2 Peter 3:5\u20137"])
ch(8, "The Waters Recede",
   "\u201cBut God remembered Noah.\u201d The waters subside, the ark rests on the mountains of Ararat, and Noah sends out a raven and a dove until the earth is dry. Noah leaves the ark and builds an altar, and the LORD promises never again to curse the ground or strike down every living creature in this way while the earth remains.",
   ["What does it mean that God \u201cremembered\u201d Noah (8:1)?",
    "Why is Noah\u2019s first act after leaving the ark to build an altar? What does that teach about worship?",
    "God makes His promise even though \u201cthe intention of man\u2019s heart is evil from his youth\u201d (8:21). What does this reveal about grace?"],
   ["Exodus 2:24", "Psalm 29:10", "Isaiah 54:9"])
ch(9, "God\u2019s Covenant with Noah",
   "God blesses Noah and his sons, renews the creation mandate, and establishes the sanctity of human life because humans are made in God\u2019s image. He makes a covenant never again to destroy the earth by flood, with the rainbow as its sign. The chapter ends with Noah\u2019s drunkenness, Ham\u2019s dishonor, and the curse on Canaan.",
   ["How does 9:6 ground the value of human life in the image of God?",
    "What does the rainbow covenant teach about God\u2019s faithfulness to all creation?",
    "What does Noah\u2019s failure (9:20\u201327) show us about even the most faithful people?"],
   ["Romans 13:4", "Isaiah 54:9\u201310", "Revelation 4:3", "James 3:9"])
ch(10, "The Table of Nations",
   "The descendants of Shem, Ham, and Japheth spread out across the earth, forming the nations, lands, and languages of the ancient world. This list sets the stage for God\u2019s later promise that through Abraham \u201call the families of the earth\u201d will be blessed.",
   ["Why do you think Genesis carefully records the origins of so many nations?",
    "How does this chapter prepare for God\u2019s global purpose in 12:3?",
    "How does Acts 17:26 connect to this chapter?"],
   ["Acts 17:26", "Deuteronomy 32:8", "Revelation 7:9"])
ch(11, "The Tower of Babel; Shem to Abram",
   "United by one language, people build a city and a tower to \u201cmake a name\u201d for themselves and avoid being scattered. God confuses their language and scatters them. A genealogy then narrows from Shem to Terah and introduces Abram and his barren wife Sarai, who move from Ur toward Canaan but settle in Haran.",
   ["What was wrong with wanting to \u201cmake a name for ourselves\u201d (11:4)? How do we do the same?",
    "Compare 11:4 with God\u2019s promise to Abram in 12:2. Who makes Abram\u2019s name great?",
    "How does Pentecost (Acts 2) reverse Babel?"],
   ["Acts 2:5\u201311", "Revelation 7:9\u201310", "Joshua 24:2"])
ch(12, "The Call of Abram",
   "God calls Abram to leave his country and family and go to a land He will show him, promising to make him a great nation, to bless him, and to bless all the families of the earth through him. Abram obeys at 75 and builds altars in Canaan. But when famine comes he goes to Egypt and, out of fear, passes Sarai off as his sister, and God protects her.",
   ["List the promises of 12:1\u20133. Which of them reach all the way to you?",
    "What did Abram have to leave behind? What might God be calling you to leave?",
    "How does Abram\u2019s fear in Egypt (12:10\u201320) contrast with his faith in 12:4?"],
   ["Hebrews 11:8\u201310", "Galatians 3:8\u20139", "Acts 7:2\u20134"])
ch(13, "Abram and Lot Separate",
   "Abram and Lot\u2019s herds grow too large to live together. Abram graciously lets Lot choose first, and Lot chooses the well-watered Jordan Valley near wicked Sodom. God then renews His promise of land and countless offspring to Abram.",
   ["What does Abram\u2019s generosity in 13:8\u20139 show about his trust in God?",
    "Lot chose by sight (13:10). How do we make choices based on appearances?",
    "Why does God renew His promise right after Lot leaves (13:14\u201317)?"],
   ["2 Corinthians 5:7", "Philippians 2:3\u20134", "2 Peter 2:7\u20138"])
ch(14, "Abram Rescues Lot; Melchizedek",
   "Four eastern kings defeat the kings of the Jordan Valley and capture Lot. Abram leads 318 trained men to rescue him. Returning, Abram is blessed by Melchizedek, king of Salem and priest of God Most High, and gives him a tenth of everything, but he refuses any reward from the king of Sodom.",
   ["Why does Abram refuse the king of Sodom\u2019s offer (14:22\u201324)?",
    "Who is Melchizedek, and how does Hebrews 7 connect him to Jesus?",
    "What does Abram\u2019s tithe teach about acknowledging God as the source of victory?"],
   ["Hebrews 7:1\u201317", "Psalm 110:4", "Proverbs 3:9"])
ch(15, "God\u2019s Covenant with Abram",
   "Abram, still childless, questions God. God brings him outside to count the stars and promises offspring as numerous. Abram believes the LORD, and it is counted to him as righteousness. God then confirms the land promise in a solemn covenant ceremony, passing alone between the animal pieces, and foretells Israel\u2019s 400 years of affliction and deliverance.",
   ["Why is 15:6 so central to the whole Bible\u2019s teaching on faith and righteousness?",
    "What does it mean that only God (the smoking fire pot and flaming torch) passed between the pieces?",
    "Abram honestly brings his doubts to God (15:2\u20133). How can you do the same?"],
   ["Romans 4:1\u201325", "Galatians 3:6\u20139", "James 2:23", "Exodus 12:40\u201341"])
ch(16, "Hagar and Ishmael",
   "Impatient for the promised child, Sarai gives her Egyptian servant Hagar to Abram, and Hagar conceives. Conflict follows, and Hagar flees. The angel of the LORD meets her in the wilderness, promises her a son named Ishmael, and Hagar calls God \u201cEl Roi,\u201d the God who sees.",
   ["What went wrong when Sarai and Abram tried to fulfill God\u2019s promise their own way?",
    "What does it mean to you that God is \u201ca God of seeing\u201d (16:13)?",
    "How does God care for Hagar, an outsider with little power?"],
   ["Galatians 4:21\u201331", "Psalm 139:1\u20134", "Psalm 33:18"])
ch(17, "The Covenant of Circumcision",
   "When Abram is 99, God appears as God Almighty (El Shaddai), renames him Abraham (\u201cfather of a multitude\u201d) and Sarai Sarah, and gives circumcision as the sign of the everlasting covenant. God promises that Sarah herself will bear a son, Isaac, while also blessing Ishmael.",
   ["Why do you think God changed Abram\u2019s and Sarai\u2019s names?",
    "What did circumcision signify, and how does the New Testament speak of circumcision of the heart?",
    "Abraham laughed (17:17). How do God\u2019s promises sometimes seem impossible to us?"],
   ["Romans 4:9\u201312", "Colossians 2:11\u201312", "Deuteronomy 30:6"])
ch(18, "The LORD Visits Abraham; Intercession for Sodom",
   "Three visitors come to Abraham at Mamre, and he shows them generous hospitality. The LORD promises that Sarah will have a son within a year; Sarah laughs, and the LORD asks, \u201cIs anything too hard for the LORD?\u201d Abraham then boldly intercedes for Sodom, asking if God will spare it for fifty, and eventually ten, righteous people.",
   ["What can we learn from Abraham\u2019s hospitality (18:1\u20138)? See Hebrews 13:2.",
    "Answer the question of 18:14 for a situation in your own life.",
    "What does Abraham\u2019s intercession teach about prayer and about God\u2019s justice?"],
   ["Hebrews 13:2", "Luke 1:37", "James 5:16", "Jeremiah 32:17"])
ch(19, "Sodom and Gomorrah Destroyed",
   "Two angels arrive in Sodom, and Lot takes them in. The men of the city surround the house in violent wickedness. The angels urge Lot\u2019s family to flee; Lot lingers, and they are dragged out by the hand because the LORD was merciful. Fire rains on Sodom and Gomorrah, Lot\u2019s wife looks back and becomes a pillar of salt, and Lot\u2019s daughters later bear Moab and Ammon.",
   ["Lot \u201clingered\u201d (19:16). Where are you tempted to linger near sin?",
    "Why did Jesus say, \u201cRemember Lot\u2019s wife\u201d (Luke 17:32)?",
    "How does 19:29 connect Lot\u2019s rescue to Abraham\u2019s prayer?"],
   ["Luke 17:28\u201332", "2 Peter 2:6\u20139", "Jude 7", "Ezekiel 16:49\u201350"])
ch(20, "Abraham and Abimelech",
   "Abraham again claims Sarah is his sister, this time in Gerar, and King Abimelech takes her. God warns Abimelech in a dream and keeps him from touching her. Abimelech rebukes Abraham, returns Sarah with gifts, and Abraham prays for Abimelech\u2019s household to be healed.",
   ["Why do you think Abraham repeated the same sin from chapter 12?",
    "How does God protect His promise even when Abraham fails?",
    "What patterns of sin do you find yourself repeating, and how does God\u2019s faithfulness encourage you?"],
   ["2 Timothy 2:13", "Psalm 105:12\u201315", "1 John 1:9"])
ch(21, "The Birth of Isaac",
   "The LORD visits Sarah as He promised, and she bears Isaac to 100-year-old Abraham. Sarah\u2019s laughter turns to joy. At Sarah\u2019s demand, Hagar and Ishmael are sent away, and God provides water for them in the wilderness. Abraham makes a treaty with Abimelech at Beersheba and calls on the name of the LORD, the Everlasting God.",
   ["How does 21:1\u20132 emphasize God\u2019s faithfulness to His exact word?",
    "How is God compassionate toward Hagar and Ishmael (21:15\u201321)?",
    "What promise has God kept in your life that you once laughed at or doubted?"],
   ["Hebrews 11:11\u201312", "Galatians 4:28\u201331", "Romans 9:7\u20139"])
ch(22, "The Binding of Isaac",
   "God tests Abraham by commanding him to offer Isaac as a burnt offering on Mount Moriah. Abraham obeys, telling Isaac, \u201cGod will provide for himself the lamb.\u201d At the last moment the angel of the LORD stops him, and God provides a ram in Isaac\u2019s place. Abraham names the place \u201cThe LORD will provide,\u201d and God reaffirms His promise with an oath.",
   ["Why would God test Abraham this way? What was being revealed?",
    "How does Hebrews 11:17\u201319 explain Abraham\u2019s faith in this moment?",
    "List the parallels between Isaac and Jesus (the beloved son, the wood, the mountain, the substitute).",
    "What \u201cIsaac\u201d might God be asking you to hold with an open hand?"],
   ["Hebrews 11:17\u201319", "John 3:16", "Romans 8:32", "James 2:21\u201323", "2 Chronicles 3:1"])
ch(23, "Sarah\u2019s Death and Burial",
   "Sarah dies at 127, and Abraham mourns her. As a sojourner in the land, he negotiates with the Hittites and buys the field and cave of Machpelah near Hebron as a burial place, the first piece of the promised land he legally owns.",
   ["Why is it significant that Abraham insists on paying full price for the cave?",
    "How is this small plot of land a down payment on God\u2019s promise?",
    "How does Abraham model grief combined with hope?"],
   ["Hebrews 11:13\u201316", "Acts 7:5", "1 Thessalonians 4:13\u201314"])
ch(24, "A Wife for Isaac",
   "Abraham sends his servant to his relatives to find a wife for Isaac. The servant prays for a specific sign, and before he finishes praying Rebekah appears and fulfills it. Rebekah\u2019s family agrees, Rebekah willingly goes, and Isaac takes her as his wife and loves her.",
   ["What stands out to you about the servant\u2019s prayer and his response to God\u2019s answer (24:12\u201327)?",
    "How does God\u2019s guidance work through ordinary circumstances in this chapter?",
    "What can we learn from Rebekah\u2019s willingness to say \u201cI will go\u201d (24:58)?"],
   ["Proverbs 3:5\u20136", "Proverbs 19:14", "Philippians 4:6"])
ch(25, "Abraham\u2019s Death; Jacob and Esau",
   "Abraham dies \u201cin a good old age\u201d and is buried by Isaac and Ishmael. Ishmael\u2019s descendants are listed. Rebekah, barren for twenty years, conceives twins after Isaac prays, and God declares that the older will serve the younger. Esau becomes a hunter and Jacob a quiet man, and Esau despises his birthright, selling it for a bowl of stew.",
   ["What does God\u2019s word in 25:23 teach about His choice not being based on human rank?",
    "Why does Hebrews 12:16 warn us not to be like Esau?",
    "What are some \u201cbowls of stew\u201d that tempt us to trade lasting blessings for momentary desires?"],
   ["Romans 9:10\u201313", "Hebrews 12:16\u201317", "Malachi 1:2\u20133"])
ch(26, "God\u2019s Promise to Isaac",
   "During a famine God tells Isaac not to go to Egypt and confirms the Abrahamic promises to him. Isaac repeats his father\u2019s sister-lie in Gerar. Blessed with great harvests, he faces envy and disputes over wells, but keeps moving and digging until there is room. God appears at Beersheba, and Abimelech seeks a peace treaty.",
   ["How is Isaac both like and unlike his father in this chapter?",
    "What does Isaac\u2019s response to the well disputes teach about peacemaking?",
    "How does God\u2019s promise pass from one generation to the next?"],
   ["Romans 12:18", "Matthew 5:9", "Psalm 37:11"])
ch(27, "Jacob Steals Esau\u2019s Blessing",
   "Isaac, old and blind, plans to bless Esau. Rebekah and Jacob scheme to deceive him, and Jacob, disguised as his brother, receives the blessing of the firstborn. Esau weeps bitterly and vows to kill Jacob, so Rebekah arranges for Jacob to flee to her brother Laban.",
   ["List every person in this chapter who acts wrongly. What does that say about this family?",
    "How does God\u2019s purpose (25:23) still go forward through sinful choices?",
    "What did deception cost Rebekah and Jacob?"],
   ["Hebrews 11:20", "Hebrews 12:17", "Proverbs 19:21"])
ch(28, "Jacob\u2019s Dream at Bethel",
   "Isaac blesses Jacob and sends him away to find a wife among Rebekah\u2019s family. On the way, Jacob dreams of a stairway reaching to heaven with angels ascending and descending, and the LORD standing above it, renewing the Abrahamic promise and pledging to be with him. Jacob names the place Bethel (\u201chouse of God\u201d) and makes a vow.",
   ["Jacob is a fugitive when God meets him. What does this show about grace?",
    "How does Jesus apply this dream to Himself in John 1:51?",
    "Jacob said, \u201cSurely the LORD is in this place, and I did not know it\u201d (28:16). Where might God be present in your life that you have overlooked?"],
   ["John 1:51", "Hebrews 13:5", "Psalm 139:7\u201310"])
ch(29, "Jacob Marries Leah and Rachel",
   "Jacob meets Rachel at a well and serves Laban seven years for her, which seem \u201cbut a few days\u201d because of his love. On the wedding night Laban substitutes Leah, and the deceiver is deceived. Jacob serves seven more years for Rachel. Unloved Leah bears Reuben, Simeon, Levi, and Judah, and with Judah\u2019s birth she says, \u201cThis time I will praise the LORD.\u201d",
   ["How does Jacob experience the same kind of deception he used on his father?",
    "Trace Leah\u2019s naming of her sons (29:32\u201335). How does her focus shift?",
    "How does God care for the overlooked and unloved in this story?"],
   ["Galatians 6:7", "Psalm 68:5\u20136", "Matthew 1:2\u20133"])
ch(30, "Jacob\u2019s Children and Prosperity",
   "Rivalry between Rachel and Leah drives a competition to bear children, including through their servants Bilhah and Zilpah. Eleven sons and a daughter, Dinah, are born, and at last God remembers Rachel, who bears Joseph. Jacob then outwits Laban in their agreement over the flocks, and God prospers him greatly.",
   ["What damage does jealousy do in this family?",
    "What does 30:22 (\u201cGod remembered Rachel\u201d) teach about God\u2019s timing?",
    "How does God bless Jacob in spite of Laban\u2019s schemes (see 31:7\u20139)?"],
   ["James 3:16", "1 Samuel 1:19\u201320", "Psalm 127:3"])
ch(31, "Jacob Flees from Laban",
   "God tells Jacob to return to his homeland. Jacob leaves secretly with his family and flocks, and Rachel steals her father\u2019s household gods. Laban pursues, but God warns him in a dream not to harm Jacob. After a heated confrontation, the two make a covenant at Mizpah and set up a heap of stones as a witness.",
   ["How had God protected Jacob during twenty years with Laban (31:38\u201342)?",
    "Why might Rachel have taken the household gods? What idols do we carry with us?",
    "What does a boundary like the Mizpah covenant teach about resolving conflict?"],
   ["Psalm 124:1\u20133", "Romans 8:31", "1 John 5:21"])
ch(32, "Jacob Wrestles with God",
   "Jacob fearfully prepares to meet Esau, dividing his camp, sending gifts, and praying a humble prayer that rests on God\u2019s promises. Alone at the Jabbok at night, he wrestles with a man until daybreak and refuses to let go without a blessing. He is renamed Israel, leaves limping, and calls the place Peniel: \u201cI have seen God face to face, and yet my life has been delivered.\u201d",
   ["What stands out to you in Jacob\u2019s prayer (32:9\u201312)?",
    "Why do you think God left Jacob with a limp?",
    "What does it mean to \u201cwrestle\u201d with God in prayer? Have you experienced this?"],
   ["Hosea 12:3\u20134", "2 Corinthians 12:7\u201310", "Luke 18:1"])
ch(33, "Jacob Meets Esau",
   "Esau runs to meet Jacob and embraces him, and the brothers weep together. Jacob says that seeing Esau\u2019s face is \u201clike seeing the face of God.\u201d Jacob declines to travel with Esau and settles at Succoth and then Shechem, where he buys land and builds an altar called \u201cGod, the God of Israel.\u201d",
   ["How does the reunion exceed Jacob\u2019s fears?",
    "How does Esau\u2019s welcome picture the father in Luke 15:20?",
    "Is there a relationship in your life where God might be preparing reconciliation?"],
   ["Luke 15:20", "Matthew 5:23\u201324", "Proverbs 16:7"])
ch(34, "Dinah and the Shechemites",
   "Shechem, a local prince, violates Jacob\u2019s daughter Dinah and then seeks to marry her. Jacob\u2019s sons answer deceitfully, requiring the men of the city to be circumcised, and then Simeon and Levi slaughter the men while they are still sore. Jacob rebukes them for making him odious in the land.",
   ["How does this dark chapter show the danger of mixing with Canaanite culture and of answering evil with evil?",
    "What do you make of Jacob\u2019s passive response compared to his sons\u2019 violent one?",
    "How should God\u2019s people respond to injustice? (See Romans 12:17\u201321.)"],
   ["Romans 12:17\u201321", "Genesis 49:5\u20137", "Deuteronomy 22:28\u201329"])
ch(35, "God Blesses and Renames Jacob",
   "God tells Jacob to return to Bethel. Jacob orders his household to put away their foreign gods and purify themselves. At Bethel God again names him Israel and repeats the promises. Rachel dies giving birth to Benjamin, Reuben sins against his father, and Isaac dies and is buried by Esau and Jacob.",
   ["Why did Jacob need to put away foreign gods before returning to Bethel?",
    "How does God\u2019s renewed blessing (35:9\u201312) echo Genesis 1:28 and 17:6?",
    "How do joy and sorrow mix in this chapter?"],
   ["Joshua 24:14\u201315", "2 Corinthians 6:16\u20137:1", "Matthew 2:18"])
ch(36, "Esau\u2019s Descendants",
   "A detailed record of Esau\u2019s family, the chiefs of Edom, and the kings who reigned in Edom \u201cbefore any king reigned over the Israelites.\u201d Esau settles in the hill country of Seir.",
   ["Why include Esau\u2019s genealogy in a book about the chosen line?",
    "How does 36:31 hint at Israel\u2019s future?",
    "How does God keep His promise that Esau would also become a nation (27:39\u201340)?"],
   ["Obadiah 1\u201321", "Deuteronomy 2:4\u20135", "Numbers 20:14\u201321"])
ch(37, "Joseph\u2019s Dreams; Sold into Slavery",
   "Jacob favors seventeen-year-old Joseph and gives him a special robe. Joseph shares two dreams in which his family bows to him, and his brothers hate him. When Joseph visits them in the fields, they throw him into a pit and sell him to traders bound for Egypt, then deceive Jacob with his bloodied robe. Joseph is sold to Potiphar.",
   ["How did favoritism and pride contribute to this family\u2019s crisis?",
    "Notice that Jacob, once the deceiver with a goat and clothing (ch. 27), is deceived with a goat and clothing. What do you see?",
    "Where is God in this chapter, even though He is not mentioned?"],
   ["Acts 7:9\u201310", "Psalm 105:16\u201319", "James 1:14\u201315"])
ch(38, "Judah and Tamar",
   "Judah leaves his brothers, marries a Canaanite, and has three sons. When his sons die and Judah fails to give Tamar his youngest as promised, she disguises herself and conceives by Judah himself. Confronted with the evidence, Judah confesses, \u201cShe is more righteous than I.\u201d Tamar bears twins, Perez and Zerah, and Perez becomes an ancestor of David and Jesus.",
   ["Why do you think this story interrupts the Joseph narrative?",
    "What does Judah\u2019s confession (38:26) show about the beginning of change in him?",
    "What does Tamar\u2019s place in Jesus\u2019 genealogy (Matthew 1:3) say about grace?"],
   ["Matthew 1:3", "Ruth 4:12, 18\u201322", "Deuteronomy 25:5\u20136"])
ch(39, "Joseph and Potiphar\u2019s Wife",
   "In Potiphar\u2019s house \u201cthe LORD was with Joseph,\u201d and everything prospers under him. Potiphar\u2019s wife repeatedly tries to seduce him, but Joseph refuses: \u201cHow then can I do this great wickedness and sin against God?\u201d Falsely accused, he is thrown into prison, yet the LORD is with him there too and gives him favor.",
   ["How many times does the chapter say \u201cthe LORD was with Joseph\u201d? Why does that matter?",
    "What can we learn from how Joseph handled persistent temptation (39:8\u201312)?",
    "How do you hold onto faith when doing right leads to suffering?"],
   ["1 Corinthians 10:13", "2 Timothy 2:22", "1 Peter 2:19\u201320", "Psalm 105:17\u201319"])
ch(40, "Joseph Interprets Two Dreams",
   "In prison Joseph meets Pharaoh\u2019s cupbearer and baker, who each have a troubling dream. Joseph credits God with interpretations, and the cupbearer is restored while the baker is executed, just as Joseph said. Joseph asks the cupbearer to remember him, but the cupbearer forgets him.",
   ["How does Joseph point to God rather than himself (40:8)?",
    "How does Joseph care for others while suffering himself (40:6\u20137)?",
    "How do you handle seasons when you feel forgotten?"],
   ["Daniel 2:27\u201328", "Psalm 13:1\u20136", "Isaiah 49:15"])
ch(41, "Joseph Rises to Power",
   "Two years later Pharaoh dreams of seven fat and seven thin cows and of seven good and seven withered ears of grain. The cupbearer remembers Joseph, who explains that God is revealing seven years of plenty followed by seven years of famine. Pharaoh makes Joseph, now 30, ruler over Egypt. Joseph stores grain, marries, and names his sons Manasseh and Ephraim.",
   ["How does God use 13 years of hardship to prepare Joseph for this moment?",
    "What do the names Manasseh and Ephraim (41:51\u201352) reveal about Joseph\u2019s heart?",
    "How does Joseph show wisdom and stewardship in planning for the famine?"],
   ["Acts 7:10", "Psalm 105:20\u201322", "Daniel 2:47\u201348", "Luke 16:10"])
ch(42, "Joseph\u2019s Brothers Go to Egypt",
   "Famine drives Jacob\u2019s sons to Egypt to buy grain, and they bow before Joseph without recognizing him, fulfilling his dreams. Joseph speaks roughly, accuses them of spying, and keeps Simeon while sending the others home to bring Benjamin. The brothers connect their trouble with their guilt over Joseph.",
   ["Why do you think Joseph tested his brothers rather than revealing himself immediately?",
    "How does guilt surface in the brothers\u2019 words (42:21\u201322)?",
    "Joseph weeps privately (42:24). What does this show about him?"],
   ["Numbers 32:23", "Psalm 32:3\u20135", "Proverbs 28:13"])
ch(43, "The Return to Egypt with Benjamin",
   "As the famine worsens, Judah pledges his own life as security for Benjamin, and Jacob reluctantly lets him go. In Egypt the brothers are brought to Joseph\u2019s house and fear a trap, but they are welcomed. Joseph is overcome at seeing Benjamin and hosts a feast where Benjamin receives five times as much as the others.",
   ["What change do you see in Judah (43:8\u201310) compared with chapter 37?",
    "How does Jacob surrender control in 43:14?",
    "Why might Joseph favor Benjamin at the meal? What is he testing?"],
   ["Romans 8:28", "Hebrews 7:22", "Philippians 4:11\u201313"])
ch(44, "Joseph\u2019s Silver Cup",
   "Joseph has his silver cup hidden in Benjamin\u2019s sack and then has the brothers stopped and accused. When the cup is found, they all return. Joseph says only Benjamin must stay as a slave, but Judah steps forward with a moving plea, offering to remain as a slave in Benjamin\u2019s place for the sake of their father.",
   ["How does this test show whether the brothers have changed since they sold Joseph?",
    "In what ways does Judah\u2019s offer to take Benjamin\u2019s place anticipate Christ?",
    "What evidence of true repentance do you see in this chapter?"],
   ["Hebrews 7:14", "Mark 10:45", "2 Corinthians 7:10\u201311"])
ch(45, "Joseph Reveals Himself",
   "Unable to restrain himself, Joseph weeps aloud and says, \u201cI am Joseph!\u201d He tells his terrified brothers not to be distressed, because God sent him ahead to preserve life. Pharaoh invites Jacob\u2019s whole family to Egypt, and Jacob, hearing that Joseph is alive, revives.",
   ["Count how many times Joseph says that God sent him (45:5\u20139). What does this reveal?",
    "How does Joseph\u2019s forgiveness model the gospel?",
    "Is there someone you need to forgive with Joseph\u2019s perspective on God\u2019s sovereignty?"],
   ["Acts 7:13\u201314", "Ephesians 4:32", "Colossians 3:13", "Romans 8:28"])
ch(46, "Jacob Goes to Egypt",
   "At Beersheba God speaks to Jacob in a vision: \u201cDo not be afraid to go down to Egypt, for there I will make you into a great nation.\u201d Seventy members of Jacob\u2019s family go to Egypt, and Jacob and Joseph are tearfully reunited in Goshen.",
   ["Why might Jacob have been afraid to go to Egypt?",
    "How does God\u2019s promise in 46:3\u20134 connect to 15:13\u201314?",
    "What does it mean to you that God promises \u201cI myself will go down with you\u201d?"],
   ["Exodus 1:1\u20137", "Deuteronomy 10:22", "Acts 7:14\u201315", "Isaiah 41:10"])
ch(47, "Jacob\u2019s Family Settles in Goshen",
   "Joseph presents his family to Pharaoh, and they settle in Goshen. Jacob blesses Pharaoh. As the famine deepens, Joseph acquires money, livestock, land, and people for Pharaoh in exchange for food, keeping Egypt alive. Near death, Jacob makes Joseph swear to bury him in Canaan.",
   ["What is significant about Jacob (a shepherd and sojourner) blessing Pharaoh?",
    "How does Jacob describe his life in 47:9? How would you describe yours?",
    "Why was it so important to Jacob to be buried in Canaan?"],
   ["Hebrews 11:21", "Hebrews 7:7", "1 Peter 2:11"])
ch(48, "Jacob Blesses Ephraim and Manasseh",
   "Jacob adopts Joseph\u2019s sons Ephraim and Manasseh as his own. When he blesses them, he crosses his hands, deliberately placing his right hand on the younger, Ephraim. He speaks of \u201cthe God who has been my shepherd all my life long.\u201d",
   ["How does the younger-over-older pattern appear again here? Where else have you seen it in Genesis?",
    "What does Jacob mean by calling God \u201cmy shepherd all my life long\u201d (48:15)?",
    "How might you pass on a blessing of faith to the next generation?"],
   ["Hebrews 11:21", "Psalm 23:1", "Psalm 78:4\u20137"])
ch(49, "Jacob Blesses His Twelve Sons",
   "On his deathbed Jacob speaks prophetic words over each of his sons, foretelling the future of the tribes. Reuben loses preeminence, Simeon and Levi are scattered for their violence, and Judah receives the promise of royalty: the scepter will not depart from Judah. Joseph receives a rich blessing. Jacob charges them to bury him at Machpelah and dies.",
   ["How do the sons\u2019 past actions shape the words spoken over them?",
    "Why is the blessing on Judah (49:8\u201312) so important for the rest of the Bible?",
    "How does Revelation 5:5 connect Jesus to this chapter?"],
   ["Revelation 5:5", "Hebrews 7:14", "Numbers 24:17", "Deuteronomy 33"])
ch(50, "Joseph\u2019s Final Days",
   "Joseph and the Egyptians mourn Jacob, and a great procession buries him in Canaan. Afterward, Joseph\u2019s brothers fear revenge, but Joseph weeps and assures them: \u201cYou meant evil against me, but God meant it for good.\u201d Joseph lives to 110 and, confident in God\u2019s promise, makes Israel swear to carry his bones to the promised land.",
   ["Why do the brothers still fear Joseph after 17 years (50:15)? How does guilt linger?",
    "How does 50:20 summarize the whole Joseph story, and even the gospel?",
    "Why does Hebrews 11:22 highlight Joseph\u2019s instruction about his bones?",
    "Genesis begins with life in a garden and ends with a coffin in Egypt. What hope is left at the end?"],
   ["Romans 8:28", "Acts 2:23\u201324", "Hebrews 11:22", "Exodus 13:19", "Joshua 24:32"])

assert len(C) == 50 and [c["n"] for c in C] == list(range(1, 51))

guide = {
  "id": "genesis",
  "name": "Genesis",
  "tagline": "The book of beginnings: creation, the fall, and the promise",
  "chapters": 50,
  "overview": {
    "author": "Jewish and Christian tradition holds that Moses wrote or compiled Genesis as the first book of the Torah (the Pentateuch). Later Scripture speaks of the Law as coming from Moses (e.g., Joshua 8:31; Luke 24:27; John 5:46). Some scholars think later editors updated parts of the text, such as place names.",
    "date": "Traditionally written during the wilderness wanderings, roughly 1446\u20131406 BC (or the 13th century BC if a later Exodus date is taken). The events run from creation to the death of Joseph, around 1800 BC.",
    "audience": "The people of Israel after the Exodus, who were about to enter Canaan and needed to know who God is, where they came from, and why the land had been promised to them.",
    "setting": "It begins in Eden and the ancient Near East (Mesopotamia), follows Abraham\u2019s family to Canaan, and ends in Egypt, where Jacob\u2019s family settles during a famine.",
    "purpose": "To show that the one true God made everything good, to explain how sin and death entered the world, and to introduce God\u2019s plan to bless all nations through the family of Abraham. That covenant promise is carried by God\u2019s grace through generations of flawed people and points ahead to the coming offspring who will crush the serpent.",
    "structure": "Genesis is arranged around ten \u201cgenerations\u201d headings (Hebrew toledot: \u201cThese are the generations of\u2026\u201d) at 2:4; 5:1; 6:9; 10:1; 11:10; 11:27; 25:12; 25:19; 36:1; and 37:2. The book divides into two parts: primeval history (chs. 1\u201311) and the history of the patriarchs (chs. 12\u201350)."
  },
  "outline": [
    {"title": "Primeval History", "range": "1:1\u201311:26", "start": 1, "end": 11, "items": [
      {"title": "Creation of the heavens and the earth", "range": "1:1\u20132:3"},
      {"title": "Eden, the fall, and its aftermath", "range": "2:4\u20134:26"},
      {"title": "From Adam to Noah", "range": "5:1\u20136:8"},
      {"title": "Noah, the flood, and the covenant", "range": "6:9\u20139:29"},
      {"title": "The nations and the Tower of Babel", "range": "10:1\u201311:26"}]},
    {"title": "Abraham: The Call and the Covenant", "range": "11:27\u201325:18", "start": 11, "end": 25, "items": [
      {"title": "The call of Abram and the journey to Canaan", "range": "11:27\u201314:24"},
      {"title": "The covenant made and confirmed", "range": "15:1\u201317:27"},
      {"title": "Sodom judged, Isaac born", "range": "18:1\u201321:34"},
      {"title": "The great test on Mount Moriah", "range": "22:1\u201324"},
      {"title": "Abraham\u2019s final years and Ishmael\u2019s line", "range": "23:1\u201325:18"}]},
    {"title": "Isaac and Jacob: The Promise Carried On", "range": "25:19\u201336:43", "start": 25, "end": 36, "items": [
      {"title": "Jacob and Esau: birthright and blessing", "range": "25:19\u201328:9"},
      {"title": "Jacob at Bethel and in Haran", "range": "28:10\u201331:55"},
      {"title": "Jacob wrestles with God and returns home", "range": "32:1\u201335:29"},
      {"title": "Esau\u2019s descendants", "range": "36:1\u201343"}]},
    {"title": "Joseph: God\u2019s Providence Preserves the Family", "range": "37:1\u201350:26", "start": 37, "end": 50, "items": [
      {"title": "Joseph sold into Egypt; Judah and Tamar", "range": "37:1\u201338:30"},
      {"title": "Joseph\u2019s trials and exaltation", "range": "39:1\u201341:57"},
      {"title": "The brothers tested and reconciled", "range": "42:1\u201345:28"},
      {"title": "Israel in Egypt; Jacob\u2019s blessings and death", "range": "46:1\u201350:26"}]}
  ],
  "themes": [
    {"title": "God the Creator and Sovereign King", "text": "God creates by His word, owns all things, and rules over history. Nothing in Genesis, from floods to famines to family betrayals, falls outside His purpose (1:1; 50:20)."},
    {"title": "The Image of God", "text": "Humans uniquely bear God\u2019s image (1:26\u201327; 9:6), which gives every person dignity and calls us to represent God\u2019s rule with care."},
    {"title": "Sin and Its Spread", "text": "Sin moves from one act of distrust (ch. 3) to murder (ch. 4), widespread violence (ch. 6), and proud rebellion (ch. 11), and it lives on in the patriarchs\u2019 families."},
    {"title": "Judgment and Grace", "text": "Every judgment comes with grace: clothing for Adam and Eve, a mark for Cain, an ark for Noah, and a promise after Babel through Abraham."},
    {"title": "Covenant and Promise", "text": "God binds Himself to Abraham with promises of offspring, land, and blessing to all nations (12:1\u20133; 15; 17). These promises shape the rest of the Bible."},
    {"title": "Faith", "text": "Abraham \u201cbelieved the LORD, and he counted it to him as righteousness\u201d (15:6). Genesis shows faith that trusts God\u2019s word when circumstances seem impossible."},
    {"title": "God\u2019s Surprising Choice", "text": "Again and again God chooses the younger or the unlikely (Abel, Isaac, Jacob, Judah, Joseph, Ephraim), so that it is clear blessing comes by grace, not by rank."},
    {"title": "Providence", "text": "God works through ordinary events and even evil human choices to accomplish good, most clearly in the story of Joseph."},
    {"title": "Blessing to the Nations", "text": "From the table of nations (ch. 10) to Joseph feeding the world (ch. 41), God\u2019s plan is global: \u201cin you all the families of the earth shall be blessed.\u201d"}
  ],
  "keyVerses": [
    {"ref": "Genesis 1:1", "quote": "In the beginning, God created the heavens and the earth."},
    {"ref": "Genesis 1:27", "quote": "So God created man in his own image, in the image of God he created him; male and female he created them."},
    {"ref": "Genesis 3:15", "quote": "I will put enmity between you and the woman, and between your offspring and her offspring; he shall bruise your head, and you shall bruise his heel."},
    {"ref": "Genesis 12:2\u20133", "quote": "And I will make of you a great nation, and I will bless you\u2026 and in you all the families of the earth shall be blessed."},
    {"ref": "Genesis 15:6", "quote": "And he believed the LORD, and he counted it to him as righteousness."},
    {"ref": "Genesis 18:14", "quote": "Is anything too hard for the LORD?"},
    {"ref": "Genesis 50:20", "quote": "As for you, you meant evil against me, but God meant it for good, to bring it about that many people should be kept alive, as they are today."}
  ],
  "christInBook": [
    {"ref": "3:15", "text": "The offspring of the woman who will crush the serpent\u2019s head (Galatians 4:4; Romans 16:20; 1 John 3:8)."},
    {"ref": "12:3; 22:18", "text": "The single offspring of Abraham through whom all nations are blessed (Galatians 3:8, 16)."},
    {"ref": "14:18\u201320", "text": "Melchizedek, the priest-king, foreshadows Christ\u2019s eternal priesthood (Hebrews 7)."},
    {"ref": "22:1\u201314", "text": "The beloved son offered on a mountain, with a substitute provided by God (John 1:29; Romans 8:32)."},
    {"ref": "28:12", "text": "Jacob\u2019s stairway to heaven is fulfilled in Jesus, the true connection between heaven and earth (John 1:51)."},
    {"ref": "49:10", "text": "The scepter will not depart from Judah, pointing to the Lion of the tribe of Judah (Revelation 5:5)."},
    {"ref": "37\u201350", "text": "Joseph, rejected by his brothers, suffers unjustly, is exalted, and becomes the savior of those who betrayed him."}
  ],
  "crossReferences": [
    {"ref": "John 1:1\u20133", "note": "\u201cIn the beginning\u201d: Christ as the Word through whom all things were made."},
    {"ref": "Romans 5:12\u201321", "note": "Adam and Christ: how sin entered through one man and grace comes through one man."},
    {"ref": "Romans 4; Galatians 3", "note": "Abraham as the father of all who believe; justification by faith."},
    {"ref": "Hebrews 11:3\u201322", "note": "The \u201chall of faith\u201d: Abel, Enoch, Noah, Abraham, Sarah, Isaac, Jacob, Joseph."},
    {"ref": "Acts 7:2\u201316", "note": "Stephen retells the story of the patriarchs."},
    {"ref": "Revelation 21\u201322", "note": "The new creation: the tree of life restored and the curse removed (22:2\u20133)."}
  ],
  "reflection": [
    "Genesis 1 says that you bear God\u2019s image. How should that change the way you see yourself, and the person you find hardest to love?",
    "Like Adam and Eve, we tend to hide and shift blame. What would it look like this week to bring a hidden sin into the light before God?",
    "Abraham left the familiar on the strength of God\u2019s promise. What step of faith is God asking you to take right now?",
    "Where are you tempted to \u201chelp God out\u201d the way Sarai did with Hagar instead of waiting on His timing?",
    "Jacob was changed through wrestling and weakness. How has God used a struggle or a \u201climp\u201d in your life to shape you?",
    "Joseph said, \u201cGod meant it for good.\u201d Think of a painful season in your past. Where can you now see God at work, or trust that He is?",
    "Which family patterns in Genesis (favoritism, deception, rivalry) do you see in your own family? How can the gospel break those cycles?",
    "Who is one person you need to forgive or seek reconciliation with, as Esau and Jacob and then Joseph and his brothers did?"
  ],
  "readingPlan": "50 chapters: about 2 chapters a day finishes the book in 25 days, or 1 chapter a day takes 7 weeks. For each chapter, read it on ESV.org, then come back here for the summary, questions, and your notes."
}
guide["chapterList"] = C
out = os.path.join(os.path.dirname(__file__), "..", "data", "genesis.json")
with open(out, "w") as f:
    json.dump(guide, f, ensure_ascii=False, indent=1)
print("wrote", out, len(C))
