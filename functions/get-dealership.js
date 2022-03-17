/**
 * Get single dealership by dealerId
 */

const Cloudant = require('@cloudant/cloudant');

function main(params) {

  const cloudant = Cloudant({
    url: params.COUCH_URL,
    username: params.COUCH_USERNAME,
    plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
  });

  let dealerId = params.dealerId;
  let dealerships = getDealership(cloudant, dealerId);
  return dealerships
}

function getDealership(cloudant, dealerId) {
  let selector = { "selector": { "id": { "$eq": dealerId } } };
  return new Promise((resolve, reject) => {
    cloudant.db.use('dealerships').find(selector)
      .then(body => {
        resolve({ result: body });
      })
      .catch(err => {
        reject({ err: err });
      });
  });
}