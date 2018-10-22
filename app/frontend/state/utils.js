import camelize from 'camelize';
import api from './api';


// Recursively convert snake_case to camelCase.
const parsePythonObject = (obj) => {
  if (Array.isArray(obj)) {
    return obj.map(parsePythonObject);
  } else if (typeof (obj) === 'object') {
    return camelize(obj);
  }
  return obj;
};


// Check for an error in an API request - write appropriate message to redux store.
// Errors should always have the form { name: [msg, msg], name: [msg] }
const checkForError = dispatch => (response) => {
  let errorMessage = 'Something went wrong :(';
  if (response.status === 400) {
    // Bad request, try and get details
    errorMessage = 'Bad request - invalid data.';
    response.json().then(errorData => dispatch({ type: 'WRITE_ERROR', errors: errorData }));
  } else if (response.status === 401 || response.status === 403) {
    errorMessage = 'Forbidden - you do not have permission to do this.';
  }
  if (response.status >= 400) {
    console.error(response.status, response.statusText);
    dispatch({ type: 'WRITE_ERROR', errors: { error: [errorMessage] } });
    throw new Error(`HTTP API error: ${response.status}`);
  }
  return response;
};


// Handle response from a JSON HTTP API, returns a promise of a JS object.
const handleJSONResponse = dispatch => (response) => {
  checkForError(dispatch)(response);
  return response.json().then(parsePythonObject);
};


// Handle an API error in a catch block
const handleError = dispatch => (error) => {
  console.error(error);
};


// Return 'true' if we have already fetched a full list of dataItemName from the backend.
const isCached = (dataItemName, getState) =>
  getState().data[dataItemName].isCached;


// Generic method for fetching a list of some data
//
//    dataItemName: name of data being fetched (eg. 'company', 'campaign')
//    checkCache: should we check if we have fetched this already, before hitting the API?
//
const fetchDataList = dataItemName => checkCache => (dispatch, getState) => {
  if (checkCache && isCached(dataItemName, getState)) return null;
  dispatch({ type: 'SET_LOADING', key: dataItemName });
  return api[dataItemName].list()
    .then(handleJSONResponse(dispatch))
    .then(data => dispatch({ type: 'RECEIVE_LIST', key: dataItemName, data }))
    .catch(handleError(dispatch));
};


module.exports = {
  checkForError,
  handleError,
  handleJSONResponse,
  parsePythonObject,
  fetchDataList,
}
