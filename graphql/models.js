const mongoose = require('mongoose');
const { Schema } = mongoose;


const PageSchema = new Schema({
  "url": String,
  "domain": String,
  "title": String,
  "og_type": String,
  "og_site_name": String,
  "og_image": String,
  "og_title": String,
  "og_url": String,
  "raw_text": String    
});

const Page = mongoose.model('page', PageSchema); 


module.exports = {
    Page
}
