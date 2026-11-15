// Catalog of all 66 books. Set `ready: true` and add data/<id>.json to publish a guide.
window.BOOKS = (function () {
  const S = (testament, section, list) => list.map(([id, name, chapters, ready]) => ({ id, name, chapters, testament, section, ready: !!ready }));
  return [
    ...S("OT", "Law", [["genesis","Genesis",50,true],["exodus","Exodus",40,true],["leviticus","Leviticus",27,true],["numbers","Numbers",36,true],["deuteronomy","Deuteronomy",34,true]]),
    ...S("OT", "History", [["joshua","Joshua",24,true],["judges","Judges",21,true],["ruth","Ruth",4,true],["1-samuel","1 Samuel",31,true],["2-samuel","2 Samuel",24,true],["1-kings","1 Kings",22,true],["2-kings","2 Kings",25,true],["1-chronicles","1 Chronicles",29,true],["2-chronicles","2 Chronicles",36,true],["ezra","Ezra",10,true],["nehemiah","Nehemiah",13,true],["esther","Esther",10,true]]),
    ...S("OT", "Wisdom & Poetry", [["job","Job",42,true],["psalms","Psalms",150,true],["proverbs","Proverbs",31,true],["ecclesiastes","Ecclesiastes",12,true],["song-of-solomon","Song of Solomon",8,true]]),
    ...S("OT", "Major Prophets", [["isaiah","Isaiah",66],["jeremiah","Jeremiah",52],["lamentations","Lamentations",5],["ezekiel","Ezekiel",48],["daniel","Daniel",12]]),
    ...S("OT", "Minor Prophets", [["hosea","Hosea",14],["joel","Joel",3],["amos","Amos",9],["obadiah","Obadiah",1],["jonah","Jonah",4],["micah","Micah",7],["nahum","Nahum",3],["habakkuk","Habakkuk",3],["zephaniah","Zephaniah",3],["haggai","Haggai",2],["zechariah","Zechariah",14],["malachi","Malachi",4]]),
    ...S("NT", "Gospels", [["matthew","Matthew",28],["mark","Mark",16],["luke","Luke",24],["john","John",21]]),
    ...S("NT", "History", [["acts","Acts",28]]),
    ...S("NT", "Paul's Letters", [["romans","Romans",16],["1-corinthians","1 Corinthians",16],["2-corinthians","2 Corinthians",13],["galatians","Galatians",6],["ephesians","Ephesians",6],["philippians","Philippians",4],["colossians","Colossians",4],["1-thessalonians","1 Thessalonians",5],["2-thessalonians","2 Thessalonians",3],["1-timothy","1 Timothy",6],["2-timothy","2 Timothy",4],["titus","Titus",3],["philemon","Philemon",1]]),
    ...S("NT", "General Letters", [["hebrews","Hebrews",13],["james","James",5],["1-peter","1 Peter",5],["2-peter","2 Peter",3],["1-john","1 John",5],["2-john","2 John",1],["3-john","3 John",1],["jude","Jude",1]]),
    ...S("NT", "Prophecy", [["revelation","Revelation",22]]),
  ];
})();
