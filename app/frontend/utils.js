import { FILTERS } from 'consts';


// If there are filter values, then filter for events that match at least one value.
// Otherwise, filter for all events.
const filterFor = (filterValues, eventKey) => event =>
  (filterValues.length > 0 ?
    filterValues.some(value => event[eventKey] === value) :
    true);


// If there are filter values, then filter out events that match at least one value.
const filterOut = (filterValues, eventKey) => event =>
  (filterValues.length > 0 ?
    !filterValues.some(value => event[eventKey] === value) :
    true);


module.exports = {
  filterOutGenres: filters => filterOut(filters[FILTERS.GENRE], 'eventType'),
};
