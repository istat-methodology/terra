const fs = require("fs");

//Updates information (for application configuration)
const news = JSON.parse(fs.readFileSync("./data/general/news.json"));

//Global metadata (for application configuration)
const metadata = JSON.parse(fs.readFileSync("./data/general/metadata.json"));
const defaults = JSON.parse(fs.readFileSync("./data/general/defaults.json"));

//Products
const productsCPA = JSON.parse(fs.readFileSync("./data/classification/clsProductsCPA.json"));

const productsIntra = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphIntra.json"));


const productsExtra = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphExtraNSTR.json"));


const transports = JSON.parse(fs.readFileSync("./data/classification/clsTransport.json"));


const partners = JSON.parse(fs.readFileSync("./data/classification/clsPartners.json"));

//Map
const countries = JSON.parse(fs.readFileSync("./data/general/countries.json"));

const countriesBorders = JSON.parse(fs.readFileSync("./data/map/countriesBorders.json"));
//structural info
const ieinfo = JSON.parse(fs.readFileSync("./data/map/ieinfo.json"));
//marker && features
const importseries = JSON.parse(fs.readFileSync("./data/map/importseries.json"));
const exportseries = JSON.parse(fs.readFileSync("./data/map/exportseries.json"));

//Trade
//data value


const exportQuoteValue = JSON.parse(fs.readFileSync("./data/trade/exportQuoteValue.json"));
const importQuoteValue = JSON.parse(fs.readFileSync("./data/trade/importQuoteValue.json"));


const exportValue = JSON.parse(fs.readFileSync("./data/trade/exportValue.json"));
const importValue = JSON.parse(fs.readFileSync("./data/trade/importValue.json"));

//data quantity

const exportQuoteQuantity = JSON.parse(fs.readFileSync("./data/trade/exportQuoteQuantity.json"));
const importQuoteQuantity = JSON.parse(fs.readFileSync("./data/trade/importQuoteQuantity.json"));

const exportQuantity = JSON.parse(fs.readFileSync("./data/trade/exportQuantity.json"));
const importQuantity = JSON.parse(fs.readFileSync("./data/trade/importQuantity.json"));


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
