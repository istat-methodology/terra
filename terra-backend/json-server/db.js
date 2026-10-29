const fs = require("fs");

function readAndParse(fileName)
{
  try {
    return JSON.parse(fs.readFileSync(fileName))
  } catch (e) {
    return [];
  }
}

//Updates information (for application configuration)
const news = readAndParse("./data/general/news.json");

//Global metadata (for application configuration)
const metadata = readAndParse("./data/general/metadata.json");
const defaults = readAndParse("./data/general/defaults.json");

//Products
const productsCPA = readAndParse("./data/classification/clsProductsCPA.json");

const productsIntra = readAndParse("./data/classification/clsProductsGraphIntra.json");


const productsExtra = readAndParse("./data/classification/clsProductsGraphExtraNSTR.json");


const transports = readAndParse("./data/classification/clsTransport.json");


const partners = readAndParse("./data/classification/clsPartners.json");

//Map
const countries = readAndParse("./data/general/countries.json");

const countriesBorders = readAndParse("./data/map/countriesBorders.json");
//structural info
const ieinfo = readAndParse("./data/map/ieinfo.json");
//marker && features
const importseries = readAndParse("./data/map/importseries.json");
const exportseries = readAndParse("./data/map/exportseries.json");

//Trade
//data value


const exportQuoteValue = readAndParse("./data/trade/exportQuoteValue.json");
const importQuoteValue = readAndParse("./data/trade/importQuoteValue.json");


const exportValue = readAndParse("./data/trade/exportValue.json");
const importValue = readAndParse("./data/trade/importValue.json");

//data quantity

const exportQuoteQuantity = readAndParse("./data/trade/exportQuoteQuantity.json");
const importQuoteQuantity = readAndParse("./data/trade/importQuoteQuantity.json");

const exportQuantity = readAndParse("./data/trade/exportQuantity.json");
const importQuantity = readAndParse("./data/trade/importQuantity.json");


module.exports = () => ({
  metadata,
  news,
  defaults,
  transports,
  partners,
  productsCPA,
  productsIntra,
  productsExtra,
  //map
  countries,
  countriesBorders,  
  ieinfo,
  importseries,
  exportseries,
  //trade
  exportValue,
  importValue,
  exportQuoteValue,
  importQuoteValue,
  exportQuantity,
  importQuantity,
  exportQuoteQuantity,
  importQuoteQuantity 
});
