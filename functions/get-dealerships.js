/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');

function main(params) {

  const cloudant = Cloudant({
    url: params.COUCH_URL,
    username: params.COUCH_USERNAME,
    plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
  });

  let dealerships = getAllDealerships(cloudant);
  return dealerships
}

function getAllDealerships(cloudant) {
  return new Promise((resolve, reject) => {
    cloudant.db.use('dealerships').list({ include_docs: true })
      .then(body => {
        resolve({ rows: body.rows });
      })
      .catch(err => {
        reject({ err: err });
      });
  });
}