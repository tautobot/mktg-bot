/**
 * CHECK THE DOCUMENT TO KNOW HOW TO LOAD CUSTOM JS CODE
 * https://artillery.io/docs/http-reference/#advanced-writing-custom-logic-in-javascript
 */

/**
 * Generate random string.
 * @param {Integer} len; Length of string
 * @return {String};
 * @author Roger Knapp
 * @ref http://stackoverflow.com/a/1349426/1235074
 */
function randomStr(len)
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < len; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

/**
 * Generate random number between 2 given numbers.
 * @param {Integer} min 
 * @param {Integer} max 
 * @author Francisc
 * @ref https://stackoverflow.com/a/7228322/1235074
 */
function randomBetween(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min);
}


function randomUser(context, events, done) {
    context.vars['email_suffix'] = randomStr(6); // set the "email_suffix" variable for the virtual user
    context.vars['nricfin']      = randomBetween(Math.pow(10,6) - 1, Math.pow(10,7));
    return done();
}

/**
 * Use this function to log the response body.
 * It's very useful when you need to debug.
 */
function logResponseBody(requestParams, response, context, events, next) {
    console.log(response.body);
    return next();
}

module.exports = {randomUser, logResponseBody}