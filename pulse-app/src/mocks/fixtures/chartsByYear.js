import songPool from "./songPool";

const countryIDs = [
  "AFG",
  "AGO",
  "ALB",
  "ARE",
  "ARG",
  "ARM",
  "AUS",
  "AUT",
  "AZE",
  "BDI",
  "BEL",
  "BEN",
  "BFA",
  "BGD",
  "BGR",
  "BHS",
  "BIH",
  "BLR",
  "BLZ",
  "BOL",
  "BRA",
  "BRN",
  "BTN",
  "BWA",
  "CAF",
  "CAN",
  "CHE",
  "CHL",
  "CHN",
  "CIV",
  "CMR",
  "COD",
  "COG",
  "COL",
  "CRI",
  "CUB",
  "CYP",
  "CZE",
  "DEU",
  "DJI",
  "DNK",
  "DOM",
  "DZA",
  "ECU",
  "EGY",
  "ERI",
  "ESP",
  "EST",
  "ETH",
  "FIN",
  "FJI",
  "FRA",
  "GUF",
  "GAB",
  "GBR",
  "GEO",
  "GHA",
  "GIN",
  "GMB",
  "GNB",
  "GNQ",
  "GRC",
  "GTM",
  "GUY",
  "HND",
  "HRV",
  "HTI",
  "HUN",
  "IDN",
  "IND",
  "IRL",
  "IRN",
  "IRQ",
  "ISL",
  "ISR",
  "ITA",
  "JAM",
  "JOR",
  "JPN",
  "KAZ",
  "KEN",
  "KGZ",
  "KHM",
  "KOR",
  "XXK",
  "KWT",
  "LAO",
  "LBN",
  "LBR",
  "LBY",
  "LKA",
  "LSO",
  "LTU",
  "LUX",
  "LVA",
  "MAR",
  "MDA",
  "MDG",
  "MEX",
  "MKD",
  "MLI",
  "MMR",
  "MNE",
  "MNG",
  "MOZ",
  "MRT",
  "MWI",
  "MYS",
  "NAM",
  "NCL",
  "NER",
  "NGA",
  "NIC",
  "NLD",
  "NOR",
  "NPL",
  "NZL",
  "OMN",
  "PAK",
  "PAN",
  "PER",
  "PHL",
  "PNG",
  "POL",
  "PRI",
  "PRK",
  "PRT",
  "PRY",
  "QAT",
  "ROU",
  "RUS",
  "RWA",
  "ESH",
  "SAU",
  "SDN",
  "SSD",
  "SEN",
  "SLB",
  "SLE",
  "SLV",
  "SOM",
  "SRB",
  "SUR",
  "SVK",
  "SVN",
  "SWE",
  "SWZ",
  "SYR",
  "TCD",
  "TGO",
  "THA",
  "TJK",
  "TKM",
  "TLS",
  "TTO",
  "TUN",
  "TUR",
  "TWN",
  "TZA",
  "UGA",
  "UKR",
  "URY",
  "USA",
  "UZB",
  "VEN",
  "VNM",
  "VUT",
  "PSX",
  "YEM",
  "ZAF",
  "ZMB",
  "ZWE"
];

function generateCountryCharts(songPool, countryIDs) {
  const chartByYear = {};

  countryIDs.forEach((countryID) => {
    chartByYear[countryID] = [];
    const shuffledSongs = songPool.sort(() => 0.5 - Math.random());
    const selectedSongs = shuffledSongs.slice(0, 10); // Select top 10 songs for each country

    selectedSongs.forEach((song, index) => {
      chartByYear[countryID].push({
        position: index + 1,
        ...song
      });
    });
  });

  return chartByYear;
}

export default generateCountryCharts(songPool, countryIDs);
