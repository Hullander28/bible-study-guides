// Reading plans generated from the book catalog. Each plan splits its chapters evenly across its days.
window.PLANS = (function () {
  const B = window.BOOKS, byId = Object.fromEntries(B.map(b => [b.id, b]));
  const chaptersOf = ids => ids.flatMap(id => Array.from({ length: byId[id].chapters }, (_, i) => [id, i + 1]));
  const split = (list, days) => Array.from({ length: days }, (_, d) => list.slice(Math.floor(d * list.length / days), Math.floor((d + 1) * list.length / days)));
  const all = B.map(b => b.id), nt = B.filter(b => b.testament === "NT").map(b => b.id);
  const historical = ["genesis","job","exodus","leviticus","numbers","deuteronomy","joshua","judges","ruth","1-samuel","2-samuel","1-chronicles","psalms","1-kings","proverbs","ecclesiastes","song-of-solomon","2-kings","2-chronicles","jonah","joel","amos","hosea","isaiah","micah","nahum","zephaniah","habakkuk","jeremiah","lamentations","obadiah","ezekiel","daniel","ezra","haggai","zechariah","esther","nehemiah","malachi",
    "matthew","mark","luke","john","acts","james","galatians","1-thessalonians","2-thessalonians","1-corinthians","2-corinthians","romans","ephesians","philippians","colossians","philemon","1-timothy","titus","1-peter","hebrews","2-timothy","2-peter","jude","1-john","2-john","3-john","revelation"];
  const defs = [
    { id: "bible-1y", name: "Whole Bible in a year", desc: "Genesis to Revelation in Bible order, 365 days, about 3–4 chapters a day.", ids: all, days: 365 },
    { id: "historical-1y", name: "Whole Bible in a year, historical order", desc: "All 66 books arranged roughly in the order events happened (Job after Genesis, the prophets alongside Kings, Paul's letters in the order he wrote them). 365 days.", ids: historical, days: 365 },
    { id: "nt-90", name: "New Testament in 90 days", desc: "Matthew to Revelation, about 3 chapters a day.", ids: nt, days: 90 },
    { id: "gospels-30", name: "The Gospels in 30 days", desc: "Matthew, Mark, Luke, and John, about 3 chapters a day.", ids: ["matthew","mark","luke","john"], days: 30 }
  ];
  return defs.map(d => ({ id: d.id, name: d.name, desc: d.desc, days: d.days, total: chaptersOf(d.ids).length, schedule: split(chaptersOf(d.ids), d.days) }));
})();
