const fs = require("fs");

//Global metadata (for application configuratio)
const metadata = JSON.parse(fs.readFileSync("./data/general/metadata.json"));

//Products
const productsCPA = JSON.parse(fs.readFileSync("./data/classification/clsProductsCPA.json"));
const productsCPA_it = JSON.parse(fs.readFileSync("./data/classification/clsProductsCPA_it.json"));
const productsCPA_en = JSON.parse(fs.readFileSync("./data/classification/clsProductsCPA_en.json"));

const productsIntra = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphIntra.json"));
const productsIntra_it = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphIntra_it.json"));
const productsIntra_en = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphIntra_en.json"));

const productsExtra = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphExtraNSTR.json"));
const productsExtra_it = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphExtraNSTR_it.json"));
const productsExtra_en = JSON.parse(fs.readFileSync("./data/classification/clsProductsGraphExtraNSTR_en.json"));


const transports = JSON.parse(fs.readFileSync("./data/classification/clsTransport.json"));
const transports_it = JSON.parse(fs.readFileSync("./data/classification/clsTransport_it.json"));
const transports_en = JSON.parse(fs.readFileSync("./data/classification/clsTransport_en.json"));

const partners = JSON.parse(fs.readFileSync("./data/classification/clsPartners.json"));
const partners_it = JSON.parse(fs.readFileSync("./data/classification/clsPartners_it.json"));
const partners_en = JSON.parse(fs.readFileSync("./data/classification/clsPartners_en.json"));

//Map
const countries = JSON.parse(fs.readFileSync("./data/general/countries.json"));
const countries_it = JSON.parse(fs.readFileSync("./data/general/countries_it.json"));
const countries_en = JSON.parse(fs.readFileSync("./data/general/countries_en.json"));

const countriesBorders = JSON.parse(fs.readFileSync("./data/map/countriesBorders.json"));
//structural info
const ieinfo = JSON.parse(fs.readFileSync("./data/map/ieinfo.json"));
//marker && features
const importseries = JSON.parse(fs.readFileSync("./data/map/importseries.json"));
const exportseries = JSON.parse(fs.readFileSync("./data/map/exportseries.json"));

//Trade
//data value
const exportValue = JSON.parse(fs.readFileSync("./data/trade/exportValue.json"));
const importValue = JSON.parse(fs.readFileSync("./data/trade/importValue.json"));
//data quantity
const exportQuantity = JSON.parse(fs.readFileSync("./data/trade/exportQuantity.json"));
const importQuantity = JSON.parse(fs.readFileSync("./data/trade/importQuantity.json"));

module.exports = () => ({
  // application setup
  metadata,
  //classifications
  transports,
  transports_it,
  transports_en,
  partners,
  partners_it,
  partners_en,
  productsCPA,
  productsCPA_it,
  productsCPA_en,
  productsIntra,
  productsIntra_it,
  productsIntra_en,
  productsExtra,
  productsExtra_it,
  productsExtra_en,
  //map
  countries,
  countries_it,
  countries_en,
  countriesBorders,  
  ieinfo,
  importseries,
  exportseries,
  //trade
  exportValue,
  importValue,
  exportQuantity,
  importQuantity
});
